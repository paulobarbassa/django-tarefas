"""
=============================================================================
APPS.PY - Configuração do App
=============================================================================

Este arquivo configura o aplicativo Django.
O Django usa essas informações para:
- Identificar o app
- Carregar configurações
- Executar código de inicialização

Cada app Django deve ter este arquivo.
"""

from django.apps import AppConfig


class TarefasConfig(AppConfig):
    """
    Classe de configuração do app 'tarefas'.
    
    Atributos:
        name: Nome do app (deve corresponder ao nome da pasta)
        verbose_name: Nome amigável exibido no admin
        default_auto_field: Tipo de campo para chaves primárias automáticas
    """
    
    # Tipo padrão de chave primária
    # BigAutoField: inteiro de 64 bits (suporta mais registros)
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nome do app (deve ser igual ao nome da pasta)
    name = 'tarefas'
    
    # Nome amigável (exibido no Django Admin)
    verbose_name = '📋 Gerenciador de Tarefas'
    
    def ready(self):
        """
        Método chamado quando o app é carregado.
        
        Use para:
        - Importar signals (sinais)
        - Executar código de inicialização
        - Registrar hooks
        
        CUIDADO: Este método é chamado DUAS VEZES no runserver!
        Para evitar duplicação, use: if not self.ready_run
        
        Exemplo de uso com signals:
            from . import signals  # Importa os handlers de signals
        """
        pass  # Não precisamos de nada especial por enquanto
