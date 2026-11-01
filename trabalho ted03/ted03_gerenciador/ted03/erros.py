import csv
import json


def mensagem_erro(erro, caminho=""):
    # nos erros de arquivo o Python já diz qual arquivo deu problema
    if isinstance(erro, OSError) and erro.filename:
        caminho = erro.filename

    # a ordem importa: JSONDecodeError e UnicodeDecodeError são tipos de ValueError
    if isinstance(erro, FileNotFoundError):
        return f"Erro: o arquivo '{caminho}' não foi encontrado."
    if isinstance(erro, PermissionError):
        return f"Erro: sem permissão para acessar ou modificar o arquivo '{caminho}'."
    if isinstance(erro, UnicodeDecodeError):
        return f"Erro: o arquivo '{caminho}' não está em UTF-8, não foi possível ler os caracteres."
    if isinstance(erro, json.JSONDecodeError):
        return f"Erro: '{caminho}' não é um JSON válido ({erro.msg}, linha {erro.lineno})."
    if isinstance(erro, csv.Error):
        return f"Erro: o CSV '{caminho}' está mal formatado ({erro})."
    if isinstance(erro, ValueError):
        return f"Erro: {erro}."
    if isinstance(erro, OSError):
        return f"Erro de leitura/escrita no arquivo '{caminho}': {erro.strerror}."
    return f"Erro inesperado: {erro}"
