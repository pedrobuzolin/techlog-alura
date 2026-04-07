from app.database.local import LocalDataBase
from app.models.clientes import Cliente

class ClienteRepositorio:
    def __init__(self, banco_dados: LocalDataBase):
        self.bd = banco_dados

    async def listar_clientes(self) -> list[Cliente]:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes")
            linhas = cursor.fetchall()
            clientes = [Cliente(id_=linha[0], nome=linha[1], email=linha[2], telefone=linha[3]) for linha in linhas]
            return clientes

    async def obter_cliente(self, cliente_id: int) -> Cliente | None:
        with self.bd.conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes WHERE id = ?", (cliente_id,))
            linha = cursor.fetchone()
            if linha:
                return Cliente(id_=linha[0], nome=linha[1], email=linha[2], telefone=linha[3])
            return None