#!/usr/bin/env python3
"""
Sistema de comunicação entre módulos e mapa central.

Este módulo fornece funcionalidades para que cada módulo de conciliação
reporte seu status, progresso e resultados para o mapa central de controle.
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging


class StatusReporter:
    """
    Classe responsável por reportar status dos módulos para o mapa central.
    
    Attributes:
        db_path (Path): Caminho para o banco de dados SQLite
        logger (logging.Logger): Logger para operações
    """
    
    def __init__(self, db_path: str = "status_conciliacoes.db"):
        """
        Inicializa o reporter de status.
        
        Args:
            db_path: Caminho para o banco de dados SQLite
        """
        self.db_path = Path(db_path)
        self.logger = logging.getLogger("status_reporter")
        self._inicializar_banco()
    
    def _inicializar_banco(self) -> None:
        """
        Inicializa o banco de dados SQLite com as tabelas necessárias.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tabela de status dos módulos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS status_modulos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_modulo TEXT NOT NULL,
                        categoria TEXT NOT NULL,
                        criticidade TEXT NOT NULL,
                        status TEXT NOT NULL,
                        progresso INTEGER DEFAULT 0,
                        mensagem TEXT,
                        timestamp_inicio DATETIME,
                        timestamp_fim DATETIME,
                        timestamp_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                        dados_resultado TEXT,
                        erro TEXT
                    )
                """)
                
                # Tabela de histórico de execuções
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS historico_execucoes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome_modulo TEXT NOT NULL,
                        data_referencia TEXT NOT NULL,
                        status TEXT NOT NULL,
                        tempo_execucao REAL,
                        registros_processados INTEGER,
                        registros_validos INTEGER,
                        registros_invalidos INTEGER,
                        taxa_sucesso REAL,
                        timestamp_execucao DATETIME DEFAULT CURRENT_TIMESTAMP,
                        dados_completos TEXT
                    )
                """)
                
                # Tabela de métricas consolidadas
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS metricas_consolidadas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        data_consolidacao DATE NOT NULL,
                        total_modulos INTEGER,
                        modulos_executados INTEGER,
                        modulos_sucesso INTEGER,
                        modulos_erro INTEGER,
                        tempo_total_execucao REAL,
                        taxa_sucesso_geral REAL,
                        timestamp_consolidacao DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                self.logger.info("✅ Banco de dados inicializado")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao inicializar banco: {e}")
            raise
    
    def reportar_inicio(self, nome_modulo: str, categoria: str = "", criticidade: str = "") -> None:
        """
        Reporta o início da execução de um módulo.
        
        Args:
            nome_modulo: Nome do módulo
            categoria: Categoria do módulo
            criticidade: Criticidade do módulo
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Inserir ou atualizar status
                cursor.execute("""
                    INSERT OR REPLACE INTO status_modulos 
                    (nome_modulo, categoria, criticidade, status, progresso, 
                     mensagem, timestamp_inicio, timestamp_atualizacao)
                    VALUES (?, ?, ?, 'executando', 0, 'Iniciando execução...', ?, ?)
                """, (nome_modulo, categoria, criticidade, datetime.now(), datetime.now()))
                
                conn.commit()
                self.logger.info(f"📊 Início reportado: {nome_modulo}")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao reportar início: {e}")
    
    def reportar_progresso(self, nome_modulo: str, progresso: int, mensagem: str = "") -> None:
        """
        Reporta o progresso da execução de um módulo.
        
        Args:
            nome_modulo: Nome do módulo
            progresso: Percentual de progresso (0-100)
            mensagem: Mensagem descritiva do progresso
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE status_modulos 
                    SET progresso = ?, mensagem = ?, timestamp_atualizacao = ?
                    WHERE nome_modulo = ?
                """, (progresso, mensagem, datetime.now(), nome_modulo))
                
                conn.commit()
                self.logger.debug(f"📈 Progresso reportado: {nome_modulo} - {progresso}%")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao reportar progresso: {e}")
    
    def reportar_sucesso(self, nome_modulo: str, resultados: Dict[str, Any]) -> None:
        """
        Reporta o sucesso da execução de um módulo.
        
        Args:
            nome_modulo: Nome do módulo
            resultados: Resultados da execução
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Atualizar status do módulo
                cursor.execute("""
                    UPDATE status_modulos 
                    SET status = 'sucesso', progresso = 100, 
                        mensagem = 'Execução concluída com sucesso',
                        timestamp_fim = ?, timestamp_atualizacao = ?,
                        dados_resultado = ?
                    WHERE nome_modulo = ?
                """, (datetime.now(), datetime.now(), json.dumps(resultados), nome_modulo))
                
                # Inserir no histórico
                metricas = resultados.get("metricas", {})
                cursor.execute("""
                    INSERT INTO historico_execucoes
                    (nome_modulo, data_referencia, status, tempo_execucao,
                     registros_processados, registros_validos, registros_invalidos,
                     taxa_sucesso, dados_completos)
                    VALUES (?, ?, 'sucesso', ?, ?, ?, ?, ?, ?)
                """, (
                    nome_modulo,
                    resultados.get("data_referencia", datetime.now().strftime("%Y-%m-%d")),
                    metricas.get("tempo_execucao", 0),
                    resultados.get("total_registros", 0),
                    resultados.get("registros_validos", 0),
                    resultados.get("registros_invalidos", 0),
                    metricas.get("taxa_sucesso", 100.0),
                    json.dumps(resultados)
                ))
                
                conn.commit()
                self.logger.info(f"✅ Sucesso reportado: {nome_modulo}")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao reportar sucesso: {e}")
    
    def reportar_erro(self, nome_modulo: str, erro: str) -> None:
        """
        Reporta erro na execução de um módulo.
        
        Args:
            nome_modulo: Nome do módulo
            erro: Descrição do erro
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Atualizar status do módulo
                cursor.execute("""
                    UPDATE status_modulos 
                    SET status = 'erro', mensagem = ?, 
                        timestamp_fim = ?, timestamp_atualizacao = ?,
                        erro = ?
                    WHERE nome_modulo = ?
                """, (f"Erro: {erro}", datetime.now(), datetime.now(), erro, nome_modulo))
                
                # Inserir no histórico
                cursor.execute("""
                    INSERT INTO historico_execucoes
                    (nome_modulo, data_referencia, status, dados_completos)
                    VALUES (?, ?, 'erro', ?)
                """, (
                    nome_modulo,
                    datetime.now().strftime("%Y-%m-%d"),
                    json.dumps({"erro": erro, "timestamp": datetime.now().isoformat()})
                ))
                
                conn.commit()
                self.logger.error(f"❌ Erro reportado: {nome_modulo} - {erro}")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao reportar erro: {e}")
    
    def obter_status_modulo(self, nome_modulo: str) -> Optional[Dict[str, Any]]:
        """
        Obtém o status atual de um módulo específico.
        
        Args:
            nome_modulo: Nome do módulo
            
        Returns:
            Dicionário com status do módulo ou None se não encontrado
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT nome_modulo, categoria, criticidade, status, progresso,
                           mensagem, timestamp_inicio, timestamp_fim, 
                           timestamp_atualizacao, dados_resultado, erro
                    FROM status_modulos 
                    WHERE nome_modulo = ?
                    ORDER BY timestamp_atualizacao DESC
                    LIMIT 1
                """, (nome_modulo,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "nome_modulo": row[0],
                        "categoria": row[1],
                        "criticidade": row[2],
                        "status": row[3],
                        "progresso": row[4],
                        "mensagem": row[5],
                        "timestamp_inicio": row[6],
                        "timestamp_fim": row[7],
                        "timestamp_atualizacao": row[8],
                        "dados_resultado": json.loads(row[9]) if row[9] else None,
                        "erro": row[10]
                    }
                
                return None
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter status: {e}")
            return None
    
    def obter_status_todos_modulos(self) -> List[Dict[str, Any]]:
        """
        Obtém o status de todos os módulos.
        
        Returns:
            Lista com status de todos os módulos
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT nome_modulo, categoria, criticidade, status, progresso,
                           mensagem, timestamp_inicio, timestamp_fim, 
                           timestamp_atualizacao, dados_resultado, erro
                    FROM status_modulos 
                    ORDER BY categoria, nome_modulo
                """)
                
                modulos = []
                for row in cursor.fetchall():
                    modulos.append({
                        "nome_modulo": row[0],
                        "categoria": row[1],
                        "criticidade": row[2],
                        "status": row[3],
                        "progresso": row[4],
                        "mensagem": row[5],
                        "timestamp_inicio": row[6],
                        "timestamp_fim": row[7],
                        "timestamp_atualizacao": row[8],
                        "dados_resultado": json.loads(row[9]) if row[9] else None,
                        "erro": row[10]
                    })
                
                return modulos
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter status de todos os módulos: {e}")
            return []
    
    def obter_metricas_consolidadas(self, data_inicio: str = None, data_fim: str = None) -> Dict[str, Any]:
        """
        Obtém métricas consolidadas de execuções.
        
        Args:
            data_inicio: Data de início no formato YYYY-MM-DD
            data_fim: Data de fim no formato YYYY-MM-DD
            
        Returns:
            Dicionário com métricas consolidadas
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Query base
                where_clause = ""
                params = []
                
                if data_inicio and data_fim:
                    where_clause = "WHERE DATE(timestamp_execucao) BETWEEN ? AND ?"
                    params = [data_inicio, data_fim]
                elif data_inicio:
                    where_clause = "WHERE DATE(timestamp_execucao) >= ?"
                    params = [data_inicio]
                elif data_fim:
                    where_clause = "WHERE DATE(timestamp_execucao) <= ?"
                    params = [data_fim]
                
                # Métricas gerais
                cursor.execute(f"""
                    SELECT 
                        COUNT(*) as total_execucoes,
                        COUNT(CASE WHEN status = 'sucesso' THEN 1 END) as execucoes_sucesso,
                        COUNT(CASE WHEN status = 'erro' THEN 1 END) as execucoes_erro,
                        AVG(tempo_execucao) as tempo_medio_execucao,
                        AVG(taxa_sucesso) as taxa_sucesso_media,
                        SUM(registros_processados) as total_registros_processados
                    FROM historico_execucoes 
                    {where_clause}
                """, params)
                
                row = cursor.fetchone()
                
                # Métricas por categoria
                cursor.execute(f"""
                    SELECT 
                        sm.categoria,
                        COUNT(*) as execucoes,
                        COUNT(CASE WHEN he.status = 'sucesso' THEN 1 END) as sucessos,
                        AVG(he.tempo_execucao) as tempo_medio
                    FROM historico_execucoes he
                    JOIN status_modulos sm ON he.nome_modulo = sm.nome_modulo
                    {where_clause}
                    GROUP BY sm.categoria
                """, params)
                
                categorias = {}
                for cat_row in cursor.fetchall():
                    categorias[cat_row[0]] = {
                        "execucoes": cat_row[1],
                        "sucessos": cat_row[2],
                        "tempo_medio": cat_row[3] or 0
                    }
                
                return {
                    "periodo": {
                        "data_inicio": data_inicio,
                        "data_fim": data_fim
                    },
                    "geral": {
                        "total_execucoes": row[0] or 0,
                        "execucoes_sucesso": row[1] or 0,
                        "execucoes_erro": row[2] or 0,
                        "tempo_medio_execucao": row[3] or 0,
                        "taxa_sucesso_media": row[4] or 0,
                        "total_registros_processados": row[5] or 0
                    },
                    "por_categoria": categorias,
                    "timestamp_consulta": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter métricas: {e}")
            return {}
    
    def limpar_historico_antigo(self, dias_manter: int = 90) -> int:
        """
        Remove registros de histórico mais antigos que o especificado.
        
        Args:
            dias_manter: Número de dias de histórico para manter
            
        Returns:
            Número de registros removidos
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    DELETE FROM historico_execucoes 
                    WHERE timestamp_execucao < datetime('now', '-{} days')
                """.format(dias_manter))
                
                registros_removidos = cursor.rowcount
                conn.commit()
                
                self.logger.info(f"🧹 Histórico limpo: {registros_removidos} registros removidos")
                return registros_removidos
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao limpar histórico: {e}")
            return 0


