import importlib
import sys
import pandas as pd
import pytest


@pytest.fixture
def modulo_base(monkeypatch, dataframe_alimentos_bruto):
    """Importa base_alimentos simulando pd.read_excel para não depender do arquivo físico."""
    monkeypatch.setattr(pd, "read_excel", lambda _: dataframe_alimentos_bruto.copy())
    if "base_alimentos" in sys.modules:
        del sys.modules["base_alimentos"]
    mod = importlib.import_module("base_alimentos")
    yield mod
    if "base_alimentos" in sys.modules:
        del sys.modules["base_alimentos"]


def test_limpeza_de_dados_ao_importar(modulo_base):
    # Deve remover o cabeçalho duplicado ("ID") e a linha com Energia None
    assert len(modulo_base.base) == 7
    assert modulo_base.base["id"].dtype.kind in ("i", "u")
    assert "Descrição dos alimentos" not in modulo_base.base["nome_alimento"].values


def test_consultar_alimento_existente(modulo_base):
    res = modulo_base.consultar_alimento(1)
    assert res == {
        "ID": 1,
        "Nome": "Aveia em flocos",
        "Categoria": "Cereais e derivados",
        "Refeição": "Café da manhã",
        "Energia (kcal)": 394.0,
        "Proteína (g)": 13.9,
    }


def test_consultar_alimento_inexistente(modulo_base, capsys):
    res = modulo_base.consultar_alimento(9999)
    saida = capsys.readouterr().out
    assert res is None
    assert "9999" in saida


def test_consultar_varios_alimentos_ignora_inexistentes(modulo_base):
    df = modulo_base.consultar_varios_alimentos([1, 999, 2])
    assert isinstance(df, pd.DataFrame)
    assert list(df["ID"]) == [1, 2]


def test_consultar_categoria_ignora_maiusculas(modulo_base):
    df = modulo_base.consultar_categoria("cereais e derivados")
    assert len(df) == 2
    assert set(df["id"]) == {1, 3}


def test_consultar_refeicao_ignora_maiusculas(modulo_base):
    df = modulo_base.consultar_refeicao("almoço")
    assert len(df) == 2
    assert set(df["id"]) == {3, 4}


def test_consultar_nome_parcial(modulo_base):
    df = modulo_base.consultar_nome("arroz")
    assert len(df) == 1
    assert df.iloc[0]["id"] == 3


def test_calcular_nutrientes(modulo_base):
    res = modulo_base.calcular_nutrientes([1, 2])
    assert res["Energia total (kcal)"] == pytest.approx(394.0 + 155.0)
    assert res["Proteína total (g)"] == pytest.approx(13.9 + 13.0)


def test_calcular_nutrientes_lista_vazia_ou_invalida(modulo_base):
    assert modulo_base.calcular_nutrientes([9999]) is None