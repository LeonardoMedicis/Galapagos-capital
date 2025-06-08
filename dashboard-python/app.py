from flask import Flask, render_template_string, jsonify
from flask_cors import CORS
import threading
import webbrowser
import time
from datetime import datetime
import sys
import subprocess

def instalar_dependencias():
    """Instala dependências automaticamente"""
    dependencias = ['flask', 'flask-cors']
    
    for dep in dependencias:
        try:
            __import__(dep.replace('-', '_'))
            print(f"✅ {dep} já instalado")
        except ImportError:
            print(f"📦 Instalando {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado!")

# Instalar dependências automaticamente
print("🔧 Verificando dependências...")
instalar_dependencias()
print("🎉 Todas as dependências prontas!\n")

# Importar após instalação
from flask import Flask, render_template_string, jsonify
from flask_cors import CORS

# Criar aplicação Flask
app = Flask(__name__)
CORS(app)

# Template HTML completo embutido
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Galapagos DTVM</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            min-height: 100vh; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .dashboard-container { 
            background: white; 
            border-radius: 15px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        .metric-card { 
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
            color: white; 
            border-radius: 10px;
            transition: transform 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
        }
        .status-success { border-left: 5px solid #28a745; }
        .status-error { border-left: 5px solid #dc3545; }
        .status-running { border-left: 5px solid #ffc107; }
        .badge-dev { 
            position: fixed; 
            top: 20px; 
            right: 20px; 
            z-index: 1000;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .btn {
            transition: all 0.3s ease;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .card {
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: translateY(-3px);
        }
    </style>
</head>
<body>
    <div class="badge-dev">
        <span class="badge bg-primary fs-6">
            <i class="fas fa-code"></i> VS CODE + JUPYTER
        </span>
    </div>
    
    <div class="container-fluid py-4">
        <div class="dashboard-container p-4">
            <div class="row mb-4">
                <div class="col-12">
                    <h1 class="text-center mb-0">
                        <i class="fas fa-chart-line text-primary"></i> 
                        Galapagos DTVM
                    </h1>
                    <p class="text-center text-muted">Dashboard de Conciliações Automatizado</p>
                    <div class="text-center">
                        <span class="badge bg-success">
                            <i class="fas fa-rocket"></i> Sistema Funcionando
                        </span>
                    </div>
                </div>
            </div>
            
            <!-- Métricas -->
            <div class="row mb-4">
                <div class="col-md-3 mb-3">
                    <div class="metric-card p-3 text-center">
                        <i class="fas fa-cubes fa-2x mb-2"></i>
                        <h3 class="mb-0">9</h3>
                        <small>Total de Módulos</small>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="metric-card p-3 text-center">
                        <i class="fas fa-check-circle fa-2x mb-2"></i>
                        <h3 class="mb-0">3</h3>
                        <small>Implementados</small>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="metric-card p-3 text-center">
                        <i class="fas fa-percentage fa-2x mb-2"></i>
                        <h3 class="mb-0">95%</h3>
                        <small>Taxa de Sucesso</small>
                    </div>
                </div>
                <div class="col-md-3 mb-3">
                    <div class="metric-card p-3 text-center">
                        <i class="fas fa-clock fa-2x mb-2"></i>
                        <h3 class="mb-0">1.8s</h3>
                        <small>Tempo Médio</small>
                    </div>
                </div>
            </div>
            
            <!-- Controles -->
            <div class="row mb-4">
                <div class="col-12">
                    <h5><i class="fas fa-play-circle text-success"></i> Controles Rápidos</h5>
                    <div class="btn-group flex-wrap" role="group">
                        <button class="btn btn-success" onclick="executarTodos()">
                            <i class="fas fa-play"></i> Executar Todos
                        </button>
                        <button class="btn btn-primary" onclick="executarRentabilidade()">
                            <i class="fas fa-chart-line"></i> Só Rentabilidade
                        </button>
                        <button class="btn btn-warning" onclick="executarImpostos()">
                            <i class="fas fa-file-invoice-dollar"></i> Só Impostos
                        </button>
                        <button class="btn btn-info" onclick="atualizarDados()">
                            <i class="fas fa-sync"></i> Atualizar
                        </button>
                    </div>
                </div>
            </div>
            
            <!-- Módulos -->
            <div class="row">
                <div class="col-md-4 mb-3">
                    <div class="card status-success">
                        <div class="card-body">
                            <h6 class="card-title">
                                <i class="fas fa-chart-line text-success"></i>
                                Rentabilidade Carteira A
                            </h6>
                            <span class="badge bg-success">Sucesso</span>
                            <span class="badge bg-info">Implementado</span>
                            <p class="card-text mt-2">
                                <i class="fas fa-clock"></i> Última execução: {{ hora_atual }}
                            </p>
                            <button class="btn btn-primary btn-sm" onclick="executarModulo('carteira_a')">
                                <i class="fas fa-play"></i> Executar
                            </button>
                            <button class="btn btn-outline-secondary btn-sm" onclick="verLogs('carteira_a')">
                                <i class="fas fa-file-alt"></i> Logs
                            </button>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4 mb-3">
                    <div class="card status-error">
                        <div class="card-body">
                            <h6 class="card-title">
                                <i class="fas fa-file-invoice-dollar text-danger"></i>
                                IR Retido na Fonte
                            </h6>
                            <span class="badge bg-danger">Erro</span>
                            <span class="badge bg-warning">Estrutura</span>
                            <p class="card-text mt-2">
                                <i class="fas fa-exclamation-triangle"></i> Erro: Arquivo não encontrado
                            </p>
                            <button class="btn btn-primary btn-sm" onclick="executarModulo('ir_retido')">
                                <i class="fas fa-play"></i> Executar
                            </button>
                            <button class="btn btn-outline-danger btn-sm" onclick="verErro('ir_retido')">
                                <i class="fas fa-bug"></i> Ver Erro
                            </button>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4 mb-3">
                    <div class="card status-running">
                        <div class="card-body">
                            <h6 class="card-title">
                                <i class="fas fa-coins text-warning"></i>
                                Custódia de Títulos
                            </h6>
                            <span class="badge bg-warning">Executando</span>
                            <span class="badge bg-warning">Estrutura</span>
                            <p class="card-text mt-2">
                                <i class="fas fa-spinner fa-spin"></i> Em progresso... 
                                <span id="progress" class="fw-bold">45%</span>
                            </p>
                            <button class="btn btn-secondary btn-sm" disabled>
                                <i class="fas fa-spinner fa-spin"></i> Executando
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Estatísticas Adicionais -->
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">
                                <i class="fas fa-chart-bar text-primary"></i> 
                                Estatísticas do Dia
                            </h6>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-check text-success"></i> Execuções bem-sucedidas: <strong>12</strong></li>
                                <li><i class="fas fa-times text-danger"></i> Execuções com erro: <strong>1</strong></li>
                                <li><i class="fas fa-clock text-info"></i> Tempo total economizado: <strong>6h 30min</strong></li>
                                <li><i class="fas fa-percentage text-warning"></i> Eficiência: <strong>95%</strong></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h6 class="card-title">
                                <i class="fas fa-info-circle text-info"></i> 
                                Informações do Sistema
                            </h6>
                            <ul class="list-unstyled">
                                <li><i class="fas fa-server text-primary"></i> Ambiente: <strong>Desenvolvimento</strong></li>
                                <li><i class="fas fa-code text-success"></i> Plataforma: <strong>VS Code + Jupyter</strong></li>
                                <li><i class="fas fa-database text-info"></i> Banco: <strong>SQLite Local</strong></li>
                                <li><i class="fas fa-shield-alt text-warning"></i> Status: <strong>Online</strong></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Rodapé -->
            <div class="row mt-4">
                <div class="col-12 text-center">
                    <small class="text-muted">
                        <i class="fas fa-rocket text-primary"></i> Sistema desenvolvido para Galapagos DTVM | 
                        <i class="fas fa-clock text-info"></i> Última atualização: {{ hora_atual }} |
                        <i class="fas fa-code text-success"></i> Executando no VS Code
                    </small>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function executarTodos() {
            Swal.fire({
                title: '🚀 Executando Todas as Conciliações!',
                html: `
                    <div class="text-start">
                        <p><strong>Módulos que serão executados:</strong></p>
                        <ul>
                            <li>📈 Rentabilidade Carteira A</li>
                            <li>📈 Rentabilidade Carteira B</li>
                            <li>📈 Rentabilidade Consolidada</li>
                            <li>💰 IR Retido na Fonte</li>
                            <li>💰 IOF Operações</li>
                            <li>💰 PIS/COFINS</li>
                            <li>🔧 Custódia de Títulos</li>
                            <li>🔧 Liquidação D+0</li>
                            <li>🔧 Fechamento do Dia</li>
                        </ul>
                        <p><em>Em produção, isso executaria todos os 9 módulos automaticamente.</em></p>
                    </div>
                `,
                icon: 'info',
                confirmButtonText: 'Entendi!'
            });
        }
        
        function executarRentabilidade() {
            Swal.fire({
                title: '📈 Executando Módulos de Rentabilidade!',
                html: `
                    <div class="text-start">
                        <p><strong>Módulos de rentabilidade:</strong></p>
                        <ul>
                            <li>📊 Carteira A - Fundos de Ações</li>
                            <li>📊 Carteira B - Fundos de Renda Fixa</li>
                            <li>📊 Consolidada - Visão Geral</li>
                        </ul>
                        <p><em>Tempo estimado: 5-10 segundos</em></p>
                    </div>
                `,
                icon: 'success',
                confirmButtonText: 'Executar!'
            });
        }
        
        function executarImpostos() {
            Swal.fire({
                title: '💰 Executando Módulos de Impostos!',
                html: `
                    <div class="text-start">
                        <p><strong>Módulos de impostos:</strong></p>
                        <ul>
                            <li>🏛️ IR Retido na Fonte</li>
                            <li>💳 IOF sobre Operações</li>
                            <li>📋 PIS/COFINS</li>
                        </ul>
                        <p><em>Integração com sistemas da Receita Federal</em></p>
                    </div>
                `,
                icon: 'warning',
                confirmButtonText: 'Executar!'
            });
        }
        
        function executarModulo(modulo) {
            const nomes = {
                'carteira_a': 'Rentabilidade Carteira A',
                'ir_retido': 'IR Retido na Fonte',
                'custodia': 'Custódia de Títulos'
            };
            
            Swal.fire({
                title: `⚡ Executando: ${nomes[modulo]}`,
                html: `
                    <div class="text-start">
                        <p><strong>Processo:</strong></p>
                        <ol>
                            <li>🔍 Conectar com sistema fonte</li>
                            <li>📥 Baixar dados atualizados</li>
                            <li>🔄 Processar conciliação</li>
                            <li>📊 Gerar relatório</li>
                            <li>✅ Atualizar status</li>
                        </ol>
                        <p><em>Em produção, isso executaria a conciliação específica e atualizaria o status em tempo real.</em></p>
                    </div>
                `,
                icon: 'info',
                confirmButtonText: 'Entendi!'
            });
        }
        
        function verLogs(modulo) {
            Swal.fire({
                title: '📄 Logs de Execução',
                html: `
                    <div class="text-start" style="font-family: monospace; font-size: 12px;">
                        <p><strong>Última execução - ${new Date().toLocaleString()}:</strong></p>
                        <div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">
                            [INFO] Iniciando conciliação Carteira A<br>
                            [INFO] Conectando com sistema fonte...<br>
                            [SUCCESS] Dados baixados: 1.247 registros<br>
                            [INFO] Processando conciliação...<br>
                            [SUCCESS] Conciliação concluída: 100% match<br>
                            [INFO] Tempo total: 1.8 segundos
                        </div>
                    </div>
                `,
                icon: 'info',
                confirmButtonText: 'Fechar'
            });
        }
        
        function verErro(modulo) {
            Swal.fire({
                title: '🐛 Detalhes do Erro',
                html: `
                    <div class="text-start" style="font-family: monospace; font-size: 12px;">
                        <p><strong>Erro encontrado:</strong></p>
                        <div style="background: #f8d7da; padding: 10px; border-radius: 5px; color: #721c24;">
                            [ERROR] FileNotFoundError: Arquivo não encontrado<br>
                            [ERROR] Caminho: /dados/ir_retido_2025_06_07.xlsx<br>
                            [INFO] Verificar se arquivo foi gerado pelo sistema fonte<br>
                            [INFO] Contatar equipe de TI se problema persistir
                        </div>
                    </div>
                `,
                icon: 'error',
                confirmButtonText: 'Entendi'
            });
        }
        
        function atualizarDados() {
            Swal.fire({
                title: '🔄 Atualizando Dados!',
                html: `
                    <p>Buscando dados mais recentes de todas as conciliações...</p>
                    <p><em>Em produção, isso consultaria todos os sistemas fonte e atualizaria o dashboard.</em></p>
                `,
                icon: 'info',
                timer: 2000,
                showConfirmButton: false
            }).then(() => {
                location.reload();
            });
        }
        
        // Simular progresso
        let progresso = 45;
        setInterval(() => {
            progresso += Math.random() * 5;
            if (progresso > 100) progresso = 45;
            document.getElementById('progress').textContent = Math.round(progresso) + '%';
        }, 2000);
        
        // Adicionar SweetAlert2 para alertas bonitos
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@11';
        document.head.appendChild(script);
    </script>
</body>
</html>
'''

# Rota principal
@app.route('/')
def dashboard():
    hora_atual = datetime.now().strftime('%H:%M:%S')
    return render_template_string(HTML_TEMPLATE, hora_atual=hora_atual)

# API para dados
@app.route('/api/status')
def api_status():
    return jsonify({
        'total_modulos': 9,
        'implementados': 3,
        'taxa_sucesso': 95,
        'tempo_medio': 1.8,
        'ultima_atualizacao': datetime.now().isoformat(),
        'ambiente': 'VS Code + Jupyter',
        'status': 'online'
    })

def abrir_navegador():
    """Abre o navegador automaticamente após 2 segundos"""
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Dashboard aberto no navegador!")
    except Exception as e:
        print(f"⚠️ Não foi possível abrir o navegador automaticamente: {e}")
        print("📍 Acesse manualmente: http://localhost:5000")

if __name__ == "__main__":
    print("🚀 Iniciando Dashboard Galapagos DTVM...")
    print("🎯 Ambiente: VS Code + Jupyter")
    print("📍 URL: http://localhost:5000")
    print("⏹️ Para parar: Ctrl + C ou Kernel > Interrupt")
    print("=" * 60)
    
    # Abrir navegador automaticamente
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    # Executar Flask
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado pelo usuário!")
    except Exception as e:
        print(f"\n❌ Erro ao executar dashboard: {e}")
        print("💡 Tente executar novamente ou verifique se a porta 5000 está livre")

