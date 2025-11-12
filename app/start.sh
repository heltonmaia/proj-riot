#!/bin/bash

# Script de inicialização do R-IoT
# Suporta modo desenvolvimento (local) e produção (server)

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Banner
echo "🚀 R-IoT Application Starter"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Determinar ambiente
ENVIRONMENT=""

# 1. Checar argumento de linha de comando
if [ "$1" == "dev" ] || [ "$1" == "local" ]; then
    ENVIRONMENT="development"
elif [ "$1" == "prod" ] || [ "$1" == "production" ]; then
    ENVIRONMENT="production"
fi

# 2. Checar variável de ambiente
if [ -z "$ENVIRONMENT" ] && [ ! -z "$RIOT_ENV" ]; then
    if [ "$RIOT_ENV" == "production" ] || [ "$RIOT_ENV" == "prod" ]; then
        ENVIRONMENT="production"
    else
        ENVIRONMENT="development"
    fi
fi

# 3. Perguntar ao usuário
if [ -z "$ENVIRONMENT" ]; then
    echo -e "${YELLOW}Selecione o ambiente de execução:${NC}"
    echo "  1) Desenvolvimento/Local (hot reload, CORS *, frontend + backend)"
    echo "  2) Produção/Server (workers, CORS configurado, backend otimizado)"
    echo ""
    read -p "Escolha [1/2]: " choice

    case $choice in
        1)
            ENVIRONMENT="development"
            ;;
        2)
            ENVIRONMENT="production"
            ;;
        *)
            echo -e "${RED}✗ Opção inválida. Usando desenvolvimento.${NC}"
            ENVIRONMENT="development"
            ;;
    esac
    echo ""
fi

# Exibir ambiente escolhido
if [ "$ENVIRONMENT" == "production" ]; then
    echo -e "${BLUE}🏭 Modo: PRODUÇÃO${NC}"
    echo "   - Backend com Gunicorn (4 workers)"
    echo "   - CORS restritivo"
    echo "   - Logs em arquivo"
    echo "   - Sem hot reload"
else
    echo -e "${GREEN}🔧 Modo: DESENVOLVIMENTO${NC}"
    echo "   - Backend com Uvicorn + reload"
    echo "   - CORS permissivo (*)"
    echo "   - Frontend dev server"
    echo "   - Hot reload habilitado"
fi
echo ""

# Salvar ambiente em arquivo
echo "$ENVIRONMENT" > .environment

# ============================================
# LIMPAR PROCESSOS ANTERIORES
# ============================================
echo -e "${YELLOW}🧹 Limpando processos anteriores...${NC}"

# Matar processos nas portas
kill_port() {
    PORT=$1
    PID=$(lsof -t -i:$PORT 2>/dev/null)
    if [ ! -z "$PID" ]; then
        echo "   Matando processo na porta $PORT (PID: $PID)"
        kill -9 $PID 2>/dev/null
        sleep 1
    fi
}

kill_port 8000
kill_port 5173
kill_port 3000
kill_port 3001

# Limpar PIDs antigos
rm -f backend.pid frontend.pid

echo -e "${GREEN}✓ Processos anteriores limpos${NC}"
echo ""

# Função para verificar se porta está livre
check_port_free() {
    PORT=$1
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        return 1  # Porta ocupada
    else
        return 0  # Porta livre
    fi
}

# ============================================
# BACKEND
# ============================================
echo -e "${BLUE}📡 Iniciando Backend (FastAPI)...${NC}"
cd backend

# Verifica se venv existe
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
    source .venv/bin/activate
    echo "Instalando dependências..."
    pip install -q -r requirements.txt
else
    source .venv/bin/activate
fi

# Inicia backend conforme ambiente
if [ "$ENVIRONMENT" == "production" ]; then
    # PRODUÇÃO: Gunicorn com workers
    echo "Iniciando com Gunicorn (4 workers)..."
    gunicorn main:app \
        --workers 4 \
        --worker-class uvicorn.workers.UvicornWorker \
        --bind 0.0.0.0:8000 \
        --access-logfile ../backend-access.log \
        --error-logfile ../backend-error.log \
        --daemon \
        --pid ../backend.pid

    sleep 2

    if [ -f "../backend.pid" ]; then
        BACKEND_PID=$(cat ../backend.pid)
        echo -e "${GREEN}✓ Backend iniciado (PID: $BACKEND_PID)${NC}"
        echo "   URL: http://0.0.0.0:8000"
        echo "   Access Logs: backend-access.log"
        echo "   Error Logs: backend-error.log"
    else
        echo -e "${RED}✗ Erro ao criar PID file${NC}"
        cd ..
        exit 1
    fi
