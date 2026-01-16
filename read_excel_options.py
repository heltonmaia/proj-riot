import pandas as pd
import os

# Caminho da planilha (caminho relativo ou absoluto)
file_path = 'AI/dataset/riot/planilha_de_anotacoes_jan_2026.xlsx'

if not os.path.exists(file_path):
    print(f"Erro: Arquivo não encontrado em {file_path}")
    exit(1)

try:
    df = pd.read_excel(file_path)
    print("Colunas encontradas:", df.columns.tolist())
    
    # Colunas de interesse (baseado no pedido do usuário)
    # Vou tentar adivinhar os nomes exatos ou algo próximo
    potential_columns = {
        'classe': ['classe', 'class', 'categoria', 'animal'],
        'idade': ['idade', 'age', 'fase'],
        'sexo': ['sexo', 'sex', 'genero'],
        'sinais_clinicos': ['sinais_clinicos', 'clinical_signs', 'saude'],
        'ambiente': ['ambiente', 'environment', 'cenario', 'local'],
        'comportamento': ['comportamento', 'behavior', 'acao']
    }
    
    for key, aliases in potential_columns.items():
        found = False
        for col in df.columns:
            if col.lower() in aliases or any(alias in col.lower() for alias in aliases):
                print(f"\n--- Valore únicos para '{key}' (Coluna: {col}) ---")
                try:
                    unique_vals = df[col].dropna().unique().tolist()
                    print(unique_vals)
                except Exception as e:
                    print(f"Erro ao ler valores: {e}")
                found = True
                break
        if not found:
            print(f"\n--- Coluna para '{key}' NÃO encontrada ---")

except Exception as e:
    print(f"Erro ao ler planilha: {e}")
