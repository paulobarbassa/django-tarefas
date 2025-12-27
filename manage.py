#!/usr/bin/env python
"""
=============================================================================
MANAGE.PY - O Ponto de Entrada do Projeto Django
=============================================================================

Este arquivo é o script de linha de comando do Django que permite executar
várias tarefas administrativas como:

    - python manage.py runserver     → Inicia o servidor de desenvolvimento
    - python manage.py migrate       → Aplica migrações no banco de dados
    - python manage.py makemigrations → Cria novas migrações
    - python manage.py createsuperuser → Cria um usuário administrador
    - python manage.py shell         → Abre o shell interativo do Django

Este arquivo é gerado automaticamente pelo comando 'django-admin startproject'
e geralmente não precisa ser modificado.
"""
import os
import sys


def main():
    """
    Função principal que configura o ambiente Django e executa comandos.
    
    Passos:
    1. Define qual arquivo de configurações usar (settings.py)
    2. Importa e executa a função de linha de comando do Django
    """
    # Define a variável de ambiente que aponta para as configurações do projeto
    # 'core.settings' significa: pasta 'core', arquivo 'settings.py'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    
    try:
        # Importa a função que processa os comandos do Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Se o Django não estiver instalado, mostra uma mensagem de erro amigável
        raise ImportError(
            "Não foi possível importar o Django. Você tem certeza que ele está "
            "instalado e disponível na variável de ambiente PYTHONPATH? "
            "Você esqueceu de ativar o ambiente virtual?"
        ) from exc
    
    # Executa o comando que foi passado na linha de comando
    # sys.argv contém os argumentos, ex: ['manage.py', 'runserver']
    execute_from_command_line(sys.argv)


# Este bloco só executa se o arquivo for rodado diretamente
# (não quando é importado como módulo)
if __name__ == '__main__':
    main()
