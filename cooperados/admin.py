from django.contrib import admin
from .models import Cooperado


@admin.register(Cooperado)
class CooperadoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'situacao', 'data_entrada']
    list_filter = ['situacao']
    search_fields = ['nome', 'cpf', 'email']
