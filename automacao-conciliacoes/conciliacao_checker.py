#!/usr/bin/env python3
"""
Sistema Automatizado de Verificação de Conciliações
Galapagos DTVM - Automação de Mapa de Conciliações

Autor: Sistema de Automação Galapagos
Data: Junho 2025
Versão: 1.0.0
"""

import os
import json
import logging
import smtplib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conciliacao_checker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ResultadoConciliacao:
    """Classe para armazenar resultado de uma verificação"""
    nome_arquivo: str
    caminho_completo: str
    existe: bool
    data_modificacao: Optional[datetime]
    tamanho_arquivo: Optional[int]
    criticidade: str
    categoria: str
    descricao: str
    timestamp_verificacao: datetime

class VerificadorConciliacao:
    """Classe principal para verificação de arquivos de conciliação"""
    
    def __init__(self, config_path: str = "config.json"):
        """Inicializa o verificador com arquivo de configuração"""
        self.config = self._carregar_configuracao(config_path)
        self.resultados: List[ResultadoConciliacao] = []
        self.data_execucao = datetime.now()
        
    def _carregar_configuracao(self, config_path: str) -> Dict:
        """Carrega configuração do arquivo JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"Configuração carregada de {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Arquivo de configuração não encontrado: {config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            raise
    
    def _gerar_nome_arquivo_com_data(self, template: str, data: datetime = None) -> str:
        """Gera nome do arquivo substituindo {data} pela data atual"""
        if data is None:
            data = self.data_execucao
            
        # Tenta diferentes formatos de data
        formatos = self.config.get('formatos_data', ['%Y%m%d'])
        
        for formato in formatos:
            data_formatada = data.strftime(formato)
            nome_arquivo = template.replace('{data}', data_formatada)
            
            # Se o template não contém {data}, retorna como está
            if '{data}' not in template:
                return template
                
            return nome_arquivo
        
        # Fallback para formato padrão
        data_formatada = data.strftime('%Y%m%d')
        return template.replace('{data}', data_formatada)
    
    def _verificar_arquivo(self, arquivo_config: Dict, categoria: str) -> ResultadoConciliacao:
        """Verifica se um arquivo específico existe"""
        nome_template = arquivo_config['nome']
        caminho_base = arquivo_config['caminho']
        
        # Gera nome do arquivo com data atual
        nome_arquivo = self._gerar_nome_arquivo_com_data(nome_template)
        caminho_completo = os.path.join(caminho_base, nome_arquivo)
        
        # Verifica existência do arquivo
        existe = os.path.exists(caminho_completo)
        data_modificacao = None
        tamanho_arquivo = None
        
        if existe:
            try:
                stat_info = os.stat(caminho_completo)
                data_modificacao = datetime.fromtimestamp(stat_info.st_mtime)
                tamanho_arquivo = stat_info.st_size
                logger.info(f"✅ Arquivo encontrado: {nome_arquivo}")
            except OSError as e:
                logger.warning(f"Erro ao obter informações do arquivo {nome_arquivo}: {e}")
        else:
            logger.warning(f"❌ Arquivo não encontrado: {nome_arquivo}")
        
        return ResultadoConciliacao(
            nome_arquivo=nome_arquivo,
            caminho_completo=caminho_completo,
            existe=existe,
            data_modificacao=data_modificacao,
            tamanho_arquivo=tamanho_arquivo,
            criticidade=arquivo_config.get('criticidade', 'media'),
            categoria=categoria,
            descricao=arquivo_config.get('descricao', ''),
            timestamp_verificacao=datetime.now()
        )
    
    def executar_verificacao(self) -> List[ResultadoConciliacao]:
        """Executa verificação completa de todas as conciliações"""
        logger.info("🚀 Iniciando verificação de conciliações...")
        logger.info(f"📅 Data de execução: {self.data_execucao.strftime('%d/%m/%Y %H:%M:%S')}")
        
        self.resultados = []
        
        # Processa cada categoria de conciliação
        conciliacoes = self.config.get('conciliacoes', {})
        
        for categoria, config_categoria in conciliacoes.items():
            logger.info(f"📂 Processando categoria: {categoria.upper()}")
            
            arquivos = config_categoria.get('arquivos', [])
            for arquivo_config in arquivos:
                resultado = self._verificar_arquivo(arquivo_config, categoria)
                self.resultados.append(resultado)
        
        # Gera estatísticas
        total_arquivos = len(self.resultados)
        arquivos_encontrados = sum(1 for r in self.resultados if r.existe)
        arquivos_faltando = total_arquivos - arquivos_encontrados
        
        logger.info(f"📊 Verificação concluída:")
        logger.info(f"   Total de arquivos: {total_arquivos}")
        logger.info(f"   Encontrados: {arquivos_encontrados}")
        logger.info(f"   Faltando: {arquivos_faltando}")
        
        return self.resultados
    
    def gerar_relatorio_json(self, arquivo_saida: str = "resultado_conciliacao.json") -> str:
        """Gera relatório em formato JSON"""
        relatorio = {
            "timestamp_execucao": self.data_execucao.isoformat(),
            "total_arquivos": len(self.resultados),
            "arquivos_encontrados": sum(1 for r in self.resultados if r.existe),
            "arquivos_faltando": sum(1 for r in self.resultados if not r.existe),
            "resultados": [asdict(resultado) for resultado in self.resultados]
        }
        
        # Converte datetime para string no JSON
        for resultado in relatorio["resultados"]:
            if resultado["data_modificacao"]:
                resultado["data_modificacao"] = resultado["data_modificacao"].isoformat()
            resultado["timestamp_verificacao"] = resultado["timestamp_verificacao"].isoformat()
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 Relatório JSON salvo em: {arquivo_saida}")
        return arquivo_saida
    
    def gerar_relatorio_html(self, arquivo_saida: str = "relatorio_conciliacao.html") -> str:
        """Gera relatório em formato HTML"""
        
        # Estatísticas gerais
        total = len(self.resultados)
        encontrados = sum(1 for r in self.resultados if r.existe)
        faltando = total - encontrados
        percentual_sucesso = (encontrados / total * 100) if total > 0 else 0
        
        # Agrupa por categoria
        categorias = {}
        for resultado in self.resultados:
            if resultado.categoria not in categorias:
                categorias[resultado.categoria] = []
            categorias[resultado.categoria].append(resultado)
        
        html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Conciliações - Galapagos DTVM</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ color: #2c3e50; margin-bottom: 10px; }}
        .header .timestamp {{ color: #7f8c8d; font-size: 14px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-card.success {{ background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); }}
        .stat-card.warning {{ background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); }}
        .stat-card.error {{ background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%); }}
        .stat-number {{ font-size: 2em; font-weight: bold; margin-bottom: 5px; }}
        .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
        .category {{ margin-bottom: 30px; }}
        .category h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .file-grid {{ display: grid; gap: 15px; }}
        .file-item {{ background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; }}
        .file-item.found {{ border-left: 4px solid #28a745; }}
        .file-item.missing {{ border-left: 4px solid #dc3545; }}
        .file-name {{ font-weight: bold; color: #2c3e50; margin-bottom: 5px; }}
        .file-path {{ font-size: 0.85em; color: #6c757d; margin-bottom: 10px; word-break: break-all; }}
        .file-details {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; font-size: 0.85em; }}
        .detail-item {{ display: flex; justify-content: space-between; }}
        .status {{ padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }}
        .status.found {{ background: #d4edda; color: #155724; }}
        .status.missing {{ background: #f8d7da; color: #721c24; }}
        .criticidade {{ padding: 2px 6px; border-radius: 3px; font-size: 0.75em; }}
        .criticidade.critica {{ background: #dc3545; color: white; }}
        .criticidade.alta {{ background: #fd7e14; color: white; }}
        .criticidade.media {{ background: #ffc107; color: #212529; }}
        .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Relatório de Conciliações</h1>
            <div class="timestamp">Galapagos DTVM - {self.data_execucao.strftime('%d/%m/%Y às %H:%M:%S')}</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total}</div>
                <div class="stat-label">Total de Arquivos</div>
            </div>
            <div class="stat-card success">
                <div class="stat-number">{encontrados}</div>
                <div class="stat-label">Encontrados</div>
            </div>
            <div class="stat-card error">
                <div class="stat-number">{faltando}</div>
                <div class="stat-label">Faltando</div>
            </div>
            <div class="stat-card {'success' if percentual_sucesso >= 90 else 'warning' if percentual_sucesso >= 70 else 'error'}">
                <div class="stat-number">{percentual_sucesso:.1f}%</div>
                <div class="stat-label">Taxa de Sucesso</div>
            </div>
        </div>
"""
        
        # Adiciona seções por categoria
        for categoria, resultados_categoria in categorias.items():
            html_content += f"""
        <div class="category">
            <h2>📁 {categoria.title()}</h2>
            <div class="file-grid">
"""
            
            for resultado in resultados_categoria:
                status_class = "found" if resultado.existe else "missing"
                status_text = "Encontrado" if resultado.existe else "Não Encontrado"
                
                data_mod = ""
                tamanho = ""
                if resultado.existe and resultado.data_modificacao:
                    data_mod = resultado.data_modificacao.strftime('%d/%m/%Y %H:%M:%S')
                    if resultado.tamanho_arquivo:
                        tamanho = f"{resultado.tamanho_arquivo:,} bytes".replace(',', '.')
                
                html_content += f"""
                <div class="file-item {status_class}">
                    <div class="file-name">{resultado.nome_arquivo}</div>
                    <div class="file-path">{resultado.caminho_completo}</div>
                    <div class="file-details">
                        <div class="detail-item">
                            <span>Status:</span>
                            <span class="status {status_class}">{status_text}</span>
                        </div>
                        <div class="detail-item">
                            <span>Criticidade:</span>
                            <span class="criticidade {resultado.criticidade}">{resultado.criticidade.upper()}</span>
                        </div>
                        {f'<div class="detail-item"><span>Modificado:</span><span>{data_mod}</span></div>' if data_mod else ''}
                        {f'<div class="detail-item"><span>Tamanho:</span><span>{tamanho}</span></div>' if tamanho else ''}
                    </div>
                </div>
"""
            
            html_content += """
            </div>
        </div>
"""
        
        html_content += f"""
        <div class="footer">
            <p>Sistema Automatizado de Conciliações - Galapagos DTVM</p>
            <p>Gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"📄 Relatório HTML salvo em: {arquivo_saida}")
        return arquivo_saida
    
    def identificar_problemas_criticos(self) -> List[ResultadoConciliacao]:
        """Identifica arquivos críticos que estão faltando"""
        problemas_criticos = [
            r for r in self.resultados 
            if not r.existe and r.criticidade in ['critica', 'alta']
        ]
        
        if problemas_criticos:
            logger.warning(f"🚨 {len(problemas_criticos)} problemas críticos identificados!")
            for problema in problemas_criticos:
                logger.warning(f"   - {problema.nome_arquivo} ({problema.criticidade})")
        
        return problemas_criticos

def main():
    """Função principal"""
    try:
        # Inicializa verificador
        verificador = VerificadorConciliacao()
        
        # Executa verificação
        resultados = verificador.executar_verificacao()
        
        # Gera relatórios
        verificador.gerar_relatorio_json()
        verificador.gerar_relatorio_html()
        
        # Verifica problemas críticos
        problemas_criticos = verificador.identificar_problemas_criticos()
        
        # Define código de saída baseado nos resultados
        if problemas_criticos:
            logger.error("❌ Verificação concluída com problemas críticos")
            return 1
        else:
            logger.info("✅ Verificação concluída com sucesso")
            return 0
            
    except Exception as e:
        logger.error(f"💥 Erro durante execução: {e}")
        return 1

if __name__ == "__main__":
    exit(main())

