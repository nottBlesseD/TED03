import csv
import json

from backup import fazer_backup


def salvar_json(caminho, dados):
    # o backup sempre vem antes de mexer no arquivo
    if not fazer_backup(caminho):
        return False

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    return True


def salvar_csv(caminho, dados):
    if len(dados) == 0:
        raise ValueError("não há registros para gravar no CSV")

    # junta as colunas de todos os registros, porque nem todos têm os mesmos campos
    colunas = []
    for registro in dados:
        for campo in registro:
            if campo not in colunas:
                colunas.append(campo)

    if not fazer_backup(caminho):
        return False

    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(dados)
    return True


def salvar_arquivo(caminho, dados):
    if caminho.lower().endswith(".csv"):
        return salvar_csv(caminho, dados)
    elif caminho.lower().endswith(".json"):
        return salvar_json(caminho, dados)
    else:
        raise ValueError("formato não suportado, use um arquivo .csv ou .json")
