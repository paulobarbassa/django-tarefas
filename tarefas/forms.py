"""
=============================================================================
FORMS.PY - Formulários Django
=============================================================================

Formulários no Django facilitam:
- Geração de HTML de formulários
- Validação de dados
- Conversão de dados para tipos Python
- Salvamento no banco de dados

TIPOS DE FORMULÁRIOS:
1. Form: formulário genérico (não ligado a um model)
2. ModelForm: formulário baseado em um model (mais comum!)

ModelForm é mágico:
- Cria campos automaticamente baseado nos campos do model
- Valida dados de acordo com as regras do model
- Salva no banco com form.save()
"""

from django import forms
from .models import Tarefa, Categoria


# =============================================================================
# FORMULÁRIO BASEADO EM MODEL (ModelForm)
# =============================================================================

class TarefaForm(forms.ModelForm):
    """
    Formulário para criar e editar tarefas.
    
    ModelForm cria automaticamente:
    - Campos do formulário baseados nos campos do model
    - Validação baseada nas regras do model
    - Método save() que salva no banco
    """
    
    class Meta:
        """
        Configurações do ModelForm.
        """
        # Model que este formulário representa
        model = Tarefa
        
        # Campos que aparecerão no formulário
        # Opções:
        # - '__all__': todos os campos editáveis
        # - ['campo1', 'campo2']: lista específica de campos
        # - Use 'exclude' para excluir campos: exclude = ['criada_em']
        fields = ['titulo', 'descricao', 'prioridade', 'categoria', 'data_limite']
        
        # Widgets: personalizam a aparência dos campos HTML
        # Cada widget gera um tipo específico de input HTML
        widgets = {
            # TextInput: <input type="text">
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',  # Classe CSS (Bootstrap)
                'placeholder': 'Digite o título da tarefa',
                'autofocus': True,  # Foco automático ao carregar
            }),
            
            # Textarea: <textarea>
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descreva os detalhes (opcional)',
                'rows': 4,  # Altura do campo
            }),
            
            # Select: <select> (dropdown)
            'prioridade': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            # Select para ForeignKey
            'categoria': forms.Select(attrs={
                'class': 'form-select',
            }),
            
            # DateInput: <input type="date">
            'data_limite': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # Mostra seletor de data nativo do navegador
            }),
        }
        
        # Labels: rótulos personalizados para os campos
        labels = {
            'titulo': 'Título da Tarefa',
            'descricao': 'Descrição',
            'prioridade': 'Nível de Prioridade',
            'categoria': 'Categoria',
            'data_limite': 'Data Limite',
        }
        
        # Help texts: textos de ajuda abaixo dos campos
        help_texts = {
            'titulo': 'Um título claro e objetivo para sua tarefa.',
            'data_limite': 'Deixe em branco se não houver prazo.',
        }
        
        # Error messages: mensagens de erro personalizadas
        error_messages = {
            'titulo': {
                'required': 'O título é obrigatório!',
                'max_length': 'O título é muito longo (máximo 200 caracteres).',
            },
        }
    
    def clean_titulo(self):
        """
        Validação personalizada para o campo 'titulo'.
        
        Métodos clean_<campo>() são chamados automaticamente durante a validação.
        Devem retornar o valor limpo ou levantar ValidationError.
        """
        titulo = self.cleaned_data.get('titulo')
        
        # Remove espaços extras no início e fim
        titulo = titulo.strip()
        
        # Validação: título não pode ser muito curto
        if len(titulo) < 3:
            raise forms.ValidationError('O título deve ter pelo menos 3 caracteres.')
        
        # Validação: título não pode ser apenas números
        if titulo.isdigit():
            raise forms.ValidationError('O título não pode ser apenas números.')
        
        return titulo
    
    def clean(self):
        """
        Validação que envolve múltiplos campos.
        
        O método clean() é chamado DEPOIS dos métodos clean_<campo>().
        Use para validações que dependem de mais de um campo.
        """
        cleaned_data = super().clean()
        
        # Exemplo: se prioridade alta, descrição é obrigatória
        prioridade = cleaned_data.get('prioridade')
        descricao = cleaned_data.get('descricao')
        
        if prioridade == 'alta' and not descricao:
            self.add_error('descricao', 
                          'Tarefas de alta prioridade precisam de descrição!')
        
        return cleaned_data


# =============================================================================
# FORMULÁRIO GENÉRICO (Form)
# =============================================================================

class BuscaTarefaForm(forms.Form):
    """
    Formulário de busca (não ligado a um model).
    
    Use Form quando:
    - O formulário não corresponde a um model
    - Você precisa de campos customizados
    - É um formulário de busca/filtro
    """
    
    # Campo de texto para busca
    termo = forms.CharField(
        max_length=100,
        required=False,  # Não obrigatório
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar tarefas...',
        }),
        label='Buscar'
    )
    
    # Campo de seleção para status
    status = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('pendente', 'Pendentes'),
            ('concluida', 'Concluídas'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Status'
    )
    
    # Campo de seleção para categoria
    # Este campo será preenchido dinamicamente no __init__
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label='Todas as categorias',
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Categoria'
    )


# =============================================================================
# DICAS SOBRE FORMULÁRIOS
# =============================================================================
"""
CAMPOS DE FORMULÁRIO COMUNS:
- CharField: texto curto
- EmailField: email (com validação)
- IntegerField: número inteiro
- FloatField: número decimal
- BooleanField: checkbox
- ChoiceField: dropdown
- MultipleChoiceField: seleção múltipla
- DateField: data
- DateTimeField: data e hora
- FileField: upload de arquivo
- ImageField: upload de imagem
- ModelChoiceField: dropdown de objetos do banco
- ModelMultipleChoiceField: seleção múltipla de objetos

WIDGETS COMUNS:
- TextInput: <input type="text">
- Textarea: <textarea>
- PasswordInput: <input type="password">
- EmailInput: <input type="email">
- NumberInput: <input type="number">
- DateInput: <input type="date">
- TimeInput: <input type="time">
- Select: <select>
- SelectMultiple: <select multiple>
- CheckboxInput: <input type="checkbox">
- RadioSelect: radio buttons
- FileInput: <input type="file">

NO TEMPLATE:
    {{ form }}                  → Renderiza todo o formulário
    {{ form.as_p }}            → Cada campo em <p>
    {{ form.as_table }}        → Cada campo em <tr>
    {{ form.titulo }}          → Apenas o campo titulo
    {{ form.titulo.label }}    → Apenas o label
    {{ form.titulo.errors }}   → Apenas os erros
    {{ form.titulo.help_text }} → Texto de ajuda
    {{ form.non_field_errors }} → Erros não relacionados a campos
"""
