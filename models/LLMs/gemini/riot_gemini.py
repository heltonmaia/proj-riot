#!/usr/bin/env python3
"""
RIOT GEMINI - Sistema de Análise de Vídeos de Animais de Fazenda
================================================================

Este programa utiliza a API do Google Gemini para analisar vídeos de animais de fazenda
e gerar legendas educativas automaticamente.

Funcionalidades:
- Análise individual de vídeos
- Processamento em lote de diretórios
- Mesclagem de vídeos
- Adição de legendas aos vídeos
- Configuração flexível via arquivo YAML

Autor: Helton Maia
Versão: 1.0
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.menu import Menu
from src.config_manager import ConfigManager

def main():
    """Função principal do programa."""
    print("="*60)
    print("           RIOT GEMINI - SISTEMA DE ANÁLISE DE VÍDEOS")
    print("="*60)
    print("Sistema de análise de vídeos de animais de fazenda usando IA")
    print("Versão 1.0")
    print("="*60)
    
    # Inicializar gerenciador de configuração
    config_manager = ConfigManager()
    
    # Criar diretórios necessários
    print("Verificando estrutura de diretórios...")
    config_manager.create_directories()
    
    # Validar configuração
    errors = config_manager.validate_config()
    if errors:
        print("\nAvisos de configuração:")
        for error in errors:
            print(f"  - {error}")
        print("\nUse a opção 'Configurar API Key' no menu para resolver.")
    
    # Inicializar e exibir menu
    menu = Menu()
    menu.show_main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        sys.exit(1) 