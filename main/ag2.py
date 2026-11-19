from dieta import gerar_dieta_semanal, calcular_dieta, exibir_refeicao
import random

def avaliar_dieta(dieta, meta_kcal, meta_proteina): #Avalia cada dia.
    kcal, proteina = calcular_dieta(dieta)

    erro_kcal = abs(meta_kcal - kcal) / meta_kcal #abs gera o valor absoluto, ou seja transforma negativo em positivo.
    erro_proteina = abs(meta_proteina - proteina) / meta_proteina

    erro_total = (erro_kcal * 0.6) + (erro_proteina * 0.4)

    fitness = 1 / (1 + erro_total)

    return fitness

def avaliar_individuo(individuo, meta_kcal, meta_proteina): #Avalia o individuo no caso 7 dias (semana).
    fitness_dias = []

    for dia in individuo.values():
        fitness = avaliar_dieta(dia, meta_kcal, meta_proteina)

        fitness_dias.append(fitness)

    fitness_semana = sum(fitness_dias) / len(fitness_dias)

    return fitness_semana

def gerar_populacao(tamanho):
    populacao = []

    for i in range(tamanho):
        dieta = gerar_dieta_semanal()

        populacao.append(dieta)

    return populacao

def avaliar_populacao(populacao, meta_kcal, meta_proteina):
    fitness_populacao = []

    for individuo in populacao:
        fitness = avaliar_individuo(individuo, meta_kcal, meta_proteina)

        fitness_populacao.append(fitness)

    return fitness_populacao

def selecionar_individuo(populacao, fitness_populacao, tamanho_torneio): #metodo de selecao por torneio.
    participantes = []

    for i in range(tamanho_torneio):
        indice = random.randint(0, len(populacao)-1)

        participantes.append(populacao[indice])

    melhor = participantes[0]

    for participante in participantes:

        if fitness_populacao[populacao.index(participante)] > fitness_populacao[populacao.index(melhor)]:
            melhor = participante

    return melhor

def crossover(pai1, pai2):
    filho = {}

    for dia in range(7):
        if random.random() < 0.5:
            filho[f"dia{dia + 1}"] = pai1[f"dia{dia + 1}"]
        else:
            filho[f"dia{dia + 1}"] = pai2[f"dia{dia + 1}"]
           
    return filho

def mutacao(individuo):
    dia = random.randint(1, 7)
    chave = f"dia{dia}"

    individuo[chave] = gerar_dieta_semanal()[chave]
    
    return individuo, chave

def gerar_nova_populacao(populacao, fitness_populacao, tamanho_torneio):
    nova_populacao = []

    for i in range(len(populacao)):
        pai1 = selecionar_individuo(populacao, fitness_populacao, tamanho_torneio)
        pai2 = selecionar_individuo(populacao, fitness_populacao, tamanho_torneio)

        filho = crossover(pai1, pai2)

        if random.random() < 0.1:
            filho, dia_mutado = mutacao(filho)

        nova_populacao.append(filho)


    return nova_populacao

def algoritmo_genenetico(meta_kcal, meta_proteina):
    tamanho_populacao = 10
    numero_geracoes = 500
    tamanho_torneio = 3
    melhor_individuo = None
    melhor_fitness = 0

    populacao = gerar_populacao(tamanho_populacao)
    fitness_populacao = avaliar_populacao(populacao, meta_kcal, meta_proteina)

    indice_melhor = fitness_populacao.index(max(fitness_populacao))

    melhor_individuo = populacao[indice_melhor]
    melhor_fitness = fitness_populacao[indice_melhor]

    for geracao in range(numero_geracoes):
        populacao = gerar_nova_populacao(populacao, fitness_populacao, tamanho_torneio)
        fitness_populacao = avaliar_populacao(populacao, meta_kcal, meta_proteina)

        for i in range(len(populacao)):
            if fitness_populacao[i] > melhor_fitness:
                melhor_fitness = fitness_populacao[i]
                melhor_individuo = populacao[i]

    return melhor_individuo, melhor_fitness
























