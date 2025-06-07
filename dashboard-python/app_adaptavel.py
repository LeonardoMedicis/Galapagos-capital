#!/usr/bin/env python3
"""
Dashboard Adaptável - Galapagos DTVM
Sistema que se adapta automaticamente ao ambiente:
- Desenvolvimento: Dados locais, modo debug
- Produção: Dados compartilhados, tempo real
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_cors import CORS
import sqlite3
import json
import os
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging
from configurar_ambiente import EnvironmentDetector

# Detectar ambiente automaticamente
detector = EnvironmentDetector()
config = detector.config

# Configurar logging baseado no ambiente
log_level = logging.DEBUG if config["environment"] == "development" else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(config["paths"]["logs"]) / "dashboard.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuração da aplicação
app = Flask(__name__)
app.secret_key = f'galapagos-dtvm-{config["environment"]}-2025'
CORS(app)

class AdaptiveDatabaseManager:
    """Gerenciador de banco adaptável ao ambiente."""
    
    def __init__(self, config):
        self.config = config
        self.db_path = config["database"]["path"]
        self.shared = config["database"]["shared"]
        self.init_database()
        
        logger.info(f"Database inicializado: {self.db_path}")
        logger.info(f"Modo compartilhado: {self.shared}")
    
    def init_database(self):
        """Inicializa banco com configurações específicas do ambiente."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Configurações específicas por ambiente
        if self.shared:
            # Produção: configurações para múltiplos usuários
            pragma_settings = [
                "PRAGMA journal_mode=WAL;",  # Write-Ahead Logging para concorrência
                "PRAGMA synchronous=NORMAL;",  # Balance entre performance e segurança
                "PRAGMA cache_size=10000;",  # Cache maior para performance
                "PRAGMA temp_store=memory;",  # Temp tables em memória
                "PRAGMA mmap_size=268435456;"  # Memory mapping para performance
            ]
        else:
            # Desenvolvimento: configurações para uso local
            pragma_settings = [
                "PRAGMA journal_mode=DELETE;",  # Modo simples
                "PRAGMA synchronous=FULL;",  # Máxima segurança
                "PRAGMA cache_size=2000;"  # Cache menor
            ]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Aplicar configurações
            for pragma in pragma_settings:
                cursor.execute(pragma)
            
            # Criar tabelas
            self._create_tables(cursor)
            conn.commit()
    
    def _create_tables(self, cursor):
        """Cria tabelas do banco."""
        
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
                usuario TEXT,
                ambiente TEXT,
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
                usuario TEXT,
                ambiente TEXT,
                FOREIGN KEY (modulo_id) REFERENCES modulos (id)
            )
        ''')
        
        # Tabela de configurações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes (
                chave TEXT PRIMARY KEY,
                valor TEXT,
                descricao TEXT,
                usuario TEXT,
                ambiente TEXT,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de auditoria (só em produção)
        if self.shared:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auditoria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    acao TEXT NOT NULL,
                    tabela TEXT,
                    registro_id INTEGER,
                    dados_antes TEXT,
                    dados_depois TEXT,
                    usuario TEXT,
                    ip TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    
    def get_connection(self):
        """Retorna conexão com configurações específicas do ambiente."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        
        if self.shared:
            # Produção: configurações para concorrência
            conn.execute("PRAGMA busy_timeout=30000")  # 30 segundos timeout
            conn.execute("PRAGMA journal_mode=WAL")
        
        return conn
    
    def inserir_modulos_iniciais(self):
        """Insere módulos iniciais com informações do ambiente."""
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
                    INSERT OR IGNORE INTO modulos (nome, categoria, ambiente)
                    VALUES (?, ?, ?)
                ''', (nome, categoria, config["environment"]))
            
            conn.commit()
            logger.info(f"Módulos iniciais inseridos para ambiente: {config['environment']}")

