from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Cooperado
from .forms import CooperadoForm


@login_required(login_url='login')
def lista_cooperados(request):
    q = request.GET.get('q', '')
    cooperados = Cooperado.objects.all()
    if q:
        cooperados = cooperados.filter(nome__icontains=q) | cooperados.filter(cpf__icontains=q)
    return render(request, 'cooperados/lista.html', {'cooperados': cooperados, 'q': q})


@login_required(login_url='login')
def detalhe_cooperado(request, pk):
    cooperado = get_object_or_404(Cooperado, pk=pk)
    return render(request, 'cooperados/detalhe.html', {'cooperado': cooperado})


@login_required(login_url='login')
def criar_cooperado(request):
    if request.method == 'POST':
        form = CooperadoForm(request.POST)
        if form.is_valid():
            cooperado = form.save()
            messages.success(request, f'Cooperado "{cooperado.nome}" cadastrado com sucesso.')
            return redirect('lista_cooperados')
    else:
        form = CooperadoForm()
    return render(request, 'cooperados/form.html', {'form': form, 'titulo': 'Novo Cooperado'})


@login_required(login_url='login')
def editar_cooperado(request, pk):
    cooperado = get_object_or_404(Cooperado, pk=pk)
    if request.method == 'POST':
        form = CooperadoForm(request.POST, instance=cooperado)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cooperado "{cooperado.nome}" atualizado com sucesso.')
            return redirect('lista_cooperados')
    else:
        form = CooperadoForm(instance=cooperado)
    return render(request, 'cooperados/form.html', {'form': form, 'titulo': 'Editar Cooperado', 'cooperado': cooperado})


@login_required(login_url='login')
def excluir_cooperado(request, pk):
    cooperado = get_object_or_404(Cooperado, pk=pk)
    if request.method == 'POST':
        nome = cooperado.nome
        cooperado.delete()
        messages.success(request, f'Cooperado "{nome}" excluído com sucesso.')
        return redirect('lista_cooperados')
    return render(request, 'cooperados/confirmar_exclusao.html', {'cooperado': cooperado})
