import os
import sys

# Garante que os módulos locais em main sejam encontrados independentemente do diretório de chamada
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pessoa import Pessoa
from ag2 import algoritmo_genetico
from dieta import calcular_dieta, calcular_refeicao

def main():
    usuario = Pessoa()
    usuario.coletar_dados()
    usuario.calculo_geral()
    usuario.exibir_perfil()

    print("\nExecutando Algoritmo Genético para 6 refeições diárias...")
    print(f"Meta Calórica: {usuario.meta_kcal:.1f} kcal/dia")
    print(f"Meta Proteica: {usuario.meta_prot:.1f}g/dia (Máximo recomendado por refeição: {usuario.meta_prot / 6:.1f}g)")

    melhor_dieta, fitness = algoritmo_genetico(
        usuario.meta_kcal,
        usuario.meta_prot,
        tamanho_populacao=25,
        numero_geracoes=300
    )

    caminho_arquivo = "dieta.txt"
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write("PLANO ALIMENTAR SEMANAL (6 REFEIÇÕES DIÁRIAS)\n")
        arquivo.write("=" * 60 + "\n\n")

        for dia, refeicoes in melhor_dieta.items():
            arquivo.write(f"\n{'=' * 25} {dia.upper()} {'=' * 25}\n")

            for refeicao, alimentos in refeicoes.items():
                arquivo.write(f"\n{refeicao.upper()}\n")
                arquivo.write("-" * 35 + "\n")

                kcal, proteina = calcular_refeicao(alimentos)

                for alimento in alimentos:
                    arquivo.write(
                        f"  • {alimento['alimento']} ({alimento['cat']}) - {alimento['quantidade']}g | "
                        f"{alimento['kcal_consumida']:.1f} kcal | "
                        f"{alimento['proteina_consumida']:.1f}g proteína\n"
                    )
                arquivo.write(f"SUBTOTAL: {kcal:.1f} kcal | {proteina:.1f}g proteína\n")

            kcal_dia, proteina_dia = calcular_dieta(refeicoes)
            arquivo.write("\n" + "-" * 35 + "\n")
            arquivo.write(f"TOTAL DO DIA: {kcal_dia:.1f} kcal | {proteina_dia:.1f}g proteína\n")
            arquivo.write(f"Diferença das metas: {kcal_dia - usuario.meta_kcal:+.1f} kcal | {proteina_dia - usuario.meta_prot:+.1f}g proteína\n")

        arquivo.write("\n" + "=" * 60 + "\n")
        arquivo.write("INFORMAÇÕES E METAS DO USUÁRIO\n")
        arquivo.write("=" * 60 + "\n")
        arquivo.write(f"Nome: {usuario.nome}\n")
        arquivo.write(f"Objetivo: {usuario.objetivo}\n")
        arquivo.write(f"Meta calórica diária: {usuario.meta_kcal:.1f} kcal/dia\n")
        arquivo.write(f"Meta proteica diária: {usuario.meta_prot:.1f}g/dia\n")
        arquivo.write(f"Limite sugerido de proteína por refeição: {usuario.meta_prot / 6.0:.1f}g\n")
        arquivo.write(f"Fitness final da solução: {fitness:.4f}\n")

    print(f"\nPlano semanal gerado com sucesso no arquivo '{caminho_arquivo}'!")
    print(f"Fitness alcançado: {fitness:.4f}")

if __name__ == "__main__":
    main()
