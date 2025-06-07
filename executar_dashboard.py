#!/usr/bin/env python3
"""
Executar Dashboard Python - Galapagos DTVM

Script simples para executar o dashboard Python sem complicações.
"""

import os
import sys
import subprocess
from pathlib import Path

def verificar_python():
    """Verifica se Python está disponível."""
    try:
        import sys
        version = sys.version_info
        if version.major >= 3 and version.minor >= 6:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} encontrado")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor} muito antigo. Necessário Python 3.6+")
            return False
    except:
        print("❌ Python não encontrado")
        return False

def instalar_dependencias():
    """Instala dependências necessárias."""
    print("📦 Instalando dependências...")
    
    dependencias = [
        'flask==2.3.3',
        'flask-cors==4.0.0', 
        'plotly==5.17.0',
        'requests==2.31.0',
        'python-dateutil==2.8.2'
    ]
    
    for dep in dependencias:
        try:
            print(f"   Instalando {dep}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ Erro ao instalar {dep}: {e}")
            print("   💡 Tentando continuar...")

def main():
    """Função principal."""
    print("🐍 Dashboard Python - Galapagos DTVM")
    print("=" * 50)
    
    # Verificar Python
    if not verificar_python():
        print("💡 Instale Python 3.6+ em: https://python.org")
        input("Pressione Enter para sair...")
        return
    
    # Verificar diretório
    if not Path("dashboard-python/app.py").exists():
        print("❌ Arquivo app.py não encontrado!")
        print("💡 Certifique-se de estar na pasta raiz do repositório")
        input("Pressione Enter para sair...")
        return
    
    # Instalar dependências
    instalar_dependencias()
    
    # Executar aplicação
    print("\n🚀 Iniciando dashboard...")
    print("🌐 Abrirá automaticamente em: http://localhost:5000")
    print("💡 Para parar: Pressione Ctrl+C")
    print("=" * 50)
    
    try:
        os.chdir("dashboard-python")
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n⏹️ Dashboard parado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao executar dashboard: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()

