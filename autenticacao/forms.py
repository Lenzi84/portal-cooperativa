from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """
    Formulário de login utilizando o AuthenticationForm do Django.
    O AuthenticationForm já inclui validação de usuário e senha,
    além de integração com o sistema de autenticação do Django.
    """

    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu usuário',
            'autofocus': True,
        }),
        error_messages={
            'required': 'O campo usuário é obrigatório.',
        }
    )

    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
        }),
        error_messages={
            'required': 'O campo senha é obrigatório.',
        }
    )

    error_messages = {
        'invalid_login': (
            'Usuário ou senha incorretos. Verifique seus dados e tente novamente.'
        ),
        'inactive': 'Esta conta está inativa.',
    }
