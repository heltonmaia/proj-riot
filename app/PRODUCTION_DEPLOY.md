# Deploy em Produção - R-IoT

## 🚀 Passos para Deploy

Execute estes comandos **no servidor**:

### 1. Pare o modo desenvolvimento

```bash
cd /home/heltonmaia/work/github-projects/proj-riot/app
./stop.sh
```

### 2. Configure variáveis de ambiente

```bash
# CORS para aceitar o domínio
export ALLOWED_ORIGINS="https://playground.heltonmaia.com"

# Para tornar permanente, adicione ao .bashrc
echo 'export ALLOWED_ORIGINS="https://playground.heltonmaia.com"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Faça build do frontend

```bash
cd /home/heltonmaia/work/github-projects/proj-riot/app/frontend
npm run build
```

Isso criará a pasta `dist/` com os arquivos estáticos otimizados.

### 4. Atualize configuração do Nginx

Edite o arquivo do nginx:

```bash
sudo nano /etc/nginx/sites-available/playground
```

**Substitua** a seção do R-IoT por esta configuração (serve arquivos estáticos):

```nginx
# ====== R-IOT APP ======
# Frontend R-IoT (arquivos estáticos da build)
location /riot/ {
    alias /home/heltonmaia/work/github-projects/proj-riot/app/frontend/dist/;
    try_files $uri $uri/ /riot/index.html;

    # Cache para assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
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

### 5. Teste e recarregue o Nginx

```bash
# Testar configuração
sudo nginx -t

# Se OK, recarregar
sudo systemctl reload nginx
```

### 6. Inicie o backend em produção

```bash
cd /home/heltonmaia/work/github-projects/proj-riot/app
./start.sh prod
```

### 7. Verifique

```bash
# Backend rodando?
lsof -i :8001
curl http://localhost:8001/health

# Teste através do nginx
curl https://playground.heltonmaia.com/riot/health
```

### 8. Acesse no navegador

**https://playground.heltonmaia.com/riot/**

---

## 🔄 Para atualizar depois de mudanças no código

```bash
cd /home/heltonmaia/work/github-projects/proj-riot/app

# 1. Pare o backend
./stop.sh

# 2. Se mudou o frontend, rebuild
cd frontend
npm run build

# 3. Se mudou o backend, pull do git
cd ..
git pull

# 4. Reinicie
./start.sh prod
```

---

## 📊 Status dos Apps

| App | Frontend | Backend | Modo |
|-----|----------|---------|------|
| Neo-App | Dev (5173) | Dev (8000) | Desenvolvimento |
| R-IoT | Build estático | Prod (8001) | **Produção** |

---

## 🐛 Troubleshooting

### Erro 404 em /riot/
```bash
# Verifique se a build existe
ls -la /home/heltonmaia/work/github-projects/proj-riot/app/frontend/dist/

# Verifique permissões
chmod -R 755 /home/heltonmaia/work/github-projects/proj-riot/app/frontend/dist/
```

### Erro 502 Bad Gateway
```bash
# Backend não está rodando
lsof -i :8001

# Reinicie
cd /home/heltonmaia/work/github-projects/proj-riot/app
./start.sh prod
```

### Assets não carregam (404)
```bash
# Verifique se o base path está correto
cat frontend/vite.config.ts | grep "base:"

# Deve mostrar: base: isProduction ? '/riot/' : '/',
```

### CORS Error
```bash
# Configure ALLOWED_ORIGINS
export ALLOWED_ORIGINS="https://playground.heltonmaia.com"

# Reinicie backend
./stop.sh
./start.sh prod
```

---

## 📝 Logs

```bash
# Backend (produção)
tail -f /home/heltonmaia/work/github-projects/proj-riot/app/backend-access.log
tail -f /home/heltonmaia/work/github-projects/proj-riot/app/backend-error.log

# Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```
