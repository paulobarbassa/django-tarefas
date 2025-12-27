"""
=============================================================================
SIGNALS.PY - Sinais do Django
=============================================================================

Signals são um mecanismo de "eventos" do Django que permite executar código
quando certas ações acontecem no framework.

SIGNALS MAIS COMUNS:
- pre_save: antes de salvar um objeto
- post_save: depois de salvar um objeto
- pre_delete: antes de deletar um objeto
- post_delete: depois de deletar um objeto
- pre_migrate: antes de executar migrações
- post_migrate: depois de executar migrações
- request_started: quando uma requisição HTTP começa
- request_finished: quando uma requisição HTTP termina

COMO FUNCIONA:
1. O Django emite um "sinal" quando algo acontece
2. Funções "receivers" (receptores) escutam esses sinais
3. Quando o sinal é emitido, todos os receivers são executados

ESTE ARQUIVO:
Usamos post_migrate para popular o banco com dados iniciais de estudo.
Isso é executado automaticamente após cada 'python manage.py migrate'.
"""

from django.db.models.signals import post_migrate
from django.dispatch import receiver


# Lista de tarefas que servem como guia de estudo do projeto Django
# Cada tarefa é um passo do aprendizado, baseado neste próprio projeto!
TAREFAS_ESTUDO = [
    # ==========================================================================
    # MÓDULO 1: FUNDAMENTOS DO PROJETO
    # ==========================================================================
    {
        'titulo': '📚 Passo 1: Entender a estrutura do projeto Django',
        'descricao': '''Este projeto tem a seguinte estrutura:

📁 core/ - Configurações principais do projeto
   ├── settings.py - Configurações gerais (banco, apps, middleware)
   ├── urls.py - Rotas principais (mapeia URLs para views)
   ├── wsgi.py - Configuração para servidores web (produção)
   └── asgi.py - Configuração para servidores assíncronos

📁 tarefas/ - Nosso app de tarefas
   ├── models.py - Define as tabelas do banco (Tarefa, Categoria)
   ├── views.py - Lógica das páginas (o que mostrar ao usuário)
   ├── urls.py - Rotas do app (URLs específicas de tarefas)
   ├── forms.py - Formulários (entrada de dados do usuário)
   ├── admin.py - Configuração do painel administrativo
   └── templates/ - Arquivos HTML

📁 templates/ - Templates globais (base.html)
📁 static/ - Arquivos estáticos (CSS, JS, imagens)
📄 manage.py - Ferramenta de linha de comando do Django
📄 db.sqlite3 - Banco de dados SQLite

EXERCÍCIO: Navegue pelos arquivos e leia os comentários!''',
        'prioridade': 'alta',
        'categoria_nome': '🎓 Fundamentos',
        'categoria_cor': 'primary',
    },
    {
        'titulo': '📚 Passo 2: Entender o arquivo settings.py',
        'descricao': '''O arquivo core/settings.py é o coração do Django!

Configurações importantes que você vai encontrar:

🔐 SECRET_KEY - Chave secreta (nunca compartilhe!)
🐛 DEBUG - Modo debug (True em desenvolvimento, False em produção)
🌐 ALLOWED_HOSTS - Domínios permitidos
📦 INSTALLED_APPS - Apps instalados no projeto
🔗 MIDDLEWARE - Processadores de requisição
📂 TEMPLATES - Configuração de templates HTML
🗄️ DATABASES - Configuração do banco de dados
🌍 LANGUAGE_CODE e TIME_ZONE - Idioma e fuso horário
📁 STATIC_URL - URL para arquivos estáticos

EXERCÍCIO: Abra settings.py e identifique onde está cada configuração.
Note como o app 'tarefas' está registrado em INSTALLED_APPS!''',
        'prioridade': 'alta',
        'categoria_nome': '🎓 Fundamentos',
        'categoria_cor': 'primary',
    },
    
    # ==========================================================================
    # MÓDULO 2: MODELS E ORM
    # ==========================================================================
    {
        'titulo': '🗃️ Passo 3: Estudar os Models (models.py)',
        'descricao': '''Models definem a estrutura do banco de dados usando classes Python.

Abra tarefas/models.py e estude:

📌 Classe Categoria:
   - CharField para nome (texto curto)
   - TextField para descrição (texto longo)
   - CharField com choices para cor

📌 Classe Tarefa:
   - Campos de texto: titulo, descricao
   - BooleanField: concluida
   - DateTimeField: criada_em, atualizada_em
   - ForeignKey: relacionamento com Categoria

CONCEITOS IMPORTANTES:
- verbose_name: nome amigável para exibição
- blank=True: campo pode ficar vazio no formulário
- null=True: campo pode ser NULL no banco
- default: valor padrão
- choices: opções predefinidas

EXERCÍCIO: Adicione um novo campo ao model Tarefa!
Depois rode: python manage.py makemigrations e python manage.py migrate''',
        'prioridade': 'alta',
        'categoria_nome': '🗃️ Models e ORM',
        'categoria_cor': 'warning',
    },
    {
        'titulo': '🗃️ Passo 4: Praticar consultas no Django Shell',
        'descricao': '''O Django Shell permite testar comandos interativamente.

Execute: python manage.py shell

Depois teste estes comandos:

# Importar os models
from tarefas.models import Tarefa, Categoria

# CRIAR
tarefa = Tarefa.objects.create(titulo='Minha tarefa', prioridade='alta')

# LER TODAS
todas = Tarefa.objects.all()
print(todas)

# FILTRAR
pendentes = Tarefa.objects.filter(concluida=False)
altas = Tarefa.objects.filter(prioridade='alta')

# BUSCAR UMA
tarefa = Tarefa.objects.get(id=1)

# ATUALIZAR
tarefa.titulo = 'Título atualizado'
tarefa.save()

# DELETAR
tarefa.delete()

# CONTAR
total = Tarefa.objects.count()

EXERCÍCIO: Crie, modifique e delete algumas tarefas no shell!
Use Ctrl+D ou exit() para sair.''',
        'prioridade': 'alta',
        'categoria_nome': '🗃️ Models e ORM',
        'categoria_cor': 'warning',
    },
    
    # ==========================================================================
    # MÓDULO 3: URLs E VIEWS
    # ==========================================================================
    {
        'titulo': '🔗 Passo 5: Entender o sistema de URLs',
        'descricao': '''O Django mapeia URLs para Views em dois arquivos:

📄 core/urls.py - URLs principais (raiz do projeto)
   - Inclui as URLs do app tarefas com: include('tarefas.urls')
   - Configura o admin em: admin.site.urls

📄 tarefas/urls.py - URLs do app tarefas
   - Lista de paths que mapeiam URLs para views
   - Cada path tem: caminho, view, nome

ANATOMIA DE UM PATH:
path('tarefas/', views.lista_tarefas, name='lista')
     ↑ URL       ↑ View a chamar      ↑ Nome para referência

URLS DESTE PROJETO:
/                  → Página inicial
/lista/            → Lista de tarefas
/nova/             → Criar nova tarefa
/editar/<id>/      → Editar tarefa
/excluir/<id>/     → Excluir tarefa
/concluir/<id>/    → Marcar como concluída
/categorias/       → Gerenciar categorias

EXERCÍCIO: Adicione uma nova URL que mostra as tarefas de hoje!''',
        'prioridade': 'media',
        'categoria_nome': '🔗 URLs e Views',
        'categoria_cor': 'info',
    },
    {
        'titulo': '🔗 Passo 6: Estudar as Views (views.py)',
        'descricao': '''Views são funções que processam requisições e retornam respostas.

Abra tarefas/views.py e estude os tipos de views:

📌 VIEWS DE LEITURA:
   - index: página inicial (dashboard)
   - lista_tarefas: lista todas as tarefas
   - detalhe_tarefa: mostra uma tarefa específica

📌 VIEWS DE ESCRITA:
   - criar_tarefa: formulário para nova tarefa
   - editar_tarefa: formulário para editar
   - excluir_tarefa: confirmação de exclusão
   - concluir_tarefa: marca como concluída

ESTRUTURA DE UMA VIEW:
def nome_view(request):
    # 1. Buscar dados do banco
    # 2. Processar formulário (se for POST)
    # 3. Renderizar template com contexto
    return render(request, 'template.html', contexto)

CONCEITOS:
- request.method: GET (exibir) ou POST (enviar dados)
- get_object_or_404: busca objeto ou retorna erro 404
- redirect: redireciona para outra URL
- render: renderiza template HTML

EXERCÍCIO: Crie uma view que mostra estatísticas das tarefas!''',
        'prioridade': 'media',
        'categoria_nome': '🔗 URLs e Views',
        'categoria_cor': 'info',
    },
    
    # ==========================================================================
    # MÓDULO 4: TEMPLATES
    # ==========================================================================
    {
        'titulo': '🎨 Passo 7: Entender o sistema de Templates',
        'descricao': '''Templates são arquivos HTML com lógica do Django.

ESTRUTURA DE TEMPLATES:
📁 templates/base.html - Template base (layout principal)
📁 tarefas/templates/tarefas/ - Templates do app
   ├── index.html - Página inicial
   ├── lista.html - Lista de tarefas
   ├── form.html - Formulário de criação/edição
   ├── detalhe.html - Detalhes de uma tarefa
   └── excluir.html - Confirmação de exclusão

HERANÇA DE TEMPLATES:
base.html define blocos: {% block content %}{% endblock %}
Outros templates estendem: {% extends 'base.html' %}
E preenchem os blocos: {% block content %}...{% endblock %}

TAGS DO DJANGO:
{% for item in lista %} ... {% endfor %} - Loop
{% if condição %} ... {% else %} ... {% endif %} - Condição
{% url 'nome_url' %} - Gera URL pelo nome
{% include 'parte.html' %} - Inclui outro template
{% csrf_token %} - Token de segurança para forms
{{ variavel }} - Exibe valor de variável
{{ variavel|filtro }} - Aplica filtro (date, length, etc)

EXERCÍCIO: Modifique o template lista.html para mostrar a data de criação!''',
        'prioridade': 'media',
        'categoria_nome': '🎨 Templates',
        'categoria_cor': 'success',
    },
    {
        'titulo': '🎨 Passo 8: Estudar o template base.html',
        'descricao': '''O template base.html é o layout principal do projeto.

Abra templates/base.html e observe:

📌 ESTRUTURA HTML5:
   - DOCTYPE, html, head, body
   - Meta tags para responsividade
   - Links para CSS (Bootstrap)

📌 BLOCOS DO DJANGO:
   {% block title %} - Título da página
   {% block content %} - Conteúdo principal
   {% block extra_js %} - Scripts extras

📌 NAVEGAÇÃO:
   - Navbar com links para as páginas
   - Usando {% url 'nome' %} para links dinâmicos

📌 ARQUIVOS ESTÁTICOS:
   {% load static %} - Carrega o sistema de estáticos
   {% static 'css/style.css' %} - Referencia arquivo estático

VANTAGENS DA HERANÇA:
- Evita repetição de código HTML
- Muda o layout em um lugar só
- Templates filhos ficam mais limpos

EXERCÍCIO: Adicione um novo link na navbar!''',
        'prioridade': 'media',
        'categoria_nome': '🎨 Templates',
        'categoria_cor': 'success',
    },
    
    # ==========================================================================
    # MÓDULO 5: FORMULÁRIOS
    # ==========================================================================
    {
        'titulo': '📝 Passo 9: Entender os Formulários (forms.py)',
        'descricao': '''Formulários do Django facilitam a entrada de dados.

Abra tarefas/forms.py e estude:

📌 ModelForm:
   - Cria formulário a partir de um Model
   - Validação automática baseada no Model
   - Salva diretamente no banco

ESTRUTURA DO FORMULÁRIO:
class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa      # Model associado
        fields = [...]      # Campos a incluir
        widgets = {...}     # Personalização HTML
        labels = {...}      # Rótulos personalizados

WIDGETS COMUNS:
- TextInput: campo de texto simples
- Textarea: área de texto grande
- Select: lista suspensa
- CheckboxInput: caixa de seleção
- DateInput: seletor de data

NA VIEW:
form = TarefaForm()              # Formulário vazio
form = TarefaForm(request.POST)  # Formulário com dados
if form.is_valid():              # Valida dados
    form.save()                  # Salva no banco

NO TEMPLATE:
{{ form.as_p }}    # Renderiza como parágrafos
{{ form.campo }}   # Renderiza campo específico
{{ form.campo.errors }}  # Erros do campo

EXERCÍCIO: Adicione um novo campo ao formulário de tarefas!''',
        'prioridade': 'media',
        'categoria_nome': '📝 Formulários',
        'categoria_cor': 'secondary',
    },
    
    # ==========================================================================
    # MÓDULO 6: ADMIN
    # ==========================================================================
    {
        'titulo': '⚙️ Passo 10: Explorar o Django Admin',
        'descricao': '''O Django Admin é um painel de administração automático!

ACESSAR O ADMIN:
1. Crie um superusuário: python manage.py createsuperuser
2. Acesse: http://localhost:8000/admin/
3. Faça login com suas credenciais

CONFIGURAÇÃO EM admin.py:
- admin.site.register(Model) - Registro simples
- @admin.register(Model) - Registro com decorator
- ModelAdmin - Classe para personalizar

PERSONALIZAÇÕES COMUNS:
list_display = [...]      # Colunas na lista
list_filter = [...]       # Filtros laterais
search_fields = [...]     # Campos de busca
ordering = [...]          # Ordenação padrão
date_hierarchy = '...'    # Navegação por data
readonly_fields = [...]   # Campos somente leitura
fieldsets = [...]         # Agrupamento de campos

Abra tarefas/admin.py e veja como está configurado!

EXERCÍCIO: 
1. Crie um superusuário se ainda não tiver
2. Acesse o admin e explore
3. Adicione list_filter por prioridade no TarefaAdmin''',
        'prioridade': 'baixa',
        'categoria_nome': '⚙️ Administração',
        'categoria_cor': 'danger',
    },
    
    # ==========================================================================
    # MÓDULO 7: CONCEITOS AVANÇADOS
    # ==========================================================================
    {
        'titulo': '🚀 Passo 11: Entender os Signals (signals.py)',
        'descricao': '''Signals permitem executar código quando eventos acontecem.

VOCÊ ESTÁ VENDO ISSO GRAÇAS A UM SIGNAL!
Este conteúdo foi criado pelo signal post_migrate em tarefas/signals.py

SIGNALS COMUNS:
- post_save: após salvar um objeto
- pre_save: antes de salvar
- post_delete: após deletar
- post_migrate: após rodar migrações

ESTRUTURA DE UM SIGNAL:
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Tarefa)
def depois_de_salvar(sender, instance, created, **kwargs):
    if created:
        print(f'Nova tarefa criada: {instance.titulo}')

CONEXÃO COM O APP:
Em apps.py, no método ready():
    def ready(self):
        from . import signals

CASOS DE USO:
- Enviar email quando tarefa for criada
- Atualizar contadores
- Limpar cache
- Criar registros relacionados
- Popular banco com dados iniciais (como este!)

EXERCÍCIO: Crie um signal que printa uma mensagem quando uma tarefa for deletada!''',
        'prioridade': 'baixa',
        'categoria_nome': '🚀 Avançado',
        'categoria_cor': 'danger',
    },
    {
        'titulo': '🚀 Passo 12: Arquivos Estáticos (CSS, JS)',
        'descricao': '''Arquivos estáticos são CSS, JavaScript, imagens, etc.

ESTRUTURA:
📁 static/
   └── css/
       └── style.css

CONFIGURAÇÃO EM settings.py:
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

NO TEMPLATE:
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}">

PARA PRODUÇÃO:
- Adicione STATIC_ROOT em settings.py
- Rode: python manage.py collectstatic
- Configure seu servidor web (nginx, etc.)

Abra static/css/style.css e veja os estilos personalizados!

EXERCÍCIO: Adicione um novo estilo CSS e use em um template!''',
        'prioridade': 'baixa',
        'categoria_nome': '🚀 Avançado',
        'categoria_cor': 'danger',
    },
    {
        'titulo': '🚀 Passo 13: Migrações do Django',
        'descricao': '''Migrações são como "versões" do seu banco de dados.

QUANDO VOCÊ MODIFICA UM MODEL:
1. python manage.py makemigrations
   → Cria arquivo de migração com as mudanças

2. python manage.py migrate
   → Aplica as mudanças no banco

ARQUIVOS DE MIGRAÇÃO:
📁 tarefas/migrations/
   ├── 0001_initial.py - Migração inicial
   └── 0002_xxx.py - Migrações subsequentes

COMANDOS ÚTEIS:
python manage.py showmigrations     # Lista migrações
python manage.py migrate --fake     # Marca como aplicada sem executar
python manage.py migrate app 0001   # Reverte para migração específica
python manage.py sqlmigrate app 0001  # Mostra SQL da migração

POR QUE USAR MIGRAÇÕES?
- Versiona mudanças no banco
- Permite trabalho em equipe
- Facilita deploy em produção
- Histórico de alterações

EXERCÍCIO: 
1. Adicione um campo "urgente = BooleanField(default=False)" ao model Tarefa
2. Rode makemigrations e veja o arquivo criado
3. Rode migrate para aplicar''',
        'prioridade': 'baixa',
        'categoria_nome': '🚀 Avançado',
        'categoria_cor': 'danger',
    },
    
    # ==========================================================================
    # PROJETO FINAL
    # ==========================================================================
    {
        'titulo': '🎯 Passo 14: Desafio Final - Crie sua própria funcionalidade!',
        'descricao': '''Parabéns por chegar até aqui! Agora é hora de praticar!

SUGESTÕES DE FUNCIONALIDADES PARA IMPLEMENTAR:

📌 NÍVEL FÁCIL:
- Adicionar campo "urgente" às tarefas
- Mostrar contador de tarefas na navbar
- Filtrar tarefas por prioridade na lista

📌 NÍVEL MÉDIO:
- Criar página de estatísticas
- Adicionar tags às tarefas (ManyToMany)
- Implementar busca por título
- Ordenar tarefas arrastando (JavaScript)

📌 NÍVEL AVANÇADO:
- Sistema de login/registro de usuários
- Cada usuário vê apenas suas tarefas
- Enviar email quando tarefa vencer
- API REST com Django REST Framework
- Deploy na nuvem (Railway, Render, etc.)

DICAS:
1. Comece pelo model (se precisar de novos dados)
2. Faça makemigrations e migrate
3. Crie a view
4. Adicione a URL
5. Crie ou modifique o template
6. Teste no navegador!

BOA SORTE E CONTINUE ESTUDANDO! 🚀

Documentação oficial: https://docs.djangoproject.com/''',
        'prioridade': 'alta',
        'categoria_nome': '🎯 Projeto Final',
        'categoria_cor': 'success',
    },
]


