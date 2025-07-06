# RIOT GEMINI - Sistema de Análise de Vídeos de Animais de Fazenda

Sistema inteligente para análise de vídeos de animais de fazenda usando a API do Google Gemini, com geração automática de legendas educativas.

## 🚀 Funcionalidades

- **Análise Individual**: Analisa um vídeo específico e gera legendas SRT
- **Processamento em Lote**: Processa todos os vídeos de um diretório automaticamente
- **Mesclagem de Vídeos**: Combina múltiplos vídeos em um único arquivo
- **Adição de Legendas**: Incorpora legendas SRT aos vídeos usando FFmpeg
- **Processamento Completo**: Análise + geração de legendas + incorporação em um só processo
- **Configuração Flexível**: Sistema de configuração via arquivo YAML

## 📋 Pré-requisitos

- Python 3.8+
- FFmpeg instalado no sistema
- API Key do Google Gemini

### Dependências Python

```bash
pip install google-generativeai opencv-python pillow pyyaml
```

### Instalação do FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Baixe de [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd riot_gemini
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure sua API Key do Google Gemini:
   - Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Crie uma nova API Key
   - Execute o programa e use a opção "Configurar API Key"

## 🎯 Como Usar

### Execução do Programa

```bash
python riot_gemini.py
```

### Menu Principal

O programa apresenta um menu interativo com as seguintes opções:

1. **Configurar API Key** - Define sua chave de API do Gemini
2. **Analisar vídeo individual** - Processa um vídeo específico
3. **Analisar todos os vídeos de um diretório** - Processa múltiplos vídeos
4. **Mesclar vídeos** - Combina vídeos em um arquivo único
5. **Adicionar legendas aos vídeos** - Incorpora legendas SRT aos vídeos
6. **Processar vídeos em lote** - Análise completa (IA + legendas)
7. **Ver configuração atual** - Exibe configurações do sistema
8. **Sair** - Encerra o programa

### Estrutura de Diretórios

```
riot_gemini/
├── src/                    # Código fonte
│   ├── __init__.py
│   ├── config_manager.py   # Gerenciamento de configurações
│   ├── video_analyzer.py   # Análise de vídeos com IA
│   ├── video_merger.py     # Mesclagem e processamento
│   └── menu.py            # Interface do menu
├── videos/                 # Vídeos de entrada
├── results/               # Vídeos processados
├── tmp/                   # Arquivos temporários
├── config.yaml           # Configurações
├── riot_gemini.py        # Programa principal
└── README.md
```

## ⚙️ Configuração

O arquivo `config.yaml` permite personalizar:

```yaml
api_key: "sua-api-key-aqui"
model: "gemini-2.5-flash-preview-05-20"
video_dir: "videos/"
output_dir: "results/"
tmp_dir: "tmp/"
num_frames: 8
ffmpeg_path: "ffmpeg"
```

### Parâmetros de Configuração

- **api_key**: Sua chave de API do Google Gemini
- **model**: Modelo do Gemini a ser usado
- **video_dir**: Diretório padrão para vídeos de entrada
- **output_dir**: Diretório para vídeos processados
- **tmp_dir**: Diretório para arquivos temporários
- **num_frames**: Número de frames extraídos para análise
- **ffmpeg_path**: Caminho para o executável do FFmpeg

## 📹 Formatos Suportados

### Vídeos
- MP4
- AVI
- MOV
- MKV

### Legendas
- SRT (gerado automaticamente)

## 🔧 Desenvolvimento

### Estrutura do Código

- **VideoAnalyzer**: Classe responsável pela análise de vídeos usando IA
- **VideoMerger**: Classe para mesclagem e processamento de vídeos
- **ConfigManager**: Gerenciamento de configurações e validações
- **Menu**: Interface de usuário interativa

### Adicionando Novos Recursos

1. Crie novos módulos em `src/`
2. Atualize o menu em `src/menu.py`
3. Adicione configurações necessárias em `config.yaml`
4. Atualize este README

## 🐛 Solução de Problemas

### Erro: "No module named 'google.generativeai'"
```bash
pip install google-generativeai
```

### Erro: "ffmpeg: command not found"
Instale o FFmpeg seguindo as instruções de pré-requisitos.

### Erro de API Key
- Verifique se a API Key está configurada corretamente
- Certifique-se de que a chave tem permissões adequadas
- Verifique se há créditos disponíveis na conta

### Vídeos não processados
- Verifique se os arquivos estão nos formatos suportados
- Confirme se os diretórios existem e têm permissões adequadas
- Verifique se há espaço suficiente em disco

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 👨‍💻 Autor

**Helton Maia**
- Desenvolvedor do sistema RIOT GEMINI
- Especialista em processamento de vídeo e IA

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Entre em contato com o autor

---

**RIOT GEMINI** - Transformando vídeos de animais de fazenda em conteúdo educativo com IA! 🐄🤖 