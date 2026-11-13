from pessoa import Pessoa
from AG import executar_ag

usuario = Pessoa()

usuario.coletar_dados()
usuario.calculo_geral()
usuario.exibir_perfil()

# Gera o plano alimentar semanal
executar_ag(usuario)
