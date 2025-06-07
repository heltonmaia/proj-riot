#!/usr/bin/env python3
"""
Script simples para fazer inferência com YOLOv8 Pose Estimation
Testa uma imagem e salva o resultado com esqueleto conectado
"""

from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path

# ==================== CONFIGURAÇÕES ====================
# Caminho para seu modelo treinado
MODEL_PATH = "pose_training/yolov8l_pose/weights/best.pt"

# Imagem de teste
IMAGE_PATH = "6.jpg"

# Onde salvar o resultado
OUTPUT_DIR = "resultados_inferencia"

# Parâmetros de inferência
CONFIDENCE = 0.5  # Confiança mínima
IMG_SIZE = 640    # Tamanho da imagem para inferência
DEVICE = 'cpu'    # 'cpu', '0', '1', etc. (mudado para cpu)

# ========================================================

def draw_custom_skeleton(img, keypoints, confidence_threshold=0.5):
    """
    Desenha esqueleto personalizado para VACAS (quadrúpedes)
    
    Keypoints típicos para animais quadrúpedes (varia conforme dataset):
    Exemplo comum para bovinos:
    0: nose/focinho, 1: left_eye, 2: right_eye, 3: left_ear, 4: right_ear,
    5: neck/pescoço, 6: back/lombo, 7: tail_base/base_cauda,
    8: left_front_shoulder, 9: left_front_elbow, 10: left_front_knee, 11: left_front_hoof,
    12: right_front_shoulder, 13: right_front_elbow, 14: right_front_knee, 15: right_front_hoof,
    16: left_back_hip, 17: left_back_knee, 18: left_back_hock, 19: left_back_hoof,
    20: right_back_hip, 21: right_back_knee, 22: right_back_hock, 23: right_back_hoof
    
    AJUSTE OS ÍNDICES CONFORME SEU DATASET!
    """
    
    # Definição das conexões do esqueleto para VACA
    skeleton = [
        # Cabeça
        [0, 1], [0, 2],  # focinho -> olhos
        [1, 3], [2, 4],  # olhos -> orelhas
        [0, 5],          # focinho -> pescoço
        
        # Espinha dorsal
        [5, 6], [6, 7],  # pescoço -> lombo -> base da cauda
        
        # Pata dianteira esquerda
        [5, 8], [8, 9], [9, 10], [10, 11],  # pescoço -> ombro -> cotovelo -> joelho -> casco
        
        # Pata dianteira direita  
        [5, 12], [12, 13], [13, 14], [14, 15],  # pescoço -> ombro -> cotovelo -> joelho -> casco
        
        # Pata traseira esquerda
        [6, 16], [16, 17], [17, 18], [18, 19],  # lombo -> quadril -> joelho -> jarrete -> casco
        
        # Pata traseira direita
        [6, 20], [20, 21], [21, 22], [22, 23],  # lombo -> quadril -> joelho -> jarrete -> casco
        
        # Conexão do tronco
        [8, 12], [16, 20]  # conecta ombros e quadris
    ]
    
    # Cores para diferentes partes da vaca (BGR)
    colors = {
        'head': (0, 255, 255),        # Amarelo - cabeça
        'spine': (255, 0, 0),         # Azul - espinha
        'front_left': (0, 255, 0),    # Verde - pata dianteira esquerda
        'front_right': (0, 128, 255), # Laranja - pata dianteira direita
        'back_left': (255, 0, 128),   # Rosa - pata traseira esquerda
        'back_right': (128, 0, 255),  # Roxo - pata traseira direita
        'body': (255, 255, 0)         # Ciano - corpo/tronco
    }
    
    # Mapeia cada conexão para uma cor
    connection_colors = [
        # Cabeça (5 conexões)
        colors['head'], colors['head'], colors['head'], colors['head'], colors['head'],
        # Espinha (2 conexões)
        colors['spine'], colors['spine'],
        # Pata dianteira esquerda (4 conexões)
        colors['front_left'], colors['front_left'], colors['front_left'], colors['front_left'],
        # Pata dianteira direita (4 conexões)
        colors['front_right'], colors['front_right'], colors['front_right'], colors['front_right'],
        # Pata traseira esquerda (4 conexões)
        colors['back_left'], colors['back_left'], colors['back_left'], colors['back_left'],
        # Pata traseira direita (4 conexões)
        colors['back_right'], colors['back_right'], colors['back_right'], colors['back_right'],
        # Tronco (2 conexões)
        colors['body'], colors['body']
    ]
    
    # Para cada vaca detectada
    for animal_kpts in keypoints:
        if len(animal_kpts.shape) == 2:
            # Desenha as conexões (linhas do esqueleto)
            for i, (start_idx, end_idx) in enumerate(skeleton):
                # Verifica se os índices existem no array de keypoints
                if (start_idx < len(animal_kpts) and end_idx < len(animal_kpts) and
                    animal_kpts[start_idx][2] > confidence_threshold and 
                    animal_kpts[end_idx][2] > confidence_threshold):
                    
                    start_point = (int(animal_kpts[start_idx][0]), int(animal_kpts[start_idx][1]))
                    end_point = (int(animal_kpts[end_idx][0]), int(animal_kpts[end_idx][1]))
                    
                    # Desenha a linha
                    color_idx = min(i, len(connection_colors) - 1)
                    cv2.line(img, start_point, end_point, connection_colors[color_idx], 4)
            
            # Desenha os keypoints como círculos
            for i, (x, y, conf) in enumerate(animal_kpts):
                if conf > confidence_threshold:
                    center = (int(x), int(y))
                    
                    # Cor do keypoint baseada na parte do corpo
                    if i in [0, 1, 2, 3, 4]:  # cabeça
                        color = colors['head']
                    elif i in [5, 6, 7]:  # espinha
                        color = colors['spine']
                    elif i in [8, 9, 10, 11]:  # pata dianteira esquerda
                        color = colors['front_left']
                    elif i in [12, 13, 14, 15]:  # pata dianteira direita
                        color = colors['front_right']
                    elif i in [16, 17, 18, 19]:  # pata traseira esquerda
                        color = colors['back_left']
                    elif i in [20, 21, 22, 23]:  # pata traseira direita
                        color = colors['back_right']
                    else:
                        color = (255, 255, 255)  # branco por padrão
                    
                    # Desenha círculo preenchido
                    cv2.circle(img, center, 10, color, -1)
                    # Desenha borda preta
                    cv2.circle(img, center, 10, (0, 0, 0), 3)
                    
                    # Adiciona número do keypoint para debug
                    cv2.putText(img, str(i), (center[0]-5, center[1]+5), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return img

def main():
    """Função principal de inferência"""
    
    # Detecta automaticamente o device disponível
    import torch
    if torch.cuda.is_available():
        device = '0'  # Primeira GPU
        print(f"🚀 Usando GPU: {torch.cuda.get_device_name(0)}")
    else:
        device = 'cpu'
        print("🖥️ Usando CPU")
    
    # Verifica se os arquivos existem
    if not Path(MODEL_PATH).exists():
        print(f"❌ Modelo não encontrado: {MODEL_PATH}")
        print("💡 Certifique-se de ter treinado o modelo primeiro!")
        return
    
    if not Path(IMAGE_PATH).exists():
        print(f"❌ Imagem não encontrada: {IMAGE_PATH}")
        return
    
    # Cria diretório de saída
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    # Carrega o modelo treinado
    print(f"📥 Carregando modelo: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)
    
    # Carrega a imagem original para desenho personalizado
    original_img = cv2.imread(IMAGE_PATH)
    if original_img is None:
        print(f"❌ Erro ao carregar imagem: {IMAGE_PATH}")
        return
    
    # Carrega a imagem
    print(f"🖼️ Processando imagem: {IMAGE_PATH}")
    
    # Faz a predição
    results = model.predict(
        source=IMAGE_PATH,
        conf=CONFIDENCE,
        imgsz=IMG_SIZE,
        device=device,  # Usa o device detectado automaticamente
        save=False,
        verbose=True
    )
    
    # Processa os resultados
    for i, result in enumerate(results):
        # Nome do arquivo de saída
        input_name = Path(IMAGE_PATH).stem
        
        # Salva duas versões: padrão do YOLO e personalizada
        output_path_default = Path(OUTPUT_DIR) / f"{input_name}_yolo_default.jpg"
        output_path_custom = Path(OUTPUT_DIR) / f"{input_name}_esqueleto_vaca.jpg"
        
        # 1. Resultado padrão do YOLO
        # 1. Resultado padrão do YOLO
        annotated_img = result.plot(
            conf=True,        # Mostra confiança
            line_width=3,     # Espessura das linhas do esqueleto
            font_size=12,     # Tamanho da fonte
            pil=False,        # Retorna como numpy array
            kpt_radius=5,     # Tamanho dos keypoints
            boxes=True,       # Mostra caixas delimitadoras
            labels=True       # Mostra labels
        )
        
        # Salva resultado padrão
        cv2.imwrite(str(output_path_default), annotated_img)
        print(f"✅ Resultado padrão salvo: {output_path_default}")
        
        # 2. Resultado personalizado com esqueleto colorido
        custom_img = original_img.copy()
        
        # Desenha esqueleto personalizado se há keypoints
        if result.keypoints is not None and len(result.keypoints.data) > 0:
            # Redimensiona keypoints se necessário (YOLO pode ter redimensionado a imagem)
            h_orig, w_orig = original_img.shape[:2]
            
            keypoints_data = result.keypoints.data.cpu().numpy()
            
            # Se a imagem foi redimensionada durante a inferência, ajusta as coordenadas
            if hasattr(result, 'orig_shape'):
                h_pred, w_pred = result.orig_shape
                if h_orig != h_pred or w_orig != w_pred:
                    scale_x = w_orig / w_pred
                    scale_y = h_orig / h_pred
                    keypoints_data[:, :, 0] *= scale_x  # x coordinates
                    keypoints_data[:, :, 1] *= scale_y  # y coordinates
            
            custom_img = draw_custom_skeleton(custom_img, keypoints_data, CONFIDENCE)
            
            # Adiciona caixas delimitadoras se existirem
            if result.boxes is not None:
                for box in result.boxes.data:
                    x1, y1, x2, y2, conf, cls = box.cpu().numpy()
                    if conf > CONFIDENCE:
                        # Desenha caixa
                        cv2.rectangle(custom_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                        # Adiciona texto de confiança
                        text = f'Cow {conf:.2f}'
                        cv2.putText(custom_img, text, (int(x1), int(y1-10)), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Salva resultado personalizado
        cv2.imwrite(str(output_path_custom), custom_img)
        print(f"✅ Esqueleto da vaca salvo: {output_path_custom}")
        
        # Mostra informações das detecções
        if result.keypoints is not None:
            num_vacas = len(result.keypoints.data)
            print(f"🐄 Vacas detectadas: {num_vacas}")
            
            # Informações detalhadas para cada vaca
            for j, keypoints in enumerate(result.keypoints.data):
                print(f"\n🐄 Vaca {j+1}:")
                print(f"   Keypoints detectados: {keypoints.shape}")
                
                # Conta keypoints visíveis (confiança > 0)
                visible_kpts = (keypoints[:, 2] > 0).sum()
                total_kpts = keypoints.shape[0]
                print(f"   Keypoints visíveis: {visible_kpts}/{total_kpts}")
        
        # Mostra informações das caixas delimitadoras
        if result.boxes is not None:
            for j, box in enumerate(result.boxes.data):
                conf = box[4]
                print(f"   Confiança da detecção: {conf:.3f}")
    
    print(f"\n🎉 Inferência concluída!")
    print(f"📁 Resultados salvos em: {OUTPUT_DIR}")

def test_model_info():
    """Função para testar e mostrar informações do modelo"""
    
    if not Path(MODEL_PATH).exists():
        print(f"❌ Modelo não encontrado: {MODEL_PATH}")
        return
    
    print(f"📊 Informações do modelo: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)
    
    # Mostra informações do modelo
    print(f"Tipo: {model.task}")
    print(f"Classes: {model.names}")
    
    if hasattr(model.model, 'yaml'):
        print(f"Arquitetura: {model.model.yaml}")

if __name__ == "__main__":
    try:
        # Descomente a linha abaixo para ver informações do modelo
        # test_model_info()
        
        main()
        
    except KeyboardInterrupt:
        print("\n⚠️ Processo interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante a inferência: {str(e)}")
        raise