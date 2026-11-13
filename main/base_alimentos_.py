
import pandas as pd

# ==================================================
# 1. LEITURA DA PLANILHA
# ==================================================

dados = pd.read_excel("alimentos.xlsx")

base = dados[
    [
        "ID",
        "Descrição dos alimentos",
        "Categoria",
        "Refeição",
        "Energia(kcal)",
        "Proteína(g)"
    ]
].copy()

base = base.rename(columns={
    "ID": "id",
    "Descrição dos alimentos": "nome_alimento",
    "Categoria": "cat",
    "Refeição": "refeicao",
    "Energia(kcal)": "energia_kcal",
    "Proteína(g)": "proteina_g"
})

# Limpeza dos dados
base = base.dropna()

base = base.loc[
    base["nome_alimento"].astype(str).str.strip()
    != "Descrição dos alimentos"
]

# Conversão numérica
base["id"] = pd.to_numeric(base["id"], errors="coerce")
base["energia_kcal"] = pd.to_numeric(
    base["energia_kcal"], errors="coerce"
)
base["proteina_g"] = pd.to_numeric(
    base["proteina_g"], errors="coerce"
)

base = base.dropna(
    subset=["id", "energia_kcal", "proteina_g"]
)

base["id"] = base["id"].astype(int)

base = base.reset_index(drop=True)


# ==================================================
# 2. DICIONÁRIOS DE REFERÊNCIA
# ==================================================

food_reference = dict(zip(base["id"], base["nome_alimento"]))
category_reference = dict(zip(base["id"], base["cat"]))
meal_reference = dict(zip(base["id"], base["refeicao"]))
calories_reference = dict(zip(base["id"], base["energia_kcal"]))
protein_reference = dict(zip(base["id"], base["proteina_g"]))


# ==================================================
# 3. FUNÇÃO: CONSULTAR UM ALIMENTO PELO ID
# ==================================================

def consultar_alimento(id_alimento):

    if id_alimento not in food_reference:
        print(f"Alimento com ID {id_alimento} não encontrado.")
        return None

    return {
        "ID": id_alimento,
        "Nome": food_reference[id_alimento],
        "Categoria": category_reference[id_alimento],
        "Refeição": meal_reference[id_alimento],
        "Energia (kcal)": calories_reference[id_alimento],
        "Proteína (g)": protein_reference[id_alimento]
    }


# ==================================================
# 4. FUNÇÃO: CONSULTAR VÁRIOS ALIMENTOS
# ==================================================

def consultar_varios_alimentos(lista_ids):

    alimentos = []

    for id_alimento in lista_ids:

        alimento = consultar_alimento(id_alimento)

        if alimento is not None:
            alimentos.append(alimento)

    return pd.DataFrame(alimentos)


# ==================================================
# 5. FUNÇÃO: CONSULTAR POR CATEGORIA
# ==================================================

def consultar_categoria(categoria):

    resultado = base[
        base["cat"].str.lower() == categoria.lower()
    ]

    return resultado.copy()


# ==================================================
# 6. FUNÇÃO: CONSULTAR POR REFEIÇÃO
# ==================================================

def consultar_refeicao(refeicao):

    resultado = base[
        base["refeicao"].str.lower() == refeicao.lower()
    ]

    return resultado.copy()


# ==================================================
# 7. FUNÇÃO: CONSULTAR POR NOME
# ==================================================

def consultar_nome(nome):

    resultado = base[
        base["nome_alimento"].str.contains(
            nome,
            case=False,
            na=False
        )
    ]

    return resultado.copy()


# ==================================================
# 8. FUNÇÃO: CALCULAR VALORES NUTRICIONAIS
# ==================================================

def calcular_nutrientes(lista_ids):

    alimentos = consultar_varios_alimentos(lista_ids)

    if alimentos.empty:
        return None

    return {
        "Energia total (kcal)": alimentos["Energia (kcal)"].sum(),
        "Proteína total (g)": alimentos["Proteína (g)"].sum()
    }


# ==================================================
# 9. TESTES DAS FUNÇÕES
# ==================================================

if __name__ == "__main__":

    print("\n--- CONSULTA POR ID ---")
    print(consultar_alimento(1))

    print("\n--- CONSULTA DE VÁRIOS IDs ---")
    print(consultar_varios_alimentos([1, 2, 3]))

    print("\n--- CONSULTA POR REFEIÇÃO ---")
    print(consultar_refeicao("Almoço"))

    print("\n--- CONSULTA POR CATEGORIA ---")
    print(consultar_categoria("Cereais e derivados"))

    print("\n--- CONSULTA POR NOME ---")
    print(consultar_nome("arroz"))

    print("\n--- CÁLCULO NUTRICIONAL ---")
    print(calcular_nutrientes([1, 2, 3]))
