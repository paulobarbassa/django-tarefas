"""
=============================================================================
__INIT__.PY - Arquivo de Inicialização do Pacote Python
=============================================================================

Este arquivo indica ao Python que esta pasta é um "pacote Python".
Um pacote é uma forma de organizar módulos Python relacionados.

Mesmo estando vazio, este arquivo é OBRIGATÓRIO para que o Python
reconheça a pasta 'core' como um pacote importável.

Exemplo de uso:
    from core import settings
    from core.urls import urlpatterns

Curiosidade: A partir do Python 3.3, existem "namespace packages" que
não precisam do __init__.py, mas o Django ainda exige este arquivo
para funcionar corretamente.
"""
