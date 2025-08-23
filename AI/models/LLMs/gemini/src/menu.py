import os
import sys
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config_manager import ConfigManager
from src.video_analyzer import VideoAnalyzer
from src.video_merger import VideoMerger

class Menu:
    def __init__(self):
        """Inicializa o menu principal."""
        self.config_manager = ConfigManager()
        self.video_analyzer = None
        self.video_merger = VideoMerger()
        
        # Inicializar analisador se API key estiver configurada
        api_key = self.config_manager.get('api_key')
        if api_key:
            self.video_analyzer = VideoAnalyzer(api_key)
    
    def show_main_menu(self):
        """Exibe o menu principal."""
        while True:
            print("\n" + "="*50)
            print("           RIOT GEMINI - MENU PRINCIPAL")
            print("="*50)
            print("1. Configurar API Key")
            print("2. Analisar vídeo individual (gera a legenda)")
            print("3. Analisar todos os vídeos de um diretório (gera as legendas)")
            print("4. Adicionar legendas aos vídeos (todos do diretório)")
            print("5. Processar vídeos em lote (análise + legendas, gera os vídeos resultantes)")
            print("6. Mesclar vídeos em apenas um para análises futuras")
            print("7. Sair")
            print("="*50)
            
            choice = input("\nEscolha uma opção (1-7): ").strip()
            
            if choice == '1':
                self.configure_api_key()
            elif choice == '2':
                self.analyze_single_video()
            elif choice == '3':
                self.analyze_directory_videos()
            elif choice == '4':
                self.add_subtitles_to_videos()
            elif choice == '5':
                self.batch_process_videos()
            elif choice == '6':
                self.merge_videos()
            elif choice == '7':
                print("Saindo...")
                break
            else:
                print("Opção inválida. Tente novamente.")
    
    def configure_api_key(self):
        """Configura a API key do Gemini."""
        print("\n=== Configurar API Key ===")
        current_key = self.config_manager.get('api_key')
        if current_key:
            masked_key = current_key[:8] + '*' * (len(current_key) - 8)
            print(f"API Key atual: {masked_key}")
        
        new_key = input("Digite sua nova API Key do Google Gemini: ").strip()
        if new_key:
            if self.config_manager.update_api_key(new_key):
                self.video_analyzer = VideoAnalyzer(new_key)
                print("API Key configurada com sucesso!")
            else:
                print("Erro ao salvar API Key.")
        else:
            print("Operação cancelada.")
    
    def analyze_single_video(self):
        """Analisa um vídeo individual."""
        if not self.video_analyzer:
            print("Erro: API Key não configurada. Configure primeiro no menu.")
            return
        
        print("\n=== Analisar Vídeo Individual ===")
        video_path = input("Digite o caminho do vídeo: ").strip()
        
        if not os.path.exists(video_path):
            print("Erro: Arquivo não encontrado.")
            return
        
        output_path = input("Caminho para salvar legendas (Enter para padrão): ").strip()
        if not output_path:
            output_path = None
        
        print(f"\nAnalisando vídeo: {os.path.basename(video_path)}")
        result = self.video_analyzer.analyze_video(video_path, output_path)
        
        if result:
            print("Análise concluída com sucesso!")
        else:
            print("Erro durante a análise.")
    
    def analyze_directory_videos(self):
        """
        Analisa todos os vídeos de um diretório e gera arquivos de legendas SRT para cada um.
        """
        if not self.video_analyzer:
            print("Erro: API Key não configurada. Configure primeiro no menu.")
            return
        
        print("\n=== Analisar Vídeos do Diretório ===")
        video_dir = input(f"Diretório de vídeos (Enter para {self.config_manager.get('video_dir')}): ").strip()
        if not video_dir:
            video_dir = self.config_manager.get('video_dir')
        
        if not os.path.exists(video_dir):
            print("Erro: Diretório não encontrado.")
            return
        
        # Encontrar vídeos
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
        video_files = []
        for ext in video_extensions:
            video_files.extend(Path(video_dir).glob(ext))
        
        if not video_files:
            print("Nenhum vídeo encontrado no diretório.")
            return
        
        print(f"Encontrados {len(video_files)} vídeos.")
        proceed = input("Deseja continuar? (s/n): ").strip().lower()
        if proceed != 's':
            return
        
        success_count = 0
        for video_file in video_files:
            print(f"\nAnalisando: {video_file.name}")
            output_path = video_file.parent / f"{video_file.stem}_legendas.srt"
            
            if self.video_analyzer.analyze_video(str(video_file), str(output_path)):
                success_count += 1
        
        print(f"\nProcessamento concluído: {success_count}/{len(video_files)} vídeos analisados com sucesso.")
    
    def merge_videos(self):
        """
        Junta todos os vídeos do diretório em um único arquivo para facilitar análises posteriores.
        """
        print("\n=== Mesclar Vídeos ===")
        video_dir = input(f"Diretório de vídeos (Enter para {self.config_manager.get('video_dir')}): ").strip()
        if not video_dir:
            video_dir = self.config_manager.get('video_dir')
        
        if not os.path.exists(video_dir):
            print("Erro: Diretório não encontrado.")
            return
        
        output_path = input("Caminho do vídeo de saída (Enter para 'resultado_mesclado.mp4'): ").strip()
        if not output_path:
            output_path = "resultado_mesclado.mp4"
        
        print("Mesclando vídeos...")
        if self.video_merger.merge_videos_with_subtitles(video_dir, output_path):
            print("Mesclagem concluída com sucesso!")
        else:
            print("Erro durante a mesclagem.")
    
    def add_subtitles_to_videos(self):
        """
        Incorpora as legendas SRT nos vídeos do diretório, gerando novos vídeos com legendas.
        """
        print("\n=== Adicionar Legendas aos Vídeos ===")
        video_dir = input(f"Diretório de vídeos (Enter para {self.config_manager.get('video_dir')}): ").strip()
        if not video_dir:
            video_dir = self.config_manager.get('video_dir')
        
        subtitle_dir = input("Diretório de legendas (Enter para mesmo diretório dos vídeos): ").strip()
        if not subtitle_dir:
            subtitle_dir = video_dir
        
        output_dir = input(f"Diretório de saída (Enter para {self.config_manager.get('output_dir')}): ").strip()
        if not output_dir:
            output_dir = self.config_manager.get('output_dir')
        
        if not os.path.exists(video_dir):
            print("Erro: Diretório de vídeos não encontrado.")
            return
        
        if not os.path.exists(subtitle_dir):
            print("Erro: Diretório de legendas não encontrado.")
            return
        
        print("Processando vídeos com legendas...")
        if self.video_merger.process_videos_with_subtitles(video_dir, subtitle_dir, output_dir):
            print("Processamento concluído com sucesso!")
        else:
            print("Erro durante o processamento.")
    
    def batch_process_videos(self):
        """
        Para cada vídeo: analisa, gera legendas e já incorpora no vídeo final automaticamente.
        """
        if not self.video_analyzer:
            print("Erro: API Key não configurada. Configure primeiro no menu.")
            return
        
        print("\n=== Processamento em Lote ===")
        video_dir = input(f"Diretório de vídeos (Enter para {self.config_manager.get('video_dir')}): ").strip()
        if not video_dir:
            video_dir = self.config_manager.get('video_dir')
        
        output_dir = input(f"Diretório de saída (Enter para {self.config_manager.get('output_dir')}): ").strip()
        if not output_dir:
            output_dir = self.config_manager.get('output_dir')
        
        if not os.path.exists(video_dir):
            print("Erro: Diretório não encontrado.")
            return
        
        # Encontrar vídeos
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv']
        video_files = []
        for ext in video_extensions:
            video_files.extend(Path(video_dir).glob(ext))
        
        if not video_files:
            print("Nenhum vídeo encontrado no diretório.")
            return
        
        print(f"Encontrados {len(video_files)} vídeos.")
        proceed = input("Deseja continuar? (s/n): ").strip().lower()
        if proceed != 's':
            return
        
        # Criar diretório temporário para legendas
        tmp_dir = self.config_manager.get('tmp_dir')
        os.makedirs(tmp_dir, exist_ok=True)
        
        success_count = 0
        for video_file in video_files:
            print(f"\nProcessando: {video_file.name}")
            
            # 1. Analisar vídeo e gerar legendas
            subtitle_path = Path(tmp_dir) / f"{video_file.stem}_legendas.srt"
            if self.video_analyzer.analyze_video(str(video_file), str(subtitle_path)):
                # 2. Adicionar legendas ao vídeo
                output_path = Path(output_dir) / f"{video_file.stem}_com_legendas.mp4"
                os.makedirs(output_dir, exist_ok=True)
                
                if self.video_merger.add_subtitles_to_video(str(video_file), str(subtitle_path), str(output_path)):
                    success_count += 1
                    print(f"Vídeo processado: {output_path.name}")
        
        print(f"\nProcessamento em lote concluído: {success_count}/{len(video_files)} vídeos processados com sucesso.") 