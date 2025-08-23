import os
import google.generativeai as genai
import cv2
import numpy as np
import re
from PIL import Image
import io

class VideoAnalyzer:
    def __init__(self, api_key):
        """Inicializa o analisador de vídeos com a API key do Gemini."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        
        # Prompt para análise de vídeos de animais de fazenda
        self.prompt_template = """
        Analise detalhadamente este vídeo de animal(is) de fazenda. Forneça:

        1. **Descrição geral da cena:**
           - Ambiente (pasto, curral, estábulo, etc.)
           - Período do dia (manhã, tarde, noite)
           - Condições climáticas visíveis
           - Quantidade de animais presentes

        2. **Identificação dos animais:**
           - Espécie(s)
           - Raça(s) se identificáveis
           - Características físicas notáveis
           - Estimativa de idade (filhote, jovem, adulto)

        3. **Análise comportamental:**
           - Comportamentos naturais observados (alimentação, descanso, social, etc.)
           - Linguagem corporal e postura
           - Vocalizações (se houver áudio)
           - Interações com outros animais ou humanos
           - Indicadores de bem-estar ou estresse

        4. **Interpretação contextual:**
           - Significado etológico dos comportamentos observados
           - Possíveis motivações para as ações observadas
           - Relevância para manejo e bem-estar animal

        5. **Importante: Gere APENAS legendas em formato .srt para todo o vídeo:**
           - Use linguagem clara e acessível
           - As legendas devem explicar o que está acontecendo e incluir informações educativas sobre o comportamento animal
           - Formate as legendas no padrão .srt com timestamps corretos
           - A duração do vídeo é de {duration} segundos
           - Mantenha as frases concisas (máximo 42 caracteres por linha)
           - Cada bloco de legenda deve permanecer visível entre 3-7 segundos
           - Distribua as legendas uniformemente ao longo do vídeo
           - NÃO INCLUA NENHUM TEXTO EXPLICATIVO ALÉM DO FORMATO SRT

        Exemplo formato .srt:
        ```
        1
        00:00:01,000 --> 00:00:04,000
        O gado nelore se aproxima do bebedouro.

        2
        00:00:04,500 --> 00:00:09,000
        Comportamento típico: os animais mais 
        dominantes bebem primeiro.

        3
        00:00:09,500 --> 00:00:13,500
        O ato de beber ocorre em sessões curtas,
        intercaladas com observação do ambiente.
        ```

        FORNEÇA APENAS O ARQUIVO SRT, SEM TEXTO ADICIONAL.
        """

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