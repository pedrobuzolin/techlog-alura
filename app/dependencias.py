from typing import Annotated
from fastapi import Depends
from app.database.local import LocalDataBase
from app.database.cliente_repositorio import ClienteRepositorio

banco_de_dados = LocalDataBase()

def obter_banco_de_dados() -> LocalDataBase:
    return banco_de_dados

def obter_cliente_repositorio(banco_de_dados_local: Annotated[LocalDataBase, Depends(obter_banco_de_dados)]) -> ClienteRepositorio:
    return ClienteRepositorio(banco_de_dados_local)