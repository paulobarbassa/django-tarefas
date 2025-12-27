"""
=============================================================================
URLS.PY - Roteamento de URLs do Projeto
=============================================================================

Este arquivo define o "mapa" de URLs do projeto.
Quando um usuário acessa uma URL, o Django usa este arquivo para
determinar qual view (função/classe) deve processar a requisição.

Conceito importante: URLconf (URL Configuration)
- É como uma tabela que relaciona URLs a views
- O Django percorre a lista de cima para baixo até encontrar um match
- A primeira URL que combinar é usada

Padrões de URL:
- '' (vazio) = página inicial
- 'admin/' = painel administrativo
- 'tarefas/' = URLs do app de tarefas
"""

from django.contrib import admin
from django.urls import path, include

# =============================================================================
# LISTA DE PADRÕES DE URL
# =============================================================================
# Cada item é uma "rota" que mapeia uma URL para uma view

urlpatterns = [
    # -------------------------------------------------------------------------
    # PAINEL ADMINISTRATIVO DO DJANGO
    # -------------------------------------------------------------------------
    # path('admin/', admin.site.urls)
    # 
    # 'admin/' = URL que ativa esta rota (http://localhost:8000/admin/)
    # admin.site.urls = views do painel admin (já prontas no Django)
    # 
    # O Django Admin é uma interface automática para gerenciar dados!
    # Acesse: http://localhost:8000/admin/
    path('admin/', admin.site.urls),
    
    # -------------------------------------------------------------------------
    # URLs DO APP DE TAREFAS
    # -------------------------------------------------------------------------
    # path('', include('tarefas.urls'))
    # 
    # '' (string vazia) = raiz do site (http://localhost:8000/)
    # include('tarefas.urls') = inclui todas as URLs definidas em tarefas/urls.py
    # 
    # O include() permite que cada app tenha seu próprio arquivo urls.py
    # Isso mantém o código organizado e modular!
    path('', include('tarefas.urls')),
]

# =============================================================================
# DICAS DE URLS AVANÇADAS
# =============================================================================
"""
Exemplos de padrões de URL:

1. URL simples:
   path('sobre/', views.sobre, name='sobre')
   # Acesso: /sobre/

2. URL com parâmetro inteiro:
   path('tarefa/<int:id>/', views.detalhe, name='detalhe')
   # Acesso: /tarefa/1/, /tarefa/42/
   # O parâmetro 'id' é passado para a view

3. URL com parâmetro string:
   path('categoria/<str:nome>/', views.categoria, name='categoria')
   # Acesso: /categoria/trabalho/, /categoria/casa/

4. URL com slug (texto amigável para URL):
   path('post/<slug:slug>/', views.post, name='post')
   # Acesso: /post/meu-primeiro-post/

5. URL com múltiplos parâmetros:
   path('arquivo/<int:ano>/<int:mes>/', views.arquivo, name='arquivo')
   # Acesso: /arquivo/2024/12/

IMPORTANTE: O parâmetro 'name' é usado para referenciar a URL no código
   Exemplo no template: {% url 'detalhe' id=1 %}
   Exemplo no Python: reverse('detalhe', args=[1])
"""
