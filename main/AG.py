"""Algoritmo genético para montar um plano alimentar de 7 dias.

Integração esperada:
    from AG import executar_ag
    executar_ag(usuario)

A base deve ter as colunas padronizadas pelo arquivo base_alimentos_.py:
    id, nome_alimento, refeicao, energia_kcal, proteina_g

Por padrão, os valores nutricionais são interpretados como valores por 100 g.
Caso a planilha já informe os valores por porção, altere BASE_POR_100G para False.
"""

from __future__ import annotations

import copy
import random
import unicodedata
from typing import Any

import pandas as pd


# Ajuste para False caso Energia(kcal) e Proteína(g) já estejam calculadas por porção.
BASE_POR_100G = True

DIAS_SEMANA = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
]

CHAVES_REFEICOES = ("cafe_da_manha", "almoco", "terceira_refeicao", "lanches")


# ----------------------------------------------------------------------
# Preparação e leitura da base
# ----------------------------------------------------------------------

def normalizar_texto(valor: Any) -> str:
    """Remove acentos e padroniza texto para facilitar a comparação."""
    texto = str(valor).strip().casefold()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(caractere for caractere in texto if not unicodedata.combining(caractere))


def carregar_base_padrao():
    """Importa a base existente sem exigir que ela seja carregada ao importar AG.py."""
    try:
        from base_alimentos import base
    except FileNotFoundError as erro:
        raise FileNotFoundError(
            "Não encontrei alimentos.xlsx. Deixe a planilha na mesma pasta dos arquivos Python."
        ) from erro
    except ModuleNotFoundError as erro:
        raise ModuleNotFoundError(
            "Não encontrei base_alimentos.py. Deixe esse arquivo na mesma pasta de AG.py."
        ) from erro

    return base


