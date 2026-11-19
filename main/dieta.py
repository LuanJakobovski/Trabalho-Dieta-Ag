from base_alimentos import base
import random


def selecionar_alimento(alimentos): # Selecionado um alimento da nova base de dados aleatoriamente.
    alimento = alimentos.sample()

    alimento = {
        "id" : alimento["id"].iloc[0],
        "alimento" : alimento["alimento"].iloc[0],
        "proteina" : alimento["proteina"].iloc[0],
        "kcal" : alimento["kcal"].iloc[0],
        "cat" : alimento["cat"].iloc[0]
    }

    return alimento

def calcular_nutrientes(alimento): # Calculando proteina e caloria de cada alimento com base na quantidade.

    if alimento["cat"] == "Mistura":
        qntd = random.randint(100, 250)
    else:
        qntd = random.randint(50, 200)

    proteina = (qntd / 100) * alimento["proteina"]
    kcal = (qntd / 100) * alimento["kcal"]

    return qntd, proteina, kcal

def gerar_refeicao(tipo_refeicao): # Gerando uma refeição aleatoria com 3 a 4 itens.
    refeicao = []
    alimentos = filtrar_alimentos(tipo_refeicao)
    misturas = alimentos.loc[alimentos["cat"] == "Mistura"]
    outros = alimentos.loc[alimentos["cat"] != "Mistura"]

    if tipo_refeicao == "Almoço":
        alimento = selecionar_alimento(misturas)
    else:
        alimento = selecionar_alimento(alimentos)

    qntd, proteina, kcal = calcular_nutrientes(alimento)

    alimento["quantidade"] = qntd
    alimento["proteina_consumida"] = proteina
    alimento["kcal_consumida"] = kcal

    refeicao.append(alimento)

    qntd_alimentos = random.randint(3, 4)

    for i in range(qntd_alimentos -1):
        alimento = selecionar_alimento(outros)

        qntd, proteina, kcal = calcular_nutrientes(alimento)

        alimento["quantidade"] = qntd
        alimento["proteina_consumida"] = proteina 
        alimento["kcal_consumida"] = kcal

        refeicao.append(alimento)

        outros = outros.loc[outros["id"] != alimento["id"]]

    return refeicao

def calcular_refeicao(refeicao): # Calculando o total de proteina e calorias da refeição.
    total_kcal = 0
    total_proteina = 0

    for alimento in refeicao:
        total_kcal += alimento["kcal_consumida"]
        total_proteina += alimento["proteina_consumida"]

    return total_kcal, total_proteina

def gerar_dieta(): # gera uma dieta completa com cafe, almoco e janta.
    dieta = {
        "cafe" : gerar_refeicao("Café da manhã"),
        "almoco" : gerar_refeicao("Almoço"),
        "janta" : gerar_refeicao("Almoço")
    }

    return dieta

def filtrar_alimentos(refeicao):
    alimentos = base.loc[base["refeicao"] == refeicao] 
    
    return alimentos

def exibir_refeicao(refeicao, nome):
    print(f"\n========== {nome.upper()} ==========")

    for alimento in refeicao:
        print(f"\n{alimento['alimento']}")
        print(f"Quantidade: {alimento['quantidade']}g")
        print(f"Proteína Total: {alimento['proteina_consumida']:.2f}g")
        print(f"Calorias: {alimento['kcal_consumida']:.2f} kcal")

def calcular_dieta(dieta):
    total_kcal = 0
    total_proteina = 0

    for refeicao in dieta.values():
        kcal, proteina = calcular_refeicao(refeicao)
        total_kcal += kcal
        total_proteina += proteina

    return total_kcal, total_proteina

def gerar_dieta_semanal():
    semana = {}

    for dia in range(7):
        dieta = gerar_dieta()

        semana[f"dia{dia +1}"] = dieta

    return semana

if __name__ == "__main__":
    semana = gerar_dieta_semanal()

    print("dias", len(semana))

    for dia, dieta in semana.items():
        print(dia)
        print("qntd:", len(dieta))