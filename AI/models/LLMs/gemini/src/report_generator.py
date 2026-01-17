import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

class ReportGenerator:
    def __init__(self, results_dir):
        """
        Inicializa o gerador de relatórios.
        
        Args:
            results_dir: Diretório onde estão os arquivos JSON de classificação.
        """
        self.results_dir = results_dir

    def generate_excel_report(self, output_filename=None):
        """
        Lê todos os JSONs de classificação e gera um arquivo Excel consolidado.
        Dois formatos de aba: "Por Animal" (detalhado) e "Por Vídeo" (resumo).
        """
        if not os.path.exists(self.results_dir):
            print(f"Erro: Diretório de resultados não encontrado: {self.results_dir}")
            return None
            
        json_files = list(Path(self.results_dir).glob('*_classificacao.json'))
        
        if not json_files:
            print("Nenhum arquivo de classificação encontrado para gerar relatório.")
            return None
            
        print(f"Processando {len(json_files)} arquivos para o relatório...")
        
        rows_animals = []
        rows_videos = []
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                video_name = json_file.stem.replace('_classificacao', '')
                
                # --- Dados por Vídeo (Resumo) ---
                total_counts = data.get('contagem_total', {})
                total_animais = sum(total_counts.get(k, 0) for k in ['Bezerro', 'Novilha', 'Novilho', 'Garrote', 'Vaca', 'Touro'])
                
                row_video = {
                    'Video': video_name,
                    'Descricao_Ambiente': data.get('descricao_ambiente', ''),
                    'Total_Animais': total_animais,
                    'Total_Bezerro': total_counts.get('Bezerro', 0),
                    'Total_Novilha': total_counts.get('Novilha', 0),
                    'Total_Novilho': total_counts.get('Novilho', 0),
                    'Total_Garrote': total_counts.get('Garrote', 0),
                    'Total_Vaca': total_counts.get('Vaca', 0),
                    'Total_Touro': total_counts.get('Touro', 0),
                    'Arquivo_JSON': json_file.name
                }
                rows_videos.append(row_video)
                
                # --- Dados por Animal (Detalhado) ---
                animals = data.get('animais_identificados', [])
                if not animals:
                    # Se não houver animais, cria uma linha vazia para o vídeo constar
                     row_animal = {
                        'Video': video_name,
                        'Descricao_Ambiente': data.get('descricao_ambiente', ''),
                        'Animal_ID': 'N/A',
                        'Classe': 'Nenhum animal identificado',
                        'Sexo': '',
                        'Sinais_Clinicos': '',
                        'Comportamento': '',
                        'Descricao_Animal': ''
                    }
                     rows_animals.append(row_animal)
                else:
                    for animal in animals:
                        row_animal = {
                            'Video': video_name,
                            'Descricao_Ambiente': data.get('descricao_ambiente', ''),
                            'Animal_ID': animal.get('id', ''),
                            'Classe': animal.get('classe', ''),
                            'Sexo': animal.get('sexo', ''),
                            'Sinais_Clinicos': animal.get('sinais_clinicos', ''),
                            'Comportamento': animal.get('comportamento', ''),
                            'Descricao_Animal': animal.get('descricao_animal', '')
                        }
                        rows_animals.append(row_animal)
                        
            except Exception as e:
                print(f"Erro ao processar {json_file.name}: {e}")
        
        if not rows_videos:
            print("Nenhum dado válido extraído.")
            return None
            
        # Converter para DataFrames
        df_videos = pd.DataFrame(rows_videos)
        df_animals = pd.DataFrame(rows_animals)
        
        # Gerar nome do arquivo se não informado
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = os.path.join(self.results_dir, f"relatorio_classificacao_{timestamp}.xlsx")
            
        try:
            with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
                df_animals.to_excel(writer, sheet_name='Por Animal', index=False)
                df_videos.to_excel(writer, sheet_name='Por Video (Resumo)', index=False)
                
            print(f"Relatório gerado com sucesso: {output_filename}")
            return output_filename
        except Exception as e:
            print(f"Erro ao salvar Excel: {e}")
            return None
