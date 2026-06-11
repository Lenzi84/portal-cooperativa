from django.db import models


class Cooperado(models.Model):
    SITUACAO_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('suspenso', 'Suspenso'),
    ]

    nome = models.CharField(max_length=200, verbose_name='Nome completo')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    data_entrada = models.DateField(verbose_name='Data de entrada')
    situacao = models.CharField(
        max_length=10,
        choices=SITUACAO_CHOICES,
        default='ativo',
        verbose_name='Situação',
    )
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Cooperado'
        verbose_name_plural = 'Cooperados'

    def __str__(self):
        return self.nome
