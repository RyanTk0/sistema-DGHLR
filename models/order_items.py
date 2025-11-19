from dotenv import load_dotenv
load_dotenv()

from banco_dados.connection import Transições
from models.orders import Order


def cancelar_operacao():
    escolha = input("Deseja cancelar a operação? (s/n): ").strip().lower()
    if escolha == "s":
        print("Operação cancelada pelo usuário.")
        return True
    return False


class OrderItem:

    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def salvar(self):
        if not isinstance(self.order_id, int) or self.order_id <= 0:
            print("ID do pedido inválido.")
            if cancelar_operacao():
                return
            return

        if not isinstance(self.product_id, int) or self.product_id <= 0:
            print("ID do produto inválido.")
            if cancelar_operacao():
                return
            return

        try:
            self.quantity = int(self.quantity)
            if self.quantity <= 0:
                raise Exception
        except:
            print("Quantidade inválida.")
            if cancelar_operacao():
                return
            return

        try:
            with Transições() as cursor:
                cursor.execute("SELECT price FROM products WHERE id = %s", (self.product_id,))
                produto = cursor.fetchone()
                if not produto:
                    print("Produto não encontrado.")
                    return
                self.price = float(produto["price"])
        except:
            print("Erro ao obter preço do produto.")
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    """
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (self.order_id, self.product_id, self.quantity, self.price)
                )
                print("Item do pedido cadastrado com sucesso!")
        except Exception as e:
            print(f"Erro ao cadastrar item: {e}")
            cancelar_operacao()

    @staticmethod
    def listar(order_id=None):
        try:
            with Transições() as cursor:
                base_query = """
                    SELECT 
                        oi.id AS item_id,
                        oi.order_id,
                        oi.product_id,
                        p.name AS produto,
                        oi.quantity,
                        oi.price
                    FROM order_items oi
                    JOIN products p ON p.id = oi.product_id
                """

                if order_id is None:
                    cursor.execute(base_query + " ORDER BY oi.order_id ASC, oi.id ASC")
                else:
                    cursor.execute(
                        base_query + " WHERE oi.order_id = %s ORDER BY oi.id ASC",
                        (order_id,)
                    )

                return cursor.fetchall()

        except Exception as e:
            print(f"Erro ao listar itens: {e}")
            cancelar_operacao()
            return []

    @staticmethod
    def modificar(item_id, quantity=None, product_id=None, order_id=None):
        if not isinstance(item_id, int) or item_id <= 0:
            print("ID do item inválido.")
            cancelar_operacao()
            return

        campos = []
        valores = []

        if quantity is not None:
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise Exception
                campos.append("quantity = %s")
                valores.append(quantity)
            except:
                print("Quantidade inválida.")
                cancelar_operacao()
                return

        if product_id is not None:
            try:
                product_id = int(product_id)
                if product_id <= 0:
                    raise Exception

                with Transições() as cursor:
                    cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
                    produto = cursor.fetchone()
                    if not produto:
                        print("Produto não encontrado.")
                        return
                    novo_preco = produto["price"]

                campos.append("product_id = %s")
                valores.append(product_id)
                campos.append("price = %s")
                valores.append(novo_preco)

            except:
                print("ID de produto inválido.")
                cancelar_operacao()
                return

        if order_id is not None:
            try:
                order_id = int(order_id)
                if order_id <= 0:
                    raise Exception
                campos.append("order_id = %s")
                valores.append(order_id)
            except:
                print("ID de pedido inválido.")
                cancelar_operacao()
                return

        if not campos:
            print("Nenhum campo informado.")
            cancelar_operacao()
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    "SELECT order_id FROM order_items WHERE id = %s",
                    (item_id,)
                )
                result = cursor.fetchone()

                if not result:
                    print("Item não encontrado.")
                    cancelar_operacao()
                    return

                old_order = result["order_id"]

                valores.append(item_id)
                cursor.execute(
                    f"""
                    UPDATE order_items
                    SET {', '.join(campos)}
                    WHERE id = %s
                    """,
                    valores
                )

                print("Item atualizado com sucesso!")

            Order.atualizar_total_pedido(old_order)

            if order_id is not None:
                Order.atualizar_total_pedido(order_id)

        except Exception as e:
            print(f"Erro ao modificar item: {e}")
            cancelar_operacao()

    @staticmethod
    def excluir(item_id):
        if not isinstance(item_id, int) or item_id <= 0:
            print("ID inválido.")
            cancelar_operacao()
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    "SELECT order_id FROM order_items WHERE id = %s",
                    (item_id,)
                )
                result = cursor.fetchone()

                if not result:
                    print("Item não encontrado.")
                    cancelar_operacao()
                    return

                order_id = result["order_id"]

                cursor.execute("DELETE FROM order_items WHERE id = %s", (item_id,))
                print("Item excluído com sucesso!")

            Order.atualizar_total_pedido(order_id)

        except Exception as e:
            print(f"Erro ao excluir item: {e}")
            cancelar_operacao()
