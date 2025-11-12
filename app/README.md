# R-IoT Application

Aplicação completa de monitoramento rural inteligente com arquitetura frontend/backend.

## 📁 Estrutura

```
app/
├── frontend/          # React + TypeScript + Vite
│   ├── components/    # Componentes React
│   ├── hooks/         # Custom hooks
│   ├── services/      # Serviços (Gemini API)
│   ├── App.tsx
│   ├── config.ts      # Configurações de API
│   └── ...
│
└── backend/           # FastAPI + Python
    ├── main.py        # Aplicação FastAPI
    ├── models.py      # Modelos Pydantic
    ├── data_manager.py # Simulação de dados
    ├── animal-history.json
    └── ...
```

## 🚀 Quick Start

### Modo Rápido (Scripts Automáticos)

**Desenvolvimento (Local):**
```bash
./start.sh dev
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
```

**Produção (Server):**
```bash
./start.sh prod
# Backend: http://0.0.0.0:8000
# Frontend: faça build separado (ver DEPLOYMENT.md)
```

**Parar servidores:**
```bash
./stop.sh
```

### Modo Manual

<details>
<summary>Clique para ver instruções manuais</summary>

#### 1️⃣ Iniciar o Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Desenvolvimento
uvicorn main:app --reload

# Produção
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Backend estará em: `http://localhost:8000`

#### 2️⃣ Iniciar o Frontend (apenas desenvolvimento)

Em outro terminal:

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env.local
# Edite .env.local e adicione sua VITE_GEMINI_API_KEY

# Rodar app
npm run dev
```

Frontend estará em: `http://localhost:5173`

</details>

## 📡 Arquitetura

```
┌─────────────────────────────────────────────┐
│           Frontend (React)                  │
│  - Interface web responsiva                 │
│  - Mapa interativo                          │
│  - Chat com Gemini AI                       │
│  - Polling a cada 2s                        │
└──────────────────┬──────────────────────────┘
                   │ HTTP/REST
                   │ (GET /api/data)
┌──────────────────▼──────────────────────────┐
│           Backend (FastAPI)                 │
│  - API REST endpoints                       │
│  - Simulação em tempo real                  │
│  - Gerenciamento de dados                   │
│  - CORS habilitado                          │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
          animal-history.json
          (Dados iniciais)
```

## 🔌 Endpoints da API

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/` | GET | Info da API |
| `/health` | GET | Health check |
| `/api/data` | GET | Todos os dados (animais + rebanhos) |
| `/api/animals` | GET | Lista de animais |
| `/api/herds` | GET | Lista de rebanhos |
| `/api/animals/{id}` | GET | Animal específico |
| `/api/herds/{id}` | GET | Rebanho específico |
| `/docs` | GET | Swagger UI |

## ⚙️ Configuração

### Backend
- **Python 3.10+**
- FastAPI, Uvicorn, Pydantic
- Porta padrão: `8000`

### Frontend
- **Node.js**
- React 19.2, TypeScript, Vite
- Porta padrão: `5173`
- Requer `VITE_GEMINI_API_KEY` em `.env.local`

## 🔄 Fluxo de Dados

1. **Backend** carrega dados de `animal-history.json`
2. **Background task** simula atualizações a cada 2 segundos:
   - Movimento GPS
   - Temperatura corporal
   - Atividade (passos)
   - Alertas (temperatura alta, fora da área)
3. **Frontend** faz polling da API a cada 2 segundos
4. **Interface** atualiza em tempo real

## 📊 Simulação de Dados

O backend simula:
- ✅ **GPS**: Pequenos deslocamentos aleatórios
- ✅ **Temperatura**: Variações e eventos (febre)
- ✅ **Passos**: Incremento de atividade
- ✅ **Alertas**:
  - Temperatura ≥ 39.1°C (Warning)
  - Temperatura ≥ 40.0°C (Danger)
  - Animal fora da área designada (geofencing)

## 🛠️ Desenvolvimento

### Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm run dev
```

### Documentação da API
Acesse: http://localhost:8000/docs

## 📝 Documentação

- **[Guia de Deploy](./DEPLOYMENT.md)** - Deploy em produção, configuração de servidor, CORS, etc.
- [Backend README](./backend/README.md) - Documentação da API
- [Frontend README](./frontend/README.md) - Documentação do frontend

## 🔐 Segurança

⚠️ **IMPORTANTE**:
- Configure CORS adequadamente em produção
- Não commite `.env.local` com chaves reais
- Use HTTPS em produção

## 📦 Deploy

### Backend
- Pode ser deployado em: Railway, Render, Fly.io, AWS, GCP, etc.
- Requer Python 3.10+

### Frontend
- Pode ser deployado em: Vercel, Netlify, Cloudflare Pages, etc.
- Build estático: `npm run build` → pasta `dist/`

## 🤝 Contribuindo

1. Backend em Python (FastAPI)
2. Frontend em TypeScript (React)
3. Siga os padrões de código existentes
4. Atualize a documentação

---

Desenvolvido para o projeto **R-IoT - Monitoramento Rural Inteligente**
