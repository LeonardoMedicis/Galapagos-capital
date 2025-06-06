# Galapagos Capital - DTVM

<div align="center">

![Galapagos](https://img.shields.io/badge/Galapagos-DTVM-blue?style=for-the-badge)
![Automação](https://img.shields.io/badge/Automação-Conciliações-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Ativo-success?style=for-the-badge)

**Repositório oficial da Galapagos DTVM para automações e ferramentas**

[🚀 Dashboard](#dashboard) • [📊 Automações](#automações) • [📖 Documentação](#documentação)

</div>

---

## 🎯 Sobre a Galapagos DTVM

A Galapagos é uma distribuidora de títulos e valores mobiliários focada em inovação e excelência operacional. Este repositório centraliza nossas automações e ferramentas internas.

## 🤖 Automações Disponíveis

### 📊 Sistema de Conciliações Automatizado
**Localização:** `/automacao-conciliacoes/`

Sistema moderno que substitui processos manuais de verificação de conciliações contábeis:

- ⚡ **Execução automática diária** às 08:00 BRT
- 📊 **Dashboard web responsivo** com métricas em tempo real  
- 🔔 **Alertas inteligentes** para problemas críticos
- 📈 **Histórico completo** de verificações
- 🛠️ **Manutenção simplificada** via GitHub

**Tipos de Conciliação Monitorados:**
- 📈 **Rentabilidade** - Carteiras A, B e Consolidada
- 💰 **Impostos** - IR, IOF, PIS/COFINS  
- 🔧 **Operacionais** - Custódia, Liquidação D+0, Fechamento

**Acesso ao Dashboard:** [https://leonardomedicis.github.io/Galapagos-capital/](https://leonardomedicis.github.io/Galapagos-capital/)

## 📊 Dashboard

O dashboard principal oferece:

- 📊 **Métricas em tempo real** de todas as conciliações
- 🚨 **Alertas visuais** para problemas críticos
- 📱 **Interface responsiva** para acesso mobile
- 📈 **Gráficos de tendência** e histórico
- 🔍 **Filtros** por categoria e criticidade

## 🚀 Como Usar

### Acesso Rápido
1. **Dashboard Web:** [Clique aqui](https://leonardomedicis.github.io/Galapagos-capital/)
2. **Relatórios:** Gerados automaticamente diariamente
3. **Logs:** Disponíveis na seção Actions do GitHub

### Para Desenvolvedores
```bash
# Clonar repositório
git clone https://github.com/LeonardoMedicis/Galapagos-capital.git

# Navegar para automação de conciliações
cd Galapagos-capital/automacao-conciliacoes

# Instalar dependências
pip install -r requirements.txt

# Executar localmente
python conciliacao_checker.py
```

## 📁 Estrutura do Repositório

```
Galapagos-capital/
├── 📊 automacao-conciliacoes/           # Sistema de conciliações
│   ├── 🐍 conciliacao_checker.py       # Script principal
│   ├── ⚙️ config.json                  # Configurações
│   ├── 📋 requirements.txt             # Dependências Python
│   ├── 📚 GUIA_IMPLEMENTACAO.md        # Documentação técnica
│   └── 🌐 mapa-conciliacao-dashboard/  # Dashboard React
├── 🔧 .github/workflows/               # Automação GitHub Actions
│   └── verificacao-diaria.yml
├── 📄 docs/                            # GitHub Pages (gerado automaticamente)
└── 📖 README.md                        # Este arquivo
```

## 🔧 Configuração

### GitHub Actions
- ✅ Execução automática configurada
- ✅ Notificações em caso de problemas
- ✅ Deploy automático do dashboard
- ✅ Backup de relatórios

### GitHub Pages
- ✅ Dashboard público disponível
- ✅ Atualização automática
- ✅ Interface responsiva
- ✅ Métricas em tempo real

## 📈 Métricas e Monitoramento

### Estatísticas Atuais
- 📊 **9 tipos** de conciliação monitorados
- ⚡ **<30s** tempo médio de execução
- 🔄 **365 execuções** automáticas por ano
- 📱 **100%** compatibilidade mobile

### Alertas Configurados
- 🚨 **Crítico** - Arquivos de fechamento e consolidação
- ⚠️ **Alto** - Rentabilidade e IR
- 📝 **Médio** - Demais conciliações

## 🛠️ Manutenção

### Atualizações
- **Configurações:** Editar `automacao-conciliacoes/config.json`
- **Horários:** Modificar `.github/workflows/verificacao-diaria.yml`
- **Dashboard:** Personalizar `mapa-conciliacao-dashboard/`

### Suporte
- 📧 **Email:** [contato@galapagos.com.br]
- 💬 **Teams:** Canal da equipe
- 🐛 **Issues:** [GitHub Issues](../../issues)

## 📊 Roadmap

### 🎯 Próximas Funcionalidades
- [ ] Integração com ERP
- [ ] Notificações Teams/Slack
- [ ] API REST para integrações
- [ ] Machine Learning para predições
- [ ] Mobile app nativo

### 🚀 Melhorias Contínuas
- [ ] Performance e otimização
- [ ] Novas métricas e dashboards
- [ ] Integração com outros sistemas
- [ ] Automação de mais processos

## 🤝 Contribuição

### Como Contribuir
1. **Fork** o repositório
2. **Crie** uma branch para sua feature
3. **Commit** suas mudanças
4. **Abra** um Pull Request

### Padrões
- **Python:** PEP 8
- **JavaScript:** ESLint + Prettier
- **Commits:** Conventional Commits
- **Documentação:** Markdown

## 📄 Licença

Este projeto é propriedade da Galapagos DTVM. Uso interno apenas.

## 🏆 Equipe

Desenvolvido pela equipe de tecnologia da Galapagos DTVM com foco em:
- 🎯 **Eliminação de tarefas repetitivas**
- 📈 **Aumento de produtividade**
- 🔍 **Transparência operacional**
- 🚀 **Inovação contínua**

---

<div align="center">

**Galapagos DTVM - Inovação em Gestão de Ativos**

*Última atualização: Junho 2025*

</div>

