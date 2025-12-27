"""
=============================================================================
MIGRATIONS/__INIT__.PY - Pasta de Migrações
=============================================================================

Esta pasta contém as migrações do banco de dados.

MIGRAÇÕES são arquivos Python que descrevem alterações na estrutura
do banco de dados (criar tabelas, adicionar campos, etc.).

O Django cria migrações automaticamente quando você executa:
    python manage.py makemigrations

E aplica as migrações com:
    python manage.py migrate

FLUXO DE TRABALHO:
1. Você altera models.py (adiciona campo, cria model, etc.)
2. Executa: python manage.py makemigrations
3. Django cria arquivo de migração (ex: 0001_initial.py)
4. Executa: python manage.py migrate
5. Django aplica as alterações no banco de dados

COMANDOS ÚTEIS:
    python manage.py showmigrations      # Lista todas as migrações
    python manage.py migrate --fake      # Marca como aplicada sem executar
    python manage.py migrate app 0001    # Volta para migração específica
    python manage.py sqlmigrate app 0001 # Mostra SQL da migração

NUNCA delete migrações já aplicadas em produção!
"""
