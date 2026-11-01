from leitura import ler_csv, ler_json
from escrita import salvar_csv, salvar_json


def csv_para_json(origem, destino):
    dados = ler_csv(origem)
    if salvar_json(destino, dados):
        print(f"{len(dados)} registro(s) convertido(s) de '{origem}' para '{destino}'.")


def json_para_csv(origem, destino):
    dados = ler_json(origem)

    # se vier um objeto só, vira uma lista com um registro
    if isinstance(dados, dict):
        dados = [dados]

    if not isinstance(dados, list) or not all(isinstance(item, dict) for item in dados):
        raise ValueError("o JSON precisa ser uma lista de objetos (registros)")

    if salvar_csv(destino, dados):
        print(f"{len(dados)} registro(s) convertido(s) de '{origem}' para '{destino}'.")
