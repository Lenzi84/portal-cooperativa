# Portal Cooperativa — Plano de Deploy e Documentação

## Visão Geral

Aplicação web Django com CRUD de cooperados, autenticação nativa, pipeline CI/CD via GitHub Actions e deploy automatizado na plataforma Microsoft Azure usando containers Docker.

---

## Arquitetura da Solução

```
[Desenvolvedor]
      │ git push (main)
      ▼
[GitHub Repository]
      │ trigger: GitHub Actions
      ▼
┌─────────────────────────────────────────┐
│           GitHub Actions CI/CD          │
│  1. Checkout código                     │
│  2. Setup Python / instala deps         │
│  3. Sobe PostgreSQL (service container) │
│  4. Executa migrate + testes            │
│  5. docker build                        │
│  6. docker push → ACR                   │
│  7. az webapp deploy                    │
└─────────────────────────────────────────┘
      │
      ▼
[Azure Container Registry (ACR)]
  portal-cooperativa:latest
      │
      ▼
[Azure Web App for Containers]     ←→  [Azure Database for PostgreSQL]
  webapp-lenzi84                         postgres-lenzi84
  porta 8000 (Gunicorn)
      │
      ▼
[URL Pública]
  https://webapp-lenzi84.azurewebsites.net
```

---

## Stack de Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Framework Web | Django 5.0 |
| Servidor WSGI | Gunicorn 22 |
| Banco de Dados | PostgreSQL 16 (Azure Database) |
| Driver de BD | psycopg2-binary |
| Arquivos Estáticos | WhiteNoise 6 |
| Containerização | Docker |
| Registro de Imagens | Azure Container Registry (ACR) |
| Hospedagem | Azure Web App for Containers |
| CI/CD | GitHub Actions |

---

## Plano de Deploy

### Fase 1 — Preparação do Repositório

1. Criar repositório no GitHub (público ou privado)
2. Clonar localmente e adicionar o código-fonte
3. Verificar que `.gitignore` exclui `.env` e `db.sqlite3`
4. Fazer primeiro commit e push para `main`

### Fase 2 — Infraestrutura Azure

Execute os comandos abaixo no Azure CLI (ou Portal Azure):

```bash
# 1. Resource Group
az group create \
  --name rg-python-aula \
  --location brazilsouth

# 2. Azure Container Registry
az acr create \
  --resource-group rg-python-aula \
  --name acrlenzi84 \
  --sku Basic \
  --admin-enabled true

# Obter credenciais do ACR (usar nos Secrets do GitHub)
az acr credential show --name acraula123

# 3. Azure Database for PostgreSQL (Flexible Server)
az postgres flexible-server create \
  --resource-group rg-python-aula \
  --name postgres-aula123 \
  --location brazilsouth \
  --admin-user adminuser \
  --admin-password "SuaSenhaSegura123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --version 16 \
  --public-access 0.0.0.0

# Criar banco de dados
az postgres flexible-server db create \
  --resource-group rg-python-aula \
  --server-name postgres-aula123 \
  --database-name portal_cooperativa

# 4. App Service Plan (Linux)
az appservice plan create \
  --name plan-aula123 \
  --resource-group rg-python-aula \
  --is-linux \
  --sku B1

# 5. Web App for Containers
az webapp create \
  --resource-group rg-python-aula \
  --plan plan-aula123 \
  --name webapp-aula123 \
  --deployment-container-image-name acraula123.azurecr.io/portal-cooperativa:latest

# 6. Configurar variáveis de ambiente no Web App
az webapp config appsettings set \
  --resource-group rg-python-aula \
  --name webapp-aula123 \
  --settings \
    SECRET_KEY="troque-por-chave-forte" \
    DEBUG="False" \
    ALLOWED_HOSTS="webapp-aula123.azurewebsites.net" \
    DB_NAME="portal_cooperativa" \
    DB_USER="adminuser" \
    DB_PASSWORD="SuaSenhaSegura123!" \
    DB_HOST="postgres-aula123.postgres.database.azure.com" \
    DB_PORT="5432" \
    DB_SSLMODE="require" \
    WEBSITES_PORT="8000"

# 7. Vincular ACR ao Web App (pull automático)
az webapp config container set \
  --name webapp-aula123 \
  --resource-group rg-python-aula \
  --docker-custom-image-name acraula123.azurecr.io/portal-cooperativa:latest \
  --docker-registry-server-url https://acraula123.azurecr.io \
  --docker-registry-server-user $(az acr credential show --name acraula123 --query username -o tsv) \
  --docker-registry-server-password $(az acr credential show --name acraula123 --query passwords[0].value -o tsv)
```

