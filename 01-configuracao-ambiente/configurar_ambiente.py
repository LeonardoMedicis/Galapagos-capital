#!/usr/bin/env python3
"""
Configuração Adaptável - Galapagos DTVM
Sistema que detecta automaticamente o ambiente e se adapta:
- Desenvolvimento: GitHub (dados locais)
- Produção: Pasta Colaborativa (dados compartilhados)
"""

import os
import sys
import platform
from pathlib import Path
import json
from datetime import datetime

class EnvironmentDetector:
    """Detecta automaticamente o ambiente de execução."""
    
    def __init__(self):
        self.system = platform.system()
        self.current_path = Path.cwd()
        self.environment = self._detect_environment()
        self.config = self._load_config()
    
    def _detect_environment(self):
        """Detecta se está em desenvolvimento (GitHub) ou produção (Pasta Colaborativa)."""
        
        # Verifica se está em pasta de rede (Windows)
        if self.system == "Windows":
            # Testa caminhos típicos de rede
            network_paths = [
                "\\\\servidor\\galapagos",
                "\\\\galapagos-srv\\conciliacoes", 
                "\\\\192.168.",
                "Z:\\",
                "Y:\\",
                "X:\\"
            ]
            
            current_str = str(self.current_path)
            for network_path in network_paths:
                if network_path in current_str:
                    return "production"
        
        # Verifica se está em pasta compartilhada (Linux/Mac)
        if "/mnt/" in str(self.current_path) or "/media/" in str(self.current_path):
            return "production"
        
        # Verifica se tem arquivo .git (desenvolvimento)
        if (self.current_path / ".git").exists():
            return "development"
        
        # Verifica se tem arquivo de produção
        if (self.current_path / ".production").exists():
            return "production"
        
        # Default: desenvolvimento
        return "development"
    
    def _load_config(self):
        """Carrega configuração baseada no ambiente."""
        
        if self.environment == "production":
            return self._production_config()
        else:
            return self._development_config()
    
    def _production_config(self):
        """Configuração para ambiente de produção (pasta colaborativa)."""
        base_path = self.current_path
        
        return {
            "environment": "production",
            "database": {
                "type": "sqlite",
                "path": str(base_path / "database" / "conciliacoes.db"),
                "shared": True
            },
            "paths": {
                "dados": str(base_path / "dados_conciliacoes"),
                "resultados": str(base_path / "resultados"),
                "logs": str(base_path / "logs"),
                "backup": str(base_path / "backup")
            },
            "features": {
                "real_time": True,
                "shared_execution": True,
                "auto_backup": True,
                "network_sync": False
            },
            "security": {
                "multi_user": True,
                "file_locking": True,
                "audit_log": True
            }
        }
    
    def _development_config(self):
        """Configuração para ambiente de desenvolvimento (GitHub)."""
        base_path = self.current_path
        
        return {
            "environment": "development", 
            "database": {
                "type": "sqlite",
                "path": str(base_path / "dashboard-python" / "database" / "conciliacoes.db"),
                "shared": False
            },
            "paths": {
                "dados": str(base_path / "dados_simulados"),
                "resultados": str(base_path / "resultados_teste"),
                "logs": str(base_path / "logs_dev"),
                "backup": str(base_path / "backup_dev")
            },
            "features": {
                "real_time": True,
                "shared_execution": False,
                "auto_backup": False,
                "network_sync": True
            },
            "security": {
                "multi_user": False,
                "file_locking": False,
                "audit_log": False
            }
        }
    
    def create_directories(self):
        """Cria diretórios necessários baseado na configuração."""
        paths = self.config["paths"]
        
        for path_name, path_value in paths.items():
            path_obj = Path(path_value)
            path_obj.mkdir(parents=True, exist_ok=True)
            print(f"✅ Diretório criado: {path_name} -> {path_value}")
        
        # Criar diretório do banco
        db_path = Path(self.config["database"]["path"])
        db_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"✅ Diretório do banco: {db_path.parent}")
    
    def save_config_file(self):
        """Salva arquivo de configuração para referência."""
        config_file = self.current_path / "config_ambiente.json"
        
        config_data = {
            "detected_at": datetime.now().isoformat(),
            "environment": self.environment,
            "system": self.system,
            "current_path": str(self.current_path),
            "config": self.config
        }
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Configuração salva: {config_file}")
    
    def create_production_marker(self):
        """Cria marcador de ambiente de produção."""
        if self.environment == "production":
            marker_file = self.current_path / ".production"
            with open(marker_file, 'w') as f:
                f.write(f"Ambiente de produção - Galapagos DTVM\n")
                f.write(f"Criado em: {datetime.now().isoformat()}\n")
                f.write(f"Sistema: {self.system}\n")
            print(f"✅ Marcador de produção criado: {marker_file}")
    
    def print_environment_info(self):
        """Exibe informações do ambiente detectado."""
        print("=" * 60)
        print("🔍 DETECÇÃO DE AMBIENTE - GALAPAGOS DTVM")
        print("=" * 60)
        print(f"🖥️  Sistema: {self.system}")
        print(f"📁 Pasta atual: {self.current_path}")
        print(f"🎯 Ambiente: {self.environment.upper()}")
        print()
        
        if self.environment == "production":
            print("🏭 AMBIENTE DE PRODUÇÃO")
            print("✅ Dados compartilhados em tempo real")
            print("✅ Banco SQLite centralizado")
            print("✅ Multi-usuário habilitado")
            print("✅ Backup automático")
            print("✅ Logs de auditoria")
        else:
            print("🔧 AMBIENTE DE DESENVOLVIMENTO")
            print("✅ Dados locais para testes")
            print("✅ Banco SQLite local")
            print("✅ Sincronização via Git")
            print("✅ Modo debug habilitado")
        
        print()
        print("📊 CONFIGURAÇÕES:")
        print(f"   Database: {self.config['database']['path']}")
        print(f"   Dados: {self.config['paths']['dados']}")
        print(f"   Resultados: {self.config['paths']['resultados']}")
        print(f"   Logs: {self.config['paths']['logs']}")
        print("=" * 60)

def main():
    """Função principal para configurar ambiente."""
    print("🚀 Configurando ambiente Galapagos DTVM...")
    
    # Detectar ambiente
    detector = EnvironmentDetector()
    detector.print_environment_info()
    
    # Criar estrutura
    detector.create_directories()
    detector.save_config_file()
    detector.create_production_marker()
    
    print()
    print("✅ Configuração concluída com sucesso!")
    print()
    
    if detector.environment == "production":
        print("🎯 PRÓXIMOS PASSOS (PRODUÇÃO):")
        print("1. Execute: python executar_dashboard.py")
        print("2. Acesse: http://localhost:5000")
        print("3. Toda equipe verá os mesmos dados!")
    else:
        print("🎯 PRÓXIMOS PASSOS (DESENVOLVIMENTO):")
        print("1. Desenvolva e teste localmente")
        print("2. Faça commit das melhorias")
        print("3. Quando aprovado, copie para pasta colaborativa")
    
    return detector

if __name__ == "__main__":
    detector = main()

