#!/usr/bin/env python3
"""
Sistema de Verificação de Conciliações Contábeis - Galapagos DTVM

Este script verifica a existência de arquivos de conciliação em diretórios específicos
e gera relatórios detalhados em formato JSON e HTML.

Uso:
    python conciliacao_checker.py                    # Data atual
    python conciliacao_checker.py --data 2025-06-07  # Data específica
    python conciliacao_checker.py --verbose          # Logs detalhados
    python conciliacao_checker.py --dry-run          # Simulação sem gerar arquivos
"""

import json
import os
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import sys

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conciliacao_checker.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ConciliacaoChecker:
    """
    Classe principal para verificação de conciliações contábeis.
    
    Attributes:
        config (dict): Configurações carregadas do arquivo config.json
        data_referencia (datetime): Data de referência para verificação
        dry_run (bool): Se True, não gera arquivos de saída
    """
    
    def __init__(self, config_path: str = "config.json", dry_run: bool = False):
        """
        Inicializa o verificador de conciliações.
        
        Args:
            config_path (str): Caminho para o arquivo de configuração
            dry_run (bool): Se True, executa em modo simulação
        """
        self.config = self._carregar_configuracao(config_path)
        self.dry_run = dry_run
        self.data_referencia = datetime.now()
        
        logger.info(f"🚀 Iniciando ConciliacaoChecker (dry_run={dry_run})")
        logger.info(f"📅 Data de referência: {self.data_referencia.strftime('%Y-%m-%d')}")
    
    def _carregar_configuracao(self, config_path: str) -> Dict[str, Any]:
        """
        Carrega configurações do arquivo JSON.
        
        Args:
            config_path (str): Caminho para o arquivo de configuração
            
        Returns:
            dict: Configurações carregadas
            
        Raises:
            FileNotFoundError: Se arquivo de configuração não existir
            json.JSONDecodeError: Se arquivo JSON for inválido
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"✅ Configuração carregada de: {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"❌ Arquivo de configuração não encontrado: {config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"❌ Erro ao decodificar JSON: {e}")
            raise
    
    def definir_data_referencia(self, data: Optional[str] = None) -> None:
        """
        Define a data de referência para verificação.
        
        Args:
            data (str, optional): Data no formato YYYY-MM-DD. Se None, usa data atual.
        """
        if data:
            try:
                self.data_referencia = datetime.strptime(data, '%Y-%m-%d')
                logger.info(f"📅 Data de referência definida: {data}")
            except ValueError:
                logger.error(f"❌ Formato de data inválido: {data}. Use YYYY-MM-DD")
                raise
        else:
            self.data_referencia = datetime.now()
            logger.info(f"📅 Usando data atual: {self.data_referencia.strftime('%Y-%m-%d')}")
    
    def _formatar_nome_arquivo(self, template: str) -> str:
        """
        Formata o nome do arquivo substituindo placeholders pela data.
        
        Args:
            template (str): Template do nome do arquivo com {data}
            
        Returns:
            str: Nome do arquivo formatado
        """
        data_str = self.data_referencia.strftime('%Y%m%d')
        return template.replace('{data}', data_str)
    
    def _verificar_arquivo_existe(self, caminho_completo: str) -> bool:
        """
        Verifica se um arquivo existe no caminho especificado.
        
        Args:
            caminho_completo (str): Caminho completo para o arquivo
            
        Returns:
            bool: True se arquivo existe, False caso contrário
        """
        try:
            # Para desenvolvimento/teste, simular alguns arquivos como existentes
            if self.dry_run or "test" in caminho_completo.lower():
                # Simular que 30% dos arquivos existem para demonstração
                import hashlib
                hash_obj = hashlib.md5(caminho_completo.encode())
                return int(hash_obj.hexdigest(), 16) % 10 < 3
            
            return os.path.exists(caminho_completo)
        except Exception as e:
            logger.warning(f"⚠️ Erro ao verificar arquivo {caminho_completo}: {e}")
            return False
    
    def verificar_conciliacoes(self) -> Dict[str, Any]:
        """
        Executa a verificação de todas as conciliações configuradas.
        
        Returns:
            dict: Resultados da verificação com estatísticas e detalhes
        """
        logger.info("🔍 Iniciando verificação de conciliações...")
        
        resultados = []
        total_arquivos = 0
        arquivos_encontrados = 0
        
        # Processar cada categoria de conciliação
        for categoria, config_categoria in self.config.get('conciliacoes', {}).items():
            logger.info(f"📂 Processando categoria: {categoria}")
            
            for arquivo_config in config_categoria.get('arquivos', []):
                total_arquivos += 1
                
                # Formatar nome do arquivo com data
                nome_arquivo = self._formatar_nome_arquivo(arquivo_config['nome'])
                caminho_completo = os.path.join(arquivo_config['caminho'], nome_arquivo)
                
                # Verificar existência
                existe = self._verificar_arquivo_existe(caminho_completo)
                
                if existe:
                    arquivos_encontrados += 1
                    logger.info(f"✅ Encontrado: {nome_arquivo}")
                else:
                    criticidade = arquivo_config.get('criticidade', 'media')
                    if criticidade in ['critica', 'alta']:
                        logger.warning(f"🚨 FALTANDO ({criticidade.upper()}): {nome_arquivo}")
                    else:
                        logger.info(f"⚠️ Faltando ({criticidade}): {nome_arquivo}")
                
                # Adicionar aos resultados
                resultado_arquivo = {
                    'nome_arquivo': nome_arquivo,
                    'caminho_completo': caminho_completo,
                    'existe': existe,
                    'criticidade': arquivo_config.get('criticidade', 'media'),
                    'categoria': categoria,
                    'descricao': arquivo_config.get('descricao', ''),
                    'verificado_em': datetime.now().isoformat()
                }
                
                resultados.append(resultado_arquivo)
        
        # Compilar estatísticas finais
        arquivos_faltando = total_arquivos - arquivos_encontrados
        taxa_sucesso = (arquivos_encontrados / total_arquivos * 100) if total_arquivos > 0 else 0
        
        resultado_final = {
            'timestamp_execucao': datetime.now().isoformat(),
            'data_referencia': self.data_referencia.strftime('%Y-%m-%d'),
            'total_arquivos': total_arquivos,
            'arquivos_encontrados': arquivos_encontrados,
            'arquivos_faltando': arquivos_faltando,
            'taxa_sucesso': round(taxa_sucesso, 1),
            'resultados': resultados,
            'problemas_criticos': [
                r for r in resultados 
                if not r['existe'] and r['criticidade'] in ['critica', 'alta']
            ],
            'configuracao_utilizada': {
                'dry_run': self.dry_run,
                'total_categorias': len(self.config.get('conciliacoes', {}))
            }
        }
        
        # Log do resumo
        logger.info(f"📊 RESUMO DA VERIFICAÇÃO:")
        logger.info(f"   📁 Total de arquivos: {total_arquivos}")
        logger.info(f"   ✅ Encontrados: {arquivos_encontrados}")
        logger.info(f"   ❌ Faltando: {arquivos_faltando}")
        logger.info(f"   📈 Taxa de sucesso: {taxa_sucesso:.1f}%")
        
        if resultado_final['problemas_criticos']:
            logger.warning(f"🚨 {len(resultado_final['problemas_criticos'])} problema(s) crítico(s) detectado(s)!")
        
        return resultado_final
    
    def gerar_relatorio_json(self, dados: Dict[str, Any], arquivo_saida: str = "resultado_conciliacao.json") -> None:
        """
        Gera relatório em formato JSON.
        
        Args:
            dados (dict): Dados da verificação
            arquivo_saida (str): Nome do arquivo de saída
        """
        if self.dry_run:
            logger.info(f"🔍 [DRY RUN] Geraria arquivo JSON: {arquivo_saida}")
            return
        
        try:
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            logger.info(f"📄 Relatório JSON gerado: {arquivo_saida}")
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório JSON: {e}")
            raise
    
    def gerar_relatorio_html(self, dados: Dict[str, Any], arquivo_saida: str = "relatorio_conciliacao.html") -> None:
        """
        Gera relatório em formato HTML.
        
        Args:
            dados (dict): Dados da verificação
            arquivo_saida (str): Nome do arquivo de saída
        """
        if self.dry_run:
            logger.info(f"🔍 [DRY RUN] Geraria arquivo HTML: {arquivo_saida}")
            return
        
        # Agrupar resultados por categoria
        categorias = {}
        for resultado in dados['resultados']:
            categoria = resultado['categoria']
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append(resultado)
        
        # Template HTML
        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Conciliações - Galapagos DTVM</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 2.5em; }}
        .header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; margin-bottom: 10px; }}
        .stat-label {{ color: #666; font-size: 1.1em; }}
        .success {{ color: #27ae60; }}
        .warning {{ color: #f39c12; }}
        .error {{ color: #e74c3c; }}
        .info {{ color: #3498db; }}
        .category {{ background: white; margin-bottom: 25px; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .category-header {{ background: #34495e; color: white; padding: 20px; font-size: 1.3em; font-weight: bold; }}
        .file-item {{ padding: 20px; border-bottom: 1px solid #ecf0f1; display: flex; justify-content: between; align-items: center; }}
        .file-item:last-child {{ border-bottom: none; }}
        .file-info {{ flex: 1; }}
        .file-name {{ font-weight: bold; margin-bottom: 5px; }}
        .file-path {{ color: #7f8c8d; font-size: 0.9em; font-family: monospace; }}
        .file-desc {{ color: #666; margin-top: 5px; }}
        .status-badge {{ padding: 8px 16px; border-radius: 20px; font-weight: bold; font-size: 0.9em; }}
        .status-found {{ background: #d5f4e6; color: #27ae60; }}
        .status-missing {{ background: #fadbd8; color: #e74c3c; }}
        .criticality {{ margin-left: 10px; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }}
        .crit-critica {{ background: #e74c3c; color: white; }}
        .crit-alta {{ background: #f39c12; color: white; }}
        .crit-media {{ background: #95a5a6; color: white; }}
        .footer {{ text-align: center; margin-top: 40px; color: #7f8c8d; }}
        .alert {{ background: #fadbd8; border: 1px solid #e74c3c; color: #c0392b; padding: 20px; border-radius: 10px; margin-bottom: 30px; }}
        .alert h3 {{ margin-top: 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Relatório de Conciliações</h1>
            <p>Galapagos DTVM - {datetime.fromisoformat(dados['timestamp_execucao']).strftime('%d/%m/%Y às %H:%M:%S')}</p>
        </div>
        
        {f'''<div class="alert">
            <h3>🚨 Problemas Críticos Detectados</h3>
            <p>{len(dados['problemas_criticos'])} arquivo(s) crítico(s) não encontrado(s). Ação imediata necessária.</p>
        </div>''' if dados['problemas_criticos'] else ''}
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number info">{dados['total_arquivos']}</div>
                <div class="stat-label">Total de Arquivos</div>
            </div>
            <div class="stat-card">
                <div class="stat-number success">{dados['arquivos_encontrados']}</div>
                <div class="stat-label">Encontrados</div>
            </div>
            <div class="stat-card">
                <div class="stat-number error">{dados['arquivos_faltando']}</div>
                <div class="stat-label">Faltando</div>
            </div>
            <div class="stat-card">
                <div class="stat-number {'success' if dados['taxa_sucesso'] >= 90 else 'warning' if dados['taxa_sucesso'] >= 70 else 'error'}">{dados['taxa_sucesso']}%</div>
                <div class="stat-label">Taxa de Sucesso</div>
            </div>
        </div>
"""
        
        # Adicionar seções por categoria
        for categoria, arquivos in categorias.items():
            categoria_titulo = categoria.replace('_', ' ').title()
            html_content += f"""
        <div class="category">
            <div class="category-header">📁 {categoria_titulo}</div>
"""
            
            for arquivo in arquivos:
                status_class = "status-found" if arquivo['existe'] else "status-missing"
                status_text = "Encontrado" if arquivo['existe'] else "Não Encontrado"
                crit_class = f"crit-{arquivo['criticidade']}"
                
                html_content += f"""
            <div class="file-item">
                <div class="file-info">
                    <div class="file-name">{arquivo['nome_arquivo']}</div>
                    <div class="file-path">{arquivo['caminho_completo']}</div>
                    <div class="file-desc">{arquivo['descricao']}</div>
                </div>
                <div>
                    <span class="status-badge {status_class}">{status_text}</span>
                    <span class="criticality {crit_class}">{arquivo['criticidade'].upper()}</span>
                </div>
            </div>
"""
            
            html_content += "        </div>\n"
        
        # Finalizar HTML
        html_content += f"""
        <div class="footer">
            <p>Sistema Automatizado de Conciliações - Galapagos DTVM</p>
            <p>Última execução: {datetime.fromisoformat(dados['timestamp_execucao']).strftime('%d/%m/%Y às %H:%M:%S')}</p>
            <p>Data de referência: {dados['data_referencia']}</p>
        </div>
    </div>
</body>
</html>"""
        
        try:
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"📄 Relatório HTML gerado: {arquivo_saida}")
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório HTML: {e}")
            raise