else
    # DESENVOLVIMENTO: Uvicorn com reload
    echo "Iniciando com Uvicorn (hot reload)..."
    uvicorn main:app \
        --host 0.0.0.0 \
        --port 8000 \
        --reload \
        --log-level info > ../backend.log 2>&1 &

    BACKEND_PID=$!
    echo "$BACKEND_PID" > ../backend.pid
    echo -e "${GREEN}✓ Backend iniciado (PID: $BACKEND_PID)${NC}"
    echo "   URL: http://localhost:8000"
    echo "   Logs: backend.log"
fi

cd ..

# Aguarda backend inicializar
echo "⏳ Aguardando backend inicializar..."
sleep 3

# Verifica se backend está rodando
MAX_RETRIES=5
RETRY_COUNT=0
BACKEND_RUNNING=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if ! check_port_free 8000; then
        BACKEND_RUNNING=true
        break
    fi
    echo "   Tentativa $((RETRY_COUNT + 1))/$MAX_RETRIES..."
    sleep 1
    RETRY_COUNT=$((RETRY_COUNT + 1))
done

if [ "$BACKEND_RUNNING" = true ]; then
    echo -e "${GREEN}✓ Backend está rodando na porta 8000${NC}"
else
    echo -e "${RED}✗ Erro ao iniciar backend${NC}"
    echo ""
    echo "Verifique os logs:"
    if [ "$ENVIRONMENT" == "production" ]; then
        echo "  cat backend-error.log"
    else
        echo "  cat backend.log"
    fi

    if [ -f "backend.pid" ]; then
        kill $(cat backend.pid) 2>/dev/null
        rm backend.pid
    fi
    exit 1
fi
echo ""

# ============================================
# FRONTEND (apenas em desenvolvimento)
# ============================================
if [ "$ENVIRONMENT" == "development" ]; then
    echo -e "${BLUE}🎨 Iniciando Frontend (React)...${NC}"
    cd frontend

    # Verifica se node_modules existe
    if [ ! -d "node_modules" ]; then
        echo "Instalando dependências..."
        npm install
    fi

    # Verifica .env.local
    if [ ! -f ".env.local" ]; then
        echo -e "${YELLOW}⚠️  Arquivo .env.local não encontrado!${NC}"
        echo "Copiando .env.example..."
        cp .env.example .env.local
        echo -e "${YELLOW}⚠️  Configure sua VITE_GEMINI_API_KEY em .env.local${NC}"
    fi

    # Inicia frontend
    npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo "$FRONTEND_PID" > ../frontend.pid
    echo -e "${GREEN}✓ Frontend iniciado (PID: $FRONTEND_PID)${NC}"
    echo "   URL: http://localhost:5173"
    echo "   Logs: frontend.log"

    # Aguarda frontend inicializar
    echo "⏳ Aguardando frontend inicializar..."
    sleep 3

    # Verifica se frontend está rodando
    FRONTEND_RUNNING=false
    RETRY_COUNT=0

    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        if ! check_port_free 5173; then
            FRONTEND_RUNNING=true
            break
        fi
        echo "   Tentativa $((RETRY_COUNT + 1))/$MAX_RETRIES..."
        sleep 1
        RETRY_COUNT=$((RETRY_COUNT + 1))
    done

    if [ "$FRONTEND_RUNNING" = true ]; then
        echo -e "${GREEN}✓ Frontend está rodando na porta 5173${NC}"
    else
        echo -e "${RED}✗ Erro ao iniciar frontend${NC}"
        echo "  Verifique: cat frontend.log"
    fi
    echo ""

    cd ..
else
    echo -e "${YELLOW}ℹ️  Frontend não iniciado (modo produção)${NC}"
    echo "   Em produção, faça build do frontend:"
    echo "   cd frontend && npm run build"
    echo "   Sirva a pasta 'dist/' com nginx, apache, etc."
    echo ""
fi

# ============================================
# RESUMO
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✓ R-IoT Application está rodando!${NC}"
echo ""
echo "  Ambiente: $ENVIRONMENT"
echo "  Backend:  http://$([ "$ENVIRONMENT" == "production" ] && echo "0.0.0.0" || echo "localhost"):8000"
echo "  API Docs: http://$([ "$ENVIRONMENT" == "production" ] && echo "0.0.0.0" || echo "localhost"):8000/docs"

if [ "$ENVIRONMENT" == "development" ]; then
    echo "  Frontend: http://localhost:5173"
fi

echo ""
echo "Para parar os servidores:"
echo "  ./stop.sh"
echo ""

if [ "$ENVIRONMENT" == "development" ]; then
    echo "Logs em tempo real:"
    echo "  Backend:  tail -f backend.log"
    echo "  Frontend: tail -f frontend.log"
else
    echo "Logs:"
    echo "  Backend Access: tail -f backend-access.log"
    echo "  Backend Error:  tail -f backend-error.log"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Exportar variável de ambiente para outros scripts
export RIOT_ENV=$ENVIRONMENT
