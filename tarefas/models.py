"""
=============================================================================
MODELS.PY - Modelos de Dados (ORM do Django)
=============================================================================

Os Models são classes Python que representam tabelas no banco de dados.
O Django usa um ORM (Object-Relational Mapping) que permite:
- Definir estrutura do banco usando classes Python
- Interagir com o banco usando objetos Python (sem SQL!)
- Migrações automáticas quando você muda a estrutura

CONCEITO: Cada classe Model = Uma tabela no banco
          Cada atributo da classe = Uma coluna na tabela
          Cada instância da classe = Uma linha na tabela

TIPOS DE CAMPOS MAIS COMUNS:
- CharField: texto curto (requer max_length)
- TextField: texto longo (sem limite)
- IntegerField: números inteiros
- FloatField: números decimais
- BooleanField: verdadeiro/falso
- DateField: data
- DateTimeField: data e hora
- EmailField: email (com validação)
- URLField: URL (com validação)
- ForeignKey: relacionamento muitos-para-um
- ManyToManyField: relacionamento muitos-para-muitos
- OneToOneField: relacionamento um-para-um
"""

from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    """
    Model que representa uma categoria de tarefas.
    
    Exemplos de categorias: Trabalho, Casa, Estudos, Pessoal
    
    RELACIONAMENTO: Uma categoria pode ter MUITAS tarefas
    (relacionamento um-para-muitos)
    """
    
    # -------------------------------------------------------------------------
    # CAMPOS DO MODEL
    # -------------------------------------------------------------------------
    
    # CharField: campo de texto curto
    # - max_length: tamanho máximo (OBRIGATÓRIO para CharField)
    # - verbose_name: nome amigável exibido no admin e formulários
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome da Categoria'
    )
    
    # TextField: campo de texto longo (sem limite de caracteres)
    # - blank=True: permite deixar vazio no formulário
    # - null=True: permite valor NULL no banco de dados
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    
    # CharField com choices: campo com opções predefinidas
    # Primeiro definimos as opções como tuplas (valor_banco, valor_exibido)
    CORES = [
        ('primary', '🔵 Azul'),
        ('success', '🟢 Verde'),
        ('danger', '🔴 Vermelho'),
        ('warning', '🟡 Amarelo'),
        ('info', '🔵 Ciano'),
        ('secondary', '⚫ Cinza'),
    ]
    cor = models.CharField(
        max_length=20,
        choices=CORES,          # Define as opções disponíveis
        default='primary',      # Valor padrão
        verbose_name='Cor'
    )
    
    # -------------------------------------------------------------------------
    # CLASSE META
    # -------------------------------------------------------------------------
    # A classe Meta define metadados do model (como ordenação, nomes, etc.)
    
    class Meta:
        # verbose_name: nome singular para exibição
        verbose_name = 'Categoria'
        
        # verbose_name_plural: nome plural para exibição
        verbose_name_plural = 'Categorias'
        
        # ordering: ordenação padrão das consultas
        # ['nome'] = ordena por nome A-Z
        # ['-nome'] = ordena por nome Z-A
        ordering = ['nome']
    
    # -------------------------------------------------------------------------
    # MÉTODOS DO MODEL
    # -------------------------------------------------------------------------
    
    def __str__(self):
        """
        Método especial que define como o objeto é exibido como string.
        Usado no admin, shell, e quando você faz print(objeto).
        
        Sem este método, você veria: <Categoria: Categoria object (1)>
        Com este método, você vê: <Categoria: Trabalho>
        """
        return self.nome


