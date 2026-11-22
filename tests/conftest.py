import pandas as pd
import pytest
from pessoa import Pessoa


@pytest.fixture
def dataframe_alimentos_bruto():
    """Simula o DataFrame exato lido da planilha 'alimentos (1).xlsx'."""
    return pd.DataFrame({
        "ID": [1, 2, 3, 4, 5, 6, 7, "ID", None],
        "Descrição dos alimentos": [
            "Aveia em flocos",
            "Ovo cozido",
            "Arroz integral",
            "Peito de frango grelhado",
            "Feijão carioca",
            "Banana prata",
            "Iogurte natural",
            "Descrição dos alimentos",  # Linha de cabeçalho repetida a ser filtrada
            "Linha inválida",
        ],
        "Categoria": [
            "Cereais e derivados",
            "Ovos e derivados",
            "Cereais e derivados",
            "Carnes e derivados",
            "Leguminosas",
            "Frutas",
            "Leite e derivados",
            "Categoria",
            "Frutas",
        ],
        "Refeição": [
            "Café da manhã",
            "Café da manhã",
            "Almoço",
            "Almoço",
            "Jantar",
            "Lanche",
            "Café da tarde",
            "Refeição",
            "Lanche",
        ],
        "Energia(kcal)": [394.0, 155.0, 124.0, 165.0, 76.0, 98.0, 61.0, "Energia(kcal)", None],
        "Proteína(g)": [13.9, 13.0, 2.6, 31.0, 4.8, 1.3, 3.5, "Proteína(g)", 1.0],
    })


@pytest.fixture
def base_alimentos_padronizada():
    """DataFrame já limpo e padronizado no formato esperado por AG.py."""
    return pd.DataFrame([
        {"id": 1, "nome_alimento": "Aveia", "refeicao": "Café da manhã", "energia_kcal": 394.0, "proteina_g": 13.9},
        {"id": 2, "nome_alimento": "Ovo", "refeicao": "Café da manhã", "energia_kcal": 155.0, "proteina_g": 13.0},
        {"id": 3, "nome_alimento": "Pão integral", "refeicao": "Café da manhã", "energia_kcal": 250.0, "proteina_g": 9.0},
        {"id": 4, "nome_alimento": "Arroz", "refeicao": "Almoço", "energia_kcal": 130.0, "proteina_g": 2.7},
        {"id": 5, "nome_alimento": "Frango", "refeicao": "Almoço", "energia_kcal": 165.0, "proteina_g": 31.0},
        {"id": 6, "nome_alimento": "Feijão", "refeicao": "Almoço", "energia_kcal": 76.0, "proteina_g": 4.8},
        {"id": 7, "nome_alimento": "Brócolis", "refeicao": "Almoço", "energia_kcal": 35.0, "proteina_g": 2.8},
        {"id": 8, "nome_alimento": "Sopa de legumes", "refeicao": "Jantar", "energia_kcal": 60.0, "proteina_g": 3.0},
        {"id": 9, "nome_alimento": "Omelete", "refeicao": "Jantar", "energia_kcal": 154.0, "proteina_g": 11.0},
        {"id": 10, "nome_alimento": "Banana", "refeicao": "Lanche", "energia_kcal": 89.0, "proteina_g": 1.1},
        {"id": 11, "nome_alimento": "Castanha", "refeicao": "Lanche", "energia_kcal": 607.0, "proteina_g": 14.0},
        {"id": 12, "nome_alimento": "Iogurte", "refeicao": "Café da tarde", "energia_kcal": 61.0, "proteina_g": 3.5},
    ])


@pytest.fixture
def usuario_masculino():
    p = Pessoa()
    p.nome = "Thiago"
    p.sexo = "Masculino"
    p.idade = 28
    p.peso = 101.0
    p.altura = 183.0
    p.atividade_fisica = 1.2
    p.objetivo = "Emagrecimento"
    p.calculo_geral()
    return p