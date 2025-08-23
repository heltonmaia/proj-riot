import yaml
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file="config.yaml"):
        """Inicializa o gerenciador de configurações."""
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Carrega a configuração do arquivo YAML."""
        default_config = {
            'api_key': '',
            'model': 'gemini-2.5-flash-preview-05-20',
            'video_dir': 'videos/',
            'output_dir': 'results/',
            'tmp_dir': 'tmp/',
            'num_frames': 8,
            'ffmpeg_path': 'ffmpeg'
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = yaml.safe_load(f) or {}
                    # Mesclar com configuração padrão
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")
        
        return default_config
    
    def save_config(self):
        """Salva a configuração atual no arquivo YAML."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            print(f"Configuração salva em: {self.config_file}")
            return True
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
            return False
    
    def get(self, key, default=None):
        """Obtém um valor da configuração."""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Define um valor na configuração."""
        self.config[key] = value
    
    def update_api_key(self, api_key):
        """Atualiza a API key e salva a configuração."""
        self.config['api_key'] = api_key
        return self.save_config()
    
    def create_directories(self):
        """Cria os diretórios necessários se não existirem."""
        directories = [
            self.config.get('video_dir', 'videos/'),
            self.config.get('output_dir', 'results/'),
            self.config.get('tmp_dir', 'tmp/')
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Diretório criado/verificado: {directory}")
    
    def validate_config(self):
        """Valida se a configuração está correta."""
        errors = []
        
        # Verificar API key
        if not self.config.get('api_key'):
            errors.append("API key não configurada")
        
        # Verificar diretórios
        for dir_key in ['video_dir', 'output_dir', 'tmp_dir']:
            directory = self.config.get(dir_key)
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory, exist_ok=True)
                except Exception as e:
                    errors.append(f"Não foi possível criar diretório {dir_key}: {e}")
        
        return errors
    
    def show_config(self):
        """Exibe a configuração atual."""
        print("\n=== Configuração Atual ===")
        for key, value in self.config.items():
            if key == 'api_key':
                # Mascarar API key por segurança
                masked_value = value[:8] + '*' * (len(value) - 8) if value else 'Não configurada'
                print(f"{key}: {masked_value}")
            else:
                print(f"{key}: {value}")
        print("==========================\n") 