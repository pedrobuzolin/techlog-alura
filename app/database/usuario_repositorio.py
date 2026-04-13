from app.database.local import LocalDataBase
from app.models.usuarios import Usuario, UsuarioCriarAtualizar

class UsuarioRepositorio:
    def __init__(self, banco_dados: LocalDataBase):
        self.bd = banco_dados

    async def buscar_usuario_por_email_senha(self, email: str, senha: str) -> Usuario | None:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
            linha = cursor.fetchone()
            if linha:
                return Usuario(id_=linha[0], nome=linha[1], email=linha[2])
            return None
        
    async def buscar_usuario_por_email(self, email: str) -> Usuario:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email FROM usuarios WHERE email = ?", (email,))
            linha = cursor.fetchone()
            if linha:
                return Usuario(id_=linha[0], nome=linha[1], email=linha[2])
            return None
        
    async def criar_usuario(self, usuario_criar: UsuarioCriarAtualizar) -> Usuario:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (usuario_criar.nome, usuario_criar.email, usuario_criar.senha))
            usuario_id = cursor.lastrowid
            return Usuario(id_=usuario_id, nome=usuario_criar.nome, email=usuario_criar.email, senha=usuario_criar.senha)