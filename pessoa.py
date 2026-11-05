class Pessoa:
    def __init__(self):
        self.nome = None
        self.idade = 0
        self.sexo = None
        self.peso = 0
        self.altura = 0
        self.atividade_fisica = None
        self.objetivo = None

        self.objetivos = {
            1: "Emagrecimento",
            2: "Manter peso",
            3: "Ganho de massa muscular"
        }

        self.atividade = {
            1: 1.2,
            2: 1.375,
            3: 1.55,
            4: 1.725,
            5: 1.9
        }

    def coletar_dados(self):
        self.nome = input("Digite seu nome: ")
        print("\n1 : Masculino.\n" \
            "2 : Feminino")
        opcao = int(input("Informe o seu sexo biológico: "))

        while opcao not in (1, 2):
            opcao = int(input("Opção não disponível, informe novamente: "))

        if opcao == 1:
             self.sexo = "Masculino"
        else:
             self.sexo = "Feminino"

        self.idade = int(input("\n" + self.nome + ", Informe a sua idade: "))
        self.peso = float(input("\n" + self.nome + ", Agora informe seu peso (KG): "))
        self.altura = float(input("\nInforme a sua altura (CM): "))
        print("\nNíveis de atividade:")
        print("1 : Sedentário.\n" 
            "2 : Levemente ativo.\n"
            "3 : Moderamente ativo.\n"
            "4 : Muito ativo.\n"
            "5 : Extremamente ativo.")

        opcao = int(input("Informe seu nível de atividade: "))
        while opcao not in (1, 2, 3, 4, 5):
            opcao = int(input("Opção não disponível, informe novamente: "))

        self.atividade_fisica = self.atividade.get(opcao)
        
        print("\nObjetivos:\n" 
            "1 : Emagrecimento.\n" 
            "2 : Manter peso.\n" 
            "3 : Ganho de massa muscular.")

        opcao = int(input("Informe seu objetivo: "))
        while opcao not in (1, 2, 3):
                opcao = int(input("Opção não disponível, informe novamente: "))
        
        self.objetivo = self.objetivos.get(opcao)

    def exibir_perfil(self):
        print("\nPerfil Geral:"
            "\nNome: ", self.nome,
              "\nSexo: ", self.sexo,
              "\nIdade: ", self.idade,
              "\nAltura: ", self.altura,
              "\nPeso: ", self.peso,
              "\nObjetivo: ", self.objetivo,
              f"\nTMB: {self.tmb:.2f} kcal/dia.",
              f"\nGET: {self.get:.2f} kcal/dia.",
              f"\nMeta Calórica: {self.meta_kcal:.2f} kcal/dia",
              f"\nMeta Proteica: {self.meta_prot:.2f} g/dia.")

    def calcular_tmb(self):
        if self.sexo == "Masculino":
            self.tmb = (10 * self.peso) + (6.25 * self.altura) - (5 * self.idade) + 5
        else:
            self.tmb = (10 * self.peso) + (6.25 * self.altura) - (5 * self.idade) - 161

        return self.tmb

    def calcular_get(self):
        self.get = self.tmb * self.atividade_fisica

        return self.get
    
    def meta_calorica(self):
        if self.objetivo == "Emagrecimento":
            self.meta_kcal = self.get - 400
        elif self.objetivo == "Manter peso":
            self.meta_kcal = self.get
        else:
            self.meta_kcal = self.get + 400

        return self.meta_kcal

    def meta_proteica(self):
        if self.objetivo == "Emagrecimento":
            self.meta_prot = self.peso * 2.0
        elif self.objetivo == "Manter peso":
            self.meta_prot = self.peso * 1.6
        else:
            self.meta_prot = self.peso * 1.8

        return self.meta_prot

    def calculo_geral(self):
        self.calcular_tmb()
        self.calcular_get()
        self.meta_calorica()
        self.meta_proteica()