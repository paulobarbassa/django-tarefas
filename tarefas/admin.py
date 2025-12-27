"""
=============================================================================
ADMIN.PY - Configuração do Painel Administrativo
=============================================================================

O Django Admin é uma interface web automática para gerenciar dados.
É uma das funcionalidades mais poderosas do Django!

Com poucas linhas de código, você tem:
- CRUD completo (Create, Read, Update, Delete)
- Busca, filtros e ordenação
- Ações em massa
- Permissões por usuário

ACESSO: http://localhost:8000/admin/
(Precisa criar um superuser: python manage.py createsuperuser)
"""

from django.contrib import admin
from .models import Tarefa, Categoria


# =============================================================================
# ADMINISTRAÇÃO SIMPLES
# =============================================================================
# A forma mais simples de registrar um model no admin

# admin.site.register(Categoria)  # Registro básico (sem customização)


# =============================================================================
# ADMINISTRAÇÃO CUSTOMIZADA
# =============================================================================
# Use classes ModelAdmin para customizar a interface

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o model Categoria.
    
    @admin.register(Model) é um decorador que registra o admin automaticamente.
    É equivalente a: admin.site.register(Categoria, CategoriaAdmin)
    """
    
    # -------------------------------------------------------------------------
    # LISTAGEM
    # -------------------------------------------------------------------------
    
    # Colunas exibidas na listagem
    # Pode incluir campos do model e métodos
    list_display = ['nome', 'cor', 'quantidade_tarefas', 'descricao']
    
    # Campos clicáveis que levam ao formulário de edição
    list_display_links = ['nome']
    
    # Campos que podem ser editados diretamente na listagem
    # list_editable = ['cor']
    
    # Campos usados na busca
    search_fields = ['nome', 'descricao']
    
    # Filtros na barra lateral
    list_filter = ['cor']
    
    # Ordenação padrão
    ordering = ['nome']
    
    # Quantidade de itens por página
    list_per_page = 20
    
    # -------------------------------------------------------------------------
    # MÉTODOS PERSONALIZADOS
    # -------------------------------------------------------------------------
    
    @admin.display(description='Qtd. Tarefas')
    def quantidade_tarefas(self, obj):
        """
        Método que retorna a quantidade de tarefas na categoria.
        
        @admin.display: decorador que define metadados do método
        - description: texto do cabeçalho da coluna
        - ordering: campo usado para ordenar por esta coluna
        - boolean: se True, exibe ✅/❌ ao invés de True/False
        """
        return obj.tarefas.count()


@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o model Tarefa.
    """
    
    # -------------------------------------------------------------------------
    # LISTAGEM
    # -------------------------------------------------------------------------
    
    list_display = [
        'titulo', 
        'categoria', 
        'prioridade_colorida',
        'concluida',
        'data_limite', 
        'criada_em'
    ]
    
    list_display_links = ['titulo']
    
    # Campos editáveis na listagem (checkbox de concluída)
    list_editable = ['concluida']
    
    # Busca em múltiplos campos
    search_fields = ['titulo', 'descricao', 'categoria__nome']
    
    # Filtros na sidebar
    list_filter = ['concluida', 'prioridade', 'categoria', 'criada_em']
    
    # Ordenação
    ordering = ['-criada_em']
    
    # Itens por página
    list_per_page = 25
    
    # Filtro de datas na parte superior
    date_hierarchy = 'criada_em'
    
    # -------------------------------------------------------------------------
    # FORMULÁRIO DE EDIÇÃO
    # -------------------------------------------------------------------------
    
    # Campos somente leitura (não podem ser editados)
    readonly_fields = ['criada_em', 'atualizada_em', 'concluida_em']
    
    # Organização dos campos em seções (fieldsets)
    fieldsets = [
        # (Nome da seção, {opções})
        ('Informações Básicas', {
            'fields': ['titulo', 'descricao'],
            'description': 'Preencha as informações principais da tarefa.'
        }),
        ('Classificação', {
            'fields': ['prioridade', 'categoria', 'data_limite'],
        }),
        ('Status', {
            'fields': ['concluida', 'concluida_em'],
            'classes': ['collapse'],  # Seção recolhível
        }),
        ('Metadados', {
            'fields': ['criada_em', 'atualizada_em'],
            'classes': ['collapse'],  # Seção recolhível
        }),
    ]
    
    # Campos preenchidos automaticamente (ex: slug a partir do título)
    # prepopulated_fields = {'slug': ('titulo',)}
    
    # -------------------------------------------------------------------------
    # AÇÕES EM MASSA
    # -------------------------------------------------------------------------
    
    # Ações personalizadas aparecem no dropdown de ações
    actions = ['marcar_como_concluida', 'marcar_como_pendente', 'definir_prioridade_alta']
    
    @admin.action(description='✅ Marcar selecionadas como concluídas')
    def marcar_como_concluida(self, request, queryset):
        """
        Ação para marcar múltiplas tarefas como concluídas.
        
        queryset: QuerySet com os objetos selecionados
        """
        from django.utils import timezone
        count = queryset.update(concluida=True, concluida_em=timezone.now())
        self.message_user(request, f'{count} tarefa(s) marcada(s) como concluída(s).')
    
    @admin.action(description='⬜ Marcar selecionadas como pendentes')
    def marcar_como_pendente(self, request, queryset):
        """Ação para marcar múltiplas tarefas como pendentes."""
        count = queryset.update(concluida=False, concluida_em=None)
        self.message_user(request, f'{count} tarefa(s) marcada(s) como pendente(s).')
    
    @admin.action(description='🔴 Definir prioridade alta')
    def definir_prioridade_alta(self, request, queryset):
        """Ação para definir prioridade alta em múltiplas tarefas."""
        count = queryset.update(prioridade='alta')
        self.message_user(request, f'{count} tarefa(s) atualizada(s) para prioridade alta.')
    
    # -------------------------------------------------------------------------
    # MÉTODOS PERSONALIZADOS PARA EXIBIÇÃO
    # -------------------------------------------------------------------------
    
    @admin.display(description='Prioridade', ordering='prioridade')
    def prioridade_colorida(self, obj):
        """
        Exibe a prioridade com cor/emoji.
        
        Retorna HTML para estilizar a célula.
        """
        from django.utils.html import format_html
        
        cores = {
            'baixa': '#28a745',   # Verde
            'media': '#ffc107',   # Amarelo
            'alta': '#dc3545',    # Vermelho
        }
        emojis = {
            'baixa': '🟢',
            'media': '🟡',
            'alta': '🔴',
        }
        
        cor = cores.get(obj.prioridade, '#6c757d')
        emoji = emojis.get(obj.prioridade, '⚪')
        
        # format_html: escapa HTML exceto onde você marcar como seguro
        return format_html(
            '<span style="color: {};">{} {}</span>',
            cor,
            emoji,
            obj.get_prioridade_display()  # Retorna o label do choice
        )
    
    # -------------------------------------------------------------------------
    # AUTOCOMPLETE
    # -------------------------------------------------------------------------
    
    # Campos com autocomplete (útil quando há muitas opções)
    # autocomplete_fields = ['categoria']
    
    # Para funcionar, CategoriaAdmin precisa ter search_fields definido


# =============================================================================
# CUSTOMIZAÇÃO GLOBAL DO ADMIN
# =============================================================================

# Título do site admin (aparece na aba do navegador)
admin.site.site_title = 'Tarefas Admin'

# Título no cabeçalho do admin
admin.site.site_header = '📋 Gerenciador de Tarefas'

# Texto no topo da página inicial do admin
admin.site.index_title = 'Painel de Administração'
