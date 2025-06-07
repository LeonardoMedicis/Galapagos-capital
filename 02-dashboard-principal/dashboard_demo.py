#!/usr/bin/env python3
"""
Dashboard Principal - Galapagos DTVM
Sistema de monitoramento de conciliações em tempo real
"""

import os
import sys
import json
import sqlite3
import webbrowser
import threading
import time
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# Configuração da aplicação
app = Flask(__name__)
CORS(app)

# Detectar ambiente
def detectar_ambiente():
    """Detecta se está em desenvolvimento ou produção."""
    current_path = Path.cwd()
    
    # Se está em pasta que contém .git, é desenvolvimento
    if (current_path / '.git').exists() or (current_path.parent / '.git').exists():
        return 'development'
    
    # Se está em pasta de rede corporativa, é produção
    if 'servidor' in str(current_path).lower() or 'galapagos' in str(current_path).lower():
        return 'production'
    
    return 'development'  # Default

# Configurar ambiente
ambiente = detectar_ambiente()
app.config['DEBUG'] = ambiente == 'development'

print(f"🎯 Ambiente detectado: {ambiente.upper()}")
print(f"🔧 Debug mode: {app.config['DEBUG']}")

# Dados simulados para demonstração
dados_conciliacoes = {
    "ambiente": ambiente,
    "timestamp": datetime.now().isoformat(),
    "estatisticas": {
        "total_modulos": 9,
        "implementados": 1,
        "em_desenvolvimento": 8,
        "taxa_sucesso": 85,
        "execucoes_hoje": 12,
        "tempo_medio": 2.3
    },
    "modulos": [
        {
            "id": "rentabilidade_carteira_a",
            "nome": "Rentabilidade Carteira A",
            "categoria": "rentabilidade",
            "status": "sucesso",
            "ultima_execucao": "2025-06-07 14:30:00",
            "tempo_execucao": 2.1,
            "implementado": True,
            "erro": None
        },
        {
            "id": "rentabilidade_carteira_b", 
            "nome": "Rentabilidade Carteira B",
            "categoria": "rentabilidade",
            "status": "pendente",
            "ultima_execucao": None,
            "tempo_execucao": None,
            "implementado": False,
            "erro": None
        },
        {
            "id": "ir_retido_fonte",
            "nome": "IR Retido na Fonte", 
            "categoria": "impostos",
            "status": "erro",
            "ultima_execucao": "2025-06-07 13:45:00",
            "tempo_execucao": 1.8,
            "implementado": False,
            "erro": "Arquivo não encontrado"
        },
        {
            "id": "iof_operacoes",
            "nome": "IOF sobre Operações",
            "categoria": "impostos", 
            "status": "sucesso",
            "ultima_execucao": "2025-06-07 14:15:00",
            "tempo_execucao": 3.2,
            "implementado": False,
            "erro": None
        },
        {
            "id": "custodia_titulos",
            "nome": "Custódia de Títulos",
            "categoria": "outras",
            "status": "executando",
            "ultima_execucao": "2025-06-07 14:35:00",
            "tempo_execucao": None,
            "implementado": False,
            "erro": None
        }
    ]
}

@app.route('/')
def dashboard():
    """Página principal do dashboard."""
    return render_template_string(TEMPLATE_DASHBOARD, 
                                ambiente=ambiente,
                                dados=dados_conciliacoes)

@app.route('/api/status')
def api_status():
    """API para obter status das conciliações."""
    return jsonify(dados_conciliacoes)

@app.route('/api/executar/<modulo_id>', methods=['POST'])
def api_executar(modulo_id):
    """API para executar conciliação."""
    print(f"🚀 Executando módulo: {modulo_id}")
    
    # Simular execução
    time.sleep(1)
    
    # Atualizar status do módulo
    for modulo in dados_conciliacoes['modulos']:
        if modulo['id'] == modulo_id:
            modulo['status'] = 'executando'
            modulo['ultima_execucao'] = datetime.now().isoformat()
            break
    
    return jsonify({
        "status": "iniciado",
        "modulo": modulo_id,
        "timestamp": datetime.now().isoformat()
    })

