"""
=============================================================================
URLS.PY - Roteamento de URLs do App Tarefas
=============================================================================

Este arquivo define as URLs específicas do app 'tarefas'.
Cada app pode ter seu próprio urls.py, mantendo o código organizado.

As URLs definidas aqui são "incluídas" no urls.py principal do projeto
usando a função include().

ESTRUTURA DE UMA ROTA:
    path('caminho/', view, name='nome_da_rota')
    
    - 'caminho/': parte da URL após o domínio
    - view: função ou classe que processa a requisição
    - name: identificador único para referenciar a URL no código
"""

from django.urls import path
from . import views  # Importa views do mesmo pacote (tarefas/views.py)


# =============================================================================
# LISTA DE URLS DO APP
# =============================================================================

urlpatterns = [
    # -------------------------------------------------------------------------
    # PÁGINA INICIAL
    # -------------------------------------------------------------------------
    # URL: http://localhost:8000/
    # View: index (função)
    # Nome: 'index' (usado em templates: {% url 'index' %})
    path('', views.index, name='index'),
    
    # -------------------------------------------------------------------------
    # LISTAGEM DE TAREFAS
    # -------------------------------------------------------------------------
    # URL: http://localhost:8000/tarefas/
    path('tarefas/', views.lista_tarefas, name='lista_tarefas'),
    
    # -------------------------------------------------------------------------
    # CRUD DE TAREFAS (Function-Based Views)
    # -------------------------------------------------------------------------
    
    # Criar nova tarefa
    # URL: http://localhost:8000/tarefas/nova/
    path('tarefas/nova/', views.criar_tarefa, name='criar_tarefa'),
    
    # Editar tarefa existente
    # URL: http://localhost:8000/tarefas/1/editar/
    # <int:pk> = parâmetro inteiro chamado 'pk' (primary key)
    # O valor é passado para a view como argumento
    path('tarefas/<int:pk>/editar/', views.editar_tarefa, name='editar_tarefa'),
    
    # Excluir tarefa
    # URL: http://localhost:8000/tarefas/1/excluir/
    path('tarefas/<int:pk>/excluir/', views.excluir_tarefa, name='excluir_tarefa'),
    
    # Alternar status (concluída/pendente)
    # URL: http://localhost:8000/tarefas/1/alternar/
    path('tarefas/<int:pk>/alternar/', views.alternar_status, name='alternar_status'),
    
    # -------------------------------------------------------------------------
    # DETALHES DA TAREFA (Class-Based View)
    # -------------------------------------------------------------------------
    # Para CBVs, usamos .as_view() para converter a classe em view
    # URL: http://localhost:8000/tarefas/1/
    path('tarefas/<int:pk>/', views.TarefaDetailView.as_view(), name='detalhe_tarefa'),
    
    # -------------------------------------------------------------------------
    # CATEGORIAS
    # -------------------------------------------------------------------------
    # URL: http://localhost:8000/categorias/
    path('categorias/', views.CategoriaListView.as_view(), name='lista_categorias'),
    
    # -------------------------------------------------------------------------
    # API (JSON)
    # -------------------------------------------------------------------------
    # URL: http://localhost:8000/api/tarefas/
    # Retorna dados em formato JSON
    path('api/tarefas/', views.api_tarefas, name='api_tarefas'),
]


# =============================================================================
# REFERÊNCIA RÁPIDA DE CONVERSORES DE URL
# =============================================================================
"""
Conversores disponíveis para parâmetros de URL:

<int:nome>    → Números inteiros positivos (0, 1, 42, ...)
<str:nome>    → Qualquer string não-vazia, exceto '/'
<slug:nome>   → Letras, números, hífens e underscores (ex: meu-post-123)
<uuid:nome>   → UUID formatado (ex: 075194d3-6885-417e-a8a8-6c931e272f00)
<path:nome>   → Qualquer string, incluindo '/' (para caminhos)

Exemplos:
    path('usuario/<str:username>/', views.perfil)    → /usuario/joao/
    path('post/<slug:slug>/', views.post_detalhe)    → /post/meu-primeiro-post/
    path('arquivo/<path:caminho>/', views.arquivo)   → /arquivo/pasta/subpasta/doc.pdf/
"""
