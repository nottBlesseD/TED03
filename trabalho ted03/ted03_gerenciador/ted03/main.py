from conversao import csv_para_json, json_para_csv
from erros import mensagem_erro
from leitura import ler_arquivo
from registros import adicionar_registro


def mostrar_menu():
    print()
    print("===== Gerenciador de dados CSV / JSON =====")
    print("1 - Converter CSV para JSON")
    print("2 - Converter JSON para CSV")
    print("3 - Mostrar registros de um arquivo")
    print("4 - Adicionar registro")
    print("0 - Sair")


def pedir(texto, padrao):
    # se apertar Enter usa o valor que aparece entre colchetes
    resposta = input(f"{texto} [{padrao}]: ").strip()
    if resposta == "":
        return padrao
    return resposta


def main():
    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Até mais!")
            break

        elif opcao == "1":
            origem = pedir("CSV de origem", "dados/alunos.csv")
            destino = pedir("JSON de destino", "dados/alunos_convertido.json")
            try:
                csv_para_json(origem, destino)
            except Exception as erro:
                print(mensagem_erro(erro, origem))

        elif opcao == "2":
            origem = pedir("JSON de origem", "dados/alunos.json")
            destino = pedir("CSV de destino", "dados/alunos_convertido.csv")
            try:
                json_para_csv(origem, destino)
            except Exception as erro:
                print(mensagem_erro(erro, origem))

        elif opcao == "3":
            caminho = pedir("Arquivo (.csv ou .json)", "dados/alunos.csv")
            try:
                dados = ler_arquivo(caminho)
                print(f"{len(dados)} registro(s) em '{caminho}':")
                for i, registro in enumerate(dados, start=1):
                    print(f"{i} - {registro}")
            except Exception as erro:
                print(mensagem_erro(erro, caminho))

        elif opcao == "4":
            caminho = pedir("Arquivo (.csv ou .json)", "dados/alunos.csv")
            try:
                dados = ler_arquivo(caminho)
                if len(dados) == 0:
                    print("O arquivo não tem registros, não dá pra saber quais são os campos.")
                    continue
                novo = {}
                for campo in dados[0]:
                    novo[campo] = input(f"{campo}: ").strip()
                adicionar_registro(caminho, novo)
            except Exception as erro:
                print(mensagem_erro(erro, caminho))

        else:
            print("Opção inválida, digite um número do menu.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma encerrado.")
