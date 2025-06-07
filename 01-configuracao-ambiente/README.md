# 🔧 Configuração de Ambiente - Galapagos DTVM

## 📋 **O que é este módulo?**

Este módulo **detecta automaticamente** em que ambiente o sistema está rodando e configura tudo automaticamente:

- **🔧 Desenvolvimento:** Quando está no GitHub (seu computador)
- **🏭 Produção:** Quando está na pasta colaborativa da empresa

## 🎯 **Para que serve?**

- ✅ **Detecta automaticamente** se você está desenvolvendo ou usando em produção
- ✅ **Configura caminhos** corretos para cada ambiente
- ✅ **Cria estrutura** de pastas necessárias
- ✅ **Otimiza configurações** para cada uso
- ✅ **Zero configuração manual** - funciona sozinho!

## 🚀 **Como usar?**

### **Opção 1: Executar diretamente**
```bash
python configurar_ambiente.py
```

### **Opção 2: Usar o Notebook Jupyter**
1. Abra o arquivo `Configuracao_Ambiente.ipynb`
2. Execute todas as células
3. Veja o ambiente detectado e configurado!

## 📊 **O que acontece quando executa?**

1. **🔍 Detecta ambiente:**
   - Verifica se está em pasta de rede (produção)
   - Verifica se tem `.git` (desenvolvimento)
   - Escolhe configurações apropriadas

2. **📁 Cria estrutura:**
   - Pastas para dados
   - Pastas para resultados
   - Pastas para logs
   - Pasta para banco de dados

3. **⚙️ Configura sistema:**
   - Banco SQLite otimizado
   - Caminhos corretos
   - Logs apropriados
   - Permissões necessárias

4. **💾 Salva configuração:**
   - Arquivo `config_ambiente.json`
   - Marcador de ambiente
   - Logs de configuração

## 🎨 **Diferenças por ambiente:**

### **🔧 Desenvolvimento (GitHub):**
- **Dados:** Simulados para testes
- **Banco:** Local (só você vê)
- **Execução:** Rápida e simulada
- **Debug:** Habilitado
- **Cor:** Azul

### **🏭 Produção (Pasta Colaborativa):**
- **Dados:** Reais da empresa
- **Banco:** Compartilhado (equipe toda vê)
- **Execução:** Real com dados verdadeiros
- **Auditoria:** Completa
- **Cor:** Verde

## 📁 **Arquivos nesta pasta:**

- `configurar_ambiente.py` - Script principal
- `Configuracao_Ambiente.ipynb` - Notebook para Jupyter
- `README.md` - Esta documentação

## 🆘 **Problemas comuns:**

### **Erro: "Não conseguiu detectar ambiente"**
- **Solução:** Execute na pasta correta do projeto

### **Erro: "Permissão negada"**
- **Solução:** Execute como administrador ou verifique permissões da pasta

### **Erro: "Pasta não encontrada"**
- **Solução:** Verifique se está na pasta correta do projeto

## 💡 **Dicas:**

- ✅ **Execute sempre** antes de usar outros módulos
- ✅ **Não precisa configurar** nada manualmente
- ✅ **Funciona em Windows, Mac e Linux**
- ✅ **Detecta automaticamente** o ambiente correto

## 🔗 **Próximos passos:**

Depois de configurar o ambiente, você pode:
1. **Executar o Dashboard Principal** (pasta 02)
2. **Usar módulos de conciliação** (pasta 03)
3. **Explorar utilitários** (pasta 04)

---
*💡 Este módulo é a base de todo o sistema - sempre execute primeiro!*

