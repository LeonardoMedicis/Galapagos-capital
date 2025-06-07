#!/usr/bin/env python3
"""
Mapa Central de Controle - Orquestrador de Conciliações

Este módulo serve como ponto central de controle para todos os módulos
de conciliação, fornecendo execução coordenada, monitoramento em tempo
real e consolidação de resultados.
"""

import argparse
import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import importlib.util
import subprocess

# Configurar path para imports
sys.path.append(str(Path(__file__).parent))

from shared.status_reporter import StatusReporter, MapaCentralAPI
from shared.base_conciliacao import BaseConciliacao


class MapaCentral:
    """
    Classe principal do mapa central de controle.
    
    Attributes:
        config (dict): Configurações globais
        status_reporter (StatusReporter): Reporter de status
        api (MapaCentralAPI): API para comunicação
        logger (logging.Logger): Logger principal
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        Inicializa o mapa central.
        
        Args:
            config_path: Caminho para arquivo de configuração
        """
        self.config = self._carregar_configuracao(config_path)
        self.status_reporter = StatusReporter()
        self.api = MapaCentralAPI()
        self.logger = self._configurar_logger()
        
        self.logger.info("🗺️ Mapa Central de Controle inicializado")
    
    def _configurar_logger(self) -> logging.Logger:
        """
        Configura logger principal do mapa central.
        
        Returns:
            Logger configurado
        """
        logger = logging.getLogger("mapa_central")
        
        if not logger.handlers:
            # Handler para arquivo
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(
                log_dir / "mapa_central.log",
                encoding='utf-8'
            )
            
            # Handler para console
            console_handler = logging.StreamHandler()
            
            # Formato
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            logger.setLevel(logging.INFO)
        
        return logger
    
    def _carregar_configuracao(self, config_path: str) -> Dict[str, Any]:
        """
        Carrega configurações globais.
        
        Args:
            config_path: Caminho para arquivo de configuração
            
        Returns:
            Configurações carregadas
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"⚠️ Erro ao carregar configuração: {e}")
            return self._configuracao_padrao()
    
    def _configuracao_padrao(self) -> Dict[str, Any]:
        """
        Retorna configuração padrão.
        
        Returns:
            Configuração padrão
        """
        return {
            "configuracao": {
                "timeout_execucao": 300,
                "max_execucoes_paralelas": 3,
                "retry_attempts": 2
            },
            "conciliacoes": {}
        }
    
    def descobrir_modulos(self) -> List[Dict[str, Any]]:
        """
        Descobre automaticamente todos os módulos de conciliação disponíveis.
        
        Returns:
            Lista de módulos descobertos
        """
        modulos = []
        conciliacoes_dir = Path("../conciliacoes")
        
        if not conciliacoes_dir.exists():
            self.logger.warning("📁 Diretório de conciliações não encontrado")
            return modulos
        
        for modulo_dir in conciliacoes_dir.iterdir():
            if modulo_dir.is_dir() and not modulo_dir.name.startswith('.'):
                # Verificar se tem arquivo conciliacao.py
                arquivo_conciliacao = modulo_dir / "conciliacao.py"
                config_modulo = modulo_dir / "config.json"
                
                if arquivo_conciliacao.exists():
                    # Carregar configuração do módulo se existir
                    config = {}
                    if config_modulo.exists():
                        try:
                            with open(config_modulo, 'r', encoding='utf-8') as f:
                                config = json.load(f)
                        except Exception as e:
                            self.logger.warning(f"⚠️ Erro ao carregar config de {modulo_dir.name}: {e}")
                    
                    modulos.append({
                        "nome": modulo_dir.name,
                        "caminho": str(arquivo_conciliacao),
                        "diretorio": str(modulo_dir),
                        "categoria": config.get("modulo", {}).get("categoria", "outras"),
                        "criticidade": config.get("modulo", {}).get("criticidade", "media"),
                        "config": config
                    })
        
        self.logger.info(f"🔍 Descobertos {len(modulos)} módulos de conciliação")
        return modulos
    
    async def executar_modulo(self, modulo: Dict[str, Any], data_referencia: Optional[str] = None) -> Dict[str, Any]:
        """
        Executa um módulo específico de conciliação.
        
        Args:
            modulo: Informações do módulo
            data_referencia: Data de referência para execução
            
        Returns:
            Resultados da execução
        """
        nome_modulo = modulo["nome"]
        
        try:
            self.logger.info(f"🚀 Iniciando execução: {nome_modulo}")
            
            # Registrar módulo no sistema central
            self.api.registrar_modulo(
                nome_modulo,
                modulo["categoria"],
                modulo["criticidade"]
            )
            
            # Reportar início
            self.status_reporter.reportar_inicio(
                nome_modulo,
                modulo["categoria"],
                modulo["criticidade"]
            )
            
            # Executar módulo via subprocess para isolamento
            cmd = [
                sys.executable,
                modulo["caminho"]
            ]
            
            if data_referencia:
                cmd.extend(["--data", data_referencia])
            
            # Executar com timeout
            timeout = self.config.get("configuracao", {}).get("timeout_execucao", 300)
            
            processo = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=modulo["diretorio"],
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    processo.communicate(),
                    timeout=timeout
                )
                
                if processo.returncode == 0:
                    # Sucesso
                    resultado = {
                        "status": "sucesso",
                        "modulo": nome_modulo,
                        "stdout": stdout.decode('utf-8'),
                        "stderr": stderr.decode('utf-8'),
                        "codigo_saida": processo.returncode,
                        "data_referencia": data_referencia or datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    self.status_reporter.reportar_sucesso(nome_modulo, resultado)
                    self.logger.info(f"✅ Sucesso: {nome_modulo}")
                    
                else:
                    # Erro
                    erro = stderr.decode('utf-8') or "Erro desconhecido"
                    self.status_reporter.reportar_erro(nome_modulo, erro)
                    self.logger.error(f"❌ Erro: {nome_modulo} - {erro}")
                    
                    resultado = {
                        "status": "erro",
                        "modulo": nome_modulo,
                        "erro": erro,
                        "codigo_saida": processo.returncode
                    }
                
                return resultado
                
            except asyncio.TimeoutError:
                # Timeout
                processo.kill()
                erro = f"Timeout após {timeout} segundos"
                self.status_reporter.reportar_erro(nome_modulo, erro)
                self.logger.error(f"⏰ Timeout: {nome_modulo}")
                
                return {
                    "status": "timeout",
                    "modulo": nome_modulo,
                    "erro": erro
                }
                
        except Exception as e:
            erro = f"Erro na execução: {str(e)}"
            self.status_reporter.reportar_erro(nome_modulo, erro)
            self.logger.error(f"❌ Erro: {nome_modulo} - {erro}")
            
            return {
                "status": "erro",
                "modulo": nome_modulo,
                "erro": erro
            }
    
    async def executar_todos_modulos(self, data_referencia: Optional[str] = None) -> Dict[str, Any]:
        """
        Executa todos os módulos de conciliação.
        
        Args:
            data_referencia: Data de referência para execução
            
        Returns:
            Resultados consolidados
        """
        self.logger.info("🚀 Iniciando execução de todos os módulos")
        
        modulos = self.descobrir_modulos()
        if not modulos:
            self.logger.warning("⚠️ Nenhum módulo encontrado")
            return {"status": "erro", "mensagem": "Nenhum módulo encontrado"}
        
        # Configurar limite de execuções paralelas
        max_paralelas = self.config.get("configuracao", {}).get("max_execucoes_paralelas", 3)
        semaforo = asyncio.Semaphore(max_paralelas)
        
        async def executar_com_semaforo(modulo):
            async with semaforo:
                return await self.executar_modulo(modulo, data_referencia)
        
        # Executar módulos
        inicio = datetime.now()
        tarefas = [executar_com_semaforo(modulo) for modulo in modulos]
        resultados = await asyncio.gather(*tarefas, return_exceptions=True)
        fim = datetime.now()
        
        # Consolidar resultados
        sucessos = 0
        erros = 0
        timeouts = 0
        
        for resultado in resultados:
            if isinstance(resultado, Exception):
                erros += 1
            elif resultado.get("status") == "sucesso":
                sucessos += 1
            elif resultado.get("status") == "timeout":
                timeouts += 1
            else:
                erros += 1
        
        consolidado = {
            "timestamp_execucao": inicio.isoformat(),
            "tempo_total_execucao": (fim - inicio).total_seconds(),
            "total_modulos": len(modulos),
            "sucessos": sucessos,
            "erros": erros,
            "timeouts": timeouts,
            "taxa_sucesso": (sucessos / len(modulos) * 100) if modulos else 0,
            "resultados_detalhados": resultados,
            "data_referencia": data_referencia or datetime.now().strftime("%Y-%m-%d")
        }
        
        self.logger.info(f"📊 Execução concluída: {sucessos}/{len(modulos)} sucessos em {consolidado['tempo_total_execucao']:.1f}s")
        
        return consolidado
    
    async def executar_por_categoria(self, categoria: str, data_referencia: Optional[str] = None) -> Dict[str, Any]:
        """
        Executa módulos de uma categoria específica.
        
        Args:
            categoria: Categoria dos módulos (rentabilidade, impostos, outras)
            data_referencia: Data de referência para execução
            
        Returns:
            Resultados da categoria
        """
        self.logger.info(f"🚀 Executando categoria: {categoria}")
        
        modulos = self.descobrir_modulos()
        modulos_categoria = [m for m in modulos if m["categoria"] == categoria]
        
        if not modulos_categoria:
            self.logger.warning(f"⚠️ Nenhum módulo encontrado para categoria: {categoria}")
            return {"status": "erro", "mensagem": f"Nenhum módulo encontrado para categoria: {categoria}"}
        
        # Executar módulos da categoria
        resultados = []
        for modulo in modulos_categoria:
            resultado = await self.executar_modulo(modulo, data_referencia)
            resultados.append(resultado)
        
        # Consolidar resultados
        sucessos = len([r for r in resultados if r.get("status") == "sucesso"])
        
        return {
            "categoria": categoria,
            "total_modulos": len(modulos_categoria),
            "sucessos": sucessos,
            "taxa_sucesso": (sucessos / len(modulos_categoria) * 100) if modulos_categoria else 0,
            "resultados": resultados,
            "data_referencia": data_referencia or datetime.now().strftime("%Y-%m-%d")
        }
    
    def gerar_relatorio_consolidado(self) -> str:
        """
        Gera relatório consolidado de todas as execuções.
        
        Returns:
            Caminho do arquivo de relatório gerado
        """
        try:
            # Obter dados do dashboard
            dados = self.api.obter_dashboard_data()
            
            # Criar diretório de relatórios
            relatorio_dir = Path("relatorios")
            relatorio_dir.mkdir(exist_ok=True)
            
            # Nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo_relatorio = relatorio_dir / f"relatorio_consolidado_{timestamp}.json"
            
            # Salvar relatório
            with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"📄 Relatório consolidado gerado: {arquivo_relatorio}")
            return str(arquivo_relatorio)
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao gerar relatório: {e}")
            raise
    
    def obter_status_dashboard(self) -> Dict[str, Any]:
        """
        Obtém dados para o dashboard em tempo real.
        
        Returns:
            Dados formatados para dashboard
        """
        return self.api.obter_dashboard_data()


async def main():
    """Função principal do mapa central."""
    parser = argparse.ArgumentParser(
        description="Mapa Central de Controle - Galapagos DTVM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python mapa_central.py --all                           # Executar todos os módulos
  python mapa_central.py --categoria rentabilidade       # Executar categoria específica
  python mapa_central.py --modulos "Mod1,Mod2"          # Executar módulos específicos
  python mapa_central.py --status                       # Mostrar status atual
  python mapa_central.py --relatorio                    # Gerar relatório consolidado
        """
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Executar todos os módulos de conciliação'
    )
    
    parser.add_argument(
        '--categoria',
        type=str,
        choices=['rentabilidade', 'impostos', 'outras'],
        help='Executar módulos de categoria específica'
    )
    
    parser.add_argument(
        '--modulos',
        type=str,
        help='Lista de módulos específicos separados por vírgula'
    )
    
    parser.add_argument(
        '--data',
        type=str,
        help='Data de referência no formato YYYY-MM-DD'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Mostrar status atual de todos os módulos'
    )
    
    parser.add_argument(
        '--relatorio',
        action='store_true',
        help='Gerar relatório consolidado'
    )
    
    parser.add_argument(
        '--descobrir',
        action='store_true',
        help='Descobrir e listar módulos disponíveis'
    )
    
    args = parser.parse_args()
    
    # Inicializar mapa central
    mapa = MapaCentral()
    
    try:
        if args.descobrir:
            # Descobrir módulos
            modulos = mapa.descobrir_modulos()
            print(f"\n🔍 Módulos descobertos: {len(modulos)}")
            for modulo in modulos:
                print(f"  📦 {modulo['nome']} ({modulo['categoria']}) - {modulo['criticidade']}")
        
        elif args.status:
            # Mostrar status
            dados = mapa.obter_status_dashboard()
            print(f"\n📊 Status do Sistema:")
            print(f"  Total de módulos: {dados.get('estatisticas', {}).get('total_modulos', 0)}")
            print(f"  Sucessos: {dados.get('estatisticas', {}).get('modulos_sucesso', 0)}")
            print(f"  Erros: {dados.get('estatisticas', {}).get('modulos_erro', 0)}")
            print(f"  Executando: {dados.get('estatisticas', {}).get('modulos_executando', 0)}")
            print(f"  Taxa de sucesso: {dados.get('estatisticas', {}).get('taxa_sucesso', 0):.1f}%")
        
        elif args.relatorio:
            # Gerar relatório
            arquivo = mapa.gerar_relatorio_consolidado()
            print(f"\n📄 Relatório gerado: {arquivo}")
        
        elif args.all:
            # Executar todos
            resultado = await mapa.executar_todos_modulos(args.data)
            print(f"\n✅ Execução concluída:")
            print(f"  Sucessos: {resultado['sucessos']}/{resultado['total_modulos']}")
            print(f"  Taxa de sucesso: {resultado['taxa_sucesso']:.1f}%")
            print(f"  Tempo total: {resultado['tempo_total_execucao']:.1f}s")
        
        elif args.categoria:
            # Executar categoria
            resultado = await mapa.executar_por_categoria(args.categoria, args.data)
            print(f"\n✅ Categoria '{args.categoria}' executada:")
            print(f"  Sucessos: {resultado['sucessos']}/{resultado['total_modulos']}")
            print(f"  Taxa de sucesso: {resultado['taxa_sucesso']:.1f}%")
        
        elif args.modulos:
            # Executar módulos específicos
            nomes_modulos = [nome.strip() for nome in args.modulos.split(',')]
            modulos_disponiveis = mapa.descobrir_modulos()
            
            for nome in nomes_modulos:
                modulo = next((m for m in modulos_disponiveis if m['nome'] == nome), None)
                if modulo:
                    resultado = await mapa.executar_modulo(modulo, args.data)
                    status = "✅" if resultado.get("status") == "sucesso" else "❌"
                    print(f"{status} {nome}: {resultado.get('status', 'erro')}")
                else:
                    print(f"❌ Módulo não encontrado: {nome}")
        
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n⏹️ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

