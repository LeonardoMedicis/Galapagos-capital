#!/usr/bin/env python3
"""
🚀 Executar Dashboard Galapagos DTVM no VS Code

Este script executa o dashboard diretamente no VS Code com Jupyter ou Python.
Detecta automaticamente o ambiente e configura tudo necessário.

Uso:
    python executar_dashboard_adaptavel.py
    
    Ou no VS Code:
    - F5 (Run Python File)
    - Ctrl + F5 (Run Without Debugging)
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def verificar_dependencias():
    """Verifica e instala dependências automaticamente"""
    dependencias = ['flask', 'flask-cors']
    
    print("🔧 Verificando dependências...")
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep} já instalado")
        except ImportError:
            print(f"📦 Instalando {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado!")
    
    print("🎉 Todas as dependências prontas!\n")

def detectar_ambiente():
    """Detecta se está rodando no VS Code ou Jupyter"""
    # Verificar se está no VS Code
    if 'VSCODE_PID' in os.environ or 'TERM_PROGRAM' in os.environ:
        return 'vscode'
    
    # Verificar se está no Jupyter
    try:
        from IPython import get_ipython
        if get_ipython() is not None:
            return 'jupyter'
    except ImportError:
        pass
    
    # Padrão: terminal/script
    return 'terminal'

def executar_dashboard():
    """Executa o dashboard Flask"""
    # Importar após verificar dependências
    from flask import Flask, render_template, jsonify
    from flask_cors import CORS
    from datetime import datetime
    
    # Criar aplicação Flask
    app = Flask(__name__)
    CORS(app)
    
    # Configurar pasta de templates
    template_dir = Path(__file__).parent / 'dashboard-python' / 'templates'
    if template_dir.exists():
        app.template_folder = str(template_dir)
    
    @app.route('/')
    def dashboard():
        """Página principal do dashboard"""
        try:
            return render_template('dashboard_adaptavel.html')
        except Exception as e:
            # Fallback para HTML embutido se template não existir
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Dashboard Galapagos DTVM</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            </head>
            <body class="bg-primary">
                <div class="container mt-5">
                    <div class="row justify-content-center">
                        <div class="col-md-8">
                            <div class="card">
                                <div class="card-body text-center">
                                    <h1 class="card-title">
                                        <i class="fas fa-chart-line text-primary"></i>
                                        Galapagos DTVM
                                    </h1>
                                    <p class="card-text">Dashboard de Conciliações</p>
                                    <div class="alert alert-success">
                                        <i class="fas fa-check-circle"></i>
                                        <strong>Sistema funcionando!</strong><br>
                                        Executando no VS Code + Python
                                    </div>
                                    <div class="row">
                                        <div class="col-md-3">
                                            <div class="bg-primary text-white p-3 rounded">
                                                <h3>9</h3>
                                                <small>Módulos</small>
                                            </div>
                                        </div>
                                        <div class="col-md-3">
                                            <div class="bg-success text-white p-3 rounded">
                                                <h3>95%</h3>
                                                <small>Sucesso</small>
                                            </div>
                                        </div>
                                        <div class="col-md-3">
                                            <div class="bg-info text-white p-3 rounded">
                                                <h3>1.8s</h3>
                                                <small>Tempo</small>
                                            </div>
                                        </div>
                                        <div class="col-md-3">
                                            <div class="bg-warning text-white p-3 rounded">
                                                <h3>3</h3>
                                                <small>Ativos</small>
                                            </div>
                                        </div>
                                    </div>
                                    <hr>
                                    <p class="text-muted">
                                        <i class="fas fa-code"></i> Executando no VS Code |
                                        <i class="fas fa-clock"></i> {datetime.now().strftime('%H:%M:%S')}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
    
    @app.route('/api/status')
    def api_status():
        """API com status do sistema"""
        return jsonify({
            'total_modulos': 9,
            'implementados': 3,
            'taxa_sucesso': 95,
            'tempo_medio': 1.8,
            'ambiente': 'VS Code + Python',
            'status': 'online',
            'ultima_atualizacao': datetime.now().isoformat()
        })
    
    return app

def abrir_navegador():
    """Abre o navegador automaticamente"""
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Dashboard aberto no navegador!")
    except Exception as e:
        print(f"⚠️ Não foi possível abrir automaticamente: {e}")
        print("📍 Acesse manualmente: http://localhost:5000")

def main():
    """Função principal"""
    print("🚀 Dashboard Galapagos DTVM - VS Code Edition")
    print("=" * 50)
    
    # Detectar ambiente
    ambiente = detectar_ambiente()
    print(f"🎯 Ambiente detectado: {ambiente.upper()}")
    
    # Verificar dependências
    verificar_dependencias()
    
    # Executar dashboard
    print("🚀 Iniciando dashboard...")
    print("📍 URL: http://localhost:5000")
    print("⏹️ Para parar: Ctrl + C")
    print("=" * 50)
    
    # Abrir navegador em thread separada
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    # Executar Flask
    try:
        app = executar_dashboard()
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro ao executar dashboard: {e}")
        print("💡 Verifique se a porta 5000 está livre")
        print("💡 Tente executar novamente")

if __name__ == "__main__":
    main()

