from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Cooperado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome completo')),
                ('cpf', models.CharField(max_length=14, unique=True, verbose_name='CPF')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('telefone', models.CharField(max_length=20, verbose_name='Telefone')),
                ('data_entrada', models.DateField(verbose_name='Data de entrada')),
                ('situacao', models.CharField(
                    choices=[('ativo', 'Ativo'), ('inativo', 'Inativo'), ('suspenso', 'Suspenso')],
                    default='ativo',
                    max_length=10,
                    verbose_name='Situação',
                )),
                ('observacoes', models.TextField(blank=True, verbose_name='Observações')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cooperado',
                'verbose_name_plural': 'Cooperados',
                'ordering': ['nome'],
            },
        ),
    ]
