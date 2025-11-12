#!/bin/bash

# Script de inicialização do R-IoT
# Inicia backend e frontend simultaneamente

echo "🚀 Iniciando R-IoT Application..."
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para verificar se porta está em uso
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${RED}⚠️  Porta $1 já está em uso!${NC}"
        return 1
    fi
    return 0
}

# Verifica portas
echo "🔍 Verificando portas..."
check_port 8000 || exit 1
check_port 5173 || exit 1
echo -e "${GREEN}✓ Portas disponíveis${NC}"
echo ""

# Inicia backend
echo -e "${BLUE}📡 Iniciando Backend (FastAPI)...${NC}"
cd backend

# Verifica se venv existe
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Instalando dependências..."
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

# Inicia backend em background
python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend iniciado (PID: $BACKEND_PID)${NC}"
echo "   URL: http://localhost:8000"
echo "   Logs: backend.log"
echo ""

cd ..

# Aguarda backend inicializar
echo "⏳ Aguardando backend inicializar..."
sleep 3

# Verifica se backend está rodando
if ! check_port 8000; then
    echo -e "${GREEN}✓ Backend está rodando${NC}"
else
    echo -e "${RED}✗ Erro ao iniciar backend${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi
echo ""

# Inicia frontend
echo -e "${BLUE}🎨 Iniciando Frontend (React)...${NC}"
cd frontend

# Verifica se node_modules existe
if [ ! -d "node_modules" ]; then
    echo "Instalando dependências..."
    npm install
fi

# Verifica .env.local
if [ ! -f ".env.local" ]; then
    echo -e "${RED}⚠️  Arquivo .env.local não encontrado!${NC}"
    echo "Copiando .env.example..."
    cp .env.example .env.local
    echo -e "${RED}⚠️  Configure sua VITE_GEMINI_API_KEY em .env.local${NC}"
fi

# Inicia frontend em background
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend iniciado (PID: $FRONTEND_PID)${NC}"
echo "   URL: http://localhost:5173"
echo "   Logs: frontend.log"
echo ""

cd ..

# Salva PIDs em arquivo
echo "$BACKEND_PID" > .backend.pid
echo "$FRONTEND_PID" > .frontend.pid

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✓ R-IoT Application está rodando!${NC}"
echo ""
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Para parar os servidores, execute:"
echo "  ./stop.sh"
echo ""
echo "Logs em tempo real:"
echo "  Backend:  tail -f backend.log"
echo "  Frontend: tail -f frontend.log"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
