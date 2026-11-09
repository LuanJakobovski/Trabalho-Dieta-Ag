import pandas as pd

dados = pd.read_excel("alimentos.xlsx")

base = dados[["Número do", "Unnamed: 1", "Proteína", "Energia"]] # Pegando apenas as colunas que nos interessam.
base = base.dropna() # Removendo linhas com valores ausentes.

base = base.rename(columns={ # Renomeando os nomes das colunas.
    "Número do": "id",
    "Unnamed: 1": "alimento",
    "Proteína": "proteina",
    "Energia": "kcal"
    }) 

base = base.loc[base["alimento"] != "Descrição dos alimentos"] # Seleciona todas as linhas q tem resultado diferente da condição.

base["proteina"] = pd.to_numeric(base["proteina"], errors="coerce") # Convertendo as linhas da Proteina para numerico.
base["kcal"] = pd.to_numeric(base["kcal"], errors="coerce") # Convertendo as linhas da Kcal para numerico.

base = base.dropna(subset=["proteina", "kcal"]) #dropna novamente para retirar novos valores NaN.

print(base.isna().sum())

print("Total de alimentos: ", len(base))