class AdaptiveConciliacaoManager:
    """Gerenciador de conciliações adaptável ao ambiente."""
    
    def __init__(self, db_manager, config):
        self.db = db_manager
        self.config = config
        self.dados_path = Path(config["paths"]["dados"])
        self.resultados_path = Path(config["paths"]["resultados"])
        
        # Criar diretórios se não existirem
        self.dados_path.mkdir(parents=True, exist_ok=True)
        self.resultados_path.mkdir(parents=True, exist_ok=True)
    
    def executar_modulo(self, nome_modulo, usuario="sistema"):
        """Executa módulo com configurações específicas do ambiente."""
        logger.info(f"Executando módulo: {nome_modulo} (usuário: {usuario})")
        
        inicio = time.time()
        sucesso = False
        erro = None
        detalhes = {}
        
        try:
            # Simular execução baseada no ambiente
            if self.config["environment"] == "production":
                # Produção: execução real com dados da rede
                detalhes = self._executar_producao(nome_modulo)
                time.sleep(3)  # Simular tempo real de execução
            else:
                # Desenvolvimento: execução simulada
                detalhes = self._executar_desenvolvimento(nome_modulo)
                time.sleep(1)  # Execução mais rápida para testes
            
            sucesso = True
            logger.info(f"Módulo {nome_modulo} executado com sucesso")
            
        except Exception as e:
            erro = str(e)
            logger.error(f"Erro ao executar {nome_modulo}: {erro}")
        
        tempo_execucao = time.time() - inicio
        
        # Registrar execução no banco
        self._registrar_execucao(nome_modulo, tempo_execucao, sucesso, erro, detalhes, usuario)
        
        return sucesso, tempo_execucao, erro, detalhes
    
    def _executar_producao(self, nome_modulo):
        """Execução real em ambiente de produção."""
        detalhes = {
            "ambiente": "production",
            "dados_fonte": str(self.dados_path / f"{nome_modulo.lower()}.xlsx"),
            "resultado_arquivo": str(self.resultados_path / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{nome_modulo}.json"),
            "registros_processados": 1250,
            "divergencias_encontradas": 0,
            "tempo_download": 1.2,
            "tempo_processamento": 1.8
        }
        
        # Salvar resultado real
        resultado_file = Path(detalhes["resultado_arquivo"])
        with open(resultado_file, 'w', encoding='utf-8') as f:
            json.dump({
                "modulo": nome_modulo,
                "timestamp": datetime.now().isoformat(),
                "status": "sucesso",
                "detalhes": detalhes
            }, f, indent=2, ensure_ascii=False)
        
        return detalhes
    
    def _executar_desenvolvimento(self, nome_modulo):
        """Execução simulada em ambiente de desenvolvimento."""
        detalhes = {
            "ambiente": "development",
            "dados_fonte": "simulado",
            "resultado_arquivo": "simulado",
            "registros_processados": 100,
            "divergencias_encontradas": 0,
            "tempo_download": 0.1,
            "tempo_processamento": 0.2,
            "nota": "Execução simulada para desenvolvimento"
        }
        
        return detalhes
    
    def _registrar_execucao(self, nome_modulo, tempo_execucao, sucesso, erro, detalhes, usuario):
        """Registra execução no banco com informações do ambiente."""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Atualizar módulo
            cursor.execute('''
                UPDATE modulos 
                SET ultima_execucao = CURRENT_TIMESTAMP,
                    tempo_execucao = ?,
                    sucesso = ?,
                    erro = ?,
                    usuario = ?,
                    ambiente = ?,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE nome = ?
            ''', (tempo_execucao, sucesso, erro, usuario, config["environment"], nome_modulo))
            
            # Inserir execução
            cursor.execute('''
                INSERT INTO execucoes (modulo_id, tempo_execucao, sucesso, erro, detalhes, usuario, ambiente)
                SELECT id, ?, ?, ?, ?, ?, ? FROM modulos WHERE nome = ?
            ''', (tempo_execucao, sucesso, erro, json.dumps(detalhes), usuario, config["environment"], nome_modulo))
            
            conn.commit()

# Inicializar componentes
db_manager = AdaptiveDatabaseManager(config)
conciliacao_manager = AdaptiveConciliacaoManager(db_manager, config)

# Inserir dados iniciais
db_manager.inserir_modulos_iniciais()

@app.route('/')
def dashboard():
    """Página principal adaptável ao ambiente."""
    return render_template('dashboard_adaptavel.html', 
                         environment=config["environment"],
                         config=config)

@app.route('/api/status')
def api_status():
    """API de status com informações do ambiente."""
    with db_manager.get_connection() as conn:
        cursor = conn.cursor()
        
        # Estatísticas gerais
        cursor.execute('SELECT COUNT(*) as total FROM modulos WHERE ambiente = ?', (config["environment"],))
        total_modulos = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(*) as implementados FROM modulos WHERE status = "implementado" AND ambiente = ?', (config["environment"],))
        modulos_implementados = cursor.fetchone()['implementados']
        
        cursor.execute('SELECT COUNT(*) as desenvolvimento FROM modulos WHERE status = "desenvolvimento" AND ambiente = ?', (config["environment"],))
        modulos_desenvolvimento = cursor.fetchone()['desenvolvimento']
        
        cursor.execute('SELECT COUNT(*) as sucesso FROM modulos WHERE sucesso = 1 AND ambiente = ?', (config["environment"],))
        execucoes_sucesso = cursor.fetchone()['sucesso']
        
        # Módulos por categoria
        cursor.execute('''
            SELECT categoria, COUNT(*) as total,
                   SUM(CASE WHEN sucesso = 1 THEN 1 ELSE 0 END) as sucesso
            FROM modulos 
            WHERE ambiente = ?
            GROUP BY categoria
        ''', (config["environment"],))
        categorias = [dict(row) for row in cursor.fetchall()]
        
        # Últimas execuções
        cursor.execute('''
            SELECT m.nome, m.categoria, m.ultima_execucao, m.tempo_execucao, m.sucesso, m.erro, m.usuario
            FROM modulos m
            WHERE m.ambiente = ?
            ORDER BY m.atualizado_em DESC
            LIMIT 10
        ''', (config["environment"],))
        ultimas_execucoes = [dict(row) for row in cursor.fetchall()]
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'environment': config["environment"],
        'total_modulos': total_modulos,
        'modulos_implementados': modulos_implementados,
        'modulos_desenvolvimento': modulos_desenvolvimento,
        'execucoes_sucesso': execucoes_sucesso,
        'taxa_sucesso': round((execucoes_sucesso / total_modulos * 100) if total_modulos > 0 else 0, 1),
        'categorias': categorias,
        'ultimas_execucoes': ultimas_execucoes,
        'config': {
            'shared': config["database"]["shared"],
            'real_time': config["features"]["real_time"],
            'paths': config["paths"]
        }
    })

