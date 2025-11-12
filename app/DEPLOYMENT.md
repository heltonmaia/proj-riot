# R-IoT - Guia de Deploy e Execução

Este guia explica como executar o R-IoT em diferentes ambientes (desenvolvimento e produção).

## 🚀 Modos de Execução

### Modo Desenvolvimento (Local)
- Backend com Uvicorn + hot reload
- Frontend dev server (Vite)
- CORS permissivo (*)
- Logs em tempo real
- Ideal para desenvolvimento

### Modo Produção (Server)
- Backend com Gunicorn (4 workers)
- Frontend não iniciado (fazer build separado)
- CORS configurável por variável de ambiente
- Logs de acesso e erro separados
- Otimizado para performance

## 📋 Como Executar

### Opção 1: Modo Interativo (Pergunta ao Usuário)

```bash
./start.sh
```

O script perguntará qual ambiente usar:
- `1` - Desenvolvimento
- `2` - Produção

### Opção 2: Argumento de Linha de Comando

**Desenvolvimento:**
```bash
./start.sh dev
# ou
./start.sh local
```

**Produção:**
```bash
./start.sh prod
# ou
./start.sh production
```

### Opção 3: Variável de Ambiente

**Desenvolvimento:**
```bash
export RIOT_ENV=development
./start.sh
```

**Produção:**
```bash
export RIOT_ENV=production
./start.sh
```

## 🛑 Parar os Servidores

```bash
./stop.sh
```

O script detecta automaticamente o ambiente e para os processos corretamente.

## 🔧 Configuração de Produção

### 1. CORS (Backend)

Por padrão, em desenvolvimento o CORS aceita todas as origens (`*`).

**Em produção**, configure domínios específicos:

```bash
# Antes de executar start.sh
export ALLOWED_ORIGINS="https://seu-dominio.com,https://app.seu-dominio.com"
./start.sh prod
```

Ou adicione ao `.bashrc` / `.zshrc` no servidor:
```bash
echo 'export ALLOWED_ORIGINS="https://seu-dominio.com"' >> ~/.bashrc
```

### 2. Frontend (Produção)

Em produção, o frontend **não é iniciado automaticamente**. Você precisa fazer o build:

```bash
cd frontend
npm install
npm run build
```

A pasta `dist/` gerada deve ser servida por:
- **Nginx** (recomendado)
- **Apache**
- **Caddy**
- Ou qualquer servidor web estático

#### Exemplo Nginx

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    # Frontend (React build)
    location / {
        root /path/to/app/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API (proxy)
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend docs
    location /docs {
        proxy_pass http://localhost:8000/docs;
    }
}
```

### 3. Backend (Produção)

O backend em produção usa **Gunicorn** com 4 workers:

```bash
# Iniciado automaticamente por ./start.sh prod
# Configuração:
# - 4 workers (ajuste conforme CPU)
# - Bind em 0.0.0.0:8000
# - Logs separados (access/error)
```

Para ajustar número de workers, edite `start.sh`:
```bash
--workers 4  # Mude para número desejado
```

## 📦 Deploy em Servidor

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/proj-riot.git
cd proj-riot/app
```

2. **Configure variáveis de ambiente:**
```bash
# Backend CORS
export ALLOWED_ORIGINS="https://seu-dominio.com"

# Frontend (se necessário)
cd frontend
echo "VITE_GEMINI_API_KEY=sua_chave_aqui" > .env.local
echo "VITE_API_URL=https://api.seu-dominio.com" >> .env.local
```

3. **Faça build do frontend:**
```bash
cd frontend
npm install
npm run build
```

4. **Configure servidor web (Nginx/Apache):**
- Sirva `frontend/dist/` como raiz
- Proxy `/api` para `localhost:8000`

5. **Inicie o backend:**
```bash
cd ..
./start.sh prod
```

6. **Configure como serviço (systemd):**

Crie `/etc/systemd/system/riot-backend.service`:
```ini
[Unit]
Description=R-IoT Backend API
After=network.target

[Service]
Type=forking
User=seu-usuario
WorkingDirectory=/path/to/app
Environment="ALLOWED_ORIGINS=https://seu-dominio.com"
ExecStart=/path/to/app/start.sh prod
ExecStop=/path/to/app/stop.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Ative:
```bash
sudo systemctl enable riot-backend
sudo systemctl start riot-backend
sudo systemctl status riot-backend
```

## 📊 Logs

### Desenvolvimento
```bash
tail -f backend.log
tail -f frontend.log
```

### Produção
```bash
tail -f backend-access.log
tail -f backend-error.log
```

## 🔒 Segurança

### Checklist de Produção

- [ ] Configure CORS com domínios específicos (`ALLOWED_ORIGINS`)
- [ ] Use HTTPS (Let's Encrypt + Nginx)
- [ ] Configure firewall (apenas portas 80/443 abertas)
- [ ] Mantenha dependências atualizadas
- [ ] Configure rate limiting (Nginx)
- [ ] Use variáveis de ambiente para secrets
- [ ] Não commite `.env.local` ou chaves de API
- [ ] Configure backups dos dados

## 🐛 Troubleshooting

### Backend não inicia
```bash
# Verifique logs
cat backend-error.log

# Verifique se porta está livre
lsof -i :8000

# Reinstale dependências
cd backend
source .venv/bin/activate
pip install -r requirements.txt --upgrade
```

### Frontend não conecta ao backend
```bash
# Verifique CORS
curl -I http://localhost:8000/api/data

# Verifique URL da API em .env.local
cat frontend/.env.local
```

### Gunicorn não encontrado (produção)
```bash
cd backend
source .venv/bin/activate
pip install gunicorn==23.0.0
```

## 📚 Recursos

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Vite Production Build](https://vitejs.dev/guide/build.html)

---

**Desenvolvido para R-IoT - Monitoramento Rural Inteligente**