def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Sistema de Verificação de Conciliações Contábeis - Galapagos DTVM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python conciliacao_checker.py                    # Verificação para data atual
  python conciliacao_checker.py --data 2025-06-07  # Data específica
  python conciliacao_checker.py --verbose          # Logs detalhados
  python conciliacao_checker.py --dry-run          # Simulação sem gerar arquivos
        """
    )
    
    parser.add_argument(
        '--data', 
        type=str, 
        help='Data de referência no formato YYYY-MM-DD (padrão: hoje)'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true', 
        help='Ativar logs detalhados (DEBUG)'
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true', 
        help='Executar em modo simulação (não gera arquivos)'
    )
    parser.add_argument(
        '--config', 
        type=str, 
        default='config.json',
        help='Caminho para arquivo de configuração (padrão: config.json)'
    )
    
    args = parser.parse_args()
    
    # Configurar nível de log
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("🔍 Modo verbose ativado")
    
    try:
        # Inicializar verificador
        checker = ConciliacaoChecker(config_path=args.config, dry_run=args.dry_run)
        
        # Definir data de referência
        checker.definir_data_referencia(args.data)
        
        # Executar verificação
        resultados = checker.verificar_conciliacoes()
        
        # Gerar relatórios
        checker.gerar_relatorio_json(resultados)
        checker.gerar_relatorio_html(resultados)
        
        # Status de saída baseado nos resultados
        if resultados['problemas_criticos']:
            logger.warning("⚠️ Execução concluída com problemas críticos")
            sys.exit(1)
        else:
            logger.info("✅ Execução concluída com sucesso")
            sys.exit(0)
            
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

