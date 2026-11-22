import copy
import random
from dieta import gerar_dieta, gerar_dieta_semanal, calcular_dieta, gerar_refeicao

def avaliar_dieta(dieta, meta_kcal, meta_proteina):
    """
    Avalia a aptidão (fitness) de uma dieta de 1 dia considerando:
    1. Proximidade com as metas diárias de calorias e proteínas.
    2. Punição para refeições sem variação de classe (categoria).
    3. Punição para refeições com proteína superior a (meta_proteina / 6).
    4. Recompensa para lanches menos calóricos (lanches leves).
    """
    kcal_total, proteina_total = calcular_dieta(dieta)

    # 1. Erro diário de calorias e proteínas totais
    erro_kcal = abs(meta_kcal - kcal_total) / meta_kcal
    erro_proteina = abs(meta_proteina - proteina_total) / meta_proteina

    # 2. Heurística: Punição de refeição com proteína > meta_proteina / 6
    limite_prot_refeicao = meta_proteina / 6.0
    penalidade_prot_refeicao = 0.0

    # 3. Heurística: Punição de refeições sem variação de classe
    penalidade_classe = 0.0

    # 4. Heurística: Recompensa para lanches menos calóricos
    recompensa_lanches = 0.0
    penalidade_lanche_pesado = 0.0
    limite_kcal_lanche = meta_kcal / 6.0  # Referência média calórica por refeição

    for nome_ref, itens in dieta.items():
        # Proteína da refeição
        prot_ref = sum(item["proteina_consumida"] for item in itens)
        if prot_ref > limite_prot_refeicao:
            excesso = prot_ref - limite_prot_refeicao
            penalidade_prot_refeicao += excesso / limite_prot_refeicao

        # Variação de classes na refeição
        if len(itens) > 1:
            classes = [item["cat"] for item in itens]
            classes_unicas = set(classes)
            if len(classes_unicas) == 1:
                # Refeição com múltiplos itens da mesma classe: punição maior
                penalidade_classe += 1.0
            elif len(classes_unicas) < len(classes):
                # Repetição parcial de classes
                penalidade_classe += 0.3 * (len(classes) - len(classes_unicas))

        # Recompensa para lanches menos calóricos
        eh_lanche = "lanche" in nome_ref.lower() or "ceia" in nome_ref.lower()
        if eh_lanche:
            kcal_lanche = sum(item["kcal_consumida"] for item in itens)
            if kcal_lanche < limite_kcal_lanche:
                # Quanto menor a caloria do lanche, maior a recompensa
                fator_economia = (limite_kcal_lanche - kcal_lanche) / limite_kcal_lanche
                recompensa_lanches += fator_economia * 0.15
            else:
                # Lanche excessivamente calórico recebe penalidade
                excesso_kcal = (kcal_lanche - limite_kcal_lanche) / limite_kcal_lanche
                penalidade_lanche_pesado += excesso_kcal * 0.20

    # Função custo combinada
    custo_total = (
        (erro_kcal * 1.20) +
        (erro_proteina * 1.00) +
        (penalidade_prot_refeicao * 0.50) +
        (penalidade_classe * 0.40) +
        (penalidade_lanche_pesado * 0.25)
    )

    # Recompensa como multiplicador positivo para valorizar lanches leves
    multiplicador_recompensa = 1.0 + min(0.35, recompensa_lanches)
    fitness = multiplicador_recompensa / (1.0 + custo_total)

    return fitness

def avaliar_individuo(individuo, meta_kcal, meta_proteina):
    """Calcula o fitness médio semanal de um indivíduo (7 dias)."""
    fitness_dias = [
        avaliar_dieta(dia, meta_kcal, meta_proteina)
        for dia in individuo.values()
    ]
    return sum(fitness_dias) / len(fitness_dias)

def gerar_populacao(tamanho):
    """Gera população inicial de dietas semanais."""
    return [gerar_dieta_semanal() for _ in range(tamanho)]

def avaliar_populacao(populacao, meta_kcal, meta_proteina):
    """Calcula o fitness de todos os indivíduos da população."""
    return [
        avaliar_individuo(ind, meta_kcal, meta_proteina)
        for ind in populacao
    ]

def selecionar_individuo(populacao, fitness_populacao, tamanho_torneio=3):
    """Seleção por torneio."""
    indices = random.sample(range(len(populacao)), min(tamanho_torneio, len(populacao)))
    melhor_indice = max(indices, key=lambda idx: fitness_populacao[idx])
    return populacao[melhor_indice]

