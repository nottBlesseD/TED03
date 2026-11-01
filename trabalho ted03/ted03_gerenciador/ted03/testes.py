import json
import os
import tempfile
import unittest

from backup import fazer_backup
from conversao import csv_para_json, json_para_csv
from erros import mensagem_erro
from leitura import ler_csv, ler_json

CSV_TESTE = (
    "matricula,nome,curso\n"
    "00123,João da Conceição,Engenharia\n"
    '00456,"Silva, Ângela",Medicina\n'
)

REGISTROS_TESTE = [
    {"matricula": "00123", "nome": "João da Conceição", "curso": "Engenharia"},
    {"matricula": "00456", "nome": "Silva, Ângela", "curso": "Medicina"},
]


class TestePersistencia(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.pasta = self.temp.name

    def tearDown(self):
        self.temp.cleanup()

    def caminho(self, nome):
        return os.path.join(self.pasta, nome)

    def criar_arquivo(self, nome, texto, encoding="utf-8"):
        caminho = self.caminho(nome)
        with open(caminho, "w", encoding=encoding, newline="") as arquivo:
            arquivo.write(texto)
        return caminho

    # ---------- conversões ----------

    def test_csv_para_json(self):
        origem = self.criar_arquivo("a.csv", CSV_TESTE)
        destino = self.caminho("a.json")
        csv_para_json(origem, destino)
        self.assertEqual(ler_json(destino), REGISTROS_TESTE)

    def test_json_para_csv(self):
        origem = self.criar_arquivo("a.json", json.dumps(REGISTROS_TESTE, ensure_ascii=False))
        destino = self.caminho("a.csv")
        json_para_csv(origem, destino)
        self.assertEqual(ler_csv(destino), REGISTROS_TESTE)

    def test_ida_e_volta(self):
        original = self.criar_arquivo("a.csv", CSV_TESTE)
        csv_para_json(original, self.caminho("b.json"))
        json_para_csv(self.caminho("b.json"), self.caminho("c.csv"))
        self.assertEqual(ler_csv(self.caminho("c.csv")), ler_csv(original))

    def test_json_com_campos_diferentes(self):
        dados = [{"id": 1, "nome": "Ana"}, {"id": 2, "nome": "Bia", "extra": "x"}]
        origem = self.criar_arquivo("a.json", json.dumps(dados))
        destino = self.caminho("a.csv")
        json_para_csv(origem, destino)
        linhas = ler_csv(destino)
        self.assertEqual(linhas[0]["extra"], "")
        self.assertEqual(linhas[1]["extra"], "x")

    # ---------- backup ----------

    def test_backup_antes_de_sobrescrever(self):
        origem = self.criar_arquivo("a.csv", CSV_TESTE)
        destino = self.criar_arquivo("saida.json", "conteúdo antigo")
        csv_para_json(origem, destino)

        pasta_backup = self.caminho("backups")
        arquivos = os.listdir(pasta_backup)
        self.assertEqual(len(arquivos), 1)
        with open(os.path.join(pasta_backup, arquivos[0]), "r", encoding="utf-8") as arquivo:
            self.assertEqual(arquivo.read(), "conteúdo antigo")

    def test_sem_backup_se_arquivo_novo(self):
        origem = self.criar_arquivo("a.csv", CSV_TESTE)
        csv_para_json(origem, self.caminho("novo.json"))
        self.assertFalse(os.path.exists(self.caminho("backups")))

    def test_backup_falhando_nao_altera_arquivo(self):
        origem = self.criar_arquivo("a.csv", CSV_TESTE)
        destino = self.criar_arquivo("saida.json", "original")
        # existe um ARQUIVO chamado backups, então a pasta não pode ser criada
        self.criar_arquivo("backups", "oi")
        csv_para_json(origem, destino)
        with open(destino, "r", encoding="utf-8") as arquivo:
            self.assertEqual(arquivo.read(), "original")

    # ---------- erros ----------

    def test_arquivo_inexistente(self):
        caminho = self.caminho("nao_existe.csv")
        with self.assertRaises(FileNotFoundError) as contexto:
            ler_csv(caminho)
        self.assertIn("não foi encontrado", mensagem_erro(contexto.exception, caminho))

    def test_encoding_errado(self):
        caminho = self.criar_arquivo("latin1.csv", "nome\nJoão\n", encoding="latin-1")
        with self.assertRaises(UnicodeDecodeError) as contexto:
            ler_csv(caminho)
        self.assertIn("UTF-8", mensagem_erro(contexto.exception, caminho))

    def test_json_invalido(self):
        caminho = self.criar_arquivo("ruim.json", '[{"nome": "Ana",}]')
        with self.assertRaises(json.JSONDecodeError) as contexto:
            ler_json(caminho)
        self.assertIn("JSON válido", mensagem_erro(contexto.exception, caminho))

    def test_json_com_formato_errado(self):
        origem = self.criar_arquivo("a.json", "[1, 2, 3]")
        with self.assertRaises(ValueError):
            json_para_csv(origem, self.caminho("a.csv"))

    def test_mensagem_de_permissao(self):
        erro = PermissionError(13, "Permission denied", "dados/a.csv")
        self.assertIn("sem permissão", mensagem_erro(erro))


if __name__ == "__main__":
    unittest.main(verbosity=2)
