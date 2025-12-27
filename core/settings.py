"""
=============================================================================
SETTINGS.PY - Configurações do Projeto Django
=============================================================================

Este é o arquivo MAIS IMPORTANTE do projeto Django!
Aqui definimos todas as configurações: banco de dados, apps instalados,
segurança, idioma, timezone, arquivos estáticos, templates, etc.

ATENÇÃO: Nunca compartilhe a SECRET_KEY em repositórios públicos!
Em produção, use variáveis de ambiente para dados sensíveis.
"""

from pathlib import Path

# =============================================================================
# DIRETÓRIO BASE DO PROJETO
# =============================================================================
# Path(__file__) = caminho deste arquivo (settings.py)
# .resolve() = converte para caminho absoluto
# .parent = pasta pai (core/)
# .parent = pasta pai novamente (Projeto Django/)
BASE_DIR = Path(__file__).resolve().parent.parent
# Resultado: BASE_DIR aponta para 'c:\dev\Projeto Django'


# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA
# =============================================================================

# SECRET_KEY: Chave secreta usada para criptografia
# IMPORTANTE: Em produção, NUNCA deixe esta chave no código!
# Use variáveis de ambiente: os.environ.get('SECRET_KEY')
SECRET_KEY = 'django-insecure-chave-de-desenvolvimento-apenas-nao-use-em-producao!'

# DEBUG: Modo de desenvolvimento
# True  = Mostra erros detalhados (APENAS para desenvolvimento!)
# False = Esconde erros (OBRIGATÓRIO em produção!)
DEBUG = True

# ALLOWED_HOSTS: Lista de domínios/IPs permitidos para acessar o site
# Em desenvolvimento: pode ficar vazio (Django permite localhost)
# Em produção: ['www.meusite.com', 'meusite.com', '192.168.1.100']
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# =============================================================================
# APLICAÇÕES INSTALADAS
# =============================================================================
# Lista de todas as apps que o Django deve carregar
# Apps são módulos que adicionam funcionalidades ao projeto

INSTALLED_APPS = [
    # -------------------------------------------------------------------------
    # APPS NATIVAS DO DJANGO (já vêm instaladas)
    # -------------------------------------------------------------------------
    'django.contrib.admin',         # Interface administrativa (painel admin)
    'django.contrib.auth',          # Sistema de autenticação (login, usuários)
    'django.contrib.contenttypes',  # Framework de tipos de conteúdo
    'django.contrib.sessions',      # Gerenciamento de sessões
    'django.contrib.messages',      # Framework de mensagens flash
    'django.contrib.staticfiles',   # Gerenciamento de arquivos estáticos (CSS, JS)
    
    # -------------------------------------------------------------------------
    # NOSSAS APPS CUSTOMIZADAS
    # -------------------------------------------------------------------------
    'tarefas',  # Nossa app de lista de tarefas!
]


# =============================================================================
# MIDDLEWARES
# =============================================================================
# Middlewares são "camadas" que processam requisições e respostas
# Pense neles como filtros que a requisição passa antes de chegar à view
# e a resposta passa antes de voltar ao usuário

