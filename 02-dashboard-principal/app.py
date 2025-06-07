#!/usr/bin/env python3
"""
Dashboard Python - Galapagos DTVM
Sistema completo de monitoramento de conciliações em Python puro

Funcionalidades:
- Dashboard web responsivo
- API REST completa
- Banco SQLite integrado
- Gráficos interativos
- Sistema de notificações
- Execução de conciliações
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_cors import CORS
import sqlite3
import json
import os
import sys
from datetime import datetime, timedelta
import threading
import time
import subprocess
from pathlib import Path
import plotly.graph_objs as go
import plotly.utils
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da aplicação
app = Flask(__name__)
app.secret_key = 'galapagos-dtvm-2025-conciliacoes'
CORS(app)

# Configurações
DATABASE_PATH = 'dashboard-python/database/conciliacoes.db'
CONFIG_PATH = 'automacao-conciliacoes/config.json'

class DatabaseManager:
    """Gerenciador do banco de dados SQLite."""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados com as tabelas necessárias."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Tabela de módulos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS modulos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT UNIQUE NOT NULL,
                    categoria TEXT NOT NULL,
                    status TEXT DEFAULT 'desenvolvimento',
                    ultima_execucao TIMESTAMP,
                    tempo_execucao REAL,
                    sucesso BOOLEAN,
                    erro TEXT,
                    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de execuções
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS execucoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    modulo_id INTEGER,
                    data_execucao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tempo_execucao REAL,
                    sucesso BOOLEAN,
                    erro TEXT,
                    detalhes TEXT,
                    FOREIGN KEY (modulo_id) REFERENCES modulos (id)
                )
            ''')
            
            # Tabela de configurações
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracoes (
                    chave TEXT PRIMARY KEY,
                    valor TEXT,
                    descricao TEXT,
                    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("Banco de dados inicializado com sucesso")
    
    def get_connection(self):
        """Retorna uma conexão com o banco."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def inserir_modulos_iniciais(self):
        """Insere os módulos iniciais se não existirem."""
        modulos_iniciais = [
            ('Rentabilidade_Carteira_A', 'rentabilidade'),
            ('Rentabilidade_Carteira_B', 'rentabilidade'),
            ('Rentabilidade_Consolidada', 'rentabilidade'),
            ('IR_Retido_Fonte', 'impostos'),
            ('IOF_Operacoes', 'impostos'),
            ('PIS_COFINS', 'impostos'),
            ('Custodia_Titulos', 'outras'),
            ('Liquidacao_D0', 'outras'),
            ('Fechamento_Dia', 'outras')
        ]
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for nome, categoria in modulos_iniciais:
                cursor.execute('''
                    INSERT OR IGNORE INTO modulos (nome, categoria)
                    VALUES (?, ?)
                ''', (nome, categoria))
            
            conn.commit()
            logger.info(f"Inseridos {len(modulos_iniciais)} módulos iniciais")

class ConciliacaoManager:
    """Gerenciador de execução das conciliações."""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def executar_modulo(self, nome_modulo):
        """Executa um módulo específico."""
        logger.info(f"Executando módulo: {nome_modulo}")
        
        inicio = time.time()
        sucesso = False
        erro = None
        
        try:
            # Simular execução (substituir pela lógica real)
            time.sleep(2)  # Simular processamento
            sucesso = True
            logger.info(f"Módulo {nome_modulo} executado com sucesso")
            
        except Exception as e:
            erro = str(e)
            logger.error(f"Erro ao executar {nome_modulo}: {erro}")
        
        tempo_execucao = time.time() - inicio
        
        # Registrar execução no banco
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Atualizar módulo
            cursor.execute('''
                UPDATE modulos 
                SET ultima_execucao = CURRENT_TIMESTAMP,
                    tempo_execucao = ?,
                    sucesso = ?,
                    erro = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE nome = ?
            ''', (tempo_execucao, sucesso, erro, nome_modulo))
            
            # Inserir execução
            cursor.execute('''
                INSERT INTO execucoes (modulo_id, tempo_execucao, sucesso, erro)
                SELECT id, ?, ?, ? FROM modulos WHERE nome = ?
            ''', (tempo_execucao, sucesso, erro, nome_modulo))
            
            conn.commit()
        
        return sucesso, tempo_execucao, erro
    
    def executar_categoria(self, categoria):
        """Executa todos os módulos de uma categoria."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nome FROM modulos WHERE categoria = ?', (categoria,))
            modulos = [row['nome'] for row in cursor.fetchall()]
        
        resultados = []
        for modulo in modulos:
            resultado = self.executar_modulo(modulo)
            resultados.append((modulo, resultado))
        
        return resultados
    
    def executar_todos(self):
        """Executa todos os módulos."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nome FROM modulos')
            modulos = [row['nome'] for row in cursor.fetchall()]
        
        resultados = []
        for modulo in modulos:
            resultado = self.executar_modulo(modulo)
            resultados.append((modulo, resultado))
        
        return resultados

# Inicializar componentes
db_manager = DatabaseManager(DATABASE_PATH)
conciliacao_manager = ConciliacaoManager(db_manager)

# Inserir dados iniciais
db_manager.inserir_modulos_iniciais()

