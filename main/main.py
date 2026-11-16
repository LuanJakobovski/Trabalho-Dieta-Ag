from pessoa import Pessoa
from AG import executar_ag

usuario = Pessoa()
usuario.nome = "Luan"
usuario.sexo = "Masculino"
usuario.idade = 20
usuario.peso = 70
usuario.altura = 172
usuario.atividade_fisica = 1.55
usuario.objetivo = "Ganho de massa muscular"

usuario.calculo_geral()
usuario.exibir_perfil()

# Gera o plano alimentar semanal
executar_ag(usuario)
