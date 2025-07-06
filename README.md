## Estrutura do Projeto

```
proj-riot/
├── dataset/
│   ├── pose_estimation/
│   └── segmentation/
│       └── raw/
│           └── processed/
├── docs/
├── models/
│   ├── LLMs/
│   │   ├── gemini/
│   │   │   ├── install.sh
│   │   │   ├── README.md
│   │   │   ├── requirements.txt
│   │   │   ├── riot_gemini.py
│   │   │   ├── run.sh
│   │   │   ├── src/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── config_manager.py
│   │   │   │   ├── menu.py
│   │   │   │   ├── video_analyzer.py
│   │   │   │   └── video_merger.py
│   │   │   ├── results/
│   │   │   ├── tmp/
│   │   │   └── videos/
│   │   └── ... (outros LLMs podem ser adicionados aqui)
│   └── yolo_train_infer/
│       ├── pose_estimation/
│       └── segmentation/
│           └── yolo11/
│               └── Segundo_Treinamento/
│                   └── runs/
│                       └── segment/
│                           └── train/
│               └── Terceiro_Treinamento/
│                   └── riot_tracking_seg/
│                       └── exp3/
│           ├── yolo_predict_seg.py
│           └── yolo_predict_seg2.py
├── pipelines/
├── pyproject.toml
├── README.md
├── tests/
└── utils/
```

- A pasta `models/LLMs/` agora contém integrações de modelos de linguagem, como o Gemini, com scripts, dependências e exemplos de uso.
- Outras pastas importantes: `dataset/` (dados), `models/yolo_train_infer/` (modelos de visão computacional), `pipelines/`, `tests/`, `utils/`.

[Website](https://r-iot.ufrn.br/)

### Folder Descriptions

* `dataset/`: Datasets for segmentation and pose estimation tasks.
* `models/`: Training and inference files for various models.
* `pipelines/`: Processing pipelines and orchestration scripts.
* `tests/`: Unit and integration tests.
* `utils/`: Utility functions and helper scripts.
* `config.yaml`: Main configuration file.
* `pyproject.toml`: Project metadata and build configuration.

## Instalação de dependências com uv

Para instalar todas as dependências do projeto usando [uv](https://github.com/astral-sh/uv), execute:

```sh
uv pip install --requirement pyproject.toml
```

### Criando o ambiente com uv

Se ainda não possui o uv instalado, instale-o com:

```sh
pip install uv
```

Crie um ambiente virtual (recomendado):

```sh
python -m venv .venv
source .venv/bin/activate
```

Agora, instale as dependências do projeto usando o uv:

```sh
uv pip install --requirement pyproject.toml
```