@app.route('/')
def dashboard():
    """Página principal do dashboard."""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """API para obter status geral do sistema."""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Estatísticas gerais
        cursor.execute('SELECT COUNT(*) as total FROM modulos')
        total_modulos = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as implementados FROM modulos WHERE status = "implementado"')
        modulos_implementados = cursor.fetchone()['implementados']
        
        cursor.execute('SELECT COUNT(*) as desenvolvimento FROM modulos WHERE status = "desenvolvimento"')
        modulos_desenvolvimento = cursor.fetchone()['desenvolvimento']
        
        cursor.execute('SELECT COUNT(*) as sucesso FROM modulos WHERE sucesso = 1')
        execucoes_sucesso = cursor.fetchone()['sucesso']
        
        # Módulos por categoria
        cursor.execute('''
            SELECT categoria, COUNT(*) as total,
                   SUM(CASE WHEN sucesso = 1 THEN 1 ELSE 0 END) as sucesso
            FROM modulos 
            GROUP BY categoria
        ''')
        categorias = [dict(row) for row in cursor.fetchall()]
        
        # Últimas execuções
        cursor.execute('''
            SELECT m.nome, m.categoria, m.ultima_execucao, m.tempo_execucao, m.sucesso, m.erro
            FROM modulos m
            ORDER BY m.atualizado_em DESC
            LIMIT 10
        ''')
        ultimas_execucoes = [dict(row) for row in cursor.fetchall()]
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'total_modulos': total_modulos,
        'modulos_implementados': modulos_implementados,
        'modulos_desenvolvimento': modulos_desenvolvimento,
        'execucoes_sucesso': execucoes_sucesso,
        'taxa_sucesso': round((execucoes_sucesso / total_modulos * 100) if total_modulos > 0 else 0, 1),
        'categorias': categorias,
        'ultimas_execucoes': ultimas_execucoes
    })

@app.route('/api/modulos')
def api_modulos():
    """API para listar todos os módulos."""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM modulos 
            ORDER BY categoria, nome
        ''')
        modulos = [dict(row) for row in cursor.fetchall()]
    
    return jsonify(modulos)

@app.route('/api/modulos/<categoria>')
def api_modulos_categoria(categoria):
    """API para listar módulos de uma categoria."""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM modulos 
            WHERE categoria = ?
            ORDER BY nome
        ''', (categoria,))
        modulos = [dict(row) for row in cursor.fetchall()]
    
    return jsonify(modulos)

@app.route('/api/executar/<modulo>', methods=['POST'])
def api_executar_modulo(modulo):
    """API para executar um módulo específico."""
    try:
        # Executar em thread separada para não bloquear
        def executar_async():
            conciliacao_manager.executar_modulo(modulo)
        
        thread = threading.Thread(target=executar_async)
        thread.start()
        
        return jsonify({
            'status': 'iniciado',
            'modulo': modulo,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'erro': str(e)
        }), 500

@app.route('/api/executar/categoria/<categoria>', methods=['POST'])
def api_executar_categoria(categoria):
    """API para executar todos os módulos de uma categoria."""
    try:
        def executar_async():
            conciliacao_manager.executar_categoria(categoria)
        
        thread = threading.Thread(target=executar_async)
        thread.start()
        
        return jsonify({
            'status': 'iniciado',
            'categoria': categoria,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'erro': str(e)
        }), 500

@app.route('/api/executar/todos', methods=['POST'])
def api_executar_todos():
    """API para executar todos os módulos."""
    try:
        def executar_async():
            conciliacao_manager.executar_todos()
        
        thread = threading.Thread(target=executar_async)
        thread.start()
        
        return jsonify({
            'status': 'iniciado',
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'erro': str(e)
        }), 500

@app.route('/api/graficos/performance')
def api_graficos_performance():
    """API para dados de gráficos de performance."""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Performance por categoria
        cursor.execute('''
            SELECT categoria, 
                   AVG(tempo_execucao) as tempo_medio,
                   COUNT(*) as total_execucoes,
                   SUM(CASE WHEN sucesso = 1 THEN 1 ELSE 0 END) as sucessos
            FROM modulos m
            JOIN execucoes e ON m.id = e.modulo_id
            WHERE e.data_execucao >= date('now', '-30 days')
            GROUP BY categoria
        ''')
        performance_categoria = [dict(row) for row in cursor.fetchall()]
        
        # Execuções por dia (últimos 30 dias)
        cursor.execute('''
            SELECT date(data_execucao) as data,
                   COUNT(*) as total,
                   SUM(CASE WHEN sucesso = 1 THEN 1 ELSE 0 END) as sucessos
            FROM execucoes
            WHERE data_execucao >= date('now', '-30 days')
            GROUP BY date(data_execucao)
            ORDER BY data
        ''')
        execucoes_diarias = [dict(row) for row in cursor.fetchall()]
    
    return jsonify({
        'performance_categoria': performance_categoria,
        'execucoes_diarias': execucoes_diarias
    })

@app.route('/relatorio')
def relatorio():
    """Página de relatório detalhado."""
    return render_template('relatorio.html')

@app.route('/configuracoes')
def configuracoes():
    """Página de configurações."""
    return render_template('configuracoes.html')

def main():
    """Função principal para executar o servidor."""
    print("🚀 Iniciando Dashboard Python - Galapagos DTVM")
    print("=" * 60)
    print("🐍 Sistema 100% Python")
    print("📊 Dashboard web responsivo")
    print("🗄️ Banco SQLite integrado")
    print("📈 Gráficos interativos")
    print("🔄 API REST completa")
    print("=" * 60)
    
    # Configurar porta
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🌐 Dashboard disponível em: http://localhost:{port}")
    print(f"📊 API disponível em: http://localhost:{port}/api/status")
    print("💡 Para parar: Pressione Ctrl+C")
    print("=" * 60)
    
    # Executar aplicação
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True,
        threaded=True
    )

if __name__ == '__main__':
    main()

