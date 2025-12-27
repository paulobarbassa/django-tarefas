"""
=============================================================================
VIEWS.PY - Lógica de Negócio (Controladores)
=============================================================================

Views são funções ou classes que recebem requisições HTTP e retornam
respostas HTTP. Elas são o "cérebro" da aplicação, onde a lógica acontece.

FLUXO:
1. Usuário acessa uma URL
2. Django encontra a view correspondente (via urls.py)
3. View processa a requisição (consulta banco, valida formulário, etc.)
4. View retorna uma resposta (HTML, JSON, redirect, etc.)

TIPOS DE VIEWS:
1. Function-Based Views (FBV): funções simples
2. Class-Based Views (CBV): classes com métodos predefinidos

Este arquivo mostra exemplos de AMBOS os tipos!
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Tarefa, Categoria
from .forms import TarefaForm


# =============================================================================
# FUNCTION-BASED VIEWS (FBV)
# =============================================================================
# Views baseadas em funções são simples e diretas.
# Boas para lógica personalizada ou views simples.

def index(request):
    """
    View da página inicial.
    
    Parâmetros:
        request: objeto HttpRequest contendo informações da requisição
                 - request.method: 'GET', 'POST', 'PUT', etc.
                 - request.GET: parâmetros da URL (?nome=valor)
                 - request.POST: dados enviados por formulário
                 - request.user: usuário logado (ou AnonymousUser)
    
    Retorna:
        HttpResponse: resposta HTTP (geralmente HTML renderizado)
    """
    # Busca estatísticas para exibir na página inicial
    total_tarefas = Tarefa.objects.count()
    tarefas_pendentes = Tarefa.objects.filter(concluida=False).count()
    tarefas_concluidas = Tarefa.objects.filter(concluida=True).count()
    tarefas_atrasadas = sum(1 for t in Tarefa.objects.filter(concluida=False) if t.esta_atrasada)
    
    # Busca as últimas 5 tarefas criadas
    ultimas_tarefas = Tarefa.objects.all()[:5]
    
    # Contexto: dicionário com dados que serão passados para o template
    context = {
        'total_tarefas': total_tarefas,
        'tarefas_pendentes': tarefas_pendentes,
        'tarefas_concluidas': tarefas_concluidas,
        'tarefas_atrasadas': tarefas_atrasadas,
        'ultimas_tarefas': ultimas_tarefas,
    }
    
    # render(): função que combina template + contexto e retorna HTML
    # Argumentos: request, caminho do template, dicionário de contexto
    return render(request, 'tarefas/index.html', context)


def lista_tarefas(request):
    """
    View que lista todas as tarefas com filtros.
    
    Demonstra:
    - Filtros via parâmetros GET
    - QuerySet encadeado
    - Paginação simples
    """
    # Obtém parâmetros de filtro da URL
    # request.GET.get('nome', 'padrao') retorna 'padrao' se 'nome' não existir
    filtro_status = request.GET.get('status', 'todas')
    filtro_prioridade = request.GET.get('prioridade', '')
    filtro_categoria = request.GET.get('categoria', '')
    
    # Começa com todas as tarefas
    tarefas = Tarefa.objects.all()
    
    # Aplica filtro de status
    if filtro_status == 'pendentes':
        tarefas = tarefas.filter(concluida=False)
    elif filtro_status == 'concluidas':
        tarefas = tarefas.filter(concluida=True)
    
    # Aplica filtro de prioridade
    if filtro_prioridade:
        tarefas = tarefas.filter(prioridade=filtro_prioridade)
    
    # Aplica filtro de categoria
    if filtro_categoria:
        tarefas = tarefas.filter(categoria_id=filtro_categoria)
    
    # Busca todas as categorias para o filtro
    categorias = Categoria.objects.all()
    
    context = {
        'tarefas': tarefas,
        'categorias': categorias,
        'filtro_status': filtro_status,
        'filtro_prioridade': filtro_prioridade,
        'filtro_categoria': filtro_categoria,
    }
    
    return render(request, 'tarefas/lista.html', context)


def criar_tarefa(request):
    """
    View para criar uma nova tarefa.
    
    Demonstra:
    - Diferença entre GET e POST
    - Uso de formulários Django
    - Mensagens flash
    - Redirecionamento
    """
    # Se for POST, o usuário está enviando o formulário
    if request.method == 'POST':
        # Cria o formulário com os dados enviados
        form = TarefaForm(request.POST)
        
        # Valida o formulário
        if form.is_valid():
            # Salva no banco de dados
            tarefa = form.save()
            
            # Adiciona mensagem de sucesso (flash message)
            # Será exibida na próxima página
            messages.success(request, f'Tarefa "{tarefa.titulo}" criada com sucesso!')
            
            # Redireciona para a lista de tarefas
            return redirect('lista_tarefas')
        else:
            # Se o formulário for inválido, mostra erro
            messages.error(request, 'Erro ao criar tarefa. Verifique os dados.')
    else:
        # Se for GET, cria um formulário vazio
        form = TarefaForm()
    
    context = {'form': form, 'acao': 'Criar'}
    return render(request, 'tarefas/form.html', context)


def editar_tarefa(request, pk):
    """
    View para editar uma tarefa existente.
    
    Parâmetros:
        pk: chave primária da tarefa (vem da URL)
    
    Demonstra:
    - get_object_or_404: busca objeto ou retorna erro 404
    - Edição de registros existentes
    """
    # get_object_or_404: busca o objeto ou retorna página 404 se não existir
    # É mais seguro que Tarefa.objects.get() que lança exceção
    tarefa = get_object_or_404(Tarefa, pk=pk)
    
    if request.method == 'POST':
        # instance=tarefa: vincula o formulário a um objeto existente
        form = TarefaForm(request.POST, instance=tarefa)
        
        if form.is_valid():
            form.save()
            messages.success(request, f'Tarefa "{tarefa.titulo}" atualizada!')
            return redirect('lista_tarefas')
    else:
        # Preenche o formulário com os dados atuais da tarefa
        form = TarefaForm(instance=tarefa)
    
    context = {
        'form': form,
        'tarefa': tarefa,
        'acao': 'Editar'
    }
    return render(request, 'tarefas/form.html', context)


def excluir_tarefa(request, pk):
    """
    View para excluir uma tarefa.
    
    Demonstra:
    - Confirmação de exclusão
    - Deleção de registros
    """
    tarefa = get_object_or_404(Tarefa, pk=pk)
    
    if request.method == 'POST':
        titulo = tarefa.titulo
        tarefa.delete()
        messages.success(request, f'Tarefa "{titulo}" excluída!')
        return redirect('lista_tarefas')
    
    context = {'tarefa': tarefa}
    return render(request, 'tarefas/excluir.html', context)


def alternar_status(request, pk):
    """
    View para alternar o status de uma tarefa (concluída/pendente).
    
    Demonstra:
    - Views que não precisam de template
    - Ações simples via GET (em produção, use POST!)
    """
    tarefa = get_object_or_404(Tarefa, pk=pk)
    
    # Alterna o status
    if tarefa.concluida:
        tarefa.marcar_pendente()
        messages.info(request, f'Tarefa "{tarefa.titulo}" marcada como pendente.')
    else:
        tarefa.marcar_concluida()
        messages.success(request, f'Tarefa "{tarefa.titulo}" concluída! 🎉')
    
    # Redireciona para a página anterior (HTTP_REFERER) ou lista
    return redirect(request.META.get('HTTP_REFERER', 'lista_tarefas'))


def api_tarefas(request):
    """
    View que retorna dados em JSON (API simples).
    
    Demonstra:
    - JsonResponse para retornar JSON
    - Serialização manual de dados
    
    Para APIs mais robustas, use Django REST Framework!
    """
    tarefas = Tarefa.objects.all()
    
    # Serializa os dados manualmente
    dados = [
        {
            'id': t.id,
            'titulo': t.titulo,
            'descricao': t.descricao,
            'concluida': t.concluida,
            'prioridade': t.prioridade,
            'categoria': t.categoria.nome if t.categoria else None,
            'criada_em': t.criada_em.isoformat(),
        }
        for t in tarefas
    ]
    
    # JsonResponse converte o dicionário/lista em JSON automaticamente
    # safe=False permite retornar listas (por padrão, só aceita dicts)
    return JsonResponse(dados, safe=False)


# =============================================================================
# CLASS-BASED VIEWS (CBV)
# =============================================================================
# Views baseadas em classes oferecem funcionalidades prontas.
# Boas para operações CRUD comuns.

class TarefaDetailView(DetailView):
    """
    View que exibe detalhes de uma tarefa.
    
    DetailView é uma CBV que:
    - Busca um objeto pelo pk ou slug
    - Renderiza um template com o objeto
    
    Você só precisa definir:
    - model: qual modelo usar
    - template_name: qual template renderizar
    
    O objeto fica disponível no template como 'object' ou 'tarefa' (nome do modelo)
    """
    model = Tarefa
    template_name = 'tarefas/detalhe.html'
    context_object_name = 'tarefa'  # Nome da variável no template


class TarefaCreateView(CreateView):
    """
    View para criar tarefas usando CBV.
    
    CreateView:
    - Exibe formulário vazio no GET
    - Valida e salva no POST
    - Redireciona após sucesso
    """
    model = Tarefa
    form_class = TarefaForm  # Formulário a usar
    template_name = 'tarefas/form.html'
    success_url = reverse_lazy('lista_tarefas')  # URL após salvar
    
    def get_context_data(self, **kwargs):
        """
        Adiciona dados extras ao contexto.
        
        Este método é chamado automaticamente antes de renderizar.
        Use para passar variáveis adicionais ao template.
        """
        context = super().get_context_data(**kwargs)
        context['acao'] = 'Criar'
        return context
    
    def form_valid(self, form):
        """
        Chamado quando o formulário é válido.
        
        Use para executar lógica adicional antes de salvar.
        """
        messages.success(self.request, 'Tarefa criada com sucesso!')
        return super().form_valid(form)


class TarefaUpdateView(UpdateView):
    """
    View para editar tarefas usando CBV.
    
    UpdateView é igual CreateView, mas edita um objeto existente.
    """
    model = Tarefa
    form_class = TarefaForm
    template_name = 'tarefas/form.html'
    success_url = reverse_lazy('lista_tarefas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acao'] = 'Editar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tarefa atualizada!')
        return super().form_valid(form)


class TarefaDeleteView(DeleteView):
    """
    View para excluir tarefas usando CBV.
    
    DeleteView:
    - GET: mostra página de confirmação
    - POST: exclui o objeto
    """
    model = Tarefa
    template_name = 'tarefas/excluir.html'
    success_url = reverse_lazy('lista_tarefas')
    
    def delete(self, request, *args, **kwargs):
        """Adiciona mensagem antes de excluir."""
        messages.success(request, 'Tarefa excluída!')
        return super().delete(request, *args, **kwargs)


class CategoriaListView(ListView):
    """
    View que lista todas as categorias.
    
    ListView:
    - Busca todos os objetos do modelo
    - Renderiza template com a lista
    - Suporta paginação automática
    """
    model = Categoria
    template_name = 'tarefas/categorias.html'
    context_object_name = 'categorias'  # Nome da lista no template
    
    # Paginação: mostra 10 itens por página
    # paginate_by = 10
