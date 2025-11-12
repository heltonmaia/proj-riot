#!/bin/bash

# Script para parar os servidores do R-IoT
# Detecta automaticamente o ambiente

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🛑 Parando R-IoT Application..."
echo ""

# Detectar ambiente
ENVIRONMENT=""
if [ -f ".environment" ]; then
    ENVIRONMENT=$(cat .environment)
    echo -e "${YELLOW}Ambiente detectado: $ENVIRONMENT${NC}"
    echo ""
fi

# Função para matar processo por PID file
kill_process() {
    PID_FILE=$1
    NAME=$2

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            kill $PID 2>/dev/null
            # Aguarda até 5 segundos para o processo terminar
            for i in {1..10}; do
                if ! ps -p $PID > /dev/null 2>&1; then
                    break
                fi
                sleep 0.5
            done
            # Force kill se ainda estiver rodando
            if ps -p $PID > /dev/null 2>&1; then
                kill -9 $PID 2>/dev/null
            fi
            echo -e "${GREEN}✓ $NAME parado (PID: $PID)${NC}"
        else
            echo -e "${YELLOW}⚠ $NAME não estava rodando${NC}"
        fi
        rm "$PID_FILE"
    else
        echo -e "${YELLOW}⚠ Arquivo PID não encontrado para $NAME${NC}"
    fi
}

# Para backend
kill_process "backend.pid" "Backend"

# Para frontend (apenas se estava rodando)
if [ -f "frontend.pid" ]; then
    kill_process "frontend.pid" "Frontend"
fi

# Limpa processos órfãos nas portas
echo ""
echo "🧹 Limpando processos órfãos nas portas..."

# Porta 8001 (backend R-IoT)
PID_8001=$(lsof -t -i:8001 2>/dev/null)
if [ ! -z "$PID_8001" ]; then
    kill -9 $PID_8001 2>/dev/null
    echo -e "${GREEN}✓ Processo órfão na porta 8001 terminado${NC}"
fi

# Porta 5174 (frontend R-IoT)
PID_5174=$(lsof -t -i:5174 2>/dev/null)
if [ ! -z "$PID_5174" ]; then
    kill -9 $PID_5174 2>/dev/null
    echo -e "${GREEN}✓ Processo órfão na porta 5174 terminado${NC}"
fi

# Limpa arquivo de ambiente
if [ -f ".environment" ]; then
    rm ".environment"
fi

echo ""
echo -e "${GREEN}✓ R-IoT Application parado com sucesso!${NC}"

# Dica sobre logs
if [ "$ENVIRONMENT" == "production" ]; then
    echo ""
    echo "Logs mantidos em:"
    echo "  - backend-access.log"
    echo "  - backend-error.log"
fi