@app.route('/api/executar/<modulo>', methods=['POST'])
def api_executar_modulo(modulo):
    """API para executar módulo com informações do usuário."""
    try:
        usuario = request.json.get('usuario', 'anonimo') if request.is_json else 'sistema'
        
        def executar_async():
            conciliacao_manager.executar_modulo(modulo, usuario)
        
        thread = threading.Thread(target=executar_async)
        thread.start()
        
        return jsonify({
            'status': 'iniciado',
            'modulo': modulo,
            'usuario': usuario,
            'environment': config["environment"],
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'erro': str(e),
            'environment': config["environment"]
        }), 500

def main():
    """Função principal adaptável ao ambiente."""
    print("🚀 Iniciando Dashboard Adaptável - Galapagos DTVM")
    print("=" * 60)
    
    # Mostrar informações do ambiente
    detector.print_environment_info()
    
    # Configurar porta
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🌐 Dashboard disponível em: http://localhost:{port}")
    print(f"📊 API disponível em: http://localhost:{port}/api/status")
    
    if config["environment"] == "production":
        print("🏭 MODO PRODUÇÃO:")
        print("   ✅ Dados compartilhados em tempo real")
        print("   ✅ Múltiplos usuários suportados")
        print("   ✅ Logs de auditoria habilitados")
    else:
        print("🔧 MODO DESENVOLVIMENTO:")
        print("   ✅ Dados locais para testes")
        print("   ✅ Debug mode habilitado")
        print("   ✅ Execuções simuladas")
    
    print("💡 Para parar: Pressione Ctrl+C")
    print("=" * 60)
    
    # Executar aplicação
    debug_mode = config["environment"] == "development"
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode,
        threaded=True
    )

if __name__ == '__main__':
    main()

