# 🎯 Dashboard no VS Code - Guia Completo

## 📋 **Pré-requisitos**

### 1. **VS Code Instalado**
- Download: https://code.visualstudio.com/

### 2. **Python Instalado**
- Python 3.7+ (verificar: `python --version`)

### 3. **Extensão Jupyter no VS Code**
- Abrir VS Code
- Ir em **Extensions** (Ctrl + Shift + X)
- Buscar: **"Jupyter"**
- Instalar: **"Jupyter" da Microsoft**

## 🚀 **Como Executar o Dashboard**

### **Passo 1: Baixar o Repositório**
```bash
# Opção A: Git
git clone https://github.com/LeonardoMedicis/Galapagos-capital.git

# Opção B: Download ZIP
# Baixar do GitHub e extrair
```

### **Passo 2: Abrir no VS Code**
```bash
# Abrir pasta no VS Code
code Galapagos-capital
```

### **Passo 3: Abrir o Notebook**
1. **Navegar** para: `02-dashboard-principal/Dashboard_Principal.ipynb`
2. **Clicar** no arquivo
3. **VS Code abre** automaticamente como notebook

### **Passo 4: Executar**
1. **Célula 1:** Shift + Enter (instala dependências)
2. **Célula 2:** Shift + Enter (executa dashboard)
3. **Dashboard abre** automaticamente no navegador!

## ✅ **Vantagens do VS Code + Jupyter**

### **🎨 Interface Integrada:**
- **Notebook dentro** do VS Code
- **Terminal integrado** para comandos
- **Explorer** para navegar arquivos
- **Git integrado** para commits

### **⚡ Funcionalidades:**
- **IntelliSense** - Autocomplete inteligente
- **Debug** - Debugging completo
- **Extensions** - Milhares de extensões
- **Themes** - Personalização visual

### **🔧 Controles:**
- **Shift + Enter** - Executar célula
- **Ctrl + Enter** - Executar sem avançar
- **A** - Adicionar célula acima
- **B** - Adicionar célula abaixo
- **DD** - Deletar célula

## 🎯 **Resultado Esperado**

### **Após Executar:**
1. **Terminal mostra:** "🚀 Iniciando Dashboard Galapagos DTVM..."
2. **Navegador abre:** http://localhost:5000
3. **Dashboard carrega** com interface completa
4. **Métricas visíveis:** 9 módulos, 95% sucesso, 1.8s

### **Interface do Dashboard:**
- ✅ **Header:** Galapagos DTVM
- ✅ **Métricas:** Cards com estatísticas
- ✅ **Controles:** Botões para executar
- ✅ **Módulos:** Status de cada conciliação
- ✅ **Animações:** Progresso em tempo real

## 🔧 **Troubleshooting**

### **Problema: Extensão Jupyter não aparece**
**Solução:**
1. Reinstalar extensão Jupyter
2. Reiniciar VS Code
3. Verificar se Python está no PATH

### **Problema: Kernel não conecta**
**Solução:**
1. Ctrl + Shift + P
2. "Python: Select Interpreter"
3. Escolher Python correto

### **Problema: Dashboard não abre**
**Solução:**
1. Verificar se porta 5000 está livre
2. Abrir manualmente: http://localhost:5000
3. Verificar logs no terminal

### **Problema: Dependências não instalam**
**Solução:**
```bash
# No terminal integrado:
pip install flask flask-cors
```

## 🎬 **Para Apresentação**

### **Roteiro no VS Code:**
1. **Abrir VS Code** com o projeto
2. **Mostrar estrutura** organizada
3. **Abrir notebook** Dashboard_Principal.ipynb
4. **Executar células** ao vivo
5. **Dashboard abre** automaticamente
6. **Demonstrar funcionalidades**

### **Pontos de Destaque:**
- **"Vejam como é profissional"** (VS Code)
- **"Execução com um clique"** (Shift + Enter)
- **"Dashboard abre sozinho"** (automação)
- **"Interface moderna"** (resultado)

## 💡 **Dicas Extras**

### **Atalhos Úteis:**
- **Ctrl + `** - Abrir/fechar terminal
- **Ctrl + Shift + E** - Explorer
- **Ctrl + Shift + G** - Git
- **F5** - Debug (se configurado)

### **Extensões Recomendadas:**
- **Python** - Suporte completo ao Python
- **GitLens** - Git avançado
- **Prettier** - Formatação de código
- **Material Icon Theme** - Ícones bonitos

**Agora você pode executar tudo direto no VS Code! 🚀**

