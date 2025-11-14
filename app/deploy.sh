#!/bin/bash

# Script de Deploy Automatizado para R-IoT em Produção
# Este script faz todo o processo de atualização

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🚀 R-IoT Deploy em Produção"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Parar serviços
echo -e "${BLUE}1. Parando serviços...${NC}"
./stop.sh
echo ""

# 2. Atualizar código do repositório
echo -e "${BLUE}2. Atualizando código do repositório...${NC}"
git pull
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Erro ao atualizar repositório${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Código atualizado${NC}"
echo ""

# 3. Build do frontend
echo -e "${BLUE}3. Fazendo build do frontend...${NC}"
cd frontend

# Instalar dependências se necessário
if [ ! -d "node_modules" ]; then
    echo "Instalando dependências..."
    npm install
fi

# Build em modo produção
npm run build
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Erro ao fazer build do frontend${NC}"
    cd ..
    exit 1
fi
echo -e "${GREEN}✓ Build do frontend concluído${NC}"
echo ""

cd ..

# 4. Verificar se build foi criado
if [ ! -d "frontend/dist" ]; then
    echo -e "${RED}✗ Pasta dist/ não foi criada${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Pasta dist/ criada com sucesso${NC}"
echo "   Arquivos:"
ls -lh frontend/dist/ | head -10
echo ""

# 5. Configurar variáveis de ambiente para produção
echo -e "${BLUE}4. Configurando variáveis de ambiente...${NC}"
export ALLOWED_ORIGINS="https://playground.heltonmaia.com"
echo -e "${GREEN}✓ CORS configurado para: ${ALLOWED_ORIGINS}${NC}"
echo ""

# 6. Iniciar backend em produção
echo -e "${BLUE}5. Iniciando backend em produção...${NC}"
./start.sh prod

# 7. Verificar se backend está rodando
sleep 5
if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${GREEN}✓ Backend está rodando na porta 8001${NC}"
else
    echo -e "${RED}✗ Backend NÃO está rodando${NC}"
    echo "Verifique os logs: cat backend-error.log"
    exit 1
fi
echo ""

# 8. Resumo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✓ Deploy concluído com sucesso!${NC}"
echo ""
echo "📊 Status:"
echo "  ✓ Frontend build: frontend/dist/"
echo "  ✓ Backend rodando: http://localhost:8001"
echo "  ✓ CORS configurado para: playground.heltonmaia.com"
echo ""
echo "🌐 Acesse:"
echo "  https://playground.heltonmaia.com/riot/"
echo ""
echo "📝 Logs:"
echo "  Backend: tail -f backend-access.log backend-error.log"
echo ""
echo "⚠️  IMPORTANTE:"
echo "  Se esta é a primeira vez fazendo deploy, configure o NGINX:"
echo "  Veja instruções em: PRODUCTION_DEPLOY.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
