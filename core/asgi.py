"""
=============================================================================
ASGI.PY - Asynchronous Server Gateway Interface
=============================================================================

ASGI é a evolução do WSGI, adicionando suporte a:
- Requisições assíncronas (async/await)
- WebSockets (comunicação em tempo real)
- HTTP/2
- Long polling

Este arquivo é usado quando você precisa de funcionalidades assíncronas,
como:
- Chat em tempo real
- Notificações push
- Streaming de dados
- Aplicações que precisam de alta concorrência

QUANDO USAR ASGI vs WSGI:
- WSGI: Aplicações tradicionais, APIs REST simples
- ASGI: WebSockets, apps em tempo real, alta concorrência

Para usar ASGI, você precisa de um servidor compatível como:
- Daphne
- Uvicorn
- Hypercorn

Exemplo de comando para rodar com Uvicorn:
    uvicorn core.asgi:application --host 0.0.0.0 --port 8000
"""

import os

from django.core.asgi import get_asgi_application

# Define qual arquivo de configurações usar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Cria a aplicação ASGI
# Esta variável 'application' é o ponto de entrada para servidores ASGI
application = get_asgi_application()
