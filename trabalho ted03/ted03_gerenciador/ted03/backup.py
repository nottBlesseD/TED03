import os
import shutil
from datetime import datetime


def fazer_backup(caminho):
    # retorna True se pode continuar com a gravação e False se o backup deu errado
    if not os.path.exists(caminho):
        # arquivo novo, não tem nada pra copiar
        return True

    pasta = os.path.join(os.path.dirname(caminho), "backups")
    nome = os.path.basename(caminho)
    data = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(pasta, f"{data}_{nome}.bak")

    try:
        os.makedirs(pasta, exist_ok=True)
        # copia em modo binário pra não ter problema com encoding
        with open(caminho, "rb") as origem:
            with open(destino, "wb") as copia:
                shutil.copyfileobj(origem, copia)
    except OSError as erro:
        print(f"Não foi possível criar o backup de '{caminho}': {erro}")
        print("A gravação foi cancelada pra não perder os dados originais.")
        return False

    print(f"Backup criado em: {destino}")
    return True
