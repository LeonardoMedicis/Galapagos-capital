# 📊 Dashboard Principal - Galapagos DTVM

## 📋 **O que é este módulo?**

Este é o **coração do sistema** - um dashboard web moderno que mostra todas as conciliações em tempo real!

## 🎯 **Para que serve?**

- ✅ **Visualizar status** de todas as conciliações
- ✅ **Executar conciliações** com um clique
- ✅ **Monitorar progresso** em tempo real
- ✅ **Ver histórico** de execuções
- ✅ **Controlar sistema** via interface web
- ✅ **Acessar de qualquer dispositivo** (PC, tablet, celular)

## 🚀 **Como usar?**

### **Opção 1: Executar diretamente**
```bash
python executar_dashboard_adaptavel.py
```

### **Opção 2: Usar o Notebook Jupyter**
1. Abra o arquivo `Dashboard_Principal.ipynb`
2. Execute todas as células
3. Dashboard abre automaticamente no navegador!

### **Opção 3: Execução rápida**
```bash
python app_adaptavel.py
```

## 🌐 **Como acessar?**

Depois de executar, acesse no navegador:
- **URL:** http://localhost:5000
- **Alternativa:** http://127.0.0.1:5000

## 🎨 **Interface do Dashboard:**

### **🏠 Página Principal:**
- **📊 Estatísticas gerais** - Total de módulos, taxa de sucesso
- **🎮 Controles rápidos** - Executar todos, por categoria
- **📈 Módulos por categoria** - Rentabilidade, Impostos, Outras
- **📋 Histórico** - Últimas execuções

### **🔧 Funcionalidades:**
- **▶️ Botões de execução** - Para cada conciliação
- **📊 Gráficos interativos** - Status e performance
- **🔄 Atualização automática** - A cada 30 segundos
- **📱 Design responsivo** - Funciona em celular
- **🎨 Cores por ambiente** - Azul (dev) / Verde (prod)

## 📁 **Arquivos nesta pasta:**

- `app_adaptavel.py` - Aplicação Flask principal
- `executar_dashboard_adaptavel.py` - Script de execução
- `Dashboard_Principal.ipynb` - Notebook para Jupyter
- `templates/` - Templates HTML
- `static/` - CSS, JS, imagens
- `README.md` - Esta documentação

## 🔧 **Configurações automáticas:**

### **🔧 Desenvolvimento:**
- **Porta:** 5000
- **Debug:** Habilitado
- **Dados:** Simulados
- **Cor:** Azul
- **Banco:** Local

### **🏭 Produção:**
- **Porta:** 5000
- **Debug:** Desabilitado
- **Dados:** Reais
- **Cor:** Verde
- **Banco:** Compartilhado

## 🎯 **Principais recursos:**

### **📊 Monitoramento:**
- Status de cada conciliação
- Tempo de execução
- Taxa de sucesso
- Últimas execuções
- Usuário que executou

### **🎮 Controles:**
- Executar conciliação individual
- Executar todas de uma categoria
- Executar todas as conciliações
- Atualizar dados manualmente
- Ver logs detalhados

### **📈 Relatórios:**
- Gráficos de performance
- Histórico de execuções
- Estatísticas consolidadas
- Alertas automáticos

## 🆘 **Problemas comuns:**

### **Erro: "Porta 5000 já está em uso"**
- **Solução:** Feche outros programas ou use porta diferente

### **Erro: "Não consegue conectar"**
- **Solução:** Verifique se o script está rodando

### **Dashboard não carrega**
- **Solução:** Aguarde alguns segundos e recarregue a página

### **Botões não funcionam**
- **Solução:** Verifique se JavaScript está habilitado

## 💡 **Dicas:**

- ✅ **Execute sempre** após configurar ambiente
- ✅ **Deixe rodando** para monitoramento contínuo
- ✅ **Acesse de qualquer dispositivo** na rede
- ✅ **Use atalhos** Ctrl+R para atualizar

## 🔗 **Integração com outros módulos:**

- **Configuração:** Usa configuração da pasta 01
- **Módulos:** Executa conciliações da pasta 03
- **Utilitários:** Integra com ferramentas da pasta 04
- **Logs:** Salva em pasta configurada

## 🎯 **Próximos passos:**

Depois de usar o dashboard, você pode:
1. **Explorar módulos** específicos (pasta 03)
2. **Usar utilitários** avançados (pasta 04)
3. **Consultar documentação** (pasta 05)

---
*💡 Este é o módulo mais importante - sua central de comando!*