class MapaCentralAPI:
    """
    API simples para comunicação com o mapa central.
    
    Esta classe fornece uma interface REST-like para que os módulos
    possam se comunicar com o sistema central.
    """
    
    def __init__(self):
        self.status_reporter = StatusReporter()
        self.logger = logging.getLogger("mapa_central_api")
    
    def registrar_modulo(self, nome: str, categoria: str, criticidade: str) -> bool:
        """
        Registra um novo módulo no sistema central.
        
        Args:
            nome: Nome do módulo
            categoria: Categoria do módulo
            criticidade: Criticidade do módulo
            
        Returns:
            True se registrado com sucesso
        """
        try:
            # Verificar se módulo já existe
            status_atual = self.status_reporter.obter_status_modulo(nome)
            
            if not status_atual:
                # Registrar novo módulo
                self.status_reporter.reportar_inicio(nome, categoria, criticidade)
                self.logger.info(f"📝 Módulo registrado: {nome}")
                return True
            else:
                self.logger.info(f"📝 Módulo já registrado: {nome}")
                return True
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao registrar módulo: {e}")
            return False
    
    def obter_dashboard_data(self) -> Dict[str, Any]:
        """
        Obtém dados consolidados para o dashboard.
        
        Returns:
            Dados formatados para o dashboard
        """
        try:
            # Status de todos os módulos
            modulos = self.status_reporter.obter_status_todos_modulos()
            
            # Métricas consolidadas
            metricas = self.status_reporter.obter_metricas_consolidadas()
            
            # Agrupar por categoria
            categorias = {}
            for modulo in modulos:
                categoria = modulo["categoria"]
                if categoria not in categorias:
                    categorias[categoria] = []
                categorias[categoria].append(modulo)
            
            # Estatísticas gerais
            total_modulos = len(modulos)
            modulos_sucesso = len([m for m in modulos if m["status"] == "sucesso"])
            modulos_erro = len([m for m in modulos if m["status"] == "erro"])
            modulos_executando = len([m for m in modulos if m["status"] == "executando"])
            
            return {
                "timestamp_atualizacao": datetime.now().isoformat(),
                "estatisticas": {
                    "total_modulos": total_modulos,
                    "modulos_sucesso": modulos_sucesso,
                    "modulos_erro": modulos_erro,
                    "modulos_executando": modulos_executando,
                    "taxa_sucesso": (modulos_sucesso / total_modulos * 100) if total_modulos > 0 else 0
                },
                "modulos_por_categoria": categorias,
                "metricas_historicas": metricas,
                "alertas": self._gerar_alertas(modulos)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao obter dados do dashboard: {e}")
            return {}
    
    def _gerar_alertas(self, modulos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Gera alertas baseados no status dos módulos.
        
        Args:
            modulos: Lista de módulos
            
        Returns:
            Lista de alertas
        """
        alertas = []
        
        for modulo in modulos:
            # Alertas para módulos com erro
            if modulo["status"] == "erro":
                alertas.append({
                    "tipo": "erro",
                    "criticidade": modulo["criticidade"],
                    "modulo": modulo["nome_modulo"],
                    "mensagem": f"Módulo {modulo['nome_modulo']} falhou: {modulo.get('erro', 'Erro desconhecido')}",
                    "timestamp": modulo["timestamp_atualizacao"]
                })
            
            # Alertas para módulos críticos parados há muito tempo
            if modulo["criticidade"] == "critica" and modulo["status"] != "executando":
                ultima_atualizacao = datetime.fromisoformat(modulo["timestamp_atualizacao"])
                if (datetime.now() - ultima_atualizacao).total_seconds() > 3600:  # 1 hora
                    alertas.append({
                        "tipo": "atencao",
                        "criticidade": "critica",
                        "modulo": modulo["nome_modulo"],
                        "mensagem": f"Módulo crítico {modulo['nome_modulo']} não executado há mais de 1 hora",
                        "timestamp": datetime.now().isoformat()
                    })
        
        return alertas

