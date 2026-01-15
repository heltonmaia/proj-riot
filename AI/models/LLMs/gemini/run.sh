#!/bin/bash
#execute manualmente os comandos abaixo no terminal:

# Caminho relativo para o ambiente virtual na raiz do projeto
VENV_PATH="../../../../uv-env"

if [ -d "$VENV_PATH" ]; then
    source "$VENV_PATH/bin/activate"
    python -m riot_gemini
else
    echo "❌ Ambiente virtual não encontrado em $VENV_PATH"
    echo "Por favor, execute o setup do projeto primeiro."
    exit 1
fi 