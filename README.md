# Trabalho-Dieta-Ag: Planejamento Alimentar Semanal com Algoritmo Genético

Sistema em Python voltado para a criação e otimização automatizada de cardápios semanais personalizados utilizando princípios de Computação Evolutiva (Algoritmos Genéticos). A aplicação avalia as características corporais e a rotina do usuário para calcular suas necessidades energéticas e de macronutrientes, estruturando uma dieta completa de segunda a domingo, distribuída em seis refeições diárias com variedade alimentar e equilíbrio nutricional.

---

## Sumário

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Conceitos Fundamentais para Usuários sem Conhecimento Prévio](#conceitos-fundamentais-para-usuários-sem-conhecimento-prévio)
   - [O que são Calorias e Macronutrientes?](#o-que-são-calorias-e-macronutrientes)
   - [O que são TMB e GET?](#o-que-são-tmb-e-get)
   - [O que é um Algoritmo Genético? (Analogia Simples)](#o-que-é-um-algoritmo-genético-analogia-simples)
3. [Diferenciais e Regras Nutricionais do Sistema](#diferenciais-e-regras-nutricionais-do-sistema)
   - [Estrutura de Seis Refeições Diárias](#estrutura-de-seis-refeições-diárias)
   - [Variedade de Grupos de Alimentos no Prato](#variedade-de-grupos-de-alimentos-no-prato)
   - [Distribuição Segura de Proteína ao Longo do Dia](#distribuição-segura-de-proteína-ao-longo-do-dia)
   - [Incentivo a Lanches Intermediários Leves](#incentivo-a-lanches-intermediários-leves)
   - [Base de Alimentos Higienizada e Padronizada](#base-de-alimentos-higienizada-e-padronizada)
4. [Fundamentos Matemáticos e Fórmulas Nutricionais](#fundamentos-matemáticos-e-fórmulas-nutricionais)
   - [Taxa Metabólica Basal (Equação de Mifflin-St Jeor)](#taxa-metabólica-basal-equação-de-mifflin-st-jeor)
   - [Gasto Energético Total (GET) e Fatores de Atividade](#gasto-energético-total-get-e-fatores-de-atividade)
   - [Metas Diárias de Energia e Proteínas por Objetivo](#metas-diárias-de-energia-e-proteínas-por-objetivo)
5. [Modelagem Técnica do Algoritmo Genético](#modelagem-técnica-do-algoritmo-genético)
   - [Estrutura do Cromossomo (Indivíduo)](#estrutura-do-cromossomo-indivíduo)
   - [Função de Aptidão (Fitness) e Penalidades](#função-de-aptidão-fitness-e-penalidades)
   - [Operadores Genéticos: Seleção, Cruzamento, Mutação e Elitismo](#operadores-genéticos-seleção-cruzamento-mutação-e-elitismo)
6. [Estrutura do Repositório e Descrição dos Módulos](#estrutura-do-repositório-e-descrição-dos-módulos)
7. [Guia Passo a Passo de Instalação e Execução](#guia-passo-a-passo-de-instalação-e-execução)
   - [Pré-requisitos](#pré-requisitos)
   - [Passo 1: Habilitar Execução de Scripts no PowerShell](#passo-1-habilitar-execução-de-scripts-no-powershell)
   - [Passo 2: Acessar a Pasta do Projeto no Terminal](#passo-2-acessar-a-pasta-do-projeto-no-terminal)
   - [Passo 3: Criar e Ativar o Ambiente Virtual](#passo-3-criar-e-ativar-o-ambiente-virtual)
   - [Passo 4: Instalar as Bibliotecas Necessárias](#passo-4-instalar-as-bibliotecas-necessárias)
   - [Passo 5: Executar o Programa](#passo-5-executar-o-programa)
8. [Manual de Utilização do Sistema](#manual-de-utilização-do-sistema)
   - [Perguntas Apresentadas no Terminal](#perguntas-apresentadas-no-terminal)
   - [Processamento Evolutivo](#processamento-evolutivo)
9. [Como Interpretar o Arquivo Gerado (dieta.txt)](#como-interpretar-o-arquivo-gerado-dietatxt)
   - [Organização das Informações](#organização-das-informações)
   - [Exemplo de Visualização](#exemplo-de-visualização)
10. [Diagnóstico e Solução de Problemas Comuns](#diagnóstico-e-solução-de-problemas-comuns)
11. [Execução dos Testes Automatizados](#execução-dos-testes-automatizados)
12. [Informações Acadêmicas e Autoria](#informações-acadêmicas-e-autoria)

---

## Sobre o Projeto

O planejamento dietético manual é uma tarefa complexa. É necessário escolher dezenas de alimentos, controlar pesos em gramas, atingir metas calóricas rigorosas e distribuir proteínas de forma saudável, evitando repetições cansativas ou combinações incoerentes. Na ciência da computação e na pesquisa operacional, esse desafio é conhecido como o **Problema da Dieta** (*Diet Problem*).

O **Trabalho-Dieta-Ag** resolve essa demanda por meio de inteligência artificial bioinspirada. Em vez de testar combinações manuais ou usar cálculos simplistas de tentativa e erro, o sistema gera uma população de dezenas de cardápios completos e faz com que eles evoluam ao longo de centenas de gerações. O resultado final é um cronograma de 7 dias com refeições equilibradas, calorias ajustadas e porções realistas.

---

## Conceitos Fundamentais para Usuários sem Conhecimento Prévio

Se você não tem formação em nutrição ou tecnologia da informação, os tópicos abaixo explicam de forma direta os conceitos utilizados pelo programa.

### O que são Calorias e Macronutrientes?

* **Caloria (kcal)**: É a unidade de medida da energia fornecida pelos alimentos. O corpo precisa de energia para respirar, bombear sangue, trabalhar e praticar exercícios. Se consumirmos mais calorias do que gastamos, o peso aumenta; se consumirmos menos, o peso diminui.
* **Proteína (g)**: Nutriente essencial para a construção e manutenção de tecidos, músculos, enzimas e células do sistema imunológico. Cada pessoa necessita de uma quantidade mínima de gramas diárias calculadas com base no seu peso corporal.
* **Carboidratos e Gorduras**: Fornecem energia imediata e de reserva, além de auxiliarem no funcionamento hormonal. No programa, esses nutrientes estão incorporados nos alimentos selecionados da base de dados.

### O que são TMB e GET?

* **Taxa Metabólica Basal (TMB)**: É a quantidade mínima de energia que o corpo gastaria em repouso absoluto ao longo de 24 horas apenas para manter órgãos vitais em funcionamento (coração, cérebro, pulmões).
* **Gasto Energético Total (GET)**: É a TMB somada ao esforço físico realizado durante o dia (caminhar, trabalhar, treinar). Uma pessoa muito ativa gasta substancialmente mais energia do que alguém sedentário, mesmo que ambas tenham peso e altura idênticos.

### O que é um Algoritmo Genético? (Analogia Simples)

Um **Algoritmo Genético** é uma técnica inspirada na teoria da evolução biológica de Charles Darwin. O funcionamento do programa pode ser entendido pela seguinte analogia:

1. **Criação da População**: O programa monta aleatoriamente 25 opções diferentes de cardápios semanais completos.
2. **Avaliação (Seleção Natural)**: Cada cardápio recebe uma nota (chamada de *fitness* ou pontuação de aptidão). Cardápios que chegam perto das metas de calorias, usam pratos variados e não exageram na proteína ganham notas altas. Cardápios desequilibrados recebem notas baixas.
3. **Cruzamento (Herança Genética)**: Os melhores cardápios são selecionados para "cruzar". O sistema combina os dias bem estruturados do Cardápio A com os dias bem estruturados do Cardápio B para gerar um novo cardápio "filho".
4. **Mutação**: Para evitar mesmice, o programa aplica pequenas alterações aleatórias, como aumentar ligeiramente a porção de arroz, trocar uma fruta ou substituir uma refeição inteira.
5. **Gerações Sucessivas**: Esse ciclo se repete 300 vezes em poucos segundos. Ao final da 300ª geração, o programa seleciona o cardápio mais refinado de toda a história do processo.

---

## Diferenciais e Regras Nutricionais do Sistema

Muitos algoritmos simples sugerem planos impraticáveis, como comer arroz puro ou consumir 150 gramas de frango logo pela manhã. Para contornar esse problema, este projeto implementa regras nutricionais avançadas:

### Estrutura de Seis Refeições Diárias

Cada dia da semana é obrigatoriamente dividido em seis refeições bem delineadas:
1. Café da manhã
2. Lanche da manhã
3. Almoço
4. Lanche da tarde
5. Jantar / Café da tarde
6. Lanche da noite (Ceia)

Essa segmentação garante que o consumo energético seja distribuído confortavelmente sem sobrecarregar a digestão.

### Variedade de Grupos de Alimentos no Prato

O algoritmo pune severamente refeições que contenham apenas uma categoria de alimento (por exemplo, um prato com dois tipos de carnes sem nenhum acompanhamento). 
* **Almoço e Jantar**: O sistema seleciona de 3 a 4 itens distintos, priorizando uma fonte proteica principal (categoria *Mistura*), um cereal, uma leguminosa e verduras/hortaliças.
* **Café da manhã**: Contém de 2 a 3 itens de classes distintas (como cereais, frutas e laticínios/ovos).
* **Lanches**: Compostos por 1 a 2 itens de categorias diferentes.

### Distribuição Segura de Proteína ao Longo do Dia

O trato gastrointestinal humano possui limites saudáveis de absorção e síntese proteica por momento alimentar. Por essa razão, o sistema define um teto de referência por refeição:

$$\text{Limite de Proteína por Refeição} = \frac{\text{Meta Proteica Diária}}{6}$$

Se uma refeição individual ultrapassar essa cota média, o algoritmo aplica uma penalidade matemática em sua pontuação, incentivando a redistribuição da proteína entre as outras refeições do dia.

### Incentivo a Lanches Intermediários Leves

Em uma rotina alimentar equilibrada, os lanches entre as refeições principais devem ser leves e funcionais. O algoritmo calcula um valor de referência calórico para os lanches:

$$\text{Limite Calórico de Lanche} = \frac{\text{Meta Calórica Diária}}{6}$$

Se um lanche contiver menos calorias que esse teto (por exemplo, uma fruta com castanhas ou um iogurte), a dieta recebe um bônus numérico na função de aptidão. Caso o lanche seja excessivamente pesado, ele recebe uma penalidade.

### Base de Alimentos Higienizada e Padronizada

O arquivo de dados nutricionais (`alimentos.xlsx`) contém 28 itens essenciais sem duplicidades confusas. Cada alimento possui sua classificação por categoria, indicação de refeição adequada, calorias e teor proteico aferidos para 100 gramas.

---

## Fundamentos Matemáticos e Fórmulas Nutricionais

Todos os cálculos biométricos são processados pela classe `Pessoa` localizada no módulo `main/pessoa.py`.

### Taxa Metabólica Basal (Equação de Mifflin-St Jeor)

Reconhecida internacionalmente como uma das fórmulas preditivas mais precisas da literatura científica:

* **Para indivíduos do sexo masculino**:
  $$\text{TMB} = (10 \times \text{peso em kg}) + (6.25 \times \text{altura em cm}) - (5 \times \text{idade}) + 5$$

* **Para indivíduos do sexo feminino**:
  $$\text{TMB} = (10 \times \text{peso em kg}) + (6.25 \times \text{altura em cm}) - (5 \times \text{idade}) - 161$$

### Gasto Energético Total (GET) e Fatores de Atividade

O GET representa o consumo calórico diário real, obtido pela multiplicação da TMB pelo fator correspondente ao estilo de vida:

$$\text{GET} = \text{TMB} \times \text{Fator de Atividade}$$

| Nível de Atividade | Descrição da Rotina | Fator Multiplicador |
| :--- | :--- | :---: |
| **1. Sedentário** | Trabalho sentado, pouco ou nenhum exercício semanal | 1.200 |
| **2. Levemente ativo** | Exercício leve de 1 a 3 dias por semana | 1.375 |
| **3. Moderadamente ativo** | Exercício moderado de 3 a 5 dias por semana | 1.550 |
| **4. Muito ativo** | Exercício pesado de 6 a 7 dias por semana | 1.725 |
| **5. Extremamente ativo** | Treinos intensos diários ou trabalho com grande esforço braçal | 1.900 |

### Metas Diárias de Energia e Proteínas por Objetivo

Conforme a meta selecionada pelo usuário, o sistema ajusta o balanço calórico e a oferta proteica:

| Objetivo | Ajuste Calórico Diário | Meta Proteica Diária |
| :--- | :---: | :---: |
| **Emagrecimento** | $\text{GET} - 400 \text{ kcal}$ (Déficit Calórico) | $2.0 \text{ g por kg de peso corporal}$ |
| **Manter peso** | $\text{GET}$ (Balanço Energético Neutro) | $1.6 \text{ g por kg de peso corporal}$ |
| **Ganho de massa muscular** | $\text{GET} + 400 \text{ kcal}$ (Superávit Calórico) | $1.8 \text{ g por kg de peso corporal}$ |

---

## Modelagem Técnica do Algoritmo Genético

A inteligência bioinspirada é executada no módulo `main/ag2.py`.

### Estrutura do Cromossomo (Indivíduo)

Um cromossomo completo representa um plano semanal de 7 dias (`dia1` a `dia7`). Cada dia é composto por um dicionário de 6 refeições, contendo listas de itens com os seguintes dados:
* Identificador único (`id`)
* Nome do alimento (`alimento`)
* Categoria nutricional (`cat`)
* Quantidade em gramas (`quantidade`)
* Calorias consumidas (`kcal_consumida`)
* Proteína consumida (`proteina_consumida`)

### Função de Aptidão (Fitness) e Penalidades

A função `avaliar_dieta()` processa o desvio nutricional e as restrições comportamentais da dieta:

1. **Desvio Percentual de Calorias Diárias**:
   $$\text{erro\_kcal} = \frac{|\text{meta\_kcal} - \text{kcal\_consumida}|}{\text{meta\_kcal}}$$

2. **Desvio Percentual de Proteínas Diárias**:
   $$\text{erro\_proteina} = \frac{|\text{meta\_proteina} - \text{proteina\_consumida}|}{\text{meta\_proteina}}$$

3. **Penalidade por Excesso de Proteína em uma Refeição**:
   $$\text{Se } \text{prot\_refeicao} > \frac{\text{meta\_proteina}}{6} \implies \text{penalidade} += \frac{\text{prot\_refeicao} - (\text{meta\_proteina}/6)}{\text{meta\_proteina}/6}$$

4. **Penalidade por Falta de Diversidade no Prato**:
   * Refeição com múltiplos alimentos da mesma categoria: penalidade severa de $+1.0$.
   * Repetição pontual de categoria: penalidade incremental de $+0.3$ por item repetido.

5. **Incentivo e Penalidade para Lanches**:
   * Se as calorias do lanche estiverem abaixo do teto de referência ($\text{meta\_kcal} / 6$):
     $$\text{fator\_economia} = \frac{\text{limite\_kcal\_lanche} - \text{kcal\_lanche}}{\text{limite\_kcal\_lanche}}$$
     $$\text{recompensa\_lanches} += \text{fator\_economia} \times 0.15$$
   * Se o lanche for excessivamente volumoso, aplica-se penalidade proporcional ao excedente.

**Consolidação da Função Custo e Fitness**:
$$\text{custo\_total} = 1.20 \cdot \text{erro\_kcal} + 1.00 \cdot \text{erro\_proteina} + 0.50 \cdot \text{penalidade\_proteina} + 0.40 \cdot \text{penalidade\_classe} + 0.25 \cdot \text{penalidade\_lanche}$$

$$\text{multiplicador\_recompensa} = 1.0 + \min(0.35, \text{recompensa\_lanches})$$

$$\text{fitness} = \frac{\text{multiplicador\_recompensa}}{1.0 + \text{custo\_total}}$$

Quanto mais próxima de 1.0 (ou superior) for a pontuação de aptidão, mais fiel à meta nutricional será o cardápio.

### Operadores Genéticos: Seleção, Cruzamento, Mutação e Elitismo

* **Seleção por Torneio**: Três indivíduos são sorteados aleatoriamente da população. Aquele que apresentar a maior nota de fitness vence o torneio e é qualificado para a reprodução.
* **Cruzamento Uniforme Diário (Crossover)**: Para cada dia da semana (de segunda a domingo), o novo indivíduo herda com 50% de probabilidade o planejamento correspondente do Pai 1 ou do Pai 2.
* **Mutação Multinível Calibrada**:
  * **45% de chance - Ajuste de Gramatura**: Altera a porção de um alimento sorteado ($\pm 15$g a $\pm 50$g) respeitando limites fisiológicos máximos por classe (oleaginosas limitadas a 35g, carnes e pescados limitados a 180g, queijos a 60g, etc.).
  * **35% de chance - Troca de Refeição**: Substitui uma refeição específica por uma nova combinação equilibrada.
  * **20% de chance - Regeneração Diária**: Reconstrói integralmente um dia da semana para escapar de mínimos locais.
* **Elitismo**: Os dois melhores indivíduos de cada geração são transferidos intactos para a geração seguinte, impedindo que boas soluções sejam perdidas ao longo do processo.

---

## Estrutura do Repositório e Descrição dos Módulos

```text
Trabalho-Dieta-Ag/
│
├── README.md                 # Documentação detalhada e guia de instruções
├── requirements.txt          # Lista de dependências externas para instalação
├── alimentos.xlsx            # Base de dados tabular com a composição dos 28 alimentos
├── .gitignore                # Arquivos e pastas excluídos do versionamento
│
├── main/
│   ├── main.py               # Ponto de entrada do programa: orquestra coleta, AG e exportação
│   ├── pessoa.py             # Classe Pessoa: coleta dados do usuário, calcula TMB, GET e metas
│   ├── base_alimentos.py     # Carga, sanitização de dados e consultas à planilha Excel
│   ├── dieta.py              # Regras de montagem das 6 refeições, porções e pools de categorias
│   ├── ag2.py                # Algoritmo Genético principal com heurísticas, mutação e fitness
│   └── AG.py                 # Implementação orientada a objetos alternativa do algoritmo genético
│
└── tests/
    ├── conftest.py            # Configuração compartilhada de fixtures para testes
    ├── test_novas_regras.py   # Testes unitários das regras nutricionais (6 refeições, lanches e teto)
    ├── test_pessoa.py         # Testes dos cálculos de TMB, GET e limites metabólicos
    ├── test_base_alimentos.py # Testes de filtros e sanitização da base de dados
    └── test_ag.py             # Testes de operadores genéticos e funções do módulo AG
```

---

## Guia Passo a Passo de Instalação e Execução

Este guia foi elaborado para qualquer pessoa conseguir executar o projeto em um computador com sistema operacional **Windows**, mesmo sem ter familiaridade com programação.

### Pré-requisitos

1. **Python Instalado**: O computador precisa ter o Python instalado (versão 3.10 ou superior recomendada).
   * Para verificar se o Python está instalado, pressione as teclas `Windows + R`, digite `powershell`, pressione `Enter` e digite:
     ```powershell
     python --version
     ```
   * Caso o comando retorne uma versão (por exemplo, `Python 3.11.x`), o ambiente está pronto. Caso exiba erro ou abra a Microsoft Store, faça o download gratuito no site oficial [python.org](https://www.python.org/downloads/) marcando a opção **"Add Python to PATH"** durante a instalação.

---

### Passo 1: Habilitar Execução de Scripts no PowerShell

O Windows possui uma configuração de segurança padrão que pode impedir a inicialização de ambientes virtuais, gerando a mensagem: `File ... Activate.ps1 cannot be loaded because running scripts is disabled on this system`.

Para autorizar a execução segura de scripts criados em seu próprio computador:

1. Abra o **PowerShell** no Windows (não é necessário executar como Administrador).
2. Cole o comando abaixo e pressione `Enter`:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

3. Digite `S` (para Sim) e aperte `Enter` para confirmar.

> [!NOTE]
> Essa configuração altera permissões apenas para o seu usuário local (`CurrentUser`) e permite unicamente a execução de scripts locais confiáveis, preservando a segurança do sistema operacional.

---

### Passo 2: Acessar a Pasta do Projeto no Terminal

No mesmo terminal do PowerShell, digite o comando `cd` acompanhado do caminho da pasta do projeto e pressione `Enter`:

```powershell
cd D:\Projeto-Prático\Trabalho-Dieta-Ag
```

*(Se o seu projeto estiver em outra pasta, ajuste o caminho para a localização correta no seu computador).*

---

### Passo 3: Criar e Ativar o Ambiente Virtual

O ambiente virtual cria um diretório isolado para as bibliotecas do projeto, evitando conflitos com outros programas:

1. Crie o ambiente virtual executando:

```powershell
python -m venv .venv
```

2. Ative o ambiente virtual executando:

```powershell
.venv\Scripts\Activate.ps1
```

Quando o ambiente estiver ativado com sucesso, o terminal exibirá a indicação `(.venv)` no início da linha de comando.

---

### Passo 4: Instalar as Bibliotecas Necessárias

Com o ambiente virtual ativado, instale os pacotes listados no arquivo `requirements.txt`:

```powershell
pip install -r requirements.txt
```

O instalador baixará automaticamente as seguintes dependências:
* **pandas**: Utilizado para carregar e consultar a tabela de alimentos.
* **openpyxl**: Permite a leitura nativa da planilha do Excel (`alimentos.xlsx`).
* **pytest**: Ferramenta de testes automatizados para verificação do código.

---

### Passo 5: Executar o Programa

Inicie a aplicação com o seguinte comando:

```powershell
python main/main.py
```

O sistema solicitará suas informações no terminal para dar início ao processo de montagem da dieta.

---

## Manual de Utilização do Sistema

Ao iniciar o programa, você responderá a sete perguntas no terminal:

### Perguntas Apresentadas no Terminal

1. **Nome**: Digite seu nome ou apelido e pressione `Enter`.
2. **Sexo Biológico**:
   * Digite `1` para **Masculino**.
   * Digite `2` para **Feminino**.
3. **Idade**: Digite sua idade em anos inteiros (exemplo: `28`).
4. **Peso**: Digite seu peso em quilogramas. O programa aceita tanto vírgula quanto ponto decimal (exemplo: `74.5` ou `74,5`).
5. **Altura**: Digite sua altura em metros (exemplo: `1.78`) ou em centímetros (exemplo: `178`). O sistema faz a conversão automaticamente.
6. **Nível de Atividade Física**: Escolha o número de 1 a 5 que melhor reflete sua rotina:
   * `1`: Sedentário (pouco ou nenhum movimento no dia a dia).
   * `2`: Levemente ativo (caminhadas ou exercícios de 1 a 3 vezes por semana).
   * `3`: Moderadamente ativo (atividades esportivas regulares de 3 a 5 vezes por semana).
   * `4`: Muito ativo (treinos intensos quase todos os dias).
   * `5`: Extremamente ativo (rotina diária pesada de atleta ou trabalho com esforço físico constante).
7. **Objetivo**: Escolha o número correspondente ao seu objetivo pessoal:
   * `1`: Emagrecimento (redução calórica orientada).
   * `2`: Manter peso (estabilidade energética).
   * `3`: Ganho de massa muscular (acréscimo de calorias e proteínas).

### Processamento Evolutivo

Assim que os dados são informados, o sistema exibe o perfil calculado na tela (TMB, GET, Meta Calórica e Meta de Proteína) e inicia o Algoritmo Genético. Em poucos segundos, 300 gerações de planos alimentares são processadas.

Ao finalizar, a aplicação exibe a pontuação final de aptidão (*fitness*) e cria o arquivo **`dieta.txt`** na pasta principal do projeto.

---

## Como Interpretar o Arquivo Gerado (dieta.txt)

O arquivo `dieta.txt` contém a distribuição completa da sua alimentação ao longo de todos os 7 dias da semana.

### Organização das Informações

Cada dia apresenta:
* As seis refeições com os alimentos selecionados, a respectiva categoria, o peso em gramas sugerido, as calorias e o teor de proteínas.
* **Subtotal da Refeição**: Soma calórica e proteica do momento alimentar.
* **Total do Dia**: Consumo calórico e proteico somado das 6 refeições.
* **Diferença das Metas**: Informa a variação do plano gerado em relação à sua meta teórica (exemplo: `+12.4 kcal`, `-1.2g proteína`), demonstrando a precisão do algoritmo.
* **Rodapé Informativo**: Repassa seus dados corporais, objetivos e a pontuação final do algoritmo genético.

### Exemplo de Visualização

```text
PLANO ALIMENTAR SEMANAL (6 REFEIÇÕES DIÁRIAS)
============================================================

========================= DIA1 =========================

CAFÉ DA MANHÃ
-----------------------------------
  • Queijo mozarela (Leite e derivados) - 30g | 99.0 kcal | 6.8g proteína
  • Maçã (Frutas) - 95g | 59.4 kcal | 0.2g proteína
  • Ovo de galinha cozido (Ovos e derivados) - 100g | 145.7 kcal | 13.3g proteína
SUBTOTAL: 304.1 kcal | 20.3g proteína

LANCHE DA MANHÃ
-----------------------------------
  • Torrada (Cereais e derivados) - 35g | 132.1 kcal | 3.7g proteína
SUBTOTAL: 132.1 kcal | 3.7g proteína

ALMOÇO
-----------------------------------
  • Peito de frango grelhado (Mistura) - 90g | 143.3 kcal | 28.8g proteína
  • Arroz cozido (Cereais e derivados) - 120g | 153.8 kcal | 3.0g proteína
  • Feijão carioca cozido (Leguminosas e derivados) - 80g | 61.1 kcal | 3.8g proteína
  • Brócolis cozido (Verduras, hortaliças e derivados) - 80g | 19.8 kcal | 1.7g proteína
SUBTOTAL: 378.0 kcal | 37.3g proteína

LANCHE DA TARDE
-----------------------------------
  • Iogurte natural (Leite e derivados) - 160g | 82.4 kcal | 6.5g proteína
SUBTOTAL: 82.4 kcal | 6.5g proteína

JANTAR / CAFÉ DA TARDE
-----------------------------------
  • Salmão grelhado (Mistura) - 85g | 194.5 kcal | 20.3g proteína
  • Batata inglesa cozida (Verduras, hortaliças e derivados) - 90g | 46.5 kcal | 1.1g proteína
  • Lentilha cozida (Leguminosas e derivados) - 75g | 69.4 kcal | 4.7g proteína
SUBTOTAL: 310.4 kcal | 26.1g proteína

LANCHE DA NOITE
-----------------------------------
  • Castanha-de-caju torrada (Nozes e sementes) - 20g | 114.0 kcal | 3.7g proteína
SUBTOTAL: 114.0 kcal | 3.7g proteína

-----------------------------------
TOTAL DO DIA: 1421.0 kcal | 97.6g proteína
Diferença das metas: -8.0 kcal | +1.2g proteína
```

---

## Diagnóstico e Solução de Problemas Comuns

### 1. Mensagem de erro: "python não é reconhecido como um comando interno"
* **Causa**: O Python não foi adicionado às variáveis de ambiente do Windows durante a instalação.
* **Solução**: Reinstale o Python marcando a caixa de seleção **"Add Python to PATH"** na tela inicial do instalador.

### 2. Mensagem de erro: "A execução de scripts foi desabilitada neste sistema"
* **Causa**: A política de execução do PowerShell está restrita.
* **Solução**: Siga o [Passo 1 do Guia de Instalação](#passo-1-habilitar-execução-de-scripts-no-powershell) e execute `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.

### 3. Erro ao abrir a planilha "alimentos.xlsx"
* **Causa**: A biblioteca `openpyxl` não está instalada ou o arquivo `alimentos.xlsx` foi movido.
* **Solução**: Certifique-se de que o arquivo `alimentos.xlsx` está localizado na pasta raiz do projeto e execute `pip install openpyxl`.

### 4. Onde encontrar o arquivo gerado?
* O arquivo com o resultado chama-se `dieta.txt` e é gravado automaticamente na mesma pasta onde o comando foi executado. Você pode abri-lo clicando duas vezes sobre ele para visualizá-lo no Bloco de Notas ou em qualquer outro editor de texto.

---

## Execução dos Testes Automatizados

O projeto conta com uma suíte de **34 testes unitários automatizados** construídos com `pytest`. Esses testes validam o comportamento das fórmulas matemáticas, a integridade da base de dados e a convergência dos operadores genéticos.

Para rodar todos os testes no terminal com o ambiente virtual ativado:

```powershell
pytest tests
```

Para uma visualização detalhada com o resultado de cada teste individual:

```powershell
pytest tests -v
```

Caso o terminal acuse que o comando `pytest` não foi localizado, execute chamando o Python do ambiente virtual:

```powershell
python -m pytest tests -v
```

---

## Informações Acadêmicas e Autoria

Este software foi concebido e estruturado para fins acadêmicos e de pesquisa, aplicando técnicas de Inteligência Artificial e Algoritmos Bioinspirados à resolução prática de problemas de otimização em saúde e nutrição.

> [!IMPORTANT]
> Os cardápios e valores calculados por esta aplicação constituem sugestões matemáticas e simulações computacionais. Para intervenções nutricionais clínicas ou prescrições alimentares individuais, consulte sempre um profissional nutricionista ou médico devidamente habilitado.
