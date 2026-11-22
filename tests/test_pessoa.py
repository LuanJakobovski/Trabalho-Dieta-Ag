import pytest
from pessoa import Pessoa


class TestPessoaCalculos:
    def test_calcular_tmb_masculino(self):
        p = Pessoa()
        p.sexo = "Masculino"
        p.peso = 80
        p.altura = 180
        p.idade = 30
        # (10*80) + (6.25*180) - (5*30) + 5 = 800 + 1125 - 150 + 5 = 1780
        assert p.calcular_tmb() == pytest.approx(1780.0)

    def test_calcular_tmb_feminino(self):
        p = Pessoa()
        p.sexo = "Feminino"
        p.peso = 60
        p.altura = 165
        p.idade = 25
        # (10*60) + (6.25*165) - (5*25) - 161 = 600 + 1031.25 - 125 - 161 = 1345.25
        assert p.calcular_tmb() == pytest.approx(1345.25)

    def test_calcular_get(self):
        p = Pessoa()
        p.tmb = 1800.0
        p.atividade_fisica = 1.55
        assert p.calcular_get() == pytest.approx(2790.0)

    @pytest.mark.parametrize(
        "objetivo, delta_kcal, fator_prot",
        [
            ("Emagrecimento", -400, 2.0),
            ("Manter peso", 0, 1.6),
            ("Ganho de massa muscular", 400, 1.8),
        ],
    )
    def test_metas_por_objetivo(self, objetivo, delta_kcal, fator_prot):
        p = Pessoa()
        p.peso = 75.0
        p.get = 2500.0
        p.objetivo = objetivo

        assert p.meta_calorica() == pytest.approx(2500.0 + delta_kcal)
        assert p.meta_proteica() == pytest.approx(75.0 * fator_prot)

    def test_calculo_geral_integrado(self, usuario_masculino):
        # Thiago: peso=101, altura=183, idade=28, Masculino, fator=1.2, Emagrecimento
        tmb_esperada = (10 * 101) + (6.25 * 183) - (5 * 28) + 5  # 2018.75
        get_esperado = tmb_esperada * 1.2  # 2422.5
        assert usuario_masculino.tmb == pytest.approx(tmb_esperada)
        assert usuario_masculino.get == pytest.approx(get_esperado)
        assert usuario_masculino.meta_kcal == pytest.approx(get_esperado - 400)
        assert usuario_masculino.meta_prot == pytest.approx(202.0)


class TestPessoaInteracaoTerminal:
    def test_coletar_dados_com_tentativas_invalidas(self, monkeypatch):
        entradas = iter([
            "Ana",      # nome
            "9",        # sexo inválido -> pede novamente
            "2",        # sexo válido (Feminino)
            "29",       # idade
            "62,5",     # peso com vírgula
            "1,68",     # altura em metros -> converte para 168 cm
            "0",        # atividade inválida -> pede novamente
            "3",        # atividade válida (1.55)
            "99",       # objetivo inválido -> pede novamente
            "2",        # objetivo válido ("Manter peso")
        ])
        monkeypatch.setattr("builtins.input", lambda _: next(entradas))

        p = Pessoa()
        p.coletar_dados()

        assert p.nome == "Ana"
        assert p.sexo == "Feminino"
        assert p.idade == 29
        assert p.peso == pytest.approx(62.5)
        assert p.altura == pytest.approx(168.0)
        assert p.atividade_fisica == pytest.approx(1.55)
        assert p.objetivo == "Manter peso"

    def test_exibir_perfil_imprime_valores(self, usuario_masculino, capsys):
        usuario_masculino.exibir_perfil()
        saida = capsys.readouterr().out
        assert "Thiago" in saida
        assert "Emagrecimento" in saida
        assert "Meta Calórica" in saida
        assert "Meta Proteica" in saida