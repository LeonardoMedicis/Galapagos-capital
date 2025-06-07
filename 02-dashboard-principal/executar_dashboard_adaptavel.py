#!/usr/bin/env python3
"""
Executar Dashboard Adaptável - Galapagos DTVM
Script único que detecta ambiente e executa dashboard apropriado
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Executa dashboard com detecção automática de ambiente."""
    
    print("🚀 Iniciando Dashboard Galapagos DTVM...")
    print("🔍 Detectando ambiente...")
    
    # Verificar se configurar_ambiente.py existe
    config_script = Path("configurar_ambiente.py")
    if not config_script.exists():
        print("❌ Arquivo configurar_ambiente.py não encontrado!")
        print("📁 Certifique-se de estar na pasta correta do projeto.")
        return 1
    
    try:
        # Executar configuração de ambiente
        print("⚙️ Configurando ambiente...")
        result = subprocess.run([sys.executable, "configurar_ambiente.py"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Erro ao configurar ambiente:")
            print(result.stderr)
            return 1
        
        # Verificar se app_adaptavel.py existe
        app_script = Path("dashboard-python/app_adaptavel.py")
        if not app_script.exists():
            print("❌ Arquivo app_adaptavel.py não encontrado!")
            print("📁 Estrutura do projeto pode estar incorreta.")
            return 1
        
        # Instalar dependências se necessário
        print("📦 Verificando dependências...")
        try:
            import flask
            import flask_cors
        except ImportError:
            print("📦 Instalando dependências...")
            subprocess.run([sys.executable, "-m", "pip", "install", "flask", "flask-cors"], 
                          check=True)
        
        # Executar dashboard
        print("🌐 Iniciando servidor dashboard...")
        os.chdir("dashboard-python")
        subprocess.run([sys.executable, "app_adaptavel.py"])
        
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado pelo usuário.")
        return 0
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

