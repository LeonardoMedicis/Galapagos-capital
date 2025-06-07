#!/usr/bin/env python3
"""
Classe base para todos os módulos de conciliação.

Esta classe fornece a estrutura padrão que todos os módulos de conciliação
devem seguir, garantindo consistência e facilitando a integração com o
mapa central de controle.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging
import json
import os
from pathlib import Path


class BaseConciliacao(ABC):
    """
    Classe base abstrata para todos os módulos de conciliação.
    
    Attributes:
        nome (str): Nome único do módulo de conciliação
        categoria (str): Categoria da conciliação (rentabilidade, impostos, outras)
        criticidade (str): Nível de criticidade (critica, alta, media)
        logger (logging.Logger): Logger específico do módulo
        config (dict): Configurações específicas do módulo
    """
    
    def __init__(self, nome: str, categoria: str, criticidade: str):
        """
        Inicializa a classe base de conciliação.
        
        Args:
            nome: Nome único do módulo
            categoria: Categoria da conciliação
            criticidade: Nível de criticidade
        """
        self.nome = nome
        self.categoria = categoria
        self.criticidade = criticidade
        self.logger = self._configurar_logger()
        self.config = self._carregar_configuracao()
        
        self.logger.info(f"🚀 Inicializando módulo: {self.nome}")
    
    def _configurar_logger(self) -> logging.Logger:
        """
        Configura logger específico para o módulo.
        
        Returns:
            Logger configurado
        """
        logger = logging.getLogger(f"conciliacao.{self.nome}")
        
        if not logger.handlers:
            # Configurar handler para arquivo
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(
                log_dir / f"{self.nome}.log",
                encoding='utf-8'
            )
            
            # Configurar handler para console
            console_handler = logging.StreamHandler()
            
            # Configurar formato
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            logger.setLevel(logging.INFO)
        
        return logger
    
    def _carregar_configuracao(self) -> Dict[str, Any]:
        """
        Carrega configurações específicas do módulo.
        
        Returns:
            Dicionário com configurações
        """
        config_path = Path("config.json")
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"✅ Configuração carregada: {config_path}")
                return config
            except Exception as e:
                self.logger.warning(f"⚠️ Erro ao carregar configuração: {e}")
                return self._configuracao_padrao()
        else:
            self.logger.info("📋 Usando configuração padrão")
            return self._configuracao_padrao()
    
    def _configuracao_padrao(self) -> Dict[str, Any]:
        """
        Retorna configuração padrão para o módulo.
        
        Returns:
            Configuração padrão
        """
        return {
            "modulo": {
                "nome": self.nome,
                "categoria": self.categoria,
                "criticidade": self.criticidade,
                "versao": "1.0.0"
            },
            "execucao": {
                "timeout": 300,
                "retry_attempts": 3,
                "retry_delay": 5
            },
            "validacoes": {
                "tolerancia_percentual": 0.01,
                "verificar_duplicatas": True,
                "validar_datas": True
            },
            "saida": {
                "gerar_relatorio": True,
                "salvar_historico": True,
                "reportar_status_central": True
            }
        }
    
    @abstractmethod
    def executar_conciliacao(self, data_referencia: Optional[str] = None) -> Dict[str, Any]:
        """
        Método abstrato para executar a conciliação específica.
        
        Args:
            data_referencia: Data de referência no formato YYYY-MM-DD
            
        Returns:
            Dicionário com resultados da conciliação
            
        Raises:
            NotImplementedError: Se não implementado na classe filha
        """
        pass
    
    @abstractmethod
    def _carregar_dados(self, data_referencia: str) -> Dict[str, Any]:
        """
        Método abstrato para carregar dados específicos do módulo.
        
        Args:
            data_referencia: Data de referência
            
        Returns:
            Dados carregados
        """
        pass
    
    @abstractmethod
    def _executar_validacoes(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método abstrato para executar validações específicas.
        
        Args:
            dados: Dados a serem validados
            
        Returns:
            Resultados das validações
        """
        pass
    
    def _gerar_relatorio(self, resultados: Dict[str, Any]) -> str:
        """
        Gera relatório padrão dos resultados.
        
        Args:
            resultados: Resultados da conciliação
            
        Returns:
            Caminho do arquivo de relatório gerado
        """
        try:
            # Criar diretório de relatórios
            relatorio_dir = Path("relatorios")
            relatorio_dir.mkdir(exist_ok=True)
            
            # Nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_relatorio = relatorio_dir / f"{self.nome}_{timestamp}.json"
            
            # Dados do relatório
            relatorio_data = {
                "modulo": self.nome,
                "categoria": self.categoria,
                "criticidade": self.criticidade,
                "timestamp_execucao": datetime.now().isoformat(),
                "resultados": resultados,
                "configuracao": self.config
            }
            
            # Salvar relatório
            with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
                json.dump(relatorio_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"📄 Relatório gerado: {arquivo_relatorio}")
            return str(arquivo_relatorio)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao gerar relatório: {e}")
            raise
    
    def _validar_data_referencia(self, data_referencia: Optional[str]) -> str:
        """
        Valida e formata data de referência.
        
        Args:
            data_referencia: Data no formato YYYY-MM-DD ou None
            
        Returns:
            Data formatada
            
        Raises:
            ValueError: Se data estiver em formato inválido
        """
        if data_referencia is None:
            data_referencia = datetime.now().strftime("%Y-%m-%d")
            self.logger.info(f"📅 Usando data atual: {data_referencia}")
        else:
            try:
                # Validar formato da data
                datetime.strptime(data_referencia, "%Y-%m-%d")
                self.logger.info(f"📅 Data de referência: {data_referencia}")
            except ValueError:
                raise ValueError(f"Formato de data inválido: {data_referencia}. Use YYYY-MM-DD")
        
        return data_referencia
    
    def _salvar_historico(self, resultados: Dict[str, Any]) -> None:
        """
        Salva histórico da execução.
        
        Args:
            resultados: Resultados da execução
        """
        try:
            # Criar diretório de histórico
            historico_dir = Path("dados/historico")
            historico_dir.mkdir(parents=True, exist_ok=True)
            
            # Nome do arquivo com data
            data_execucao = datetime.now().strftime("%Y%m%d")
            arquivo_historico = historico_dir / f"{self.nome}_{data_execucao}.json"
            
            # Dados do histórico
            historico_data = {
                "modulo": self.nome,
                "timestamp": datetime.now().isoformat(),
                "resultados": resultados
            }
            
            # Salvar histórico
            with open(arquivo_historico, 'w', encoding='utf-8') as f:
                json.dump(historico_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"💾 Histórico salvo: {arquivo_historico}")
            
        except Exception as e:
            self.logger.warning(f"⚠️ Erro ao salvar histórico: {e}")
    
    def obter_status(self) -> Dict[str, Any]:
        """
        Retorna status atual do módulo.
        
        Returns:
            Dicionário com status do módulo
        """
        return {
            "nome": self.nome,
            "categoria": self.categoria,
            "criticidade": self.criticidade,
            "status": "pronto",
            "ultima_execucao": None,
            "configuracao": self.config.get("modulo", {})
        }
    
    def validar_pre_requisitos(self) -> bool:
        """
        Valida se todos os pré-requisitos estão atendidos.
        
        Returns:
            True se todos os pré-requisitos estão OK
        """
        try:
            # Verificar configuração
            if not self.config:
                self.logger.error("❌ Configuração não carregada")
                return False
            
            # Verificar diretórios necessários
            diretorios = ["dados", "logs", "relatorios"]
            for diretorio in diretorios:
                Path(diretorio).mkdir(exist_ok=True)
            
            self.logger.info("✅ Pré-requisitos validados")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erro na validação de pré-requisitos: {e}")
            return False


