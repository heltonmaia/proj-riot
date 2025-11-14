# 🚀 Deploy - R-IoT

Guia completo para deploy em produção do R-IoT.

---

## ⚡ TL;DR - Deploy Rápido

**Execute no servidor:**

```bash
cd /home/heltonmaia/work/github-projects/proj-riot/app
./deploy.sh
```

Esse comando faz tudo automaticamente!

**Primeira vez?** Configure o NGINX também (veja seção "Configuração NGINX" abaixo).

---

## 📋 O que o script `deploy.sh` faz?

1. ✓ Para os serviços (frontend/backend)
2. ✓ Atualiza código do repositório (`git pull`)
3. ✓ **Faz build do frontend** (cria pasta `dist/`)
4. ✓ Configura CORS para produção
5. ✓ Inicia backend em modo produção (Gunicorn)
6. ✓ Verifica se tudo está rodando

---

## 🔄 Workflow Completo

### 1. Desenvolvimento Local

```bash
cd /home/heltonmaia/work/github-projects/proj-riot/app

# Inicia em modo desenvolvimento (frontend + backend)
./start.sh dev

# Acesse: http://localhost:5174
```

### 2. Commit e Push

```bash
git add .
git commit -m "sua mensagem"
git push
```

### 3. Deploy no Servidor

```bash
# SSH no servidor
ssh seu-servidor

# Navegue até a pasta
cd /home/heltonmaia/work/github-projects/proj-riot/app

# Execute o deploy
./deploy.sh
```

### 4. Verifique

Acesse: **https://playground.heltonmaia.com/riot/**

---

## 📊 Diferenças Dev vs Produção

| Item | Desenvolvimento | Produção |
|------|----------------|----------|
| **Comando** | `./start.sh dev` | `./deploy.sh` |
| **Frontend** | Dev server (porta 5174) | Build estático (`dist/`) |
| **Backend** | Uvicorn (reload) | Gunicorn (4 workers) |
| **URL** | http://localhost:5174 | https://playground.heltonmaia.com/riot/ |
| **API URL** | http://localhost:8001 | /riot (relativo) |
| **CORS** | Permissivo (*) | Restritivo (domínio específico) |
| **Base path** | `/` | `/riot/` |

---

## ⚙️ Configuração NGINX (Primeira vez)

**Execute apenas na PRIMEIRA VEZ ou quando alterar o domínio.**

### 1. Edite a configuração do NGINX

```bash
sudo nano /etc/nginx/sites-available/playground
```

### 2. Adicione/Substitua a seção do R-IoT

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

### 3. Teste e recarregue o NGINX

```bash
# Testar configuração
sudo nginx -t

# Se OK, recarregar
sudo systemctl reload nginx
```

---

## 🛠️ Deploy Manual (se preferir)

Se não quiser usar `./deploy.sh`, pode fazer manualmente:

```bash
cd /home/heltonmaia/work/github-projects/proj-riot/app

# 1. Parar serviços
./stop.sh

# 2. Atualizar código
git pull

# 3. Build do frontend
cd frontend
npm run build
cd ..

# 4. Configurar CORS
export ALLOWED_ORIGINS="https://playground.heltonmaia.com"

# 5. Iniciar backend em produção
./start.sh prod
```

---

## 🐛 Troubleshooting

### Erro 404 em /riot/

**Causa:** Pasta `dist/` não existe

```bash
# Verifique se a build existe
ls -la /home/heltonmaia/work/github-projects/proj-riot/app/frontend/dist/

# Se não existir, faça o build
cd frontend
npm run build
cd ..
```

### Erro 502 Bad Gateway

**Causa:** Backend não está rodando

```bash
# Verifique se backend está rodando
lsof -i :8001

# Se não estiver, reinicie
./deploy.sh
```

### CORS Error

**Causa:** CORS não configurado

```bash
# Configure e reinicie
export ALLOWED_ORIGINS="https://playground.heltonmaia.com"
./stop.sh
./start.sh prod
```

### Assets não carregam (404 em JS/CSS)

**Causa:** Base path incorreto no build

```bash
# Verifique o vite.config.ts
cat frontend/vite.config.ts | grep "base:"

# Deve mostrar:
# base: isProduction ? '/riot/' : '/',

# Se estiver errado, corrija e faça rebuild
cd frontend
npm run build
cd ..
```

### Mudanças não aparecem após deploy

**Causa:** Cache do navegador ou build não foi feito

```bash
# 1. Force rebuild
cd frontend
rm -rf dist node_modules/.vite
npm run build
cd ..

# 2. No navegador: Ctrl + Shift + R (hard refresh)
```

---

## 📝 Logs

### Backend (produção)

```bash
# Access logs
tail -f backend-access.log

# Error logs
tail -f backend-error.log
```

### NGINX

```bash
# Error logs
sudo tail -f /var/log/nginx/error.log

# Access logs
sudo tail -f /var/log/nginx/access.log
```

---

## 🔧 Comandos Úteis

### Verificar status

```bash
# Backend rodando?
lsof -i :8001

# Health check
curl http://localhost:8001/health

# Teste via nginx
curl https://playground.heltonmaia.com/riot/health
```

### Parar/Iniciar

```bash
# Parar todos os serviços
./stop.sh

# Desenvolvimento
./start.sh dev

# Produção
./start.sh prod

# Deploy completo (recomendado)
./deploy.sh
```

### Limpar processos órfãos

```bash
# Matar processos nas portas
kill -9 $(lsof -t -i:8001)  # Backend
kill -9 $(lsof -t -i:5174)  # Frontend dev
```

---

## ⚠️ Importante

1. **Fazer `git push` NÃO faz deploy automático!**
   - Você precisa executar `./deploy.sh` no servidor

2. **Build é necessário em produção**
   - Frontend precisa ser buildado para gerar arquivos estáticos em `dist/`

3. **Diferentes portas para diferentes apps**
   - Neo-App: 8000 (backend), 5173 (frontend)
   - R-IoT: 8001 (backend), 5174 (frontend)

4. **CORS precisa estar configurado**
   - Use `export ALLOWED_ORIGINS="https://playground.heltonmaia.com"`
   - Ou adicione ao `.bashrc` para tornar permanente

---

## 📊 Checklist de Deploy

- [ ] Código commitado e pushed para o repositório
- [ ] SSH no servidor
- [ ] Executado `./deploy.sh`
- [ ] NGINX configurado (apenas primeira vez)
- [ ] Verificado `https://playground.heltonmaia.com/riot/`
- [ ] Testado funcionalidades principais
- [ ] Checado logs para erros

---

**Dúvidas?** Verifique os logs em `backend-error.log` ou logs do NGINX.