class Tarefa(models.Model):
    """
    Model principal que representa uma tarefa.
    
    Uma tarefa tem:
    - Título e descrição
    - Status de conclusão
    - Prioridade
    - Data de criação e conclusão
    - Categoria (opcional)
    """
    
    # -------------------------------------------------------------------------
    # CONSTANTES PARA CHOICES
    # -------------------------------------------------------------------------
    
    # Níveis de prioridade
    PRIORIDADE_BAIXA = 'baixa'
    PRIORIDADE_MEDIA = 'media'
    PRIORIDADE_ALTA = 'alta'
    
    PRIORIDADES = [
        (PRIORIDADE_BAIXA, '🟢 Baixa'),
        (PRIORIDADE_MEDIA, '🟡 Média'),
        (PRIORIDADE_ALTA, '🔴 Alta'),
    ]
    
    # -------------------------------------------------------------------------
    # CAMPOS DO MODEL
    # -------------------------------------------------------------------------
    
    # Título da tarefa
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Digite o título da tarefa'  # Texto de ajuda no formulário
    )
    
    # Descrição detalhada
    descricao = models.TextField(
        blank=True,  # Pode ficar vazio
        verbose_name='Descrição',
        help_text='Descreva os detalhes da tarefa (opcional)'
    )
    
    # Status de conclusão
    concluida = models.BooleanField(
        default=False,  # Novas tarefas começam como não concluídas
        verbose_name='Concluída'
    )
    
    # Prioridade
    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADES,
        default=PRIORIDADE_MEDIA,
        verbose_name='Prioridade'
    )
    
    # Data de criação
    # auto_now_add=True: define automaticamente na criação do objeto
    # Este campo NÃO pode ser editado depois
    criada_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criada em'
    )
    
    # Data de atualização
    # auto_now=True: atualiza automaticamente em cada save()
    atualizada_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizada em'
    )
    
    # Data de conclusão (preenchida quando a tarefa é marcada como concluída)
    concluida_em = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Concluída em'
    )
    
    # Data limite (prazo para conclusão)
    data_limite = models.DateField(
        blank=True,
        null=True,
        verbose_name='Data limite'
    )
    
    # -------------------------------------------------------------------------
    # RELACIONAMENTO COM CATEGORIA
    # -------------------------------------------------------------------------
    
    # ForeignKey: cria um relacionamento muitos-para-um
    # Muitas tarefas podem pertencer a UMA categoria
    # 
    # Parâmetros:
    # - Categoria: o model relacionado
    # - on_delete: o que fazer quando a categoria for deletada
    #   - CASCADE: deleta as tarefas junto
    #   - PROTECT: impede a deleção se houver tarefas
    #   - SET_NULL: define como NULL (requer null=True)
    #   - SET_DEFAULT: define um valor padrão
    # - related_name: nome para acessar tarefas a partir da categoria
    #   Exemplo: categoria.tarefas.all()
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tarefas',
        verbose_name='Categoria'
    )
    
    # -------------------------------------------------------------------------
    # CLASSE META
    # -------------------------------------------------------------------------
    
    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        
        # Ordenação: primeiro por prioridade (alta primeiro), depois por data
        # O hífen (-) indica ordem decrescente
        ordering = ['-prioridade', '-criada_em']
    
    # -------------------------------------------------------------------------
    # MÉTODOS DO MODEL
    # -------------------------------------------------------------------------
    
    def __str__(self):
        """Representação em string da tarefa."""
        status = '✅' if self.concluida else '⬜'
        return f'{status} {self.titulo}'
    
    def marcar_concluida(self):
        """
        Método personalizado para marcar a tarefa como concluída.
        
        Métodos assim encapsulam lógica de negócio no model,
        mantendo o código organizado e reutilizável.
        """
        self.concluida = True
        self.concluida_em = timezone.now()
        self.save()  # Salva as alterações no banco
    
    def marcar_pendente(self):
        """Método para desmarcar a tarefa como concluída."""
        self.concluida = False
        self.concluida_em = None
        self.save()
    
    @property
    def esta_atrasada(self):
        """
        Property que verifica se a tarefa está atrasada.
        
        @property permite acessar como atributo: tarefa.esta_atrasada
        em vez de método: tarefa.esta_atrasada()
        """
        if self.data_limite and not self.concluida:
            return timezone.now().date() > self.data_limite
        return False
    
    @property
    def emoji_prioridade(self):
        """Retorna o emoji correspondente à prioridade."""
        emojis = {
            self.PRIORIDADE_BAIXA: '🟢',
            self.PRIORIDADE_MEDIA: '🟡',
            self.PRIORIDADE_ALTA: '🔴',
        }
        return emojis.get(self.prioridade, '⚪')


# =============================================================================
# DICAS DE USO DO ORM
# =============================================================================
"""
Exemplos de consultas com o ORM do Django (use no shell: python manage.py shell)

# CRIAR registros:
tarefa = Tarefa.objects.create(titulo='Estudar Django', prioridade='alta')
tarefa = Tarefa(titulo='Outra tarefa')
tarefa.save()

# LER registros:
todas = Tarefa.objects.all()           # Todas as tarefas
uma = Tarefa.objects.get(id=1)         # Uma tarefa específica (erro se não existir)
uma = Tarefa.objects.filter(id=1).first()  # Uma tarefa (None se não existir)

# FILTRAR registros:
pendentes = Tarefa.objects.filter(concluida=False)
altas = Tarefa.objects.filter(prioridade='alta')
trabalho = Tarefa.objects.filter(categoria__nome='Trabalho')  # Filtro por relação

# EXCLUIR filtros:
nao_concluidas = Tarefa.objects.exclude(concluida=True)

# ORDENAR:
por_data = Tarefa.objects.order_by('criada_em')   # Mais antigas primeiro
por_data = Tarefa.objects.order_by('-criada_em')  # Mais recentes primeiro

# CONTAR:
total = Tarefa.objects.count()
pendentes = Tarefa.objects.filter(concluida=False).count()

# ATUALIZAR:
tarefa.titulo = 'Novo título'
tarefa.save()
# OU atualização em massa:
Tarefa.objects.filter(concluida=True).update(prioridade='baixa')

# DELETAR:
tarefa.delete()
# OU deleção em massa:
Tarefa.objects.filter(concluida=True).delete()

# ENCADEAR métodos:
tarefas = Tarefa.objects.filter(concluida=False).exclude(prioridade='baixa').order_by('-criada_em')[:10]
"""
