from leitura import ler_arquivo
from escrita import salvar_arquivo


def adicionar_registro(caminho, novo):
    dados = ler_arquivo(caminho)
    dados.append(novo)
    if salvar_arquivo(caminho, dados):
        print("Registro adicionado.")