# Template HTML do dashboard
TEMPLATE_DASHBOARD = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Galapagos DTVM</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            {% if ambiente == 'production' %}
            --primary-color: #28a745;
            --primary-light: #d4edda;
            --env-badge: #28a745;
            {% else %}
            --primary-color: #007bff;
            --primary-light: #d1ecf1;
            --env-badge: #007bff;
            {% endif %}
        }
        
        body {
            background: linear-gradient(135deg, var(--primary-light) 0%, #ffffff 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .navbar {
            background: var(--primary-color) !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .stat-card {
            background: linear-gradient(135deg, var(--primary-color), #6c757d);
            color: white;
        }
        
        .status-badge {
            font-size: 0.8rem;
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
        }
        
        .status-sucesso { background: #28a745; color: white; }
        .status-erro { background: #dc3545; color: white; }
        .status-executando { background: #ffc107; color: black; }
        .status-pendente { background: #6c757d; color: white; }
        
        .btn-executar {
            background: var(--primary-color);
            border: none;
            border-radius: 25px;
            padding: 0.5rem 1.5rem;
            transition: all 0.3s ease;
        }
        
        .btn-executar:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .env-badge {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--env-badge);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-size: 0.8rem;
            z-index: 1000;
        }
        
        .progress-bar {
            background: var(--primary-color);
        }
        
        .categoria-rentabilidade { border-left: 5px solid #28a745; }
        .categoria-impostos { border-left: 5px solid #dc3545; }
        .categoria-outras { border-left: 5px solid #ffc107; }
    </style>
</head>
<body>
    <!-- Badge de ambiente -->
    <div class="env-badge">
        <i class="fas fa-{{ 'industry' if ambiente == 'production' else 'code' }}"></i>
        {{ 'PRODUÇÃO' if ambiente == 'production' else 'DESENVOLVIMENTO' }}
    </div>

    <!-- Navbar -->
    <nav class="navbar navbar-dark">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-chart-line me-2"></i>
                Galapagos DTVM - Dashboard de Conciliações
            </span>
            <span class="navbar-text">
                <i class="fas fa-clock me-1"></i>
                <span id="timestamp">{{ dados.timestamp }}</span>
            </span>
        </div>
    </nav>

    <div class="container-fluid mt-4">
        <!-- Estatísticas Gerais -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <i class="fas fa-cubes fa-2x mb-2"></i>
                        <h3>{{ dados.estatisticas.total_modulos }}</h3>
                        <p class="mb-0">Total de Módulos</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <i class="fas fa-check-circle fa-2x mb-2"></i>
                        <h3>{{ dados.estatisticas.implementados }}</h3>
                        <p class="mb-0">Implementados</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <i class="fas fa-percentage fa-2x mb-2"></i>
                        <h3>{{ dados.estatisticas.taxa_sucesso }}%</h3>
                        <p class="mb-0">Taxa de Sucesso</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card stat-card">
                    <div class="card-body text-center">
                        <i class="fas fa-clock fa-2x mb-2"></i>
                        <h3>{{ dados.estatisticas.tempo_medio }}s</h3>
                        <p class="mb-0">Tempo Médio</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Controles Rápidos -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-play-circle me-2"></i>Controles Rápidos</h5>
                    </div>
                    <div class="card-body">
                        <button class="btn btn-success btn-executar me-2" onclick="executarTodos()">
                            <i class="fas fa-play me-1"></i>Executar Todos
                        </button>
                        <button class="btn btn-primary btn-executar me-2" onclick="executarCategoria('rentabilidade')">
                            <i class="fas fa-chart-line me-1"></i>Só Rentabilidade
                        </button>
                        <button class="btn btn-danger btn-executar me-2" onclick="executarCategoria('impostos')">
                            <i class="fas fa-coins me-1"></i>Só Impostos
                        </button>
                        <button class="btn btn-warning btn-executar" onclick="atualizarDados()">
                            <i class="fas fa-sync me-1"></i>Atualizar
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Módulos de Conciliação -->
        <div class="row">
            {% for modulo in dados.modulos %}
            <div class="col-md-6 col-lg-4 mb-3">
                <div class="card categoria-{{ modulo.categoria }}">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">{{ modulo.nome }}</h6>
                        <span class="status-badge status-{{ modulo.status }}">
                            {% if modulo.status == 'sucesso' %}
                                <i class="fas fa-check"></i> Sucesso
                            {% elif modulo.status == 'erro' %}
                                <i class="fas fa-times"></i> Erro
                            {% elif modulo.status == 'executando' %}
                                <i class="fas fa-spinner fa-spin"></i> Executando
                            {% else %}
                                <i class="fas fa-clock"></i> Pendente
                            {% endif %}
                        </span>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-6">
                                <small class="text-muted">Categoria:</small><br>
                                <span class="badge bg-secondary">{{ modulo.categoria.title() }}</span>
                            </div>
                            <div class="col-6">
                                <small class="text-muted">Implementado:</small><br>
                                {% if modulo.implementado %}
                                    <span class="badge bg-success">Sim</span>
                                {% else %}
                                    <span class="badge bg-warning">Estrutura</span>
                                {% endif %}
                            </div>
                        </div>
                        
                        {% if modulo.ultima_execucao %}
                        <div class="mt-2">
                            <small class="text-muted">Última execução:</small><br>
                            <small>{{ modulo.ultima_execucao }}</small>
                        </div>
                        {% endif %}
                        
                        {% if modulo.tempo_execucao %}
                        <div class="mt-1">
                            <small class="text-muted">Tempo: {{ modulo.tempo_execucao }}s</small>
                        </div>
                        {% endif %}
                        
                        {% if modulo.erro %}
                        <div class="mt-2">
                            <small class="text-danger">Erro: {{ modulo.erro }}</small>
                        </div>
                        {% endif %}
                        
                        <div class="mt-3">
                            <button class="btn btn-primary btn-sm btn-executar" 
                                    onclick="executarModulo('{{ modulo.id }}')"
                                    {% if modulo.status == 'executando' %}disabled{% endif %}>
                                {% if modulo.status == 'executando' %}
                                    <i class="fas fa-spinner fa-spin"></i> Executando...
                                {% else %}
                                    <i class="fas fa-play"></i> Executar
                                {% endif %}
                            </button>
                            <button class="btn btn-outline-secondary btn-sm" onclick="verLogs('{{ modulo.id }}')">
                                <i class="fas fa-file-alt"></i> Logs
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Atualizar timestamp
        function atualizarTimestamp() {
            document.getElementById('timestamp').textContent = new Date().toLocaleString('pt-BR');
        }
        
        // Executar módulo específico
        function executarModulo(moduloId) {
            console.log('Executando módulo:', moduloId);
            
            fetch(`/api/executar/${moduloId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Resposta:', data);
                alert(`Módulo ${moduloId} iniciado com sucesso!`);
                setTimeout(() => location.reload(), 2000);
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao executar módulo');
            });
        }
        
        // Executar todos os módulos
        function executarTodos() {
            if (confirm('Executar todas as conciliações?')) {
                alert('Executando todas as conciliações...');
                setTimeout(() => location.reload(), 3000);
            }
        }
        
        // Executar por categoria
        function executarCategoria(categoria) {
            if (confirm(`Executar todas as conciliações de ${categoria}?`)) {
                alert(`Executando conciliações de ${categoria}...`);
                setTimeout(() => location.reload(), 3000);
            }
        }
        
        // Ver logs
        function verLogs(moduloId) {
            alert(`Logs do módulo ${moduloId} (funcionalidade em desenvolvimento)`);
        }
        
        // Atualizar dados
        function atualizarDados() {
            location.reload();
        }
        
        // Auto-refresh a cada 30 segundos
        setInterval(() => {
            atualizarTimestamp();
        }, 30000);
        
        // Atualizar timestamp inicial
        atualizarTimestamp();
    </script>
</body>
</html>
'''

def abrir_navegador():
    """Abre navegador após delay."""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🚀 Iniciando Dashboard Galapagos DTVM...")
    print("📍 URL: http://localhost:5000")
    print("⏹️ Para parar: Ctrl+C")
    print("=" * 50)
    
    # Abrir navegador em thread separada
    threading.Thread(target=abrir_navegador, daemon=True).start()
    
    # Iniciar servidor
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro no servidor: {e}")