class ConciliacaoTemplate(BaseConciliacao):
    """
    Template de exemplo para implementação de novos módulos.
    
    Esta classe serve como exemplo de como implementar um novo módulo
    de conciliação seguindo os padrões estabelecidos.
    """
    
    def __init__(self, nome: str, categoria: str, criticidade: str):
        super().__init__(nome, categoria, criticidade)
    
    def executar_conciliacao(self, data_referencia: Optional[str] = None) -> Dict[str, Any]:
        """
        Implementação exemplo de execução de conciliação.
        
        Args:
            data_referencia: Data de referência
            
        Returns:
            Resultados da conciliação
        """
        try:
            # 1. Validar pré-requisitos
            if not self.validar_pre_requisitos():
                raise RuntimeError("Pré-requisitos não atendidos")
            
            # 2. Validar data de referência
            data_ref = self._validar_data_referencia(data_referencia)
            
            # 3. Carregar dados
            self.logger.info("📊 Carregando dados...")
            dados = self._carregar_dados(data_ref)
            
            # 4. Executar validações
            self.logger.info("🔍 Executando validações...")
            resultados = self._executar_validacoes(dados)
            
            # 5. Gerar relatório
            if self.config.get("saida", {}).get("gerar_relatorio", True):
                self.logger.info("📄 Gerando relatório...")
                self._gerar_relatorio(resultados)
            
            # 6. Salvar histórico
            if self.config.get("saida", {}).get("salvar_historico", True):
                self._salvar_historico(resultados)
            
            self.logger.info("✅ Conciliação executada com sucesso")
            return resultados
            
        except Exception as e:
            self.logger.error(f"❌ Erro na execução: {e}")
            raise
    
    def _carregar_dados(self, data_referencia: str) -> Dict[str, Any]:
        """
        Implementação exemplo de carregamento de dados.
        
        Args:
            data_referencia: Data de referência
            
        Returns:
            Dados carregados
        """
        # TODO: Implementar carregamento específico
        self.logger.info(f"📁 Carregando dados para {data_referencia}")
        
        # Exemplo de estrutura de dados
        return {
            "data_referencia": data_referencia,
            "registros": [],
            "metadados": {
                "total_registros": 0,
                "fonte": "sistema_exemplo"
            }
        }
    
    def _executar_validacoes(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Implementação exemplo de validações.
        
        Args:
            dados: Dados a serem validados
            
        Returns:
            Resultados das validações
        """
        # TODO: Implementar validações específicas
        self.logger.info("🔍 Executando validações básicas")
        
        # Exemplo de estrutura de resultados
        return {
            "status": "sucesso",
            "total_registros": dados.get("metadados", {}).get("total_registros", 0),
            "registros_validos": 0,
            "registros_invalidos": 0,
            "erros": [],
            "alertas": [],
            "metricas": {
                "tempo_execucao": 0,
                "taxa_sucesso": 100.0
            }
        }