MIDDLEWARE = [
    # Segurança: adiciona headers de segurança HTTP
    'django.middleware.security.SecurityMiddleware',
    
    # Sessões: gerencia cookies de sessão do usuário
    'django.contrib.sessions.middleware.SessionMiddleware',
    
    # Comum: adiciona funcionalidades comuns (ex: redireciona URLs sem barra final)
    'django.middleware.common.CommonMiddleware',
    
    # CSRF: proteção contra Cross-Site Request Forgery (ataques)
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Autenticação: adiciona request.user em todas as requisições
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # Mensagens: permite mostrar mensagens flash ao usuário
    'django.contrib.messages.middleware.MessageMiddleware',
    
    # Clickjacking: proteção contra ataques de clickjacking
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =============================================================================
# CONFIGURAÇÃO DE URLs
# =============================================================================
# Aponta para o arquivo principal de URLs do projeto
ROOT_URLCONF = 'core.urls'


# =============================================================================
# CONFIGURAÇÃO DE TEMPLATES (HTML)
# =============================================================================
# Templates são arquivos HTML que o Django renderiza com dados dinâmicos

TEMPLATES = [
    {
        # Engine: motor de templates (Django tem seu próprio, mas suporta Jinja2)
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        # DIRS: pastas adicionais onde procurar templates
        # BASE_DIR / 'templates' = pasta 'templates' na raiz do projeto
        'DIRS': [BASE_DIR / 'templates'],
        
        # APP_DIRS: se True, procura templates dentro de cada app
        # Exemplo: tarefas/templates/tarefas/lista.html
        'APP_DIRS': True,
        
        # OPTIONS: configurações adicionais
        'OPTIONS': {
            # Context processors: funções que adicionam variáveis a todos os templates
            'context_processors': [
                'django.template.context_processors.debug',     # Variável 'debug'
                'django.template.context_processors.request',   # Variável 'request'
                'django.contrib.auth.context_processors.auth',  # Variável 'user'
                'django.contrib.messages.context_processors.messages',  # Variável 'messages'
            ],
        },
    },
]


# =============================================================================
# WSGI - Web Server Gateway Interface
# =============================================================================
# Interface entre o servidor web (Nginx, Apache) e o Django
# Usado em produção
WSGI_APPLICATION = 'core.wsgi.application'


# =============================================================================
# BANCO DE DADOS
# =============================================================================
# Configuração de conexão com o banco de dados
# SQLite é perfeito para desenvolvimento e projetos pequenos
# Para produção, use PostgreSQL ou MySQL

DATABASES = {
    'default': {
        # ENGINE: driver do banco de dados
        # Opções: sqlite3, postgresql, mysql, oracle
        'ENGINE': 'django.db.backends.sqlite3',
        
        # NAME: caminho do arquivo do banco (SQLite) ou nome do banco (outros)
        'NAME': BASE_DIR / 'db.sqlite3',
        
        # Para PostgreSQL/MySQL, você também precisaria:
        # 'USER': 'meu_usuario',
        # 'PASSWORD': 'minha_senha',
        # 'HOST': 'localhost',
        # 'PORT': '5432',  # PostgreSQL: 5432, MySQL: 3306
    }
}


# =============================================================================
# VALIDAÇÃO DE SENHAS
# =============================================================================
# Regras que as senhas dos usuários devem seguir

AUTH_PASSWORD_VALIDATORS = [
    {
        # Verifica se a senha é muito similar aos dados do usuário
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Verifica o tamanho mínimo da senha (padrão: 8 caracteres)
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Verifica se a senha está em uma lista de senhas comuns
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Verifica se a senha não é apenas números
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =============================================================================
# INTERNACIONALIZAÇÃO (i18n) E LOCALIZAÇÃO (l10n)
# =============================================================================

# LANGUAGE_CODE: idioma padrão do projeto
# Afeta mensagens do Django Admin, validações, datas, etc.
LANGUAGE_CODE = 'pt-br'  # Português do Brasil

# TIME_ZONE: fuso horário do projeto
# Lista completa: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIME_ZONE = 'America/Sao_Paulo'

# USE_I18N: ativa sistema de tradução
USE_I18N = True

# USE_TZ: usa timezone-aware datetimes
# Recomendado: True para evitar problemas com horários
USE_TZ = True


# =============================================================================
# ARQUIVOS ESTÁTICOS (CSS, JavaScript, Imagens)
# =============================================================================

# URL base para arquivos estáticos
# Exemplo: http://meusite.com/static/css/estilo.css
STATIC_URL = '/static/'

# Pastas adicionais onde o Django procura arquivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Pasta 'static' na raiz do projeto
]

# Pasta onde o comando 'collectstatic' coleta todos os arquivos
# Usado em produção
# STATIC_ROOT = BASE_DIR / 'staticfiles'


# =============================================================================
# ARQUIVOS DE MÍDIA (uploads de usuários)
# =============================================================================

# URL base para arquivos de mídia
MEDIA_URL = '/media/'

# Pasta onde os uploads são salvos
MEDIA_ROOT = BASE_DIR / 'media'


# =============================================================================
# TIPO DE CHAVE PRIMÁRIA PADRÃO
# =============================================================================
# Define o tipo de campo usado para chaves primárias automáticas
# BigAutoField: inteiros de 64 bits (suporta mais registros)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
