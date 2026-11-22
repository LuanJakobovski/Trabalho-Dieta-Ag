# 🥗 Trabalho-Dieta-Ag: Planejamento Alimentar Semanal com Algoritmo Genético

Aplicação em Python para geração e otimização automatizada de dietas semanais personalizadas utilizando **Algoritmos Genéticos (AG)**. O sistema calcula as necessidades energéticas e proteicas do indivíduo com base em dados antropométricos e gera um cardápio semanal completo distribuído em **6 refeições diárias**, aplicando heurísticas nutricionais avançadas de variedade e equilíbrio.

---

## 📌 Sumário
1. [Visão Geral e Diferenciais](#-visão-geral-e-diferenciais)
2. [Regras de Negócio e Cálculos Nutricionais](#-regras-de-negócio-e-cálculos-nutricionais)
3. [Modelagem do Algoritmo Genético](#-modelagem-do-algoritmo-genético)
4. [Estrutura do Projeto e Explicação dos Arquivos](#-estrutura-do-projeto-e-explicação-dos-arquivos)
5. [Como Configurar e Rodar o Projeto](#-como-configurar-e-rodar-o-projeto)
   - [Configuração de Permissão no PowerShell](#passo-1-habilitar-execução-de-scripts-no-powershell)
   - [Criação e Ativação do Ambiente Virtual](#passo-2-criar-e-ativar-o-ambiente-virtual)
   - [Instalação das Dependências](#passo-3-instalar-dependências)
   - [Execução da Aplicação](#passo-4-executar-a-aplicação)
6. [Execução dos Testes Automatizados](#-execução-dos-testes-automatizados)
7. [Exemplo de Saída (`dieta.txt`)](#-exemplo-de-saída-dietatxt)

---

## 🚀 Visão Geral e Diferenciais

O projeto foi projetado para resolver o problema clássico de otimização de dieta (*Diet Problem*) respeitando restrições realistas do cotidiano:
* **6 Refeições Diárias**: Café da manhã, Lanche da manhã, Almoço, Lanche da tarde, Jantar / Café da tarde e Lanche da noite (Ceia).
* **Heurística de Diversidade de Classes**: Punição de refeições sem variação de categoria de alimento (ex.: proíbe refeições compostas apenas por proteínas ou apenas carboidratos).
* **Distribuição Proteica Equilibrada**: Punição para refeições que concentrem proteína acima da meta diária dividida por 6 ($\text{meta\_proteina} / 6$), evitando sobrecargas pontuais.
* **Recompensa para Lanches Leves**: A função de aptidão (*fitness*) premia dias em que os lanches intermediários são menos calóricos, promovendo um padrão alimentar mais saudável.
* **Base de Alimentos Padronizada**: Catálogo enxuto e higienizado com 28 alimentos essenciais sem variações repetitivas (ex.: apenas arroz cozido padrão, peito de frango grelhado, etc.).

---

## 📐 Regras de Negócio e Cálculos Nutricionais

As fórmulas metabólicas estão encapsuladas na classe `Pessoa` (`main/pessoa.py`):

### 1. Taxa Metabólica Basal (TMB) — Fórmula de Mifflin-St Jeor
Estima o gasto calórico mínimo em repouso:
* **Homens**:
  $$\text{TMB} = (10 \times \text{peso}_{\text{kg}}) + (6.25 \times \text{altura}_{\text{cm}}) - (5 \times \text{idade}) + 5$$
* **Mulheres**:
  $$\text{TMB} = (10 \times \text{peso}_{\text{kg}}) + (6.25 \times \text{altura}_{\text{cm}}) - (5 \times \text{idade}) - 161$$

### 2. Gasto Energético Total (GET)
Multiplica a TMB pelo fator de atividade física:
$$\text{GET} = \text{TMB} \times \text{fator}$$

| Opção | Nível de Atividade | Fator Multiplicador |
| :---: | :--- | :---: |
| 1 | Sedentário | 1.200 |
| 2 | Levemente ativo | 1.375 |
| 3 | Moderadamente ativo | 1.550 |
| 4 | Muito ativo | 1.725 |
| 5 | Extremamente ativo | 1.900 |

### 3. Metas Diárias por Objetivo

| Objetivo | Ajuste Calórico (kcal/dia) | Meta de Proteína (g/kg/dia) |
| :--- | :---: | :---: |
| **Emagrecimento** | $\text{GET} - 400$ kcal | $2.0 \times \text{peso}$ |
| **Manter peso** | $\text{GET}$ | $1.6 \times \text{peso}$ |
| **Ganho de massa muscular** | $\text{GET} + 400$ kcal | $1.8 \times \text{peso}$ |

---

## 🧬 Modelagem do Algoritmo Genético

O algoritmo genético está implementado em `main/ag2.py` e opera sobre as seguintes estruturas:

### 1. Representação do Cromossomo (Indivíduo)
Cada indivíduo representa um **plano semanal completo** de 7 dias (`dia1` a `dia7`). Cada dia é composto por um dicionário com as 6 refeições, contendo listas de alimentos com ID, nome, categoria, gramatura consumida e nutrientes calculados.

### 2. Função de Aptidão (Fitness) e Heurísticas
A função `avaliar_dieta()` avalia o custo total de desvio nutricional e penalidades:
1. **Erro de Calorias Diárias**: $\text{erro\_kcal} = \frac{|\text{meta\_kcal} - \text{kcal\_dia}|}{\text{meta\_kcal}}$
2. **Erro de Proteínas Diárias**: $\text{erro\_prot} = \frac{|\text{meta\_prot} - \text{prot\_dia}|}{\text{meta\_prot}}$
3. **Punição por Teto de Proteína por Refeição**:
   $$\text{limite\_prot} = \frac{\text{meta\_proteina}}{6}$$
   $$\text{Se } \text{prot\_ref} > \text{limite\_prot} \implies \text{penalidade\_prot} += \frac{\text{prot\_ref} - \text{limite\_prot}}{\text{limite\_prot}}$$
4. **Punição por Falta de Variação de Classe**:
   - Refeição com 2+ itens todos da mesma categoria: penalidade severa ($+1.0$).
   - Refeição com repetição parcial de categoria: penalidade $+0.3$ por item duplicado.
5. **Recompensa para Lanches Menos Calóricos**:
   - Referência de lanche leve: $\text{limite\_kcal\_lanche} = \frac{\text{meta\_kcal}}{6}$.
   - Se o lanche tiver calorias abaixo desse limite:
     $$\text{fator\_economia} = \frac{\text{limite\_kcal\_lanche} - \text{kcal\_lanche}}{\text{limite\_kcal\_lanche}}$$
     $$\text{recompensa\_lanches} += \text{fator\_economia} \times 0.15$$
   - Se for excessivamente calórico, recebe penalidade proporcional.

**Cálculo Consolidado do Fitness**:
$$\text{custo\_total} = (1.2 \times \text{erro\_kcal}) + (1.0 \times \text{erro\_prot}) + (0.5 \times \text{penalidade\_prot}) + (0.4 \times \text{penalidade\_classe}) + (0.25 \times \text{penalidade\_lanche\_pesado})$$
$$\text{multiplicador\_recompensa} = 1.0 + \min(0.35, \text{recompensa\_lanches})$$
$$\text{fitness} = \frac{\text{multiplicador\_recompensa}}{1.0 + \text{custo\_total}}$$

### 3. Operadores Genéticos
* **Seleção**: Seleção por torneio de tamanho 3 (`selecionar_individuo`).
* **Cruzamento (Crossover)**: Crossover uniforme por dia entre os dois pais selecionados.
* **Mutação Multinível**:
  * 45% de chance: Ajuste fino de quantidade em gramas ($\pm 15$g a $\pm 50$g) respeitando limites saudáveis por categoria (ex.: oleaginosas limitadas a 35g).
  * 35% de chance: Troca e regeneração de uma refeição individual completa.
  * 20% de chance: Regeneração completa de um dia da semana.
* **Elitismo**: Preserva intactos os 2 melhores indivíduos de cada geração.

---

## 📁 Estrutura do Projeto e Explicação dos Arquivos

```text
Trabalho-Dieta-Ag/
├── README.md                 # Este documento de documentação
├── requirements.txt          # Dependências do projeto (pandas, openpyxl, pytest)
├── alimentos.xlsx            # Base de dados com 28 alimentos limpos e padronizados
├── .gitignore                # Arquivos ignorados pelo controle de versão
├── main/
│   ├── main.py               # Interface CLI, executa o fluxo e grava 'dieta.txt'
│   ├── pessoa.py             # Classe Pessoa (coleta de dados, TMB, GET e metas)
│   ├── base_alimentos.py     # Carga, sanitização e funções de busca na base de alimentos
│   ├── dieta.py              # Composição das 6 refeições, pools de alimentos e cálculos
│   ├── ag2.py                # Algoritmo Genético ativo com novas heurísticas e mutação
│   └── AG.py                 # Algoritmo Genético alternativo orientado a objetos
└── tests/
    ├── conftest.py            # Fixtures compartilhadas para testes
    ├── test_novas_regras.py   # Testes das 4 regras (6 refeições, punições, lanches, base)
    ├── test_pessoa.py         # Testes de TMB, GET e cálculos de metas do usuário
    ├── test_base_alimentos.py # Testes de filtros e consultas na base de alimentos
    └── test_ag.py             # Testes do módulo AG.py
```

---

## 💻 Como Configurar e Rodar o Projeto

Siga os passos abaixo para configurar o ambiente no Windows utilizando o **PowerShell**.

### Passo 1: Habilitar Execução de Scripts no PowerShell

Por padrão de segurança, o Windows bloqueia a execução de scripts no PowerShell (gerando o erro: `File ... Activate.ps1 cannot be loaded because running scripts is disabled on this system`).

Para liberar a execução apenas para o seu usuário atual de forma segura:

1. Abra o **PowerShell** (não precisa ser como Administrador).
2. Execute o seguinte comando:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

3. Pressione `S` (Sim) e aperte `Enter` para confirmar.

> [!NOTE]
> O escopo `CurrentUser` afeta apenas o seu usuário local, sem alterar políticas globais da máquina. O nível `RemoteSigned` permite rodar scripts locais criados por você (como o script de ativação do ambiente virtual).

---

### Passo 2: Criar e Ativar o Ambiente Virtual

Navegue até a pasta do projeto:

```powershell
cd D:\Projeto-Prático\Trabalho-Dieta-Ag
```

Crie o ambiente virtual (recomendado Python 3.10 ou superior):

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

*(O prompt do terminal agora exibirá `(.venv)` no início da linha, indicando que o ambiente está ativo).*

---

### Passo 3: Instalar Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```powershell
pip install -r requirements.txt
```

As dependências principais são:
* `pandas`: Leitura e manipulação da base nutricional.
* `openpyxl`: Suporte para leitura de arquivos `.xlsx` do Excel.
* `pytest`: Execução da suíte de testes automatizados.

---

### Passo 4: Executar a Aplicação

Para iniciar o gerador de dietas, execute:

```powershell
python main/main.py
```

O sistema fará perguntas interativas pelo terminal:
1. Seu nome.
2. Sexo biológico (Masculino ou Feminino).
3. Idade (anos).
4. Peso corporal (kg).
5. Altura (metros ou centímetros, ex.: `1.80` ou `180`).
6. Nível de atividade física (1 a 5).
7. Objetivo nutricional (Emagrecimento, Manter peso ou Ganho de massa muscular).

Ao concluir a evolução do Algoritmo Genético, o plano semanal completo será exibido e salvo automaticamente no arquivo **`dieta.txt`**.

---

## 🧪 Execução dos Testes Automatizados

O projeto possui **34 testes unitários automatizados** cobrindo todas as fórmulas metabólicas, queries da base de dados e operadores do Algoritmo Genético.

Para rodar todos os testes com o ambiente ativado:

```powershell
$env:PYTHONPATH="main"; pytest tests
```

Para rodar com relatório detalhado de cada teste individual:

```powershell
$env:PYTHONPATH="main"; pytest tests -v
```

---

## 📄 Exemplo de Saída (`dieta.txt`)

Trecho do arquivo gerado pelo sistema:

```text
PLANO ALIMENTAR SEMANAL (6 REFEIÇÕES DIÁRIAS)
============================================================

========================= DIA1 =========================

CAFÉ DA MANHÃ
-----------------------------------
  • Queijo mozarela (Leite e derivados) - 30g | 99.0 kcal | 6.8g proteína
  • Maçã (Frutas) - 92g | 57.5 kcal | 0.2g proteína
  • Ovo de galinha cozido (Ovos e derivados) - 100g | 145.7 kcal | 13.3g proteína
SUBTOTAL: 302.2 kcal | 20.3g proteína

LANCHE DA MANHÃ
-----------------------------------
  • Torrada (Cereais e derivados) - 35g | 132.1 kcal | 3.7g proteína
SUBTOTAL: 132.1 kcal | 3.7g proteína

ALMOÇO
-----------------------------------
  • Peito de frango grelhado (Mistura) - 85g | 135.3 kcal | 27.2g proteína
  • Arroz cozido (Cereais e derivados) - 130g | 166.7 kcal | 3.3g proteína
  • Feijão carioca cozido (Leguminosas e derivados) - 90g | 68.8 kcal | 4.3g proteína
  • Brócolis cozido (Verduras, hortaliças e derivados) - 75g | 18.5 kcal | 1.6g proteína
SUBTOTAL: 389.3 kcal | 36.4g proteína

LANCHE DA TARDE
-----------------------------------
  • Iogurte natural (Leite e derivados) - 150g | 77.2 kcal | 6.1g proteína
SUBTOTAL: 77.2 kcal | 6.1g proteína

JANTAR / CAFÉ DA TARDE
-----------------------------------
  • Salmão grelhado (Mistura) - 90g | 205.9 kcal | 21.5g proteína
  • Batata inglesa cozida (Verduras, hortaliças e derivados) - 80g | 41.3 kcal | 0.9g proteína
  • Lentilha cozida (Leguminosas e derivados) - 70g | 64.8 kcal | 4.4g proteína
SUBTOTAL: 312.0 kcal | 26.8g proteína

LANCHE DA NOITE
-----------------------------------
  • Banana prata (Frutas) - 100g | 98.2 kcal | 1.3g proteína
SUBTOTAL: 98.2 kcal | 1.3g proteína

-----------------------------------
TOTAL DO DIA: 1411.0 kcal | 94.6g proteína
```

---

## 👥 Autores e Contribuições

Projeto desenvolvido no âmbito acadêmico para resolução prática do problema de planejamento alimentar utilizando algoritmos bioinspirados e inteligência artificial.
