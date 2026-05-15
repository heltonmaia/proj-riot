"""
Segmentação de vídeo com SAM3
"""

import os
import cv2

from ultralytics.models.sam import SAM3VideoSemanticPredictor


# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

WEIGHTS_PATH = "CAMINHO_DO_MODELO/sam3.pt"

INPUT_VIDEO = "CAMINHO_DO_VIDEO/video.mp4"

OUTPUT_VIDEO = "CAMINHO_DE_SAIDA/video_segmentado.mp4"

TEXT_PROMPTS = ["cow"]

CONF_THRESHOLD = 0.50

IMAGE_SIZE = 480


# ============================================================================
# PROCESSAMENTO
# ============================================================================

def run_inference():

    if not os.path.exists(WEIGHTS_PATH):
        raise FileNotFoundError(
            f"Modelo não encontrado: {WEIGHTS_PATH}"
        )

    if not os.path.exists(INPUT_VIDEO):
        raise FileNotFoundError(
            f"Vídeo não encontrado: {INPUT_VIDEO}"
        )

    output_dir = os.path.dirname(OUTPUT_VIDEO)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(INPUT_VIDEO)

    fps = cap.get(cv2.CAP_PROP_FPS)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    cap.release()

    print("\n==============================================")
    print("SAM3 - Segmentação de vídeo")
    print("==============================================")

    print(f"Entrada : {INPUT_VIDEO}")
    print(f"Saída   : {OUTPUT_VIDEO}")
    print(f"Frames  : {total_frames}")
    print(f"FPS     : {fps:.2f}")
    print(f"Tamanho : {width}x{height}")

    print("==============================================\n")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        OUTPUT_VIDEO,
        fourcc,
        fps,
        (width, height)
    )

    overrides = dict(
        conf=CONF_THRESHOLD,
        task="segment",
        mode="predict",
        imgsz=IMAGE_SIZE,
        model=WEIGHTS_PATH,
        half=True,
        save=False,
        verbose=False,
    )

    predictor = SAM3VideoSemanticPredictor(
        overrides=overrides
    )

    results = predictor(
        source=INPUT_VIDEO,
        text=TEXT_PROMPTS,
        stream=True
    )

    processed_frames = 0

    for result in results:

        annotated_frame = result.plot()

        writer.write(annotated_frame)

        processed_frames += 1

        if processed_frames % 30 == 0 or processed_frames == 1:

            detections = (
                len(result.boxes)
                if result.boxes is not None
                else 0
            )

            progress = (
                processed_frames / total_frames * 100
                if total_frames > 0
                else 0
            )

            print(
                f"Frame {processed_frames:>5}/{total_frames} "
                f"({progress:5.1f}%) "
                f"- Detecções: {detections}"
            )

    writer.release()

    print("\nProcessamento finalizado.")
    print(f"Vídeo salvo em: {OUTPUT_VIDEO}\n")


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    run_inference()