import os
import subprocess
import glob
from pathlib import Path

class VideoMerger:
    def __init__(self):
        """Inicializa o mesclador de vídeos."""
        pass
    
    def merge_videos_with_subtitles(self, video_dir, output_path, subtitle_dir=None):
        """
        Mescla vídeos com legendas usando FFmpeg.
        
        Args:
            video_dir: Diretório contendo os vídeos
            output_path: Caminho para o vídeo de saída
            subtitle_dir: Diretório contendo as legendas (opcional)
        """
        try:
            # Encontrar todos os vídeos no diretório
            video_files = []
            for ext in ['*.mp4', '*.avi', '*.mov', '*.mkv']:
                video_files.extend(glob.glob(os.path.join(video_dir, ext)))
            
            if not video_files:
                print(f"Nenhum vídeo encontrado em {video_dir}")
                return False
            
            video_files.sort()  # Ordenar para garantir ordem consistente
            print(f"Vídeos encontrados: {len(video_files)}")
            
            # Criar lista de arquivos para FFmpeg
            file_list_path = "temp_file_list.txt"
            with open(file_list_path, 'w', encoding='utf-8') as f:
                for video_file in video_files:
                    f.write(f"file '{os.path.abspath(video_file)}'\n")
            
            # Comando FFmpeg para mesclar vídeos
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', file_list_path,
                '-c', 'copy',
                output_path,
                '-y'  # Sobrescrever arquivo de saída se existir
            ]
            
            print("Mesclando vídeos...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Limpar arquivo temporário
            if os.path.exists(file_list_path):
                os.remove(file_list_path)
            
            if result.returncode == 0:
                print(f"Vídeos mesclados com sucesso: {output_path}")
                return True
            else:
                print(f"Erro ao mesclar vídeos: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Erro durante a mesclagem: {e}")
            return False
    
    def add_subtitles_to_video(self, video_path, subtitle_path, output_path):
        """
        Adiciona legendas a um vídeo usando FFmpeg.
        
        Args:
            video_path: Caminho para o vídeo
            subtitle_path: Caminho para o arquivo de legendas (.srt)
            output_path: Caminho para o vídeo de saída com legendas
        """
        try:
            if not os.path.exists(video_path):
                print(f"Vídeo não encontrado: {video_path}")
                return False
            
            if not os.path.exists(subtitle_path):
                print(f"Arquivo de legendas não encontrado: {subtitle_path}")
                return False
            
            # Comando FFmpeg para adicionar legendas
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-vf', f'subtitles={subtitle_path}',
                '-c:a', 'copy',
                output_path,
                '-y'
            ]
            
            print(f"Adicionando legendas ao vídeo: {os.path.basename(video_path)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Legendas adicionadas com sucesso: {output_path}")
                return True
            else:
                print(f"Erro ao adicionar legendas: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Erro durante a adição de legendas: {e}")
            return False
    
    def process_videos_with_subtitles(self, video_dir, subtitle_dir, output_dir):
        """
        Processa todos os vídeos em um diretório, adicionando legendas correspondentes.
        
        Args:
            video_dir: Diretório contendo os vídeos
            subtitle_dir: Diretório contendo as legendas
            output_dir: Diretório para salvar os vídeos com legendas
        """
        try:
            # Criar diretório de saída se não existir
            os.makedirs(output_dir, exist_ok=True)
            
            # Encontrar vídeos
            video_files = []
            for ext in ['*.mp4', '*.avi', '*.mov', '*.mkv']:
                video_files.extend(glob.glob(os.path.join(video_dir, ext)))
            
            if not video_files:
                print(f"Nenhum vídeo encontrado em {video_dir}")
                return False
            
            success_count = 0
            for video_file in video_files:
                video_name = os.path.splitext(os.path.basename(video_file))[0]
                subtitle_file = os.path.join(subtitle_dir, f"{video_name}_legendas.srt")
                
                if os.path.exists(subtitle_file):
                    output_file = os.path.join(output_dir, f"{video_name}_com_legendas.mp4")
                    if self.add_subtitles_to_video(video_file, subtitle_file, output_file):
                        success_count += 1
                else:
                    print(f"Legendas não encontradas para: {video_name}")
            
            print(f"Processamento concluído: {success_count}/{len(video_files)} vídeos processados")
            return success_count > 0
            
        except Exception as e:
            print(f"Erro durante o processamento: {e}")
            return False 