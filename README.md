# 📋 Gerenciador de Tarefas - Projeto Django Educativo

Este é um projeto Django **100% comentado** criado para fins educativos.
Cada arquivo contém explicações detalhadas sobre o funcionamento do Django.

## 🎯 Objetivo

Ensinar os conceitos fundamentais do Django através de um exemplo prático:
um sistema de gerenciamento de tarefas (To-Do List).

## 📚 O que você vai aprender

- **Models**: Como definir estrutura do banco de dados
- **Views**: Lógica de negócio (funções e classes)
- **Templates**: Sistema de templates HTML do Django
- **Forms**: Formulários com validação
- **Admin**: Painel administrativo automático
- **URLs**: Roteamento de requisições
- **ORM**: Consultas ao banco sem SQL

## 🚀 Como executar o projeto

### 1. Pré-requisitos

- Python 3.14 ou superior
- pip (gerenciador de pacotes Python)
- Git

> 💡 **Sobre o banco de dados**: Este projeto usa **SQLite**, que já vem embutido no Python. Não é necessário instalar nenhum banco de dados separado! O arquivo `db.sqlite3` será criado automaticamente ao executar as migrações.

#### Instalação do Python 3.14 (Windows via WinGet)

```powershell
winget install -e --id Python.Python.3.14 --scope machine
```

### 2. Clonar o repositório

```bash
git clone https://github.com/paulobarbassa/django-tarefas.git
cd django-tarefas
```

### 3. Criar ambiente virtual (recomendado)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Ativar ambiente (Linux/Mac)
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Aplicar migrações (criar banco de dados)

```bash
python manage.py migrate
```

### 6. Criar superusuário (para acessar o admin)

```bash
python manage.py createsuperuser
```

### 7. Executar o servidor

```bash
python manage.py runserver
```

### 8. Acessar o projeto

- **Site**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/

## 📁 Estrutura do Projeto

```
Projeto Django/
├── manage.py                 # Script de gerenciamento
├── requirements.txt          # Dependências do projeto
├── README.md                 # Este arquivo
├── db.sqlite3               # Banco de dados (criado após migrate)
│
├── core/             # Configurações do projeto
│   ├── __init__.py          # Marca como pacote Python
│   ├── settings.py          # Configurações principais ⭐
│   ├── urls.py              # URLs principais
│   ├── wsgi.py              # Configuração WSGI
│   └── asgi.py              # Configuração ASGI
│
├── tarefas/                 # App de tarefas
│   ├── __init__.py          # Marca como pacote Python
│   ├── admin.py             # Configuração do admin ⭐
│   ├── apps.py              # Configuração do app
│   ├── forms.py             # Formulários ⭐
│   ├── models.py            # Modelos de dados ⭐
│   ├── urls.py              # URLs do app
│   ├── views.py             # Views (lógica) ⭐
│   ├── migrations/          # Migrações do banco
│   └── templates/           # Templates HTML
│       └── tarefas/
│           ├── index.html
│           ├── lista.html
│           ├── form.html
│           ├── detalhe.html
│           ├── excluir.html
│           └── categorias.html
│
├── templates/               # Templates globais
│   └── base.html            # Template base ⭐
│
└── static/                  # Arquivos estáticos (CSS, JS)
```

⭐ = Arquivos mais importantes para estudar

## 📖 Ordem sugerida de estudo

1. **settings.py** - Entenda as configurações do Django
2. **models.py** - Como criar tabelas no banco de dados
3. **admin.py** - Como usar o painel administrativo
4. **views.py** - Lógica de negócio e processamento
5. **urls.py** - Como mapear URLs para views
6. **forms.py** - Formulários com validação
7. **templates/** - Sistema de templates HTML

## 🔧 Comandos úteis do Django

```bash
# Criar novo projeto
django-admin startproject nome_projeto

# Criar novo app
python manage.py startapp nome_app

# Criar migrações (após alterar models)
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver

# Abrir shell interativo
python manage.py shell

# Executar testes automatizados
python manage.py test

# Executar testes com cobertura
coverage run manage.py test
coverage report

# Coletar arquivos estáticos (produção)
python manage.py collectstatic
```

## 🧪 Testes Automatizados

O projeto inclui 30 testes automatizados que cobrem:

- **Models**: Criação, métodos e relacionamentos
- **Views**: Requisições GET/POST, filtros e redirecionamentos
- **Forms**: Validação de campos obrigatórios e regras de negócio
- **Integração**: Fluxos completos de criação e edição

```bash
# Rodar todos os testes
python manage.py test

# Rodar testes com detalhes
python manage.py test --verbosity=2

# Rodar testes de uma app específica
python manage.py test tarefas
```

## 🔄 CI/CD com GitHub Actions

O projeto utiliza GitHub Actions para Integração Contínua:

- ✅ Testes em múltiplas versões do Python (3.10, 3.11, 3.12)
- ✅ Verificação de código com Flake8 (linting)
- ✅ Verificação de migrações pendentes
- ✅ Análise de segurança com Bandit e pip-audit
- ✅ Cobertura de testes com Coverage

O workflow é executado automaticamente em:
- Push para branches `main` ou `develop`
- Pull Requests para branches `main` ou `develop`

## 🐚 Exemplos no Shell

```python
# Acessar o shell
python manage.py shell

# Importar modelo
from tarefas.models import Tarefa, Categoria

# Criar categoria
cat = Categoria.objects.create(nome='Trabalho', cor='primary')

# Criar tarefa
tarefa = Tarefa.objects.create(
    titulo='Estudar Django',
    descricao='Ler toda a documentação',
    prioridade='alta',
    categoria=cat
)

# Listar tarefas
Tarefa.objects.all()

# Filtrar tarefas
Tarefa.objects.filter(concluida=False)

# Marcar como concluída
tarefa.marcar_concluida()
```

## 📚 Recursos para aprender mais

- [Documentação oficial do Django](https://docs.djangoproject.com/)
- [Tutorial oficial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/pt/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## 📝 Licença

Este projeto é livre para uso educacional.
Sinta-se à vontade para estudar, modificar e compartilhar!

---

Feito com ❤️ para aprender Django
