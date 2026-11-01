import csv
import json


def ler_csv(caminho):
    with open(caminho, "r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        dados = list(leitor)
    return dados


def ler_json(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados


def ler_arquivo(caminho):
    if caminho.lower().endswith(".csv"):
        return ler_csv(caminho)
    elif caminho.lower().endswith(".json"):
        return ler_json(caminho)
    else:
        raise ValueError("formato não suportado, use um arquivo .csv ou .json")
