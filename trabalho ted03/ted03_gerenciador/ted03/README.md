# TED 03 – Gerenciador de Persistência de Dados em Arquivos Estruturados (CSV e JSON)

Instituição: Unibalsas
Curso: Análise e Desenvolvimento de Sistemas
Disciplina: Algoritmos e Programação Avançada

Integrantes da dupla:
- Esley Robson Soares Silva Filho
- Marcos Vinícius Sousa dos Santos

## Sobre o projeto

Programa em Python que lê, converte e grava dados em arquivos CSV e JSON. Antes de gravar em
um arquivo que já existe ele faz um backup automático, e os erros de arquivo (arquivo não
encontrado, sem permissão, codificação errada, JSON inválido) são tratados com mensagens
claras para o usuário. Usa só a biblioteca padrão, não precisa instalar nada.

## Funcionalidades

- Converter CSV para JSON
- Converter JSON para CSV
- Mostrar os registros de um arquivo (.csv ou .json)
- Adicionar um registro em um arquivo existente
- Backup automático antes de qualquer gravação em arquivo existente
- Todas as aberturas de arquivo usam `with open(...)` com `encoding="utf-8"`

## Organização dos arquivos

```
main.py        menu do programa
leitura.py     leitura de CSV e JSON
escrita.py     gravação de CSV e JSON (chama o backup antes)
conversao.py   conversão entre CSV e JSON
backup.py      backup automático
registros.py   adicionar registro
erros.py       mensagens de erro para o usuário
testes.py      testes automatizados
dados/         arquivos usados nos testes
```

Arquivos da pasta `dados/`:
- `alunos.csv`: CSV válido, com acentos, vírgula e aspas dentro de campos
- `alunos.json`: JSON válido, com números, booleanos e um campo que só aparece em um registro
- `alunos_latin1.csv`: CSV salvo em Latin-1, usado para gerar o erro de codificação
- `invalido.json`: JSON com erro de sintaxe, usado para gerar o erro de formato

## Como executar

Precisa do Python 3.8 ou mais novo.

```
python main.py
```

No menu, apertar Enter usa o caminho que aparece entre colchetes.

Para rodar os testes automatizados:

```
python testes.py
```

## Como testar manualmente

1. Opção 1 com Enter nas duas perguntas: converte `dados/alunos.csv` para JSON.
2. Opção 1 de novo: como o JSON já existe, aparece a mensagem de backup criado (fica em `dados/backups/`).
3. Opção 2 com Enter nas duas perguntas: converte `dados/alunos.json` para CSV.
4. Opção 4: adiciona um registro em `dados/alunos.csv` (também gera backup).
5. Opção 1 com origem `dados/nao_existe.csv`: erro de arquivo não encontrado.
6. Opção 1 com origem `dados/alunos_latin1.csv`: erro de codificação.
7. Opção 2 com origem `dados/invalido.json`: erro de JSON inválido.
8. Erro de permissão (Linux/Mac): `chmod 000 dados/alunos.csv`, opção 3, depois `chmod 644 dados/alunos.csv`.

## Observações

- Os valores do CSV são lidos como texto, para não perder os zeros à esquerda da matrícula (`00123`).
- Na conversão JSON para CSV, as colunas são a união dos campos de todos os registros. Quando um
  registro não tem um campo, a célula fica vazia.
- Se o backup falhar, a gravação é cancelada e o arquivo original não é alterado.
