from typing import Annotated
from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from app.models.usuarios import UsuarioCriarAtualizar
from app.database.usuario_repositorio import UsuarioRepositorio
from app.dependencias import obter_usuario_repositorio

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/registro"
)

@router.get("/", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="registro.html"
    )

@router.post("/", response_class=HTMLResponse)
async def login(request: Request, 
                usuario_repositorio: Annotated[UsuarioRepositorio, Depends(obter_usuario_repositorio)],
                nome=Form(...),
                email=Form(...), 
                senha=Form(...),
                confirma_senha=Form(...)
                ):
    data = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "confirma_senha": confirma_senha
    }

    if not all([nome, email, senha, confirma_senha]):
        return templates.TemplateResponse(
            request=request,
            name="registro.html",
            context={
                "error": "Campos obrigatorios faltantes",
                **data
            }
        )

    usuario_existente = await usuario_repositorio.buscar_usuario_por_email(email)
    if usuario_existente:
        return templates.TemplateResponse(
            request=request,
            name="registro.html",
            context={
                "error": "Usuario Invalido",
                **data
            }
        )
    
    usuario_criar = UsuarioCriarAtualizar(nome=nome, email=email, senha=senha)
    usuario = await usuario_repositorio.criar_usuario(usuario_criar)
    if usuario:
        response = RedirectResponse(url="/login", status_code=303)
        response.set_cookie(key="session_token", value="token-senha", httponly=True)

        return response

    return templates.TemplateResponse(
            request=request,
            name="registro.html",
            context={
                "error": "Não foi possível criar o usuario",
                **data
            }
        )