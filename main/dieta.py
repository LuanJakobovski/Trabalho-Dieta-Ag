import random
from base_alimentos import base

# Dicionário com nomes padronizados e ordem das 6 refeições diárias
NOMES_REFEICOES = [
    "Café da manhã",
    "Lanche da manhã",
    "Almoço",
    "Lanche da tarde",
    "Jantar / Café da tarde",
    "Lanche da noite"
]

def filtrar_alimentos(tipo_refeicao):
    """Filtra alimentos na base que sejam permitidos para o tipo de refeição."""
    alimentos = base[base["refeicao"].str.contains(tipo_refeicao, case=False, na=False)].copy()
    if alimentos.empty:
        # Fallback de segurança: retorna a base completa
        alimentos = base.copy()
    return alimentos

def selecionar_alimento(alimentos):
    """Seleciona aleatoriamente um alimento de um DataFrame."""
    if alimentos.empty:
        alimentos = base
    amostra = alimentos.sample()
    return {
        "id": int(amostra["id"].iloc[0]),
        "alimento": str(amostra["alimento"].iloc[0]),
        "proteina": float(amostra["proteina"].iloc[0]),
        "kcal": float(amostra["kcal"].iloc[0]),
        "cat": str(amostra["cat"].iloc[0])
    }

def calcular_nutrientes(alimento, tipo_refeicao="Geral"):
    """
    Calcula a quantidade em gramas e os nutrientes consumidos.
    As porções são calibradas por categoria e tipo de refeição para garantir
    refeições equilibradas e lanches mais leves.
    """
    cat = alimento["cat"]
    nome_lower = alimento["alimento"].lower()
    eh_lanche = "lanche" in tipo_refeicao.lower() or "ceia" in tipo_refeicao.lower()

    if cat == "Mistura":
        # Carnes, peixes e aves: porções moderadas (70g a 130g) para não estourar a proteína da refeição
        qntd = random.randint(70, 130)
    elif cat == "Nozes e sementes":
        # Castanhas são densas em calorias: porção controlada de 15g a 30g
        qntd = random.randint(15, 30)
    elif cat == "Leite e derivados":
        if "queijo" in nome_lower:
            qntd = random.randint(20, 45)
        else:
            # Iogurte ou leite
            qntd = random.randint(120, 180) if eh_lanche else random.randint(150, 200)
    elif cat == "Frutas":
        qntd = random.randint(80, 140)
    elif cat == "Cereais e derivados":
        if "pão" in nome_lower or "torrada" in nome_lower or "biscoito" in nome_lower:
            qntd = random.randint(30, 50)
        else:
            # Arroz ou macarrão
            qntd = random.randint(70, 140)
    elif cat == "Leguminosas e derivados":
        # Feijão ou lentilha
        qntd = random.randint(60, 110)
    elif cat == "Verduras, hortaliças e derivados":
        qntd = random.randint(50, 120)
    elif cat == "Ovos e derivados":
        # 1 ou 2 ovos (aprox. 50g ou 100g)
        qntd = random.choice([50, 100])
    else:
        qntd = random.randint(50, 120)

    proteina = (qntd / 100.0) * alimento["proteina"]
    kcal = (qntd / 100.0) * alimento["kcal"]

    return qntd, proteina, kcal

