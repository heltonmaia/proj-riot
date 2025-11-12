# R-IoT Frontend

Frontend React da plataforma de monitoramento rural inteligente.

## 🚀 Tecnologias

- **React 19.2** - Framework UI
- **TypeScript** - Tipagem estática
- **Vite** - Build tool e dev server
- **Google Gemini AI** - Chat inteligente

## 📋 Funcionalidades

- 🗺️ **Mapa interativo** com localização GPS dos animais
- 📊 **Dashboard** com estatísticas em tempo real
- 💬 **Chat com IA** (Gemini) para insights sobre o rebanho
- 🔔 **Sistema de alertas** (temperatura, geofencing)
- 📱 **Interface responsiva** (desktop e mobile)
- ⚡ **Atualização em tempo real** (polling a cada 2 segundos)

## 🛠️ Instalação

1. Instale as dependências:
```bash
npm install
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env.local
```

3. Edite `.env.local` e adicione suas credenciais:
```env
VITE_GEMINI_API_KEY=sua_chave_gemini_aqui
VITE_API_URL=http://localhost:8000
```

## ▶️ Execução

**IMPORTANTE**: O backend deve estar rodando primeiro!

```bash
# Desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview da build
npm run preview
```

A aplicação estará disponível em: `http://localhost:5173`

## 🏗️ Estrutura

```
frontend/
├── components/           # Componentes React
│   ├── MapPanel.tsx     # Mapa interativo
│   ├── StatsPanel.tsx   # Painel de estatísticas
│   ├── ChatPanel.tsx    # Chat com IA
│   ├── AnimalDetailPanel.tsx
│   ├── HerdPanel.tsx
│   ├── Login.tsx
│   ├── BottomNav.tsx
│   └── Icons.tsx
│
├── hooks/
│   └── useAnimalData.ts # Hook para buscar dados da API
│
├── services/
│   └── geminiService.ts # Integração com Gemini
│
├── App.tsx              # Componente principal
├── types.ts             # Tipos TypeScript
├── config.ts            # Configurações (API URLs)
├── index.tsx            # Entry point
├── index.html
└── vite.config.ts
```

## 🔗 Integração com Backend

O frontend consome a API REST do backend FastAPI:

- `GET /api/data` - Busca animais e rebanhos
- Polling automático a cada 2 segundos
- Configurável via `VITE_API_URL` em `.env.local`

## 📱 Views

### Desktop
- **Sidebar esquerda**: Dashboard + Chat
- **Área principal**: Mapa + Estatísticas
- Painel colapsável

### Mobile
- **Bottom navigation** com 3 tabs:
  - Dashboard: Estatísticas e detalhes
  - Mapa: Visualização geográfica
  - Chat: Assistente IA

## 🎨 Componentes Principais

### MapPanel
Mapa interativo mostrando:
- Marcadores GPS dos animais
- Polígonos das áreas de rebanho
- Seleção de animal no clique

### ChatPanel
Chat com IA Gemini para:
- Perguntas sobre saúde do rebanho
- Análise de tendências
- Insights contextuais

### StatsPanel
Estatísticas gerais:
- Total de animais
- Alertas ativos
- Status de saúde

### AnimalDetailPanel
Detalhes de um animal:
- Nome, tipo, raça, idade, peso
- Temperatura atual
- Passos (atividade)
- Alertas ativos
- Histórico de 7 dias

## 🔑 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `VITE_GEMINI_API_KEY` | Chave da API do Google Gemini | - |
| `VITE_API_URL` | URL do backend | `http://localhost:8000` |

## 📝 Scripts

- `npm run dev` - Inicia servidor de desenvolvimento
- `npm run build` - Build para produção
- `npm run preview` - Preview da build de produção

---

**Link do AI Studio**: https://ai.studio/apps/drive/1XfMrsEpNScdcl-fg0GIpcBMYFs91BAHb
