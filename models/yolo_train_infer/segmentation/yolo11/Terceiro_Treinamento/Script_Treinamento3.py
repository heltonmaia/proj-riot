import ultralytics
ultralytics.checks()

#treino para segmentacao
from ultralytics import YOLO

# Carregue o modelo YOLO pré-treinado para segmentação
model = YOLO('yolo11x-seg.pt')

# Treine o modelo usando o dataset configurado
model.train(
    data="/home/helton/datasets/rIoT.v4i.yolov11/data.yaml",
    epochs=100,
    batch=4,
    imgsz=640,
    task='segment',
    patience=10,  # Early stopping patience
    save=True,    # Save best checkpoint
    save_period=5,  # Save checkpoint every N epochs
    cache=False,  # Cache images in memory
    device='0',   # Use GPU if available
    workers=8,    # Number of worker threads
    project='riot_tracking_seg',  # Project name
    name='exp3',  # Experiment name
    exist_ok=True,  # Overwrite existing experiment
    pretrained=True,  # Use pretrained weights
    optimizer='auto',  # Optimizer (SGD, Adam, etc.)
    verbose=True,  # Print verbose output
    seed=42,  # Random seed for reproducibility
    deterministic=True,  # Use deterministic training
    amp=True  # Use mixed precision training
)
