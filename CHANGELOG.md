# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-12-27

### ✨ Adicionado

- **Sistema de Tarefas**
  - Criação, edição e exclusão de tarefas
  - Campos: título, descrição, prioridade, data de vencimento
  - Marcar tarefas como concluídas
  - Filtros por status (pendentes, concluídas, todas)

- **Sistema de Categorias**
  - Criação e gerenciamento de categorias
  - Cores personalizadas para cada categoria
  - Associação de tarefas a categorias

- **Interface do Usuário**
  - Design responsivo com Bootstrap
  - Template base reutilizável
  - Páginas: lista, detalhes, formulário, exclusão

- **Painel Administrativo**
  - Configuração completa do Django Admin
  - Filtros e busca para tarefas e categorias

- **Testes Automatizados**
  - 30 testes cobrindo models, views e forms
  - Integração contínua com GitHub Actions

- **Documentação**
  - README completo com instruções de instalação
  - Código 100% comentado para fins educativos
  - Ordem sugerida de estudo

### 🔧 Infraestrutura

- Configuração do projeto Django
- Migrações do banco de dados
- Arquivos estáticos (CSS)
- CI/CD com GitHub Actions
- Verificação de código com Flake8
- Análise de segurança com Bandit

---

## Tipos de mudanças

- ✨ **Adicionado** - para novas funcionalidades
- 🔄 **Modificado** - para mudanças em funcionalidades existentes
- 🗑️ **Removido** - para funcionalidades removidas
- 🐛 **Corrigido** - para correções de bugs
- 🔒 **Segurança** - para correções de vulnerabilidades
- 📚 **Documentação** - para atualizações de documentação
