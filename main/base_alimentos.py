import pandas as pd

dados = pd.read_excel("alimentos.xlsx")

base = dados[["ID", "Descrição dos alimentos", "Categoria", "Proteína(g)", "Energia(kcal)"]] # Pegando apenas as colunas que nos interessam.

base = base.rename(columns={ # Renomeando os nomes das colunas.
    "ID": "id",
    "Descrição dos alimentos": "alimento",
    "Proteína(g)": "proteina",
    "Categoria": "categoria",
    "Energia(kcal)": "kcal"
    }) 

base["proteina"] = pd.to_numeric(base["proteina"], errors="coerce") # Convertendo as linhas da Proteina para numerico.
base["kcal"] = pd.to_numeric(base["kcal"], errors="coerce") # Convertendo as linhas da Kcal para numerico.

base = base.dropna(subset = ["proteina", "kcal"], axis=0) # Removendo valores NaN


if __name__ == "__main__":
    print(base.shape)
    print(base.dtypes)
    print(base.head())
    print(base[["proteina", "kcal"]].describe())
