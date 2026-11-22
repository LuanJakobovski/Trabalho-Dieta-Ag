import pytest
from base_alimentos import base
from dieta import gerar_dieta, gerar_dieta_semanal, calcular_dieta, NOMES_REFEICOES
from ag2 import avaliar_dieta, algoritmo_genetico

class TestNovasRegras:
    def test_seis_refeicoes_por_dia(self):
        """1- Garante que cada dia tem exatamente as 6 refeições solicitadas."""
        dieta = gerar_dieta()
        assert len(dieta) == 6
        assert list(dieta.keys()) == NOMES_REFEICOES
        assert "Café da manhã" in dieta
        assert "Lanche da manhã" in dieta
        assert "Almoço" in dieta
        assert "Lanche da tarde" in dieta
        assert "Jantar / Café da tarde" in dieta
        assert "Lanche da noite" in dieta

        semana = gerar_dieta_semanal()
        assert len(semana) == 7
        for dia_nome, dia_refeicoes in semana.items():
            assert len(dia_refeicoes) == 6

    def test_base_reduzida_e_simplificada(self):
        """4- Garante base reduzida e sem variações excessivas do mesmo alimento."""
        # Deve ter apenas 1 tipo de arroz (Arroz cozido)
        arroz = base[base["alimento"].str.contains("arroz", case=False)]
        assert len(arroz) == 1
        assert "Arroz cozido" in arroz.iloc[0]["alimento"]

        # Deve ter apenas peito de frango grelhado padrão
        frango = base[base["alimento"].str.contains("frango", case=False)]
        assert len(frango) == 1

        # Deve ter carne bovina simplificada (1 variação padrão)
        carne = base[base["alimento"].str.contains("carne bovina", case=False)]
        assert len(carne) == 1

        # Base total reduzida para menos de 35 itens
        assert len(base) <= 30

    def test_heuristica_punicao_proteina_maior_que_meta_dividida_por_seis(self):
        """2- A heurística irá punir refeição com proteína > meta_prot / 6."""
        meta_kcal = 2000.0
        meta_prot = 120.0
        limite_prot = meta_prot / 6.0  # 20g por refeição

        dieta_equilibrada = {
            "Café da manhã": [{"cat": "Cereais e derivados", "proteina_consumida": 10.0, "kcal_consumida": 200.0}],
            "Lanche da manhã": [{"cat": "Frutas", "proteina_consumida": 2.0, "kcal_consumida": 80.0}],
            "Almoço": [{"cat": "Mistura", "proteina_consumida": 18.0, "kcal_consumida": 400.0}],
            "Lanche da tarde": [{"cat": "Leite e derivados", "proteina_consumida": 5.0, "kcal_consumida": 100.0}],
            "Jantar / Café da tarde": [{"cat": "Mistura", "proteina_consumida": 18.0, "kcal_consumida": 400.0}],
            "Lanche da noite": [{"cat": "Nozes e sementes", "proteina_consumida": 3.0, "kcal_consumida": 100.0}],
        }
        fitness_equilibrado = avaliar_dieta(dieta_equilibrada, meta_kcal, meta_prot)

        # Dieta desequilibrada: joga 45g de proteína numa única refeição (ultrapassa 20g)
        dieta_desequilibrada = {
            "Café da manhã": [{"cat": "Cereais e derivados", "proteina_consumida": 2.0, "kcal_consumida": 200.0}],
            "Lanche da manhã": [{"cat": "Frutas", "proteina_consumida": 1.0, "kcal_consumida": 80.0}],
            "Almoço": [{"cat": "Mistura", "proteina_consumida": 45.0, "kcal_consumida": 400.0}],  # > 20g!
            "Lanche da tarde": [{"cat": "Leite e derivados", "proteina_consumida": 2.0, "kcal_consumida": 100.0}],
            "Jantar / Café da tarde": [{"cat": "Mistura", "proteina_consumida": 4.0, "kcal_consumida": 400.0}],
            "Lanche da noite": [{"cat": "Nozes e sementes", "proteina_consumida": 2.0, "kcal_consumida": 100.0}],
        }
        fitness_desequilibrado = avaliar_dieta(dieta_desequilibrada, meta_kcal, meta_prot)

        # A dieta que concentra proteína em uma refeição deve receber fitness menor (punição)
        assert fitness_desequilibrado < fitness_equilibrado

    def test_heuristica_punicao_sem_variacao_de_classe(self):
        """2- A heurística irá punir refeições sem variações de classe."""
        meta_kcal = 2000.0
        meta_prot = 120.0

        # Refeição de almoço variada: Mistura + Cereal + Leguminosa
        dieta_com_variacao = {
            "Café da manhã": [{"cat": "Cereais e derivados", "proteina_consumida": 5.0, "kcal_consumida": 150.0}],
            "Lanche da manhã": [{"cat": "Frutas", "proteina_consumida": 2.0, "kcal_consumida": 80.0}],
            "Almoço": [
                {"cat": "Mistura", "proteina_consumida": 15.0, "kcal_consumida": 200.0},
                {"cat": "Cereais e derivados", "proteina_consumida": 3.0, "kcal_consumida": 150.0},
                {"cat": "Leguminosas e derivados", "proteina_consumida": 4.0, "kcal_consumida": 90.0}
            ],
            "Lanche da tarde": [{"cat": "Frutas", "proteina_consumida": 2.0, "kcal_consumida": 80.0}],
            "Jantar / Café da tarde": [{"cat": "Mistura", "proteina_consumida": 15.0, "kcal_consumida": 250.0}],
            "Lanche da noite": [{"cat": "Frutas", "proteina_consumida": 2.0, "kcal_consumida": 80.0}],
        }

        # Refeição de almoço sem variação: 3 itens da MESMA categoria ("Mistura")
        dieta_sem_variacao = {
            "Café da manhã": [{"cat": "Cereais e derivados", "proteina_consumida": 5.0, "kcal_consumida": 150.0}],
            "Lanche da manhã": [{"cat": "Frutas", "proteina_consumida": 2.0, "kcal_consumida": 80.0}],
            "Almoço": [
                {"cat": "Mistura", "proteina_consumida": 15.0, "kcal_consumida": 200.0},
                {"cat": "Mistura", "proteina_consumida": 3.0, "kcal_consumida": 150.0},
                {"cat": "Mistura", "proteina_consumida": 4.0, "kcal_consumida": 90.0}
            ],
            "Lanche da tarde": [{"cat": "Frutas", "proteina_consumida": 2.0, "kcal_consumida": 80.0}],
            "Jantar / Café da tarde": [{"cat": "Mistura", "proteina_consumida": 15.0, "kcal_consumida": 250.0}],
            "Lanche da noite": [{"cat": "Frutas", "proteina_consumida": 2.0, "kcal_consumida": 80.0}],
        }

        fit_com = avaliar_dieta(dieta_com_variacao, meta_kcal, meta_prot)
        fit_sem = avaliar_dieta(dieta_sem_variacao, meta_kcal, meta_prot)

        assert fit_sem < fit_com

    def test_heuristica_recompensa_lanches_menos_caloricos(self):
        """3- Lanches irão recompensar refeições menos calóricas."""
        meta_kcal = 2000.0
        meta_prot = 120.0

        # Caso A: Lanches leves (menos calóricos)
        dieta_lanches_leves = {
            "Café da manhã": [{"cat": "Cereais e derivados", "proteina_consumida": 10.0, "kcal_consumida": 300.0}],
            "Lanche da manhã": [{"cat": "Frutas", "proteina_consumida": 2.0, "kcal_consumida": 80.0}],  # Leve
            "Almoço": [{"cat": "Mistura", "proteina_consumida": 18.0, "kcal_consumida": 500.0}],
            "Lanche da tarde": [{"cat": "Leite e derivados", "proteina_consumida": 4.0, "kcal_consumida": 90.0}],  # Leve
            "Jantar / Café da tarde": [{"cat": "Mistura", "proteina_consumida": 18.0, "kcal_consumida": 500.0}],
            "Lanche da noite": [{"cat": "Frutas", "proteina_consumida": 2.0, "kcal_consumida": 60.0}],  # Leve
        }

        # Caso B: Lanches pesados (muito calóricos, acima de meta_kcal / 6)
        dieta_lanches_pesados = {
            "Café da manhã": [{"cat": "Cereais e derivados", "proteina_consumida": 10.0, "kcal_consumida": 300.0}],
            "Lanche da manhã": [{"cat": "Nozes e sementes", "proteina_consumida": 2.0, "kcal_consumida": 450.0}],  # Pesado
            "Almoço": [{"cat": "Mistura", "proteina_consumida": 18.0, "kcal_consumida": 500.0}],
            "Lanche da tarde": [{"cat": "Nozes e sementes", "proteina_consumida": 4.0, "kcal_consumida": 450.0}],  # Pesado
            "Jantar / Café da tarde": [{"cat": "Mistura", "proteina_consumida": 18.0, "kcal_consumida": 500.0}],
            "Lanche da noite": [{"cat": "Nozes e sementes", "proteina_consumida": 2.0, "kcal_consumida": 450.0}],  # Pesado
        }

        fit_leves = avaliar_dieta(dieta_lanches_leves, meta_kcal, meta_prot)
        fit_pesados = avaliar_dieta(dieta_lanches_pesados, meta_kcal, meta_prot)

        # Lanches mais leves devem ser recompensados com maior fitness
        assert fit_leves > fit_pesados
