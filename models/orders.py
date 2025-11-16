from dotenv import load_dotenv
load_dotenv()

from banco_dados.connection import Transições

class Order:

    def __init__(self, user_id):
        self.user_id = user_id

    def salvar(self):
        if not isinstance(self.user_id, int) or self.user_id <= 0:
            print("O ID do usuário é inválido.")
            return {"success": False, "error": "ID do usuário inválido."}

        if not self.usuario_existe():
            print("O ID do usuário informado não existe.")
            return {"success": False, "error": "Usuário não encontrado."}

        try:
            with Transições() as cursor:
                cursor.execute(
                    """
                    INSERT INTO orders (user_id)
                    VALUES (%s)
                    """,
                    (self.user_id,)
                )
                
                order_id = cursor.lastrowid

                cursor.execute(
                    """
                    UPDATE orders 
                    SET total = (
                        SELECT COALESCE(SUM(oi.quantity * oi.price), 0)
                        FROM order_items oi 
                        WHERE oi.order_id = %s
                    )
                    WHERE id = %s
                    """,
                    (order_id, order_id)
                )

                print(f"Pedido cadastrado com sucesso! ID do pedido: {order_id}")
                return {"success": True, "order_id": order_id}
        except Exception as e:
            print(f"Erro ao salvar pedido: {e}")
            return {"success": False, "error": str(e)}

    def usuario_existe(self):
        try:
            with Transições() as cursor:
                cursor.execute("SELECT id FROM users WHERE id = %s", (self.user_id,))
                user = cursor.fetchone()
                return user is not None
        except Exception as e:
            print(f"Erro ao verificar existência do usuário: {e}")
            return False

    @staticmethod
    def listar():
        try:
            with Transições() as cursor:
                cursor.execute("""
                    SELECT o.id, o.user_id, u.name AS usuario, o.created_at AS data_pedido
                    FROM orders o
                    JOIN users u ON u.id = o.user_id
                    ORDER BY o.id ASC;
                """)
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar pedidos: {e}")
            return []

    @staticmethod
    def modificar(order_id, user_id=None):
        if not isinstance(order_id, int) or order_id <= 0:
            print("ID do pedido inválido.")
            return

        query_parts = []
        values = []

        if user_id is not None:
            query_parts.append("user_id = %s")
            values.append(user_id)

        if not query_parts:
            print("Nenhum campo informado para alteração.")
            return

        values.append(order_id)

        try:
            with Transições() as cursor:
                cursor.execute(
                    f"""
                    UPDATE orders
                    SET {", ".join(query_parts)}
                    WHERE id = %s
                    """,
                    values
                )

                print("Pedido modificado com sucesso!")
        except Exception as e:
            print(f"Erro ao modificar pedido: {e}")

    @staticmethod
    def excluir(order_id):
        if not isinstance(order_id, int) or order_id <= 0:
            print("ID do pedido inválido.")
            return

        try:
            with Transições() as cursor:
                cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))

                if cursor.rowcount > 0:
                    print("Pedido excluído com sucesso!")
                else:
                    print("Pedido não encontrado.")
        except Exception as e:
            print(f"Erro ao excluir pedido: {e}")
