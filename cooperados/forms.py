from django import forms
from .models import Cooperado


class CooperadoForm(forms.ModelForm):
    data_entrada = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d'],
        label='Data de entrada',
    )

    class Meta:
        model = Cooperado
        fields = ['nome', 'cpf', 'email', 'telefone', 'data_entrada', 'situacao', 'observacoes']
        widgets = {
            'nome':        forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'cpf':         forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'email':       forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'telefone':    forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(41) 99999-9999'}),
            'situacao':    forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
