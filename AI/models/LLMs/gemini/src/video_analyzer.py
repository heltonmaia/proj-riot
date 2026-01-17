import os
import google.generativeai as genai
import cv2
import numpy as np
import re
import time
from PIL import Image
import io

class VideoAnalyzer:
    def __init__(self, api_key, model_name='gemini-3-pro-preview', prompt_template=None):
        """Inicializa o analisador de vídeos com a API key do Gemini."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # Prompt para análise de vídeos
        self.prompt_template = prompt_template or "Descreva este vídeo."

    def extract_frames(self, video_path, num_frames=8):
        """Extrai frames representativos do vídeo usando OpenCV."""
        try:
            # Abrir o vídeo
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print(f"Erro: Não foi possível abrir o vídeo {video_path}")
                return None, 0
            
            # Obter informações sobre o vídeo
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = total_frames / fps if fps > 0 else 0
            
            print(f"Vídeo: {total_frames} frames, {fps} FPS, duração: {duration:.2f} segundos")
            
            if total_frames <= 0:
                print("Aviso: O vídeo parece estar vazio ou danificado")
                return None, 0
                
            # Calcular os pontos para extração de frames
            frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]
            
            # Extrair e converter frames
            frames = []
            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    # Converter BGR para RGB (formato esperado pelo Gemini)
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # Converter para imagem PIL
                    pil_image = Image.fromarray(frame_rgb)
                    frames.append(pil_image)
                else:
                    print(f"Aviso: Não foi possível ler o frame {idx}")
            
            cap.release()
            
            # Verificar se conseguimos extrair frames suficientes
            if not frames:
                print("Erro: Não foi possível extrair frames do vídeo")
                return None, 0
                
            print(f"Extraídos {len(frames)} frames do vídeo")
            return frames, duration
            
        except Exception as e:
            print(f"Erro ao processar o vídeo: {e}")
            return None, 0

    def extract_srt_content(self, response_text):
        """Extrai apenas o conteúdo SRT da resposta."""
        # Tenta encontrar conteúdo SRT usando regex
        srt_pattern = r'(\d+\s*\n\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}\s*\n[\s\S]*?)(?=\n\s*\d+\s*\n\d{2}:|$)'
        srt_blocks = re.findall(srt_pattern, response_text)
        
        if srt_blocks:
            return "\n\n".join(srt_blocks)
        
        # Se não encontrar no formato esperado, tenta extrair qualquer coisa que pareça um bloco SRT
        lines = response_text.split('\n')
        content = []
        in_srt = False
        
        for line in lines:
            # Verifica se é o início de um bloco SRT (número seguido de timestamps)
            if re.match(r'^\d+\s*$', line.strip()):
                in_srt = True
                content.append(line)
            # Verifica se é um timestamp
            elif re.match(r'^\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}\s*$', line.strip()):
                content.append(line)
            # Se estamos dentro de um bloco SRT, inclui a linha
            elif in_srt:
                content.append(line)
        
        return "\n".join(content)

    def analyze_video(self, video_path, output_path=None):
        """Analisa o vídeo e gera legendas no formato SRT."""
        print("Extraindo frames do vídeo...")
        frames, duration = self.extract_frames(video_path)
        if not frames:
            print("Falha ao extrair frames do vídeo.")
            return None
        
        print(f"Vídeo carregado. Duração: {duration:.2f} segundos")
        
        # Criar prompt específico para este vídeo
        prompt = self.prompt_template.format(duration=int(duration))
        
        print("Analisando vídeo com Gemini...")
        try:
            response = self.model.generate_content([prompt, *frames])
            
            # Extrair apenas o conteúdo SRT da resposta
            srt_content = self.extract_srt_content(response.text)
            
            # Determinar o caminho de saída
            if not output_path:
                base_name = os.path.splitext(os.path.basename(video_path))[0]
                output_path = f"{base_name}_legendas.srt"
            
            # Salvar arquivo SRT
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(srt_content)
            
            print(f"Legendas geradas com sucesso: {output_path}")
            return output_path
        except Exception as e:
            print(f"Erro ao analisar o vídeo: {e}")
            return None

    def analyze_frame_classification(self, video_path, output_path=None, prompt_template=None):
        """
        Classifica animais no primeiro frame do vídeo e retorna JSON.
        """
        print("Extraindo frame inicial...")
        # Extrair apenas 1 frame
        frames, duration = self.extract_frames(video_path, num_frames=1)
        if not frames:
            print("Falha ao extrair frame do vídeo.")
            return None
            
        print(f"Frame extraído. Iniciando classificação...")
        
        # Usar prompt específico ou o padrão da instância
        prompt = prompt_template or self.prompt_template
        
        max_retries = 6
        # Delays específicos: 1min (60s), 15min (900s), 30min (1800s). Depois dobra.
        retry_delays = [60, 900, 1800]
        
        for attempt in range(max_retries):
            try:
                # Configurar para JSON se possível via prompt, mas o Gemini Flash pode precisar de instrução explícita
                response = self.model.generate_content([prompt, frames[0]])
                
                json_content = response.text
                # Limpar markdown ```json ... ``` se houver
                json_content = re.sub(r'^```json\s*', '', json_content)
                json_content = re.sub(r'\s*```$', '', json_content)
                
                # Determinar o caminho de saída
                if not output_path:
                    base_name = os.path.splitext(os.path.basename(video_path))[0]
                    output_path = f"{base_name}_classificacao.json"
                
                # Salvar o frame analisado (imagem)
                try:
                    # Derivar nome da imagem do nome do json
                    image_path = output_path.replace('.json', '.jpg')
                    # Se não terminar com .json (caso raro), forçar extensão
                    if image_path == output_path:
                        image_path = output_path + '.jpg'
                        
                    frames[0].save(image_path)
                    print(f"Frame salvo em: {image_path}")
                except Exception as e:
                    print(f"Erro ao salvar frame: {e}")
                
                # Salvar arquivo JSON
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(json_content)
                
                print(f"Classificação salva com sucesso: {output_path}")
                return output_path
                
            except Exception as e:
                is_rate_limit = "429" in str(e) or "Resource has been exhausted" in str(e)
                if is_rate_limit and attempt < max_retries - 1:
                    # Calcular delay baseado na tentativa
                    if attempt < len(retry_delays):
                        delay = retry_delays[attempt]
                    else:
                        # Dobrar o último delay se passar da lista pré-definida
                        # O último da lista é 1800, então: 3600, 7200...
                        delay = retry_delays[-1] * (2 ** (attempt - len(retry_delays) + 1))
                    
                    print(f"Cota de API excedida (429). Tentativa {attempt + 1}/{max_retries} falhou.")
                    print(f"Aguardando {delay} segundos (aprox. {delay/60:.1f} minutos) antes da próxima tentativa...")
                    
                    # Mostrar contagem regressiva para esperas longas (> 1 min)
                    if delay > 60:
                        remaining = delay
                        while remaining > 0:
                            if remaining % 60 == 0:
                                print(f"Aguardando... {remaining/60:.0f} minutos restantes.")
                            time.sleep(1)
                            remaining -= 1
                    else:
                        time.sleep(delay)
                else:
                    if is_rate_limit:
                         print(f"Cota de API excedida. Máximo de tentativas ({max_retries}) atingido.")
                    else:
                        print(f"Erro ao classificar animais: {e}")
                    return None
        
        return None 