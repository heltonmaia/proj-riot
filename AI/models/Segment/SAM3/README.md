# SAM3 Video Segmentation

Segmentação de vídeo utilizando o modelo SAM3 com prompts de texto.

O pipeline realiza inferência frame a frame em vídeos, gerando máscaras segmentadas sobrepostas no vídeo de saída.

---

## Exemplo

Entrada:
- vídeo contendo bovinos

Saída:
- vídeo segmentado com máscaras sobre os objetos detectados

---

## Requisitos

- Python 3.11
- GPU NVIDIA recomendada
- CUDA compatível com PyTorch

Instalação das dependências:

```bash
pip install -U ultralytics
```

---

## Modelo

Baixe o peso `sam3.pt` e ajuste o caminho no código:

```python
WEIGHTS_PATH = "CAMINHO_DO_MODELO/sam3.pt"
```

---

## Configuração

Defina os caminhos principais:

```python
INPUT_VIDEO = "CAMINHO_DO_VIDEO/video.mp4"

OUTPUT_VIDEO = "CAMINHO_DE_SAIDA/video_segmentado.mp4"
```

Prompts utilizados:

```python
TEXT_PROMPTS = ["cow"]
```

---

## Execução

```bash
python sam3_video_segment.py
```

---

## Observações sobre desempenho

Foram realizados testes de inferência utilizando vídeos de aproximadamente 1 minuto.

| Modelo | Video 1 | Video 2 |
|---|---|---|
| SAM3 | 89.4 s | 86.3 s |
| RFDETR | 19.0 s | 19.5 s |
| YOLO26 | 12.7 s | 12.9 s |
---

## Considerações

O SAM3 apresentou maior custo computacional em comparação aos modelos RFDETR e YOLO26 utilizados nos testes.

Entretanto, o principal diferencial do SAM3 está na capacidade de realizar segmentação em modo zero-shot, dispensando treinamento adicional e a necessidade de construção/anotação de datasets específicos para a aplicação.

Já os modelos RFDETR e YOLO26 utilizados na comparação foram previamente treinados com um dataset próprio, exigindo etapas adicionais de coleta, anotação e treinamento.

Também foi observado que vídeos com menor taxa de quadros (FPS) tendem a resultar em tempos de inferência significativamente menores.