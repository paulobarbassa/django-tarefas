"""
=============================================================================
TESTS.PY - Testes Automatizados
=============================================================================

Os testes garantem que seu código funciona corretamente e continuará
funcionando quando você fizer alterações.

TIPOS DE TESTES:
1. Unit Tests: testam funções/métodos individuais
2. Integration Tests: testam múltiplos componentes juntos
3. Functional Tests: testam funcionalidades completas

COMANDOS:
    python manage.py test                    # Roda todos os testes
    python manage.py test tarefas            # Testa apenas a app 'tarefas'
    python manage.py test tarefas.tests.NomeClasse  # Testa uma classe específica
    python manage.py test --verbosity=2      # Mostra mais detalhes

BOAS PRÁTICAS:
- Nome de métodos de teste começam com 'test_'
- Um teste deve verificar apenas uma coisa
- Use setUp() para preparar dados de teste
- Testes devem ser independentes entre si
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import Tarefa, Categoria
from .forms import TarefaForm


# =============================================================================
# TESTES DOS MODELS
# =============================================================================

class CategoriaModelTest(TestCase):
    """Testes para o model Categoria."""
    
    def setUp(self):
        """
        Configuração inicial para os testes.
        Executado antes de cada método de teste.
        """
        self.categoria = Categoria.objects.create(
            nome='Trabalho',
            descricao='Tarefas relacionadas ao trabalho',
            cor='primary'
        )
    
    def test_categoria_criacao(self):
        """Testa se a categoria é criada corretamente."""
        self.assertEqual(self.categoria.nome, 'Trabalho')
        self.assertEqual(self.categoria.cor, 'primary')
    
    def test_categoria_str(self):
        """Testa a representação em string da categoria."""
        self.assertEqual(str(self.categoria), 'Trabalho')
    
    def test_categoria_verbose_name(self):
        """Testa os nomes verbosos do model."""
        self.assertEqual(
            Categoria._meta.verbose_name,
            'Categoria'
        )
        self.assertEqual(
            Categoria._meta.verbose_name_plural,
            'Categorias'
        )


class TarefaModelTest(TestCase):
    """Testes para o model Tarefa."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.categoria = Categoria.objects.create(nome='Estudos')
        self.tarefa = Tarefa.objects.create(
            titulo='Estudar Django',
            descricao='Aprender sobre testes automatizados',
            prioridade='alta',
            categoria=self.categoria
        )
    
    def test_tarefa_criacao(self):
        """Testa se a tarefa é criada corretamente."""
        self.assertEqual(self.tarefa.titulo, 'Estudar Django')
        self.assertEqual(self.tarefa.prioridade, 'alta')
        self.assertFalse(self.tarefa.concluida)
    
    def test_tarefa_str(self):
        """Testa a representação em string da tarefa."""
        # Tarefa não concluída deve ter ⬜
        self.assertIn('⬜', str(self.tarefa))
        self.assertIn('Estudar Django', str(self.tarefa))
    
    def test_tarefa_str_concluida(self):
        """Testa a string de uma tarefa concluída."""
        self.tarefa.concluida = True
        self.tarefa.save()
        self.assertIn('✅', str(self.tarefa))
    
    def test_marcar_concluida(self):
        """Testa o método marcar_concluida()."""
        self.tarefa.marcar_concluida()
        self.assertTrue(self.tarefa.concluida)
        self.assertIsNotNone(self.tarefa.concluida_em)
    
    def test_marcar_pendente(self):
        """Testa o método marcar_pendente()."""
        self.tarefa.marcar_concluida()
        self.tarefa.marcar_pendente()
        self.assertFalse(self.tarefa.concluida)
        self.assertIsNone(self.tarefa.concluida_em)
    
    def test_esta_atrasada_sem_data_limite(self):
        """Testa esta_atrasada quando não há data limite."""
        self.assertFalse(self.tarefa.esta_atrasada)
    
    def test_esta_atrasada_com_data_futura(self):
        """Testa esta_atrasada com data limite no futuro."""
        self.tarefa.data_limite = timezone.now().date() + timedelta(days=7)
        self.tarefa.save()
        self.assertFalse(self.tarefa.esta_atrasada)
    
    def test_esta_atrasada_com_data_passada(self):
        """Testa esta_atrasada com data limite no passado."""
        self.tarefa.data_limite = timezone.now().date() - timedelta(days=1)
        self.tarefa.save()
        self.assertTrue(self.tarefa.esta_atrasada)
    
    def test_esta_atrasada_tarefa_concluida(self):
        """Tarefa concluída nunca está atrasada."""
        self.tarefa.data_limite = timezone.now().date() - timedelta(days=1)
        self.tarefa.concluida = True
        self.tarefa.save()
        self.assertFalse(self.tarefa.esta_atrasada)
    
    def test_emoji_prioridade(self):
        """Testa o emoji de prioridade."""
        self.tarefa.prioridade = 'baixa'
        self.assertEqual(self.tarefa.emoji_prioridade, '🟢')
        
        self.tarefa.prioridade = 'media'
        self.assertEqual(self.tarefa.emoji_prioridade, '🟡')
        
        self.tarefa.prioridade = 'alta'
        self.assertEqual(self.tarefa.emoji_prioridade, '🔴')
    
    def test_relacionamento_categoria(self):
        """Testa o relacionamento com Categoria."""
        self.assertEqual(self.tarefa.categoria.nome, 'Estudos')
        self.assertIn(self.tarefa, self.categoria.tarefas.all())


