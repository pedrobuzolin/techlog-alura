from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from app.models.clientes import Cliente
from app.database.cliente_repositorio import ClienteRepositorio
from app.dependencias import obter_cliente_repositorio

router = APIRouter(
    prefix="/clientes"
)

@router.get("/", response_model=list[Cliente])
async def listar_clientes(cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)]):
    
    return await cliente_repositorio.listar_clientes()

@router.get("/{cliente_id}", response_model=Cliente | None)
async def obter_clientes(cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)], cliente_id: int):
    cliente = await cliente_repositorio.obter_cliente(cliente_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")
    
    return cliente