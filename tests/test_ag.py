import pandas as pd
import pytest
from AG import (
    CHAVES_REFEICOES,
    DIAS_SEMANA,
    AlgoritmoGenetico,
    executar_ag,
    normalizar_texto,
)


class TestUtilidadesAG:
    def test_normalizar_texto(self):
        assert normalizar_texto("  Café da Manhã  ") == "cafe da manha"
        assert normalizar_texto("ALMOÇO") == "almoco"
        assert normalizar_texto("Proteína") == "proteina"


class TestValidacoesInicializacaoAG:
    def test_metas_nao_positivas_geram_erro(self, usuario_masculino, base_alimentos_padronizada):
        usuario_masculino.meta_kcal = 0
        with pytest.raises(ValueError, match="maiores que zero"):
            AlgoritmoGenetico(usuario_masculino, base_alimentos=base_alimentos_padronizada)

    def test_colunas_faltantes_geram_erro(self, usuario_masculino):
        df_incompleto = pd.DataFrame({"id": [1], "nome_alimento": ["Pão"]})
        with pytest.raises(ValueError, match="colunas necessárias"):
            AlgoritmoGenetico(usuario_masculino, base_alimentos=df_incompleto)

    def test_terceira_refeicao_invalida_gera_erro(self, usuario_masculino, base_alimentos_padronizada):
        with pytest.raises(ValueError, match="terceira refeição"):
            AlgoritmoGenetico(
                usuario_masculino,
                base_alimentos=base_alimentos_padronizada,
                terceira_refeicao="ceia",
            )

    def test_fallback_jantar_usa_almoco(self, usuario_masculino, base_alimentos_padronizada):
        base_sem_jantar = base_alimentos_padronizada[
            base_alimentos_padronizada["refeicao"] != "Jantar"
        ].copy()

        ag = AlgoritmoGenetico(
            usuario_masculino,
            base_alimentos=base_sem_jantar,
            terceira_refeicao="jantar",
            seed=42,
        )
        assert ag.jantar_usa_almoco is True
        assert ag.pools["terceira_refeicao"] == ag.pools["almoco"]

    def test_fallback_cafe_da_tarde_para_lanche_da_tarde(self, usuario_masculino, base_alimentos_padronizada):
        base_mod = base_alimentos_padronizada.copy()
        base_mod.loc[base_mod["refeicao"] == "Café da tarde", "refeicao"] = "Lanche da tarde"

        ag = AlgoritmoGenetico(
            usuario_masculino,
            base_alimentos=base_mod,
            terceira_refeicao="cafe da tarde",
            seed=42,
        )
        assert len(ag.pools["terceira_refeicao"]) == 1
        assert ag.pools["terceira_refeicao"][0]["nome"] == "Iogurte"

    def test_pool_vazio_gera_erro(self, usuario_masculino, base_alimentos_padronizada):
        sem_cafe = base_alimentos_padronizada[
            base_alimentos_padronizada["refeicao"] != "Café da manhã"
        ].copy()
        with pytest.raises(ValueError, match="Café da manhã"):
            AlgoritmoGenetico(usuario_masculino, base_alimentos=sem_cafe)


class TestOperadoresEEvolucaoAG:
    def test_calculo_nutrientes_por_100g_vs_porcao(self, usuario_masculino, base_alimentos_padronizada):
        # ID 1 = Aveia: 394 kcal, 13.9 g prot por 100g
        ag_100g = AlgoritmoGenetico(
            usuario_masculino, base_alimentos=base_alimentos_padronizada, base_por_100g=True, seed=1
        )
        kcal, prot = ag_100g._nutrientes_item({"id": 1, "quantidade": 50})
        assert kcal == pytest.approx(197.0)
        assert prot == pytest.approx(6.95)

        ag_porcao = AlgoritmoGenetico(
            usuario_masculino, base_alimentos=base_alimentos_padronizada, base_por_100g=False, seed=1
        )
        kcal_p, prot_p = ag_porcao._nutrientes_item({"id": 1, "quantidade": 1.5})
        assert kcal_p == pytest.approx(394.0 * 1.5)
        assert prot_p == pytest.approx(13.9 * 1.5)

    def test_estrutura_cromossomo_e_determinismo_com_seed(self, usuario_masculino, base_alimentos_padronizada):
        ag1 = AlgoritmoGenetico(
            usuario_masculino, base_alimentos=base_alimentos_padronizada, tamanho_populacao=8, geracoes=3, seed=123
        )
        ag2 = AlgoritmoGenetico(
            usuario_masculino, base_alimentos=base_alimentos_padronizada, tamanho_populacao=8, geracoes=3, seed=123
        )
        c1 = ag1.gerar()
        c2 = ag2.gerar()

        assert c1 == c2
        assert len(c1) == len(DIAS_SEMANA) == 7
        for dia in c1:
            assert set(dia.keys()) == set(CHAVES_REFEICOES)
            assert 1 <= len(dia["cafe_da_manha"]) <= 3
            assert 2 <= len(dia["almoco"]) <= 4
            assert 1 <= len(dia["terceira_refeicao"]) <= 3
            assert 1 <= len(dia["lanches"]) <= 6

    def test_penalizacao_almoco_repetido_consecutivo(self, usuario_masculino, base_alimentos_padronizada):
        ag = AlgoritmoGenetico(
            usuario_masculino, base_alimentos=base_alimentos_padronizada, seed=42
        )
        cromo = ag._novo_cromossomo()
        # Força exatamente o mesmo almoço no dia 0 e no dia 1
        cromo[1]["almoco"] = [dict(x) for x in cromo[0]["almoco"]]
        nota_repetido = ag._avaliar(cromo)

        cromo_distinto = [
            {k: [dict(item) for item in v] for k, v in dia.items()}
            for dia in cromo
        ]
        # Troca o dia 1 com o dia 6 para remover a repetição em dias seguidos
        cromo_distinto[1], cromo_distinto[6] = cromo_distinto[6], cromo_distinto[1]
        assert ag._avaliar(cromo_distinto) != nota_repetido

    def test_exibir_plano_e_executar_ag(self, usuario_masculino, base_alimentos_padronizada, monkeypatch, capsys):
        entradas = iter(["9", "2"])  # Primeira tentativa inválida, segunda válida ("jantar")
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))

        melhor = executar_ag(usuario_masculino, base_alimentos=base_alimentos_padronizada)
        saida = capsys.readouterr().out

        assert len(melhor) == 7
        assert "PLANO ALIMENTAR SEMANAL" in saida
        assert "SEGUNDA-FEIRA" in saida
        assert "DOMINGO" in saida
        assert "Média diária da semana" in saida