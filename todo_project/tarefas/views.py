from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tarefa
from .forms import TarefaForm, SignUpForm
from django.contrib.auth import login
from django.contrib import messages
from django.core.paginator import Paginator

@login_required
def lista_tarefas(request):
    status = request.GET.get('status')
    tarefas = Tarefa.objects.filter(usuario=request.user)
    if status in ('pendente', 'concluida'):
        tarefas = tarefas.filter(status=status)
    paginator = Paginator(tarefas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tarefas/lista_tarefas.html', {'page_obj': page_obj, 'status': status})

@login_required
def nova_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.usuario = request.user
            tarefa.save()
            messages.success(request, 'Tarefa criada com sucesso.')
            return redirect('lista_tarefas')
    else:
        form = TarefaForm()
    return render(request, 'tarefas/nova_tarefa.html', {'form': form, 'titulo_pagina': 'Nova tarefa'})

@login_required
def editar_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa atualizada.')
            return redirect('lista_tarefas')
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, 'tarefas/nova_tarefa.html', {'form': form, 'titulo_pagina': 'Editar tarefa'})

@login_required
def excluir_tarefa(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=request.user)
    if request.method == 'POST':
        tarefa.delete()
        messages.success(request, 'Tarefa removida.')
        return redirect('lista_tarefas')
    return render(request, 'tarefas/confirm_delete.html', {'tarefa': tarefa})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Conta criada com sucesso.')
            return redirect('lista_tarefas')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