def gerar_refeicao(tipo_refeicao):
    """
    Gera uma refeição garantindo variação de classes (categorias).
    - Almoço e Jantar: 3 a 4 alimentos de categorias distintas (Mistura + Cereal + Leguminosa + Verdura).
    - Café da manhã: 2 a 3 alimentos de categorias distintas (ex: Cereal + Fruta/Laticínio/Ovo).
    - Lanches: 1 a 2 alimentos de categorias distintas (Fruta, Laticínio, Oleaginosa ou Cereal).
    """
    refeicao = []
    eh_principal = tipo_refeicao in ("Almoço", "Jantar", "Jantar / Café da tarde")
    eh_lanche = "lanche" in tipo_refeicao.lower() or "ceia" in tipo_refeicao.lower()

    if eh_principal:
        # Almoço e Jantar usam o pool de refeições principais
        alimentos_pool = filtrar_alimentos("Almoço")
        classes_selecionadas = set()

        # 1. Escolhe uma Mistura (proteína principal)
        misturas = alimentos_pool[alimentos_pool["cat"] == "Mistura"]
        if not misturas.empty:
            item_mistura = selecionar_alimento(misturas)
            qntd, prot, kcal = calcular_nutrientes(item_mistura, tipo_refeicao)
            item_mistura["quantidade"] = qntd
            item_mistura["proteina_consumida"] = prot
            item_mistura["kcal_consumida"] = kcal
            refeicao.append(item_mistura)
            classes_selecionadas.add(item_mistura["cat"])

        # 2. Escolhe outros acompanhamentos garantindo variação de classe
        outras_categorias = ["Cereais e derivados", "Leguminosas e derivados", "Verduras, hortaliças e derivados"]
        random.shuffle(outras_categorias)
        qntd_total = random.randint(3, 4)

        for cat in outras_categorias:
            if len(refeicao) >= qntd_total:
                break
            pool_cat = alimentos_pool[(alimentos_pool["cat"] == cat) & (~alimentos_pool["id"].isin([x["id"] for x in refeicao]))]
            if not pool_cat.empty:
                alimento = selecionar_alimento(pool_cat)
                qntd, prot, kcal = calcular_nutrientes(alimento, tipo_refeicao)
                alimento["quantidade"] = qntd
                alimento["proteina_consumida"] = prot
                alimento["kcal_consumida"] = kcal
                refeicao.append(alimento)
                classes_selecionadas.add(alimento["cat"])

    elif eh_lanche:
        # Lanches: 1 a 2 alimentos de categorias distintas
        alimentos_pool = filtrar_alimentos("Lanche")
        qntd_itens = random.randint(1, 2)
        classes_selecionadas = set()

        for _ in range(qntd_itens):
            candidatos = alimentos_pool[
                (~alimentos_pool["cat"].isin(classes_selecionadas)) &
                (~alimentos_pool["id"].isin([x["id"] for x in refeicao]))
            ]
            if candidatos.empty:
                candidatos = alimentos_pool[~alimentos_pool["id"].isin([x["id"] for x in refeicao])]
            if candidatos.empty:
                break

            alimento = selecionar_alimento(candidatos)
            qntd, prot, kcal = calcular_nutrientes(alimento, tipo_refeicao)
            alimento["quantidade"] = qntd
            alimento["proteina_consumida"] = prot
            alimento["kcal_consumida"] = kcal
            refeicao.append(alimento)
            classes_selecionadas.add(alimento["cat"])

    else:
        # Café da manhã: 2 a 3 alimentos de categorias distintas
        alimentos_pool = filtrar_alimentos("Café da manhã")
        qntd_itens = random.randint(2, 3)
        classes_selecionadas = set()

        for _ in range(qntd_itens):
            candidatos = alimentos_pool[
                (~alimentos_pool["cat"].isin(classes_selecionadas)) &
                (~alimentos_pool["id"].isin([x["id"] for x in refeicao]))
            ]
            if candidatos.empty:
                candidatos = alimentos_pool[~alimentos_pool["id"].isin([x["id"] for x in refeicao])]
            if candidatos.empty:
                break

            alimento = selecionar_alimento(candidatos)
            qntd, prot, kcal = calcular_nutrientes(alimento, tipo_refeicao)
            alimento["quantidade"] = qntd
            alimento["proteina_consumida"] = prot
            alimento["kcal_consumida"] = kcal
            refeicao.append(alimento)
            classes_selecionadas.add(alimento["cat"])

    return refeicao

def calcular_refeicao(refeicao):
    """Calcula o total de kcal e proteína de uma lista de alimentos de uma refeição."""
    total_kcal = sum(item["kcal_consumida"] for item in refeicao)
    total_proteina = sum(item["proteina_consumida"] for item in refeicao)
    return total_kcal, total_proteina

def gerar_dieta():
    """Gera uma dieta diária completa com as 6 refeições solicitadas."""
    dieta = {
        "Café da manhã": gerar_refeicao("Café da manhã"),
        "Lanche da manhã": gerar_refeicao("Lanche"),
        "Almoço": gerar_refeicao("Almoço"),
        "Lanche da tarde": gerar_refeicao("Lanche"),
        "Jantar / Café da tarde": gerar_refeicao("Jantar"),
        "Lanche da noite": gerar_refeicao("Lanche")
    }
    return dieta

def calcular_dieta(dieta):
    """Calcula o total diário de calorias e proteínas somando todas as refeições."""
    total_kcal = 0.0
    total_proteina = 0.0

    for refeicao in dieta.values():
        kcal, proteina = calcular_refeicao(refeicao)
        total_kcal += kcal
        total_proteina += proteina

    return total_kcal, total_proteina

def gerar_dieta_semanal():
    """Gera o planejamento completo para os 7 dias da semana."""
    semana = {}
    for dia in range(7):
        semana[f"dia{dia + 1}"] = gerar_dieta()
    return semana

def exibir_refeicao(refeicao, nome):
    """Imprime no terminal os alimentos e totais de uma refeição."""
    print(f"\n========== {nome.upper()} ==========")
    for alimento in refeicao:
        print(f"\n{alimento['alimento']} ({alimento['cat']})")
        print(f"Quantidade: {alimento['quantidade']}g")
        print(f"Proteína: {alimento['proteina_consumida']:.2f}g")
        print(f"Calorias: {alimento['kcal_consumida']:.2f} kcal")
    kcal, prot = calcular_refeicao(refeicao)
    print(f"\nTOTAL DA REFEIÇÃO: {kcal:.1f} kcal | {prot:.1f}g de proteína")

if __name__ == "__main__":
    semana = gerar_dieta_semanal()
    print("Dias na semana:", len(semana))
    for dia, dieta in semana.items():
        print(f"{dia}: {len(dieta)} refeições")
        for nome_ref, itens in dieta.items():
            kcal, prot = calcular_refeicao(itens)
            print(f"  - {nome_ref}: {len(itens)} itens | {kcal:.1f} kcal | {prot:.1f}g prot")
