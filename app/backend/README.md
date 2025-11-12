# R-IoT Backend API

Backend FastAPI para o sistema de monitoramento rural inteligente.

## 🚀 Funcionalidades

- **API REST** com FastAPI
- **Simulação em tempo real** de dados de animais (atualização a cada 2 segundos)
- **CORS habilitado** para integração com frontend
- **Documentação automática** com Swagger UI
- **Validação de dados** com Pydantic

## 📋 Endpoints

### Base
- `GET /` - Informações da API
- `GET /health` - Health check

### Animais
- `GET /api/animals` - Lista todos os animais
- `GET /api/animals/{id}` - Busca animal por ID

### Rebanhos
- `GET /api/herds` - Lista todos os rebanhos
- `GET /api/herds/{id}` - Busca rebanho por ID

### Dados Completos
- `GET /api/data` - Retorna animais e rebanhos

## 🛠️ Instalação

1. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Execução

```bash
# Desenvolvimento (com auto-reload)
python main.py

# ou usando uvicorn diretamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: `http://localhost:8000`

## 📚 Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔧 Estrutura

```
backend/
├── main.py              # Aplicação FastAPI principal
├── models.py            # Modelos Pydantic
├── data_manager.py      # Gerenciador de dados e simulação
├── animal-history.json  # Dados iniciais
├── requirements.txt     # Dependências
└── README.md           # Documentação
```

## 📊 Simulação de Dados

O backend simula automaticamente:
- **Movimento GPS** (pequenos deslocamentos)
- **Temperatura corporal** (variações e eventos aleatórios)
- **Atividade** (incremento de passos)
- **Alertas** (temperatura alta, fora da área)

A simulação roda em background e atualiza os dados a cada 2 segundos.

## 🔒 CORS

Por padrão, CORS está configurado para aceitar requisições de qualquer origem (`allow_origins=["*"]`).

**⚠️ IMPORTANTE**: Em produção, configure apenas as origens específicas do seu frontend:

```python
allow_origins=["http://localhost:5173", "https://seu-dominio.com"]
```
