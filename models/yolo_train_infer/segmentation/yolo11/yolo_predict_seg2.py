# Predict usando GPU ou CPU local
from ultralytics import YOLO
import cv2
import numpy as np
from tqdm import tqdm
import os
import shutil
import torch

# Verificar se a GPU está disponível
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Usando dispositivo: {device}")

# Carregar o modelo YOLO treinado para segmentação
model = YOLO('best.pt')
model.to(device)

# Caminhos dos vídeos
input_video_path = "videos_inf/VacasEmLactacaoAlimentacao_low.mp4"
input_base_name = os.path.splitext(os.path.basename(input_video_path))[0]

# Pasta para salvar os resultados
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
output_video_path = os.path.join(output_dir, f"{input_base_name}_segmented.mp4")
masks_dir = os.path.join(output_dir, f"{input_base_name}_masks")
os.makedirs(masks_dir, exist_ok=True)

# Copiar o vídeo de entrada
shutil.copy(input_video_path, os.path.join(output_dir, os.path.basename(input_video_path)))

# Carregar o vídeo
cap = cv2.VideoCapture(input_video_path)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Configurar o vídeo de saída
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, cap.get(cv2.CAP_PROP_FPS),
                     (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# Inicializar a barra de progresso
progress_bar = tqdm(total=total_frames, desc="Processando frames", unit="frame", leave=True)

# Processar frames
current_frame = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    current_frame += 1
    progress_bar.update(1)

    # Garantir que as dimensões do frame sejam múltiplos de 32
    height, width = frame.shape[:2]
    new_height = (height // 32) * 32
    new_width = (width // 32) * 32
    resized_frame = cv2.resize(frame, (new_width, new_height))

    # Realizar a predição
    results = model(resized_frame, verbose=False)

    # Criar uma cópia do frame para desenhar a máscara
    frame_with_mask = frame.copy()

    if len(results[0].boxes.conf) > 0:  # Verificar se há detecções
        # Encontrar a detecção com maior confiança
        confidences = results[0].boxes.conf.cpu().numpy()
        max_conf_idx = np.argmax(confidences)
        
        # Obter a máscara correspondente à detecção de maior confiança
        masks = results[0].masks
        if masks is not None and len(masks.data) > 0:
            # Obter a máscara e redimensioná-la para o tamanho original do frame
            best_mask = masks.data[max_conf_idx].cpu().numpy()
            best_mask = cv2.resize(best_mask, (width, height))
            
            # Criar máscara colorida (por exemplo, vermelho semi-transparente)
            colored_mask = np.zeros_like(frame)
            colored_mask[best_mask > 0.5] = [0, 0, 255]  # Vermelho para a máscara
            
            # Sobrepor a máscara ao frame com transparência
            frame_with_mask = cv2.addWeighted(frame_with_mask, 1, colored_mask, 0.5, 0)
            
            # Salvar a máscara como arquivo NumPy
            npy_filename = os.path.join(masks_dir, f"frame_{current_frame}.npy")
            np.save(npy_filename, best_mask)

    # Escrever o frame com a máscara no vídeo de saída
    out.write(frame_with_mask)

# Fechar a barra de progresso
progress_bar.close()

# Liberar os recursos
cap.release()
out.release()

# Mensagem final
print(f"Vídeo de entrada copiado para: {os.path.join(output_dir, os.path.basename(input_video_path))}")
print(f"Vídeo com segmentação salvo em: {output_video_path}")
print(f"Máscaras salvas no formato NumPy na pasta: {masks_dir}")
