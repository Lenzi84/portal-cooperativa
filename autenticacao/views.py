from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm


def login_view(request):
    """
    View de login.
    - GET:  exibe o formulário de login.
    - POST: valida o formulário; se válido, autentica e redireciona
            para o dashboard; caso contrário, exibe os erros.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            # O AuthenticationForm já realizou authenticate() internamente;
            # basta pegar o usuário validado e chamar login().
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(
                request,
                'Usuário ou senha incorretos. Por favor, tente novamente.'
            )
    else:
        form = LoginForm(request)

    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def dashboard_view(request):
    """
    View do dashboard (área protegida).
    O decorator @login_required garante que apenas usuários
    autenticados acessem esta página.
    """
    return render(request, 'dashboard.html')


def logout_view(request):
    """
    View de logout. Encerra a sessão e redireciona para o login.
    """
    logout(request)
    messages.success(request, 'Você saiu do sistema com sucesso.')
    return redirect('login')
