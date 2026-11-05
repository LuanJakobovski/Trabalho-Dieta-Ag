import pandas as pd

dados = pd.read_excel("alimentos.xlsx")

alimentos = dados[["Número do", "Unnamed: 1", "Proteína", "Energia"]] # Pegando apenas as colunas que nos interessam.
alimentos = alimentos.dropna() # Removendo linhas com valores ausentes.
alimentos = alimentos.rename(columns={"Número do": "id", "Unnamed: 1": "alimento", "Proteína": "proteina", "Energia": "kcal"}) #Renomeando os nomes das colunas.
print(alimentos.info())
print(alimentos.describe())

