from pessoa import Pessoa
from ag2 import algoritmo_genenetico
from dieta import calcular_dieta

usuario = Pessoa()

usuario.coletar_dados()
usuario.calculo_geral()

melhor_dieta, fitness = algoritmo_genenetico(usuario.meta_kcal, usuario.meta_prot)

with open("dieta.txt", "w", encoding="utf-8") as arquivo:
    print("\nARQUIVO ""dieta.txt"" GERADO!")
    arquivo.write("DIETA SEMANAL\n")
    arquivo.write("=" * 40 + "\n")

    for dia, refeicoes in melhor_dieta.items():
        arquivo.write(f"\n\n{dia.upper()}:\n")

        for refeicao, alimentos in refeicoes.items():
            arquivo.write(f"\n{refeicao.upper()}\n")
            arquivo.write("-" * 20 + "\n")

            kcal, proteina = calcular_dieta({refeicao: alimentos})
            
            for alimento in alimentos:
                arquivo.write(
                    f"{alimento['alimento']} - {alimento['quantidade']}g | "
                    f"{alimento['kcal_consumida']:.1f} kcal | "
                    f"{alimento['proteina_consumida']:.1f}g de proteína\n"
                )
            arquivo.write(f"\nTOTAL: {kcal:.1f} kcal | {proteina:.1f}g de proteína\n")

        kcal_dia, proteina_dia = calcular_dieta(refeicoes)

        arquivo.write("\nTOTAL DO DIA:\n")
        arquivo.write(f"{kcal_dia:.1f} kcal | {proteina_dia:.1f}g de proteína\n")

    arquivo.write("\n" + "=" * 40 + "\n")
    arquivo.write("INFORMAÇÕES GERAIS\n")
    arquivo.write("=" * 40 + "\n\n")

    arquivo.write(f"Meta calórica: {usuario.meta_kcal:.1f} kcal/dia\n")
    arquivo.write(f"Meta proteica: {usuario.meta_prot:.1f}g/dia\n")
    arquivo.write(f"Fitness da dieta: {fitness:.4f}\n")