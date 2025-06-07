# 🐍 Dashboard Python - Galapagos DTVM

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-239120?style=for-the-badge&logo=plotly&logoColor=white)

**Sistema 100% Python para monitoramento de conciliações**

[🚀 Execução Rápida](#execução-rápida) • [🎯 Funcionalidades](#funcionalidades) • [📊 Screenshots](#screenshots) • [🔧 API](#api-rest)

</div>

---

## 🎯 Por Que Python?

### **✅ Vantagens para a Galapagos:**
- **🐍 Uma linguagem só** - Toda equipe foca em Python
- **🔧 Manutenção unificada** - Dashboard + conciliações + dados
- **📈 Integração nativa** - Conecta direto com sistemas existentes
- **🚀 Deploy simples** - Um requirements.txt resolve tudo
- **💰 Custo zero** - Sem licenças ou dependências pagas
- **🎓 Curva de aprendizado** - Equipe já conhece Python

### **✅ Tecnologias Utilizadas:**
- **Flask** - Framework web leve e poderoso
- **SQLite** - Banco de dados integrado
- **Plotly** - Gráficos interativos profissionais
- **Bootstrap** - Interface moderna e responsiva
- **Jinja2** - Templates dinâmicos
- **Threading** - Execução assíncrona

---

## 🚀 Execução Rápida

### **Opção 1: Script Automático (Recomendado)**
```bash
# 1. Baixar repositório
git clone https://github.com/LeonardoMedicis/Galapagos-capital.git

# 2. Entrar na pasta
cd Galapagos-capital

# 3. Executar script automático
python executar_dashboard.py

# 4. Pronto! Abre em http://localhost:5000
```

### **Opção 2: Execução Manual**
```bash
# 1. Baixar repositório
git clone https://github.com/LeonardoMedicis/Galapagos-capital.git

# 2. Entrar na pasta
cd Galapagos-capital/dashboard-python

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
python app.py

# 5. Acessar: http://localhost:5000
```

### **Opção 3: Ambiente Virtual (Produção)**
```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 3. Instalar dependências
pip install -r dashboard-python/requirements.txt

# 4. Executar
cd dashboard-python && python app.py
```

---

## 🎯 Funcionalidades

### **📊 Dashboard Completo**
- **Métricas em tempo real** - Status de todos os módulos
- **Gráficos interativos** - Performance e estatísticas
- **Interface responsiva** - Funciona em desktop e mobile
- **Auto-refresh** - Atualização automática a cada 30s
- **Alertas visuais** - Notificações de sucesso/erro

### **🗄️ Banco de Dados Integrado**
- **SQLite nativo** - Sem configuração externa
- **Histórico completo** - Todas as execuções registradas
- **Métricas avançadas** - Performance por categoria
- **Backup automático** - Dados sempre seguros

### **🔄 Execução de Conciliações**
- **Via interface web** - Botões para executar
- **Por categoria** - Rentabilidade, impostos, operacionais
- **Execução assíncrona** - Não trava a interface
- **Monitoramento real** - Status em tempo real

### **📈 Gráficos e Relatórios**
- **Plotly integrado** - Gráficos profissionais
- **Performance por categoria** - Tempo médio de execução
- **Execuções diárias** - Histórico de atividade
- **Taxa de sucesso** - Métricas de qualidade

### **🔌 API REST Completa**
- **Endpoints documentados** - Integração fácil
- **Dados JSON** - Formato padrão
- **CORS habilitado** - Acesso de qualquer origem
- **Autenticação** - Pronto para produção

---

## 📊 Screenshots

### **Dashboard Principal**
```
🗺️ Mapa de Conciliações - Galapagos DTVM
├── 📊 Estatísticas Gerais
│   ├── Total: 9 módulos
│   ├── Desenvolvimento: 9
│   ├── Implementados: 0
│   └── Taxa Sucesso: 0%
├── 📈 Gráficos Interativos
│   ├── Status por Categoria (Pizza)
│   └── Execuções Diárias (Linha)
├── 📁 Módulos por Categoria
│   ├── 📈 Rentabilidade (3)
│   ├── 💰 Impostos (3)
│   └── 🔧 Operacionais (3)
└── 🎮 Controles de Execução
    ├── 🚀 Executar Todos
    ├── 📈 Executar Rentabilidade
    ├── 💰 Executar Impostos
    ├── 🔧 Executar Operacionais
    ├── 📄 Gerar Relatório
    └── 🔗 Abrir GitHub
```

### **Interface Moderna**
- **Design Bootstrap 5** - Visual profissional
- **Cores da Galapagos** - Identidade visual
- **Ícones Font Awesome** - Interface intuitiva
- **Animações CSS** - Experiência fluida
- **Mobile-first** - Responsivo por padrão

---

## 🔌 API REST

### **Endpoints Disponíveis:**

#### **📊 Status Geral**
```http
GET /api/status
```
```json
{
  "timestamp": "2025-06-07T10:30:00",
  "total_modulos": 9,
  "modulos_implementados": 0,
  "modulos_desenvolvimento": 9,
  "execucoes_sucesso": 0,
  "taxa_sucesso": 0.0,
  "categorias": [...],
  "ultimas_execucoes": [...]
}
```

#### **📁 Listar Módulos**
```http
GET /api/modulos
GET /api/modulos/rentabilidade
GET /api/modulos/impostos
GET /api/modulos/outras
```

#### **🚀 Executar Conciliações**
```http
POST /api/executar/todos
POST /api/executar/categoria/rentabilidade
POST /api/executar/Rentabilidade_Carteira_A
```

#### **📈 Dados para Gráficos**
```http
GET /api/graficos/performance
```

---

## 🏗️ Arquitetura

### **Estrutura do Projeto:**
```
dashboard-python/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── templates/            # Templates HTML
│   ├── dashboard.html    # Dashboard principal
│   ├── relatorio.html    # Página de relatórios
│   └── configuracoes.html # Configurações
├── static/               # Arquivos estáticos
│   ├── css/             # Estilos customizados
│   ├── js/              # JavaScript customizado
│   └── img/             # Imagens e ícones
├── database/            # Banco SQLite
│   └── conciliacoes.db  # Dados das conciliações
└── api/                 # Módulos da API
    └── endpoints.py     # Endpoints REST
```

### **Classes Principais:**
- **DatabaseManager** - Gerencia SQLite e operações
- **ConciliacaoManager** - Executa e monitora conciliações
- **Flask App** - Servidor web e rotas
- **API REST** - Endpoints para integração

---

## 🔧 Configuração Avançada

### **Variáveis de Ambiente:**
```bash
# Porta do servidor (padrão: 5000)
export PORT=8080

# Modo debug (padrão: True)
export FLASK_DEBUG=False

# Caminho do banco (padrão: database/conciliacoes.db)
export DATABASE_PATH=/path/to/database.db
```

### **Configuração de Produção:**
```python
# app.py - Configurações de produção
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
```

### **Deploy em Servidor:**
```bash
# Usando Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Usando uWSGI
pip install uwsgi
uwsgi --http :5000 --wsgi-file app.py --callable app
```

---

## 🔍 Monitoramento e Logs

### **Logs Estruturados:**
```python
# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard.log'),
        logging.StreamHandler()
    ]
)
```

### **Métricas Disponíveis:**
- **Tempo de execução** por módulo
- **Taxa de sucesso** por categoria
- **Histórico de execuções** (30 dias)
- **Performance** do sistema
- **Erros e exceções** detalhados

---

## 🚀 Próximos Passos

### **Fase 1: Implementação Básica (Atual)**
- ✅ Dashboard funcional
- ✅ API REST completa
- ✅ Banco SQLite integrado
- ✅ Interface responsiva
- ✅ Execução simulada

### **Fase 2: Integração Real (Próxima)**
- 🔄 Conectar com módulos reais
- 🔄 Implementar lógica de conciliação
- 🔄 Integração com sistemas fonte
- 🔄 Notificações por email/Teams
- 🔄 Autenticação e autorização

### **Fase 3: Produção (Futuro)**
- 🚀 Deploy em servidor dedicado
- 🚀 Backup automático
- 🚀 Monitoramento avançado
- 🚀 Escalabilidade horizontal
- 🚀 Integração com ERP

---

## 💡 Vantagens vs React

### **Python (Atual)**
- ✅ **Manutenção unificada** - Uma linguagem só
- ✅ **Integração nativa** - Conecta direto com dados
- ✅ **Deploy simples** - Sem build process
- ✅ **Debugging fácil** - Tudo na mesma stack
- ✅ **Custo zero** - Sem dependências pagas
- ❌ **Interface menos moderna** que React
- ❌ **Performance frontend** um pouco menor

### **React (Anterior)**
- ✅ **Interface moderna** - Componentes reutilizáveis
- ✅ **Performance frontend** - Renderização otimizada
- ❌ **Duas linguagens** - JavaScript + Python
- ❌ **Build process** - npm, webpack, etc.
- ❌ **Deploy complexo** - Múltiplos ambientes
- ❌ **Manutenção dupla** - Frontend + backend

### **Recomendação Final:**
**Para a Galapagos, Python é a escolha certa!** A simplicidade e manutenibilidade superam a interface mais moderna do React.

---

<div align="center">

**Dashboard Python - Galapagos DTVM**

*Sistema 100% Python para máxima simplicidade e manutenibilidade*

**Uma linguagem | Uma stack | Uma solução**

</div>