class AlgoritmoGenetico:
    """Gera e evolui cromossomos que representam uma semana de alimentação."""

    def __init__(
        self,
        pessoa,
        base_alimentos=None,
        terceira_refeicao="jantar",
        base_por_100g=BASE_POR_100G,
        tamanho_populacao=50,
        geracoes=100,
        taxa_mutacao=0.15,
        elitismo=2,
        seed=None,
    ):
        self.pessoa = pessoa
        self.base_por_100g = base_por_100g
        self.tamanho_populacao = max(4, int(tamanho_populacao))
        self.geracoes = max(1, int(geracoes))
        self.taxa_mutacao = float(taxa_mutacao)
        self.elitismo = max(1, min(int(elitismo), self.tamanho_populacao - 1))
        self.rng = random.Random(seed)

        self.meta_kcal = float(pessoa.meta_kcal)
        self.meta_prot = float(pessoa.meta_prot)

        if self.meta_kcal <= 0 or self.meta_prot <= 0:
            raise ValueError("As metas calórica e proteica precisam ser maiores que zero.")

        if base_alimentos is None:
            base_alimentos = carregar_base_padrao()

        self.base = self._preparar_base(base_alimentos)
        self.terceira_refeicao = normalizar_texto(terceira_refeicao)
        self.nome_terceira_refeicao = "Café da tarde" if self.terceira_refeicao == "cafe da tarde" else "Jantar"
        self.jantar_usa_almoco = False

        self.pools = self._montar_pools()

    @staticmethod
    def _preparar_base(base_alimentos):
        colunas = {"id", "nome_alimento", "refeicao", "energia_kcal", "proteina_g"}
        faltantes = colunas.difference(base_alimentos.columns)
        if faltantes:
            raise ValueError(
                "A base de alimentos não possui as colunas necessárias: "
                + ", ".join(sorted(faltantes))
            )

        base = base_alimentos[list(colunas)].copy()
        base["id"] = pd.to_numeric(base["id"], errors="coerce")
        base["energia_kcal"] = pd.to_numeric(
            base["energia_kcal"], errors="coerce"
        )
        base["proteina_g"] = pd.to_numeric(
            base["proteina_g"], errors="coerce"
        )
        base = base.dropna(subset=["id", "nome_alimento", "refeicao", "energia_kcal", "proteina_g"])
        base = base[(base["energia_kcal"] >= 0) & (base["proteina_g"] >= 0)]
        base["id"] = base["id"].astype(int)
        base["refeicao_normalizada"] = base["refeicao"].map(normalizar_texto)

        alimentos = []
        for linha in base.to_dict(orient="records"):
            alimentos.append({
                "id": int(linha["id"]),
                "nome": str(linha["nome_alimento"]),
                "refeicao": str(linha["refeicao"]),
                "refeicao_normalizada": linha["refeicao_normalizada"],
                "energia": float(linha["energia_kcal"]),
                "proteina": float(linha["proteina_g"]),
            })

        # Remove IDs repetidos para evitar que o mesmo registro apareça duplicado nos pools.
        unicos_por_id = {}
        for alimento in alimentos:
            unicos_por_id[alimento["id"]] = alimento

        if not unicos_por_id:
            raise ValueError("A base não possui alimentos válidos para montar o plano.")

        return list(unicos_por_id.values())

    def _pool_por_refeicao(self, termos):
        termos = [normalizar_texto(termo) for termo in termos]
        return [
            alimento
            for alimento in self.base
            if any(termo in alimento["refeicao_normalizada"] for termo in termos)
        ]

    def _montar_pools(self):
        cafe = self._pool_por_refeicao(["cafe da manha"])
        almoco = self._pool_por_refeicao(["almoco"])
        lanches = self._pool_por_refeicao(["lanche"])

        if self.terceira_refeicao == "cafe da tarde":
            terceira = self._pool_por_refeicao(["cafe da tarde"])
            if not terceira:
                # Algumas planilhas classificam o café da tarde como lanche da tarde.
                terceira = self._pool_por_refeicao(["lanche da tarde"])
        elif self.terceira_refeicao == "jantar":
            terceira = self._pool_por_refeicao(["jantar"])
            if not terceira:
                # Fallback solicitado: usa alimentos classificados como Almoço para o jantar.
                terceira = almoco
                self.jantar_usa_almoco = True
        else:
            raise ValueError("A terceira refeição deve ser 'cafe da tarde' ou 'jantar'.")

        if not cafe:
            raise ValueError("Não encontrei alimentos classificados como 'Café da manhã' na coluna Refeição.")
        if not almoco:
            raise ValueError("Não encontrei alimentos classificados como 'Almoço' na coluna Refeição.")
        if not terceira:
            raise ValueError(f"Não encontrei alimentos para a refeição '{self.nome_terceira_refeicao}'.")
        if not lanches:
            raise ValueError("Não encontrei alimentos classificados como 'Lanche' na coluna Refeição.")

        return {
            "cafe_da_manha": cafe,
            "almoco": almoco,
            "terceira_refeicao": terceira,
            "lanches": lanches,
        }

    # ------------------------------------------------------------------
    # Representação do cromossomo e cálculo nutricional
    # ------------------------------------------------------------------

    def _quantidade_aleatoria(self, tipo):
        if self.base_por_100g:
            limites = {
                "cafe_da_manha": (50, 250),
                "almoco": (80, 300),
                "terceira_refeicao": (50, 250),
                "lanche": (30, 180),
            }
            minimo, maximo = limites[tipo]
            return self.rng.randrange(minimo, maximo + 1, 10)

        return self.rng.choice([0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0])

    def _novo_item(self, pool, tipo, ids_usados=None):
        candidatos = pool
        if ids_usados:
            diferentes = [item for item in pool if item["id"] not in ids_usados]
            if diferentes:
                candidatos = diferentes

        alimento = self.rng.choice(candidatos)
        return {
            "id": alimento["id"],
            "quantidade": self._quantidade_aleatoria(tipo),
        }

    def _novo_grupo(self, pool, tipo, minimo, maximo):
        quantidade = self.rng.randint(minimo, maximo)
        quantidade = min(quantidade, len(pool))
        selecionados = self.rng.sample(pool, k=quantidade)

        return [
            {
                "id": alimento["id"],
                "quantidade": self._quantidade_aleatoria(tipo),
            }
            for alimento in selecionados
        ]

    def _novo_dia(self):
        return {
            "cafe_da_manha": self._novo_grupo(
                self.pools["cafe_da_manha"], "cafe_da_manha", 1, 3
            ),
            "almoco": self._novo_grupo(self.pools["almoco"], "almoco", 2, 4),
            "terceira_refeicao": self._novo_grupo(
                self.pools["terceira_refeicao"], "terceira_refeicao", 1, 3
            ),
            # Cada gene de lanche representa uma opção/porção entre as refeições.
            "lanches": [
                self._novo_item(self.pools["lanches"], "lanche")
                for _ in range(self.rng.randint(2, 4))
            ],
        }

    def _novo_cromossomo(self):
        return [self._novo_dia() for _ in DIAS_SEMANA]

    def _alimento_por_id(self, id_alimento):
        # A base é pequena o suficiente para esta busca e mantém o código simples.
        for alimento in self.base:
            if alimento["id"] == id_alimento:
                return alimento
        raise KeyError(f"Alimento com ID {id_alimento} não encontrado na base.")

    def _nutrientes_item(self, item):
        alimento = self._alimento_por_id(item["id"])
        fator = item["quantidade"] / 100 if self.base_por_100g else item["quantidade"]
        return alimento["energia"] * fator, alimento["proteina"] * fator

    def _totais_dia(self, dia):
        energia = 0.0
        proteina = 0.0

        for chave in CHAVES_REFEICOES:
            for item in dia[chave]:
                kcal, prot = self._nutrientes_item(item)
                energia += kcal
                proteina += prot

        return energia, proteina

    # ------------------------------------------------------------------
    # Função de avaliação: aproxima as metas e evita almoços repetidos
    # ------------------------------------------------------------------

    @staticmethod
    def _assinatura_refeicao(grupo):
        return tuple(sorted(item["id"] for item in grupo))

    def _avaliar(self, cromossomo):
        penalidade = 0.0
        assinaturas_almoco = []

        for dia in cromossomo:
            kcal, proteina = self._totais_dia(dia)

            erro_kcal = abs(kcal - self.meta_kcal) / self.meta_kcal
            erro_prot = abs(proteina - self.meta_prot) / self.meta_prot

            # A proteína recebe peso ligeiramente maior na função de avaliação.
            penalidade += erro_kcal + (1.25 * erro_prot)

            # Evita que o algoritmo resolva toda a meta incluindo lanches em excesso.
            penalidade += max(0, len(dia["lanches"]) - 4) * 0.015

            assinaturas_almoco.append(self._assinatura_refeicao(dia["almoco"]))

        # Penaliza principalmente a repetição exata do almoço em dias consecutivos.
        for indice in range(1, len(assinaturas_almoco)):
            anterior = set(assinaturas_almoco[indice - 1])
            atual = set(assinaturas_almoco[indice])
            if anterior == atual:
                penalidade += 0.8
            elif anterior and atual:
                semelhanca = len(anterior.intersection(atual)) / len(anterior.union(atual))
                penalidade += semelhanca * 0.08

        return 1 / (1 + penalidade)

    # ------------------------------------------------------------------
    # Operadores do algoritmo genético
    # ------------------------------------------------------------------

    def _selecao(self, populacao, notas, tamanho_torneio=3):
        indices = self.rng.sample(range(len(populacao)), k=min(tamanho_torneio, len(populacao)))
        melhor_indice = max(indices, key=lambda indice: notas[indice])
        return populacao[melhor_indice]

    def _cruzamento(self, pai1, pai2):
        filho = []
        for indice in range(len(DIAS_SEMANA)):
            dia_filho = {}
            for chave in CHAVES_REFEICOES:
                origem = pai1[indice] if self.rng.random() < 0.5 else pai2[indice]
                dia_filho[chave] = copy.deepcopy(origem[chave])
            filho.append(dia_filho)
        return filho

    def _mutar_grupo(self, grupo, pool, tipo, minimo, maximo):
        acao = self.rng.choice(["trocar", "quantidade", "adicionar", "remover"])

        if acao == "quantidade" and grupo:
            item = self.rng.choice(grupo)
            item["quantidade"] = self._quantidade_aleatoria(tipo)

        elif acao == "trocar" and grupo:
            indice = self.rng.randrange(len(grupo))
            ids_usados = {item["id"] for pos, item in enumerate(grupo) if pos != indice}
            grupo[indice] = self._novo_item(pool, tipo, ids_usados)

        elif acao == "adicionar" and len(grupo) < maximo:
            ids_usados = {item["id"] for item in grupo}
            grupo.append(self._novo_item(pool, tipo, ids_usados))

        elif acao == "remover" and len(grupo) > minimo:
            grupo.pop(self.rng.randrange(len(grupo)))

    def _mutar(self, cromossomo):
        for dia in cromossomo:
            if self.rng.random() >= self.taxa_mutacao:
                continue

            chave = self.rng.choice(CHAVES_REFEICOES)
            if chave == "cafe_da_manha":
                self._mutar_grupo(dia[chave], self.pools[chave], chave, 1, 3)
            elif chave == "almoco":
                self._mutar_grupo(dia[chave], self.pools[chave], chave, 2, 4)
            elif chave == "terceira_refeicao":
                self._mutar_grupo(dia[chave], self.pools[chave], chave, 1, 3)
            else:
                lanches = dia["lanches"]
                acao = self.rng.choice(["adicionar", "remover", "trocar", "quantidade"])

                if acao == "adicionar" and len(lanches) < 6:
                    lanches.append(self._novo_item(self.pools["lanches"], "lanche"))
                elif acao == "remover" and len(lanches) > 1:
                    lanches.pop(self.rng.randrange(len(lanches)))
                elif acao == "trocar" and lanches:
                    indice = self.rng.randrange(len(lanches))
                    lanches[indice] = self._novo_item(self.pools["lanches"], "lanche")
                elif acao == "quantidade" and lanches:
                    item = self.rng.choice(lanches)
                    item["quantidade"] = self._quantidade_aleatoria("lanche")

    def gerar(self):
        """Executa o algoritmo e retorna o melhor cromossomo encontrado."""
        populacao = [self._novo_cromossomo() for _ in range(self.tamanho_populacao)]

        for _ in range(self.geracoes):
            notas = [self._avaliar(individuo) for individuo in populacao]
            ordem = sorted(range(len(populacao)), key=lambda indice: notas[indice], reverse=True)

            nova_populacao = [copy.deepcopy(populacao[indice]) for indice in ordem[:self.elitismo]]

            while len(nova_populacao) < self.tamanho_populacao:
                pai1 = self._selecao(populacao, notas)
                pai2 = self._selecao(populacao, notas)
                filho = self._cruzamento(pai1, pai2)
                self._mutar(filho)
                nova_populacao.append(filho)

            populacao = nova_populacao

        melhor = max(populacao, key=self._avaliar)
        return melhor

    # ------------------------------------------------------------------
    # Exibição do plano
    # ------------------------------------------------------------------

    def _descricao_item(self, item):
        alimento = self._alimento_por_id(item["id"])
        kcal, prot = self._nutrientes_item(item)

        if self.base_por_100g:
            quantidade = f"{item['quantidade']} g"
        else:
            quantidade = f"{item['quantidade']:.2f} porção(ões)"

        return (
            f"{alimento['nome']} — {quantidade} "
            f"({kcal:.0f} kcal | {prot:.1f} g proteína)"
        )

    def exibir_plano(self, cromossomo):
        print("\n" + "=" * 68)
        print("PLANO ALIMENTAR SEMANAL — ALGORITMO GENÉTICO")
        print("=" * 68)
        print(f"Meta diária: {self.meta_kcal:.0f} kcal | {self.meta_prot:.1f} g de proteína")

        if self.jantar_usa_almoco:
            print("Observação: não há categoria 'Jantar' na base; foram usados itens de 'Almoço'.")

        for indice, dia in enumerate(cromossomo):
            print(f"\n{DIAS_SEMANA[indice].upper()}")
            print("-" * 68)

            print("Café da manhã:")
            for item in dia["cafe_da_manha"]:
                print(f"  • {self._descricao_item(item)}")

            lanches = dia["lanches"]
            if lanches:
                print(f"Lanche da manhã: {self._descricao_item(lanches[0])}")

            print("Almoço:")
            for item in dia["almoco"]:
                print(f"  • {self._descricao_item(item)}")

            if len(lanches) > 1:
                print(f"Lanche da tarde: {self._descricao_item(lanches[1])}")
            for indice_lanche, item in enumerate(lanches[2:], start=1):
                print(f"Lanche extra {indice_lanche}: {self._descricao_item(item)}")

            print(f"{self.nome_terceira_refeicao}:")
            for item in dia["terceira_refeicao"]:
                print(f"  • {self._descricao_item(item)}")

            kcal, prot = self._totais_dia(dia)
            diferenca_kcal = kcal - self.meta_kcal
            diferenca_prot = prot - self.meta_prot
            print(
                f"Total do dia: {kcal:.0f} kcal | {prot:.1f} g proteína "
                f"(diferença: {diferenca_kcal:+.0f} kcal; {diferenca_prot:+.1f} g proteína)"
            )

        media_kcal = sum(self._totais_dia(dia)[0] for dia in cromossomo) / len(cromossomo)
        media_prot = sum(self._totais_dia(dia)[1] for dia in cromossomo) / len(cromossomo)
        print("\n" + "=" * 68)
        print(f"Média diária da semana: {media_kcal:.0f} kcal | {media_prot:.1f} g proteína")
        print(f"Avaliação do cromossomo: {self._avaliar(cromossomo):.4f}")
        print("=" * 68)


def executar_ag(pessoa, base_alimentos=None):
    """Pergunta a terceira refeição, gera o plano e o exibe no terminal."""
    print("\nQual será a terceira refeição principal do seu dia?")
    print("1 - Café da tarde")
    print("2 - Jantar")

    while True:
        opcao = input("Escolha uma opção (1 ou 2): ").strip()
        if opcao == "1":
            terceira_refeicao = "cafe da tarde"
            break
        if opcao == "2":
            terceira_refeicao = "jantar"
            break
        print("Opção inválida. Digite 1 ou 2.")

    algoritmo = AlgoritmoGenetico(
        pessoa=pessoa,
        base_alimentos=base_alimentos,
        terceira_refeicao=terceira_refeicao,
        base_por_100g=BASE_POR_100G,
    )

    melhor_cromossomo = algoritmo.gerar()
    algoritmo.exibir_plano(melhor_cromossomo)
    return melhor_cromossomo


if __name__ == "__main__":
    # Execução independente para testes: coleta os dados do usuário primeiro.
    from pessoa import Pessoa

    usuario = Pessoa()
    usuario.coletar_dados()
    usuario.calculo_geral()
    usuario.exibir_perfil()
    executar_ag(usuario)
