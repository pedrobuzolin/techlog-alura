from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routes import cliente

app = FastAPI(
    title="Techlog Solutions API",
    description="CRM para Techlog Solutions",
    version="1.0.0",
)

app.include_router(cliente.router)

@app.get("/")
async def health_check():
    return {"status": "OK"}

@app.get("/front", response_class=HTMLResponse)
async def front_page():
    html_content = """
    <html>
        <head>
            <title>TechLog Solutions</title>
        </head>
        <body>
            <h1>🔧 TechLog Solutions</h1>
            <p>Sistema de Gestão de Ordens de Serviço</p>
            <p>Status: <strong>Operacional</strong></p>
        </body>
    </html>
    """

    return html_content