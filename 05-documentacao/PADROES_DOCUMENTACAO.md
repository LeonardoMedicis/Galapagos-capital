# Padrões de Documentação - Galapagos DTVM

<div align="center">

![Documentation](https://img.shields.io/badge/Documentation-Standard-blue?style=for-the-badge)
![Quality](https://img.shields.io/badge/Quality-Professional-green?style=for-the-badge)
![Maintenance](https://img.shields.io/badge/Maintenance-Easy-orange?style=for-the-badge)

**Padrões obrigatórios para documentação de código no repositório Galapagos**

</div>

---

## 🎯 Objetivo

Estabelecer padrões consistentes e profissionais para documentação de todos os códigos e projetos no repositório da Galapagos DTVM, garantindo:

- 📖 **Clareza** - Qualquer pessoa da equipe entende o código
- 🔄 **Manutenibilidade** - Facilita atualizações e correções
- 🚀 **Produtividade** - Reduz tempo de onboarding e debugging
- 🏆 **Profissionalismo** - Demonstra qualidade técnica da equipe

---

## 📋 Estrutura Obrigatória do README

Todo código/projeto DEVE ter um README.md seguindo esta estrutura:

### 1. **Cabeçalho com Badges**
```markdown
# Nome do Projeto

<div align="center">

![Tecnologia](https://img.shields.io/badge/Tecnologia-Versão-cor?style=for-the-badge&logo=logo)
![Status](https://img.shields.io/badge/Status-Ativo-success?style=for-the-badge)

**Descrição breve e clara do que o projeto faz**

[🚀 Demo](#demo) • [📖 Docs](#documentação) • [⚙️ Setup](#instalação)

</div>
```

### 2. **Por que este código existe?**
```markdown
## 🎯 Por que este código existe?

### Problema Resolvido
- Descrever o problema específico que o código resolve
- Contexto do negócio
- Dor/ineficiência anterior

### Solução Implementada
- Como o código resolve o problema
- Benefícios quantificáveis
- Impacto no negócio
```

### 3. **O que este código faz?**
```markdown
## 🔍 O que este código faz?

### Funcionalidades Principais
- Lista clara das funcionalidades
- Casos de uso específicos
- Exemplos práticos

### Dados/Processos Envolvidos
- Que dados processa
- Que sistemas integra
- Que outputs gera
```

### 4. **Como funciona?**
```markdown
## ⚙️ Como funciona?

### Arquitetura/Fluxo
- Diagrama ou descrição do fluxo
- Componentes principais
- Dependências

### Lógica de Negócio
- Regras implementadas
- Algoritmos utilizados
- Decisões técnicas importantes
```

### 5. **Como utilizar?**
```markdown
## 🚀 Como utilizar?

### Opção 1: GitHub (Recomendado)
- Link direto para execução
- Interface web se houver
- Resultados automáticos

### Opção 2: Python/Notebook Local
```python
# Código de exemplo completo
# Passo a passo para executar
```

### Opção 3: Linha de Comando
```bash
# Comandos específicos
# Parâmetros disponíveis
```
```

### 6. **Instalação e Configuração**
```markdown
## 🔧 Instalação

### Pré-requisitos
- Lista de dependências
- Versões específicas
- Acessos necessários

### Passo a Passo
1. Clone/download
2. Configuração
3. Execução
4. Verificação
```

---

## 🎨 Padrões de Formatação

### Emojis Obrigatórios
Use estes emojis para padronizar as seções:

| Seção | Emoji | Uso |
|-------|-------|-----|
| Objetivo/Por quê | 🎯 | Problema e solução |
| Funcionalidades | 🔍 | O que faz |
| Arquitetura | ⚙️ | Como funciona |
| Uso/Execução | 🚀 | Como usar |
| Instalação | 🔧 | Setup técnico |
| Dados/Análise | 📊 | Processamento de dados |
| Automação | 🤖 | Processos automáticos |
| Dashboard/UI | 📱 | Interfaces |
| Documentação | 📖 | Links e refs |
| Problemas | 🚨 | Troubleshooting |
| Sucesso/OK | ✅ | Status positivo |
| Alerta | ⚠️ | Atenção necessária |
| Crítico | 🔴 | Problema grave |

### Badges Obrigatórios
Todo README deve ter pelo menos:

```markdown
![Tecnologia Principal](https://img.shields.io/badge/Tech-Version-color?style=for-the-badge&logo=logo)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
```

Exemplos por tecnologia:
- **Python:** `![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)`
- **React:** `![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react)`
- **Jupyter:** `![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=for-the-badge&logo=jupyter)`

### Estrutura de Código
```markdown
# Sempre usar blocos de código com linguagem especificada
```python
# Código Python
import pandas as pd
```

```bash
# Comandos shell
pip install requirements.txt
```

```sql
-- Queries SQL
SELECT * FROM tabela;
```
```

---

## 📁 Organização de Arquivos

### Estrutura Padrão
```
projeto/
├── 📖 README.md              # Documentação principal (OBRIGATÓRIO)
├── 📋 requirements.txt       # Dependências Python
├── ⚙️ config.json           # Configurações (se aplicável)
├── 🐍 script_principal.py    # Código principal
├── 📊 dados/                 # Dados de entrada/saída
├── 📈 notebooks/             # Jupyter notebooks
├── 🧪 tests/                 # Testes automatizados
└── 📚 docs/                  # Documentação adicional
```

### Nomenclatura de Arquivos
- **Scripts:** `snake_case.py`
- **Notebooks:** `PascalCase_Descritivo.ipynb`
- **Dados:** `dados_YYYYMMDD.csv`
- **Configs:** `config_ambiente.json`

---

## 🐍 Padrões para Python

### Docstrings Obrigatórias
```python
def processar_conciliacoes(data_referencia: str) -> dict:
    """
    Processa conciliações contábeis para uma data específica.
    
    Args:
        data_referencia (str): Data no formato YYYY-MM-DD
        
    Returns:
        dict: Resultados da verificação com status e detalhes
        
    Raises:
        FileNotFoundError: Se arquivos de conciliação não existirem
        ValueError: Se data estiver em formato inválido
        
    Example:
        >>> resultados = processar_conciliacoes('2025-06-07')
        >>> print(resultados['total_arquivos'])
        9
    """
    pass
```

### Comentários Explicativos
```python
# ✅ BOM: Explica o PORQUÊ
# Usar timezone de Brasília para garantir execução no horário correto
timezone = pytz.timezone('America/Sao_Paulo')

# ❌ RUIM: Explica o QUE (óbvio)
# Definir timezone
timezone = pytz.timezone('America/Sao_Paulo')
```

### Type Hints Obrigatórios
```python
from typing import List, Dict, Optional
from datetime import datetime

def verificar_arquivos(
    caminhos: List[str], 
    data_ref: datetime,
    timeout: Optional[int] = 30
) -> Dict[str, bool]:
    """Verificação com type hints claros."""
    pass
```

---

## 📓 Padrões para Jupyter Notebooks

### Estrutura Obrigatória
```markdown
# 1. Título e Descrição
# Nome do Notebook - Objetivo Específico

## 📋 Resumo
- O que este notebook faz
- Dados utilizados  
- Resultados esperados

## 🎯 Objetivo de Negócio
- Problema específico sendo resolvido
- Stakeholders interessados
- Decisões que serão tomadas com base nos resultados
```

### Células Obrigatórias

#### 1. **Setup e Imports**
```python
# =============================================================================
# SETUP E CONFIGURAÇÃO
# =============================================================================

# Imports padrão
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Configurações
pd.set_option('display.max_columns', None)
plt.style.use('seaborn-v0_8')

# Configurações específicas do projeto
DATA_PATH = '../dados/'
OUTPUT_PATH = '../resultados/'
```

#### 2. **Carregamento de Dados**
```python
# =============================================================================
# CARREGAMENTO E VALIDAÇÃO DE DADOS
# =============================================================================

# Carregar dados principais
df_conciliacoes = pd.read_csv(f'{DATA_PATH}conciliacoes_2025.csv')

# Validações básicas
print(f"📊 Dados carregados: {df_conciliacoes.shape}")
print(f"📅 Período: {df_conciliacoes['data'].min()} a {df_conciliacoes['data'].max()}")
print(f"🔍 Colunas: {list(df_conciliacoes.columns)}")

# Verificar qualidade dos dados
assert not df_conciliacoes.empty, "❌ Dados vazios!"
assert 'data' in df_conciliacoes.columns, "❌ Coluna 'data' não encontrada!"
```

#### 3. **Análise com Markdown Explicativo**
```markdown
## 📈 Análise de Tendências

### Contexto
Analisando a evolução das conciliações nos últimos 30 dias para identificar:
- Padrões de falhas
- Dias problemáticos
- Categorias mais críticas

### Metodologia
1. Agrupar por data e categoria
2. Calcular taxa de sucesso diária
3. Identificar outliers e tendências
```

#### 4. **Conclusões e Próximos Passos**
```markdown
## 🎯 Conclusões

### Principais Achados
1. **Taxa de sucesso geral:** 94.2% (meta: 95%)
2. **Categoria mais problemática:** Impostos (87% de sucesso)
3. **Dia mais crítico:** Segundas-feiras (91% de sucesso)

### Recomendações
1. **Imediata:** Investigar processo de geração de arquivos de impostos
2. **Curto prazo:** Implementar verificação adicional nas segundas
3. **Médio prazo:** Automatizar correção de problemas recorrentes

### Próximos Passos
- [ ] Apresentar resultados para equipe de Riscos
- [ ] Implementar alertas automáticos para taxa < 90%
- [ ] Agendar revisão mensal deste notebook
```

---

## 🔗 Padrões para Links e Referências

### Links Internos
```markdown
# Sempre usar links relativos
[Configuração](./config.json)
[Dados de Entrada](../dados/README.md)
[Notebook de Análise](./notebooks/Analise_Conciliacoes.ipynb)
```

### Links Externos
```markdown
# Sempre com contexto claro
[Dashboard de Produção](https://leonardomedicis.github.io/Galapagos-capital/)
[Documentação da API](https://api.galapagos.com.br/docs)
[Repositório Principal](https://github.com/LeonardoMedicis/Galapagos-capital)
```

### Referências Técnicas
```markdown
## 📚 Referências

### Documentação Oficial
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [React Documentation](https://react.dev/)

### Padrões Internos
- [Guia de Estilo Python - Galapagos](./docs/python-style-guide.md)
- [Convenções de Nomenclatura](./docs/naming-conventions.md)

### Contexto de Negócio
- [Processo de Conciliações - Wiki Interna](link-interno)
- [Regulamentação CVM](link-regulamentacao)
```

---

## ✅ Checklist de Qualidade

Antes de fazer commit, verificar:

### README.md
- [ ] Título claro e descritivo
- [ ] Badges apropriados
- [ ] Seção "Por que existe?" completa
- [ ] Seção "O que faz?" detalhada
- [ ] Seção "Como funciona?" clara
- [ ] Seção "Como usar?" com exemplos
- [ ] Instruções de instalação testadas
- [ ] Links funcionando
- [ ] Emojis padronizados
- [ ] Português correto (sem erros)

### Código Python
- [ ] Docstrings em todas as funções
- [ ] Type hints obrigatórios
- [ ] Comentários explicativos (porquê, não o quê)
- [ ] Nomes de variáveis descritivos
- [ ] Tratamento de erros adequado
- [ ] Logs informativos

### Jupyter Notebooks
- [ ] Título e objetivo claros
- [ ] Células organizadas logicamente
- [ ] Markdown explicativo entre análises
- [ ] Conclusões e próximos passos
- [ ] Outputs limpos (sem warnings desnecessários)
- [ ] Dados sensíveis removidos

---

## 🚨 Exemplos de Problemas Comuns

### ❌ README Ruim
```markdown
# Script

Este script faz coisas.

## Como usar
python script.py
```

### ✅ README Bom
```markdown
# Sistema de Validação de Carteiras

## 🎯 Por que este código existe?

### Problema Resolvido
A validação manual de carteiras levava 2h diárias e estava sujeita a erros...

### Solução Implementada
Sistema automatizado que reduz o tempo para 5 minutos e elimina erros...

## 🔍 O que este código faz?
- Valida 15 tipos diferentes de ativos
- Gera relatório de conformidade
- Envia alertas para discrepâncias > R$ 10.000

## 🚀 Como utilizar?
```python
from validador_carteiras import ValidadorCarteiras

validador = ValidadorCarteiras()
resultado = validador.validar_carteira('CARTEIRA_A')
print(f"Status: {resultado.status}")
```
```

---

## 🎓 Treinamento da Equipe

### Responsabilidades

#### Desenvolvedor
- Seguir todos os padrões ao criar código
- Revisar documentação antes do commit
- Atualizar README quando funcionalidades mudarem

#### Revisor (Code Review)
- Verificar se padrões foram seguidos
- Testar instruções de instalação/uso
- Validar clareza da documentação

#### Tech Lead
- Garantir consistência entre projetos
- Atualizar padrões conforme necessário
- Treinar novos membros da equipe

### Processo de Aprovação
1. **Desenvolvimento** - Seguir padrões
2. **Auto-revisão** - Checklist de qualidade
3. **Code Review** - Validação por par
4. **Aprovação** - Merge apenas se documentação OK

---

## 🔄 Evolução dos Padrões

### Versionamento
- **v1.0** - Padrões iniciais (Junho 2025)
- **v1.1** - Melhorias baseadas em feedback
- **v2.0** - Expansão para outras tecnologias

### Feedback e Melhorias
- Issues no GitHub para sugestões
- Revisão trimestral dos padrões
- Incorporação de melhores práticas da indústria

---

<div align="center">

**Padrões de Documentação - Galapagos DTVM**

*Código bem documentado é código que gera valor*

**Versão 1.0 - Junho 2025**

</div>

