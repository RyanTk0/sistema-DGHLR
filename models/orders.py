from dotenv import load_dotenv
load_dotenv()

from banco_dados.connection import Transições


class Order:

    def __init__(self, user_id, total=0):
        self.user_id = user_id
        self.total = float(total) if total is not None else 0.0

    def salvar(self):
        if not isinstance(self.user_id, int) or self.user_id <= 0:
            return {"success": False, "error": "ID de usuário inválido"}

        try:
            with Transições() as cursor:
                cursor.execute(
                    """
                    INSERT INTO orders (user_id, total)
                    VALUES (%s, %s)
                    """,
                    (self.user_id, self.total)
                )

                order_id = cursor.lastrowid

                cursor.execute("CALL sp_recalculate_order_total(%s)", (order_id,))

                print("\n✔ Pedido cadastrado com sucesso!")
                return {"success": True, "order_id": order_id}

        except Exception as e:
            if "foreign key constraint" in str(e).lower():
                print("❌ user_id informado não existe!")
                return {"success": False, "error": "user_id não existe"}
            else:
                print(f"❌ Erro ao salvar pedido: {e}")
                return {"success": False, "error": str(e)}

    @staticmethod
    def listar():
        try:
            with Transições() as cursor:
                cursor.execute("""
                    SELECT 
                        o.id,
                        o.user_id,
                        u.name AS usuario,
                        o.total
                    FROM orders o
                    JOIN users u ON u.id = o.user_id
                    ORDER BY o.id ASC;
                """)

                return cursor.fetchall()

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def modificar(order_id, user_id=None, total=None):
        if not isinstance(order_id, int) or order_id <= 0:
            return {"success": False, "error": "order_id inválido"}

        query_parts = []
        values = []

        if user_id is not None:
            query_parts.append("user_id = %s")
            values.append(user_id)

        if total is not None:
            query_parts.append("total = %s")
            values.append(float(total))

        if not query_parts:
            return {"success": False, "error": "Nenhum campo informado"}

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

                cursor.execute("CALL sp_recalculate_order_total(%s)", (order_id,))

                print("✔ Pedido modificado com sucesso!")
                return {"success": True}

        except Exception as e:
            print(f"Erro ao modificar pedido: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def excluir(order_id):
        if not isinstance(order_id, int) or order_id <= 0:
            return {"success": False, "error": "order_id inválido"}

        try:
            with Transições() as cursor:
                cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))

                if cursor.rowcount > 0:
                    print("✔ Pedido excluído com sucesso!")
                else:
                    print("⚠ Nenhum pedido encontrado com esse ID.")

                return {"success": cursor.rowcount > 0}

        except Exception as e:
            print(f"Erro ao excluir pedido: {e}")
            return {"success": False, "error": str(e)}
