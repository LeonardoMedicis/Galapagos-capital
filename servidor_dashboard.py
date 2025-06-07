#!/usr/bin/env python3
"""
Servidor Dashboard Simples - Galapagos DTVM

Este script cria um servidor web simples que serve o dashboard
sem necessidade de Node.js ou outras dependências externas.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import json
from datetime import datetime
from pathlib import Path
import threading
import time


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Handler customizado para servir o dashboard."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def end_headers(self):
        # Adicionar headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            # Redirecionar para dashboard
            self.path = '/dashboard_simples.html'
        elif self.path == '/api/status':
            # API simples para status
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status_data = {
                "timestamp": datetime.now().isoformat(),
                "total_modulos": 9,
                "modulos_implementados": 0,
                "modulos_desenvolvimento": 9,
                "taxa_sucesso": 0,
                "status": "desenvolvimento",
                "modulos": [
                    {"nome": "Rentabilidade_Carteira_A", "categoria": "rentabilidade", "status": "desenvolvimento"},
                    {"nome": "Rentabilidade_Carteira_B", "categoria": "rentabilidade", "status": "desenvolvimento"},
                    {"nome": "Rentabilidade_Consolidada", "categoria": "rentabilidade", "status": "desenvolvimento"},
                    {"nome": "IR_Retido_Fonte", "categoria": "impostos", "status": "desenvolvimento"},
                    {"nome": "IOF_Operacoes", "categoria": "impostos", "status": "desenvolvimento"},
                    {"nome": "PIS_COFINS", "categoria": "impostos", "status": "desenvolvimento"},
                    {"nome": "Custodia_Titulos", "categoria": "outras", "status": "desenvolvimento"},
                    {"nome": "Liquidacao_D0", "categoria": "outras", "status": "desenvolvimento"},
                    {"nome": "Fechamento_Dia", "categoria": "outras", "status": "desenvolvimento"}
                ]
            }
            
            self.wfile.write(json.dumps(status_data, ensure_ascii=False, indent=2).encode('utf-8'))
            return
        
        # Servir arquivos normalmente
        super().do_GET()
    
    def log_message(self, format, *args):
        """Log customizado."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {format % args}")


def encontrar_porta_livre(porta_inicial=8000, max_tentativas=10):
    """Encontra uma porta livre para o servidor."""
    import socket
    
    for i in range(max_tentativas):
        porta = porta_inicial + i
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', porta))
                return porta
        except OSError:
            continue
    
    raise RuntimeError(f"Não foi possível encontrar uma porta livre entre {porta_inicial} e {porta_inicial + max_tentativas}")


def verificar_arquivos():
    """Verifica se os arquivos necessários existem."""
    arquivos_necessarios = [
        'dashboard_simples.html'
    ]
    
    for arquivo in arquivos_necessarios:
        if not Path(arquivo).exists():
            print(f"❌ Arquivo não encontrado: {arquivo}")
            return False
    
    print("✅ Todos os arquivos necessários encontrados")
    return True


def abrir_navegador(url, delay=2):
    """Abre o navegador após um delay."""
    time.sleep(delay)
    try:
        webbrowser.open(url)
        print(f"🌐 Abrindo navegador: {url}")
    except Exception as e:
        print(f"⚠️ Não foi possível abrir o navegador automaticamente: {e}")
        print(f"💡 Abra manualmente: {url}")


def main():
    """Função principal."""
    print("🚀 Iniciando Dashboard Simples - Galapagos DTVM")
    print("=" * 60)
    
    # Verificar arquivos
    if not verificar_arquivos():
        print("❌ Arquivos necessários não encontrados!")
        print("💡 Certifique-se de estar no diretório correto do repositório")
        sys.exit(1)
    
    try:
        # Encontrar porta livre
        porta = encontrar_porta_livre()
        print(f"🔍 Porta encontrada: {porta}")
        
        # Configurar servidor
        with socketserver.TCPServer(("", porta), DashboardHandler) as httpd:
            url = f"http://localhost:{porta}"
            
            print(f"✅ Servidor iniciado com sucesso!")
            print(f"🌐 Dashboard disponível em: {url}")
            print(f"📊 API de status: {url}/api/status")
            print("=" * 60)
            print("💡 Para parar o servidor: Pressione Ctrl+C")
            print("🔄 O dashboard atualiza automaticamente")
            print("=" * 60)
            
            # Abrir navegador em thread separada
            threading.Thread(
                target=abrir_navegador, 
                args=(url,), 
                daemon=True
            ).start()
            
            # Iniciar servidor
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n⏹️ Servidor parado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