### Fase 3 — Configurar Secrets no GitHub

Acesse: **Settings → Secrets and variables → Actions** e adicione:

| Secret | Valor |
|---|---|
| `AZURE_REGISTRY` | `acraula123.azurecr.io` |
| `ACR_USERNAME` | usuário obtido em `az acr credential show` |
| `ACR_PASSWORD` | senha obtida em `az acr credential show` |
| `AZURE_WEBAPP_NAME` | `webapp-aula123` |
| `AZURE_RESOURCE_GROUP` | `rg-python-aula` |
| `AZURE_CREDENTIALS` | JSON do Service Principal (ver abaixo) |

**Criar Service Principal para o AZURE_CREDENTIALS:**

```bash
az ad sp create-for-rbac \
  --name "github-actions-portal" \
  --role contributor \
  --scopes /subscriptions/<SUB_ID>/resourceGroups/rg-python-aula \
  --sdk-auth
```

Copie o JSON inteiro gerado como valor do secret `AZURE_CREDENTIALS`.

### Fase 4 — Primeiro Deploy

```bash
# Push para main dispara o pipeline automaticamente
git add .
git commit -m "feat: deploy inicial portal cooperativa"
git push origin main
```

Acompanhe em: **GitHub → Actions → CI/CD — Build e Deploy no Azure**

### Fase 5 — Criar superusuário (uma vez)

```bash
# Via Azure CLI no container em execução
az webapp ssh --name webapp-aula123 --resource-group rg-python-aula
# Dentro do container:
python manage.py createsuperuser
```

---

## Fluxo CI/CD Detalhado

```
Push para main
      │
      ▼
JOB: test
  ├── Sobe PostgreSQL como service container
  ├── pip install -r requirements.txt
  ├── python manage.py migrate
  └── python manage.py test
      │ (falha aqui = pipeline para, sem deploy)
      ▼
JOB: build-and-push
  ├── docker login acraula123.azurecr.io
  ├── docker build -t portal-cooperativa:sha1234 .
  └── docker push (tag sha + latest)
      │
      ▼
JOB: deploy
  ├── az login (Service Principal)
  ├── az webapp deploy (aponta para :latest)
  ├── python manage.py migrate (via SSH)
  └── curl health check → HTTP 200/302
```

---

## Estrutura do Projeto

```
portal_cooperativa/
├── .github/
│   └── workflows/
│       └── deploy.yml          # Pipeline CI/CD
├── autenticacao/               # App: login/logout/dashboard
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── cooperados/                 # App: CRUD completo
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/cooperados/
│       ├── lista.html
│       ├── form.html
│       ├── detalhe.html
│       └── confirmar_exclusao.html
├── portal_cooperativa/         # Config Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/css/style.css
├── templates/                  # Templates base, login, dashboard
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
└── requirements.txt
```

---

## Endpoints da Aplicação

| Método | URL | Descrição |
|---|---|---|
| GET/POST | `/` | Login |
| GET | `/dashboard/` | Dashboard (autenticado) |
| GET | `/logout/` | Logout |
| GET | `/cooperados/` | Lista de cooperados |
| GET/POST | `/cooperados/novo/` | Criar cooperado |
| GET | `/cooperados/<id>/` | Detalhe do cooperado |
| GET/POST | `/cooperados/<id>/editar/` | Editar cooperado |
| GET/POST | `/cooperados/<id>/excluir/` | Excluir cooperado |
| GET | `/admin/` | Admin Django |

---

## Critérios de Avaliação Atendidos

| Critério | Implementação |
|---|---|
| **Funcionamento (20%)** | Django + PostgreSQL + CRUD completo + autenticação |
| **CI/CD (20%)** | GitHub Actions com 3 jobs: test → build → deploy |
| **Arquitetura Azure (20%)** | Resource Group, ACR, Web App for Containers, PostgreSQL Flexible Server |
| **Plano de Deploy (20%)** | Este documento |
| **Apresentação (20%)** | Diagrama de arquitetura, fluxo CI/CD, endpoints documentados |