# =============================================================================
# TESTES DAS VIEWS
# =============================================================================

class IndexViewTest(TestCase):
    """Testes para a view index."""
    
    def setUp(self):
        """Configuração inicial."""
        self.client = Client()
    
    def test_index_view_status_code(self):
        """Testa se a página inicial retorna status 200."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_index_view_template(self):
        """Testa se a view usa o template correto."""
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'tarefas/index.html')
    
    def test_index_view_context(self):
        """Testa se o contexto contém as estatísticas."""
        # Cria algumas tarefas
        Tarefa.objects.create(titulo='Tarefa 1', concluida=False)
        Tarefa.objects.create(titulo='Tarefa 2', concluida=True)
        
        response = self.client.get(reverse('index'))
        
        self.assertIn('total_tarefas', response.context)
        self.assertIn('tarefas_pendentes', response.context)
        self.assertIn('tarefas_concluidas', response.context)
        self.assertEqual(response.context['total_tarefas'], 2)
        self.assertEqual(response.context['tarefas_pendentes'], 1)
        self.assertEqual(response.context['tarefas_concluidas'], 1)


class ListaTarefasViewTest(TestCase):
    """Testes para a view lista_tarefas."""
    
    def setUp(self):
        """Configuração inicial."""
        self.client = Client()
        self.categoria = Categoria.objects.create(nome='Trabalho')
        self.tarefa1 = Tarefa.objects.create(
            titulo='Tarefa Pendente',
            prioridade='alta',
            concluida=False
        )
        self.tarefa2 = Tarefa.objects.create(
            titulo='Tarefa Concluída',
            prioridade='baixa',
            concluida=True
        )
    
    def test_lista_view_status_code(self):
        """Testa se a lista retorna status 200."""
        response = self.client.get(reverse('lista_tarefas'))
        self.assertEqual(response.status_code, 200)
    
    def test_lista_view_template(self):
        """Testa se usa o template correto."""
        response = self.client.get(reverse('lista_tarefas'))
        self.assertTemplateUsed(response, 'tarefas/lista.html')
    
    def test_filtro_pendentes(self):
        """Testa o filtro de tarefas pendentes."""
        response = self.client.get(reverse('lista_tarefas'), {'status': 'pendentes'})
        tarefas = response.context['tarefas']
        self.assertEqual(tarefas.count(), 1)
        self.assertFalse(tarefas.first().concluida)
    
    def test_filtro_concluidas(self):
        """Testa o filtro de tarefas concluídas."""
        response = self.client.get(reverse('lista_tarefas'), {'status': 'concluidas'})
        tarefas = response.context['tarefas']
        self.assertEqual(tarefas.count(), 1)
        self.assertTrue(tarefas.first().concluida)


class CriarTarefaViewTest(TestCase):
    """Testes para a view criar_tarefa."""
    
    def setUp(self):
        """Configuração inicial."""
        self.client = Client()
    
    def test_criar_tarefa_get(self):
        """Testa se GET retorna o formulário."""
        response = self.client.get(reverse('criar_tarefa'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tarefas/form.html')
        self.assertIn('form', response.context)
    
    def test_criar_tarefa_post_valido(self):
        """Testa criação de tarefa com dados válidos."""
        dados = {
            'titulo': 'Nova Tarefa',
            'descricao': 'Descrição da tarefa',
            'prioridade': 'media',
        }
        response = self.client.post(reverse('criar_tarefa'), dados)
        
        # Deve redirecionar após sucesso
        self.assertEqual(response.status_code, 302)
        
        # Verifica se a tarefa foi criada
        self.assertTrue(Tarefa.objects.filter(titulo='Nova Tarefa').exists())
    
    def test_criar_tarefa_post_invalido(self):
        """Testa criação de tarefa com dados inválidos."""
        dados = {
            'titulo': '',  # Título vazio é inválido
        }
        response = self.client.post(reverse('criar_tarefa'), dados)
        
        # Deve retornar o formulário com erros
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())


class TarefaDetailViewTest(TestCase):
    """Testes para a view de detalhes."""
    
    def setUp(self):
        """Configuração inicial."""
        self.client = Client()
        self.tarefa = Tarefa.objects.create(
            titulo='Tarefa de Teste',
            descricao='Descrição detalhada'
        )
    
    def test_detalhe_view_status_code(self):
        """Testa se a página de detalhes retorna status 200."""
        response = self.client.get(
            reverse('detalhe_tarefa', kwargs={'pk': self.tarefa.pk})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_detalhe_view_404(self):
        """Testa se retorna 404 para tarefa inexistente."""
        response = self.client.get(
            reverse('detalhe_tarefa', kwargs={'pk': 9999})
        )
        self.assertEqual(response.status_code, 404)


# =============================================================================
# TESTES DOS FORMULÁRIOS
# =============================================================================

class TarefaFormTest(TestCase):
    """Testes para o formulário de Tarefa."""
    
    def test_form_campos_obrigatorios(self):
        """Testa se título é obrigatório."""
        form = TarefaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('titulo', form.errors)
    
    def test_form_valido(self):
        """Testa formulário com dados válidos."""
        dados = {
            'titulo': 'Tarefa Válida',
            'descricao': 'Descrição',
            'prioridade': 'alta',
        }
        form = TarefaForm(data=dados)
        self.assertTrue(form.is_valid())
    
    def test_form_titulo_muito_longo(self):
        """Testa validação de título muito longo."""
        dados = {
            'titulo': 'A' * 201,  # Mais de 200 caracteres
            'prioridade': 'media',
        }
        form = TarefaForm(data=dados)
        self.assertFalse(form.is_valid())


# =============================================================================
# TESTES DE INTEGRAÇÃO
# =============================================================================

class TarefaWorkflowTest(TestCase):
    """Testes de fluxo completo (integração)."""
    
    def setUp(self):
        """Configuração inicial."""
        self.client = Client()
    
    def test_fluxo_criar_e_concluir_tarefa(self):
        """Testa o fluxo completo: criar, visualizar e concluir tarefa."""
        # 1. Criar tarefa (prioridade alta requer descrição)
        dados = {
            'titulo': 'Tarefa do Fluxo',
            'descricao': 'Descrição da tarefa para o teste',
            'prioridade': 'alta',
        }
        response = self.client.post(reverse('criar_tarefa'), dados, follow=True)
        self.assertEqual(response.status_code, 200)
        
        # 2. Verificar se foi criada
        tarefa = Tarefa.objects.get(titulo='Tarefa do Fluxo')
        self.assertFalse(tarefa.concluida)
        
        # 3. Alternar status para concluída
        response = self.client.get(
            reverse('alternar_status', kwargs={'pk': tarefa.pk}),
            follow=True
        )
        
        # 4. Verificar se foi concluída
        tarefa.refresh_from_db()
        self.assertTrue(tarefa.concluida)
