#!/bin/bash

# Script para parar os servidores do R-IoT

echo "🛑 Parando R-IoT Application..."
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Função para matar processo
kill_process() {
    PID_FILE=$1
    NAME=$2

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            kill $PID 2>/dev/null
            echo -e "${GREEN}✓ $NAME parado (PID: $PID)${NC}"
        else
            echo -e "${RED}⚠ $NAME não estava rodando${NC}"
        fi
        rm "$PID_FILE"
    else
        echo -e "${RED}⚠ Arquivo PID não encontrado para $NAME${NC}"
    fi
}

# Para backend
kill_process ".backend.pid" "Backend"

# Para frontend
kill_process ".frontend.pid" "Frontend"

# Limpa processos órfãos nas portas
echo ""
echo "🧹 Limpando processos nas portas..."

# Porta 8000 (backend)
PID_8000=$(lsof -t -i:8000 2>/dev/null)
if [ ! -z "$PID_8000" ]; then
    kill -9 $PID_8000 2>/dev/null
    echo -e "${GREEN}✓ Processo na porta 8000 terminado${NC}"
fi

# Porta 5173 (frontend)
PID_5173=$(lsof -t -i:5173 2>/dev/null)
if [ ! -z "$PID_5173" ]; then
    kill -9 $PID_5173 2>/dev/null
    echo -e "${GREEN}✓ Processo na porta 5173 terminado${NC}"
fi

echo ""
echo -e "${GREEN}✓ R-IoT Application parado com sucesso!${NC}"
