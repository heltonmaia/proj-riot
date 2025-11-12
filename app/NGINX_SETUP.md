# Configuração Nginx para R-IoT

## 📋 Adicionar ao arquivo existente

Edite o arquivo `/etc/nginx/sites-available/playground`:

```bash
sudo nano /etc/nginx/sites-available/playground
```

## ✂️ Adicione esta configuração

Adicione **ANTES** da seção `location /`  (depois do bloco NEO-APP):

```nginx
# ====== R-IOT APP ======
# Frontend R-IoT
location /riot/ {
    proxy_pass http://localhost:5174/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Backend API R-IoT
location /riot/api/ {
    proxy_pass http://localhost:8001/api/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

# Backend Docs R-IoT
location /riot/docs {
    proxy_pass http://localhost:8001/docs;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

# Health check R-IoT
location /riot/health {
    proxy_pass http://localhost:8001/health;
}
# ====== FIM R-IOT APP ======
```

## 📝 Configuração Completa Final

Seu arquivo `/etc/nginx/sites-available/playground` ficará assim:

```nginx
server {
    listen 443 ssl;
    server_name playground.heltonmaia.com;

    # Certificados SSL
    ssl_certificate /etc/letsencrypt/live/playground.heltonmaia.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/playground.heltonmaia.com/privkey.pem;

    # Configurações SSL recomendadas
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # ====== NEO-APP ======
    # Frontend Neo-App
    location /neo/ {
        proxy_pass http://localhost:5173;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API Neo-App
    location /neo/api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Health check Neo-App
    location /neo/health {
        proxy_pass http://localhost:8000/health;
    }
    # ====== FIM NEO-APP ======

    # ====== R-IOT APP ======
    # Frontend R-IoT
    location /riot/ {
        proxy_pass http://localhost:5174/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API R-IoT
    location /riot/api/ {
        proxy_pass http://localhost:8001/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend Docs R-IoT
    location /riot/docs {
        proxy_pass http://localhost:8001/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Health check R-IoT
    location /riot/health {
        proxy_pass http://localhost:8001/health;
    }
    # ====== FIM R-IOT APP ======

    # Proxy reverso para a aplicação Vite em https://31.220.100.112:3000/
    location / {
        proxy_pass http://31.220.100.112:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Aumenta o timeout para evitar 504
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}

# Redirecionamento HTTP para HTTPS
server {
    if ($host = playground.heltonmaia.com) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    server_name playground.heltonmaia.com;
    return 301 https://$host$request_uri;
}
```

## 🚀 Passos para Ativar

### 1. Editar configuração
```bash
sudo nano /etc/nginx/sites-available/playground
```

### 2. Testar configuração
```bash
sudo nginx -t
```

### 3. Recarregar Nginx
```bash
sudo systemctl reload nginx
```

### 4. Iniciar R-IoT
```bash
cd /home/heltonmaia/work/github-projects/proj-riot/app
./start.sh prod
```

## 🌐 URLs de Acesso

Após configurar, seus apps estarão disponíveis em:

- **Neo-App**: https://playground.heltonmaia.com/neo/
  - API: https://playground.heltonmaia.com/neo/api/
  - Health: https://playground.heltonmaia.com/neo/health

- **R-IoT**: https://playground.heltonmaia.com/riot/
  - API: https://playground.heltonmaia.com/riot/api/
  - Docs: https://playground.heltonmaia.com/riot/docs
  - Health: https://playground.heltonmaia.com/riot/health

- **Outro App**: https://playground.heltonmaia.com/ (raiz)

## 🔧 Configurar CORS no Backend

O backend precisa aceitar requisições do domínio `playground.heltonmaia.com`. Configure antes de iniciar:

```bash
export ALLOWED_ORIGINS="https://playground.heltonmaia.com"
./start.sh prod
```

Ou adicione ao `.bashrc` para ser permanente:
```bash
echo 'export ALLOWED_ORIGINS="https://playground.heltonmaia.com"' >> ~/.bashrc
source ~/.bashrc
```

## 🔍 Verificar se está Funcionando

```bash
# Backend
curl http://localhost:8001/health

# Através do Nginx
curl https://playground.heltonmaia.com/riot/health
```

## 📊 Estrutura de Portas

| App | Frontend | Backend |
|-----|----------|---------|
| Neo-App | 5173 | 8000 |
| R-IoT | 5174 | 8001 |

## ⚠️ Troubleshooting

### Erro 502 Bad Gateway
- Verifique se o R-IoT está rodando: `curl http://localhost:8001/health`
- Verifique logs: `tail -f /var/log/nginx/error.log`

### Erro 504 Gateway Timeout
- Aumente timeout no nginx (já configurado para 300s)
- Verifique se backend está respondendo

### CORS Error
- Configure `ALLOWED_ORIGINS` corretamente
- Verifique logs do backend: `tail -f backend-error.log`