@receiver(post_migrate)
def popular_tarefas_estudo(sender, **kwargs):
    """
    Signal que popula o banco com tarefas de estudo após migrações.
    
    Este receiver é executado automaticamente após 'python manage.py migrate'.
    Ele cria as tarefas apenas se ainda não existirem (evita duplicação).
    
    Parâmetros:
        sender: O app que emitiu o sinal (AppConfig)
        **kwargs: Argumentos extras (app_config, verbosity, etc.)
    """
    # Só executa quando o app 'tarefas' termina de migrar
    if sender.name != 'tarefas':
        return
    
    # Não executa durante testes automatizados
    import sys
    if 'test' in sys.argv:
        return
    
    # Importa os models aqui dentro para evitar import circular
    from .models import Tarefa, Categoria
    
    # Verifica se já existem tarefas de estudo (evita duplicação)
    # Procura por uma tarefa específica do guia
    tarefa_existente = Tarefa.objects.filter(
        titulo__startswith='📚 Passo 1:'
    ).exists()
    
    if tarefa_existente:
        # Já populado, não faz nada
        return
    
    print('\n' + '=' * 60)
    print('📚 POPULANDO BANCO COM GUIA DE ESTUDO DO DJANGO')
    print('=' * 60)
    
    # Dicionário para armazenar categorias criadas (evita criar duplicadas)
    categorias_cache = {}
    
    for i, dados in enumerate(TAREFAS_ESTUDO, 1):
        # Obtém ou cria a categoria
        cat_nome = dados.get('categoria_nome')
        if cat_nome:
            if cat_nome not in categorias_cache:
                categoria, created = Categoria.objects.get_or_create(
                    nome=cat_nome,
                    defaults={'cor': dados.get('categoria_cor', 'primary')}
                )
                categorias_cache[cat_nome] = categoria
                if created:
                    print(f'  ✅ Categoria criada: {cat_nome}')
            categoria = categorias_cache[cat_nome]
        else:
            categoria = None
        
        # Cria a tarefa
        Tarefa.objects.create(
            titulo=dados['titulo'],
            descricao=dados['descricao'],
            prioridade=dados['prioridade'],
            categoria=categoria,
            concluida=False
        )
        print(f'  📝 Tarefa {i}/{len(TAREFAS_ESTUDO)}: {dados["titulo"][:50]}...')
    
    print('=' * 60)
    print(f'✅ {len(TAREFAS_ESTUDO)} tarefas de estudo criadas com sucesso!')
    print('💡 Acesse http://localhost:8000/ para ver o guia de estudo')
    print('=' * 60 + '\n')
