# Importando biblioteca do YOLO
from ultralytics import YOLO

# Como o dataset ja esta baixado, a parte de baixar vai ser pulada
# Carregando o modelo do YOLO11 para segmentacao de imagens
model = YOLO ('yolo11x-seg.pt')

# Treinamento do modelo
model.train(data='/home/helton/datasets/rIoT.v3i.yolov11/data.yaml', epochs=100, batch=4, imgsz=640)
