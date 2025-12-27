"""
=============================================================================
WSGI.PY - Web Server Gateway Interface
=============================================================================

WSGI (pronuncia-se "whiskey") é o padrão Python para comunicação
entre servidores web e aplicações web.

Este arquivo é usado em PRODUÇÃO para servir o Django através de
servidores como:
- Gunicorn (mais popular)
- uWSGI
- mod_wsgi (Apache)

Em DESENVOLVIMENTO, usamos o comando 'python manage.py runserver'
que usa seu próprio servidor simples.

FLUXO EM PRODUÇÃO:
1. Usuário faz requisição HTTP
2. Nginx/Apache recebe a requisição
3. Nginx/Apache passa para Gunicorn via WSGI
4. Gunicorn usa este arquivo para chamar o Django
5. Django processa e retorna a resposta
6. Resposta volta pelo mesmo caminho

Exemplo de comando para rodar com Gunicorn:
    gunicorn core.wsgi:application --bind 0.0.0.0:8000
"""

import os

from django.core.wsgi import get_wsgi_application

# Define qual arquivo de configurações usar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Cria a aplicação WSGI
# Esta variável 'application' é o ponto de entrada que o servidor web usa
application = get_wsgi_application()
