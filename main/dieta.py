from base_alimentos import base
import random


def selecionar_alimento(): # Selecionado um alimento da nova base de dados aleatoriamente.
    alimento = base.sample()

    alimento = {
        "id" : alimento["id"].iloc[0],
        "nome" : alimento["alimento"].iloc[0],
        "proteina" : alimento["proteina"].iloc[0],
        "kcal" : alimento["kcal"].iloc[0]
    }

    return alimento

def calcular_nutrientes(alimento): # Calculando proteina e caloria de cada alimento com base na quantidade.
    qntd = random.randint(50, 300)

    proteina = (qntd / 100) * alimento["proteina"]
    kcal = (qntd / 100) * alimento["kcal"]

    return qntd, proteina, kcal

def gerar_refeicao(): # Gerando uma refeição aleatoria com 2 a 4 itens.
    refeicao = []

    qntd_alimentos = random.randint(2, 4)

    for i in range(qntd_alimentos):
        alimento = selecionar_alimento()

        qntd, proteina, kcal = calcular_nutrientes(alimento)

        alimento["quantidade"] = qntd
        alimento["proteina_consumida"] = proteina 
        alimento["kcal_consumida"] = kcal

        refeicao.append(alimento)

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
        "cafe" : gerar_refeicao(),
        "almoco" : gerar_refeicao(),
        "jantar" : gerar_refeicao()
    }

    return dieta

dieta = gerar_dieta()

print("CAFÉ DA MANHÃ")
print(dieta["cafe"])

print("\nALMOÇO")
print(dieta["almoco"])

print("\nJANTAR")
print(dieta["jantar"])