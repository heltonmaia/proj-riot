#!/bin/bash

# RIOT GEMINI - Script de Instalação
# ===================================

echo "============================================================"
echo "           RIOT GEMINI - INSTALAÇÃO"
echo "============================================================"
echo "Sistema de análise de vídeos de animais de fazenda usando IA"
echo "============================================================"

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale o Python 3.8+ primeiro."
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"

# Verificar se pip está instalado
if ! command -v pip &> /dev/null; then
    echo "❌ pip não encontrado. Por favor, instale o pip primeiro."
    exit 1
fi

echo "✅ pip encontrado: $(pip --version)"

# Verificar se FFmpeg está instalado
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg não encontrado."
    echo "Por favor, instale o FFmpeg:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    echo "  Windows: Baixe de https://ffmpeg.org/download.html"
    echo ""
    read -p "Deseja continuar sem FFmpeg? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
else
    echo "✅ FFmpeg encontrado: $(ffmpeg -version | head -n1)"
fi

# Criar ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
    echo "✅ Ambiente virtual criado"
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências
echo "📦 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p videos results tmp

# Tornar o script principal executável
chmod +x riot_gemini.py

echo ""
echo "============================================================"
echo "           INSTALAÇÃO CONCLUÍDA!"
echo "============================================================"
echo ""
echo "🎉 O RIOT GEMINI foi instalado com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Execute: python riot_gemini.py"
echo "2. Configure sua API Key do Google Gemini"
echo "3. Comece a analisar seus vídeos!"
echo ""
echo "📚 Para mais informações, consulte o README.md"
echo "============================================================" 