def crossover(pai1, pai2):
    """Crossover uniforme por dia entre dois indivíduos pais."""
    filho = {}
    for dia in range(7):
        chave = f"dia{dia + 1}"
        origem = pai1[chave] if random.random() < 0.5 else pai2[chave]
        filho[chave] = copy.deepcopy(origem)
    return filho

def mutacao(individuo):
    """
    Mutação multinível:
    1. Ajuste fino de quantidade (gramatura) de um alimento existente.
    2. Substituição de uma refeição específica.
    3. Regeração de um dia completo.
    """
    chave = f"dia{random.randint(1, 7)}"
    dia = individuo[chave]
    tipo_mutacao = random.random()

    if tipo_mutacao < 0.45:
        # Ajusta porção em gramas de um item selecionado aleatoriamente
        refeicoes_com_itens = [ref for ref, itens in dia.items() if itens]
        if refeicoes_com_itens:
            ref_escolhida = random.choice(refeicoes_com_itens)
            item = random.choice(dia[ref_escolhida])
            delta = random.choice([-30, -15, 15, 30, 50])
            
            # Limites saudáveis e realistas de porção por categoria
            if item["cat"] == "Nozes e sementes":
                nova_qntd = min(35, max(10, item["quantidade"] + delta))
            elif item["cat"] == "Mistura":
                nova_qntd = min(180, max(50, item["quantidade"] + delta))
            elif "queijo" in item["alimento"].lower():
                nova_qntd = min(60, max(15, item["quantidade"] + delta))
            elif item["cat"] == "Ovos e derivados":
                nova_qntd = min(150, max(50, item["quantidade"] + delta))
            else:
                nova_qntd = min(220, max(25, item["quantidade"] + delta))

            item["quantidade"] = nova_qntd
            item["kcal_consumida"] = (nova_qntd / 100.0) * item["kcal"]
            item["proteina_consumida"] = (nova_qntd / 100.0) * item["proteina"]
    elif tipo_mutacao < 0.80:
        # Substitui uma refeição inteira
        refeicoes = list(dia.keys())
        ref_escolhida = random.choice(refeicoes)
        dia[ref_escolhida] = gerar_refeicao(ref_escolhida)
    else:
        # Regera o dia completo
        individuo[chave] = gerar_dieta()

    return individuo, chave

def gerar_nova_populacao(populacao, fitness_populacao, tamanho_torneio=3, taxa_mutacao=0.20, elitismo=2):
    """Gera a próxima geração com preservação dos melhores indivíduos (elitismo)."""
    tamanho = len(populacao)
    indices_ordenados = sorted(range(tamanho), key=lambda i: fitness_populacao[i], reverse=True)
    nova_populacao = [copy.deepcopy(populacao[i]) for i in indices_ordenados[:elitismo]]

    while len(nova_populacao) < tamanho:
        pai1 = selecionar_individuo(populacao, fitness_populacao, tamanho_torneio)
        pai2 = selecionar_individuo(populacao, fitness_populacao, tamanho_torneio)

        filho = crossover(pai1, pai2)

        if random.random() < taxa_mutacao:
            filho, _ = mutacao(filho)

        nova_populacao.append(filho)

    return nova_populacao

def algoritmo_genetico(meta_kcal, meta_proteina, tamanho_populacao=25, numero_geracoes=200, tamanho_torneio=3):
    """
    Executa o Algoritmo Genético para otimização da dieta semanal de 6 refeições.
    """
    populacao = gerar_populacao(tamanho_populacao)
    fitness_populacao = avaliar_populacao(populacao, meta_kcal, meta_proteina)

    indice_melhor = max(range(len(populacao)), key=lambda i: fitness_populacao[i])
    melhor_individuo = copy.deepcopy(populacao[indice_melhor])
    melhor_fitness = fitness_populacao[indice_melhor]

    for geracao in range(numero_geracoes):
        populacao = gerar_nova_populacao(populacao, fitness_populacao, tamanho_torneio)
        fitness_populacao = avaliar_populacao(populacao, meta_kcal, meta_proteina)

        for i in range(len(populacao)):
            if fitness_populacao[i] > melhor_fitness:
                melhor_fitness = fitness_populacao[i]
                melhor_individuo = copy.deepcopy(populacao[i])

    return melhor_individuo, melhor_fitness

# Alias para compatibilidade com o código legado que possuía erro de grafia
algoritmo_genenetico = algoritmo_genetico
