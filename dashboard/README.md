# R-IoT - Rural Internet of Things

Sistema de monitoramento de gado com GPS usando Panel para visualização em tempo real.

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como executar

### Executar a aplicação R-IoT:
```bash
panel serve app_riot.py --show --autoreload
```

### Executar aplicação anterior:
```bash
panel serve app.py --show --autoreload
```

### Executar o script de mapa simples (original):
```bash
python mapa.py
```

## Funcionalidades

- 🗺️ Mapa interativo do Rio Grande do Norte
- 📍 Monitoramento de 17 vacas com GPS em 2 localizações:
  - Escola Agrícola de Jundiaí: 10 vacas
  - UFRN Campus Natal: 7 vacas
- 📊 Estatísticas do rebanho em tempo real
- 🎛️ Controles para ajustar visualização do mapa
- 🔧 Ferramentas de medição de distância e localização
- 📱 Interface responsiva usando Panel
- 🌍 Múltiplas camadas de mapa (OpenStreetMap, Terrain, CartoDB)

## Estrutura do projeto

- `app_riot.py` - Aplicação R-IoT principal
- `app.py` - Aplicação Panel anterior
- `mapa.py` - Script original com mapa simples
- `requirements.txt` - Dependências do projeto
- `vacas_jundai.html` - Mapa HTML gerado pelo script original