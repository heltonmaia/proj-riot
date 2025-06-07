#!/usr/bin/env python3
"""
Script simples para treinar YOLOv8 Large Pose Estimation
Aponta para seu arquivo .yaml do dataset
"""

from ultralytics import YOLO
import torch

# ==================== CONFIGURAÇÕES ====================
# Caminho para seu arquivo .yaml do dataset
DATASET_CONFIG = "/media/heltonmaia/HD2/datasets/cow-pose-estimation.v1i.yolov8/data.yaml"

# Parâmetros de treinamento
EPOCHS = 100
BATCH_SIZE = 16
IMG_SIZE = 640
DEVICE = 'auto'  # 'auto', 'cpu', '0', '1', etc.
LEARNING_RATE = 0.01
OPTIMIZER = 'AdamW'  # SGD, Adam, AdamW, NAdam, RAdam, RMSProp

# Configurações de salvamento
PROJECT_NAME = "pose_training"
EXPERIMENT_NAME = "yolov8l_pose"
SAVE_PERIOD = 10  # Salvar modelo a cada N épocas

# ========================================================

def main():
    """Função principal de treinamento"""
    
    # Verifica se CUDA está disponível
    print(f"PyTorch versão: {torch.__version__}")
    print(f"CUDA disponível: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
    
    # Carrega o modelo YOLOv8 Large Pose pré-treinado
    print("\n📥 Carregando YOLOv8 Large Pose...")
    model = YOLO('yolov8l-pose.pt')
    
    # Configurações de treinamento
    print("\n🚀 Iniciando treinamento...")
    print(f"Dataset: {DATASET_CONFIG}")
    print(f"Épocas: {EPOCHS}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Tamanho da imagem: {IMG_SIZE}")
    print(f"Device: {DEVICE}")
    print(f"Learning rate: {LEARNING_RATE}")
    print(f"Otimizador: {OPTIMIZER}")
    
    # Treina o modelo
    results = model.train(
        data=DATASET_CONFIG,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        device=DEVICE,
        batch=BATCH_SIZE,
        lr0=LEARNING_RATE,
        optimizer=OPTIMIZER,
        project=PROJECT_NAME,
        name=EXPERIMENT_NAME,
        save_period=SAVE_PERIOD,
        patience=50,
        exist_ok=True,
        pretrained=True,
        val=True,
        plots=True,
        verbose=True
    )
    
    print("\n✅ Treinamento concluído!")
    print(f"Modelo salvo em: {model.trainer.save_dir}")
    
    # Validação final
    print("\n📊 Executando validação final...")
    metrics = model.val()
    
    # Mostra métricas finais
    print(f"\n📈 Métricas finais:")
    try:
        if hasattr(metrics, 'box'):
            print(f"Box mAP50: {metrics.box.map50:.4f}")
            print(f"Box mAP50-95: {metrics.box.map:.4f}")
        if hasattr(metrics, 'pose'):
            print(f"Pose mAP50: {metrics.pose.map50:.4f}")
            print(f"Pose mAP50-95: {metrics.pose.map:.4f}")
    except:
        print("Métricas disponíveis:", dir(metrics))
    
    print(f"\n🎉 Treinamento finalizado!")
    print(f"Melhor modelo salvo em: {model.trainer.best}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Treinamento interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o treinamento: {str(e)}")
        raise