from dotenv import load_dotenv
load_dotenv()

from banco_dados.connection import Transições
from models.orders import Order  
class OrderItem:

    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price

    def salvar(self):
        if not isinstance(self.order_id, int) or self.order_id <= 0:
            print("ID do pedido inválido.")
            return

        if not isinstance(self.product_id, int) or self.product_id <= 0:
            print("ID do produto inválido.")
            return

        try:
            self.quantity = int(self.quantity)
            if self.quantity <= 0:
                raise Exception
        except:
            print("Quantidade inválida. Use um número inteiro maior que zero.")
            return

        try:
            self.price = float(self.price)
            if self.price < 0:
                raise Exception
        except:
            print("Preço inválido.")
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
            if "foreign key constraint" in str(e).lower():
                print("ID de pedido ou produto não existe.")
            else:
                print(f"Erro ao cadastrar item: {e}")

    @staticmethod
    def listar():
        try:
            with Transições() as cursor:
                cursor.execute("""
                    SELECT 
                        oi.id,
                        oi.order_id,
                        oi.product_id,
                        p.name AS nome_produto,
                        oi.quantity,
                        oi.price
                    FROM order_items oi
                    JOIN products p ON p.id = oi.product_id
                    ORDER BY oi.id ASC
                """)
                itens = cursor.fetchall()

            if not itens:
                print("Nenhum item cadastrado.")
            else:
                print("\n=========== ITENS DE PEDIDOS ===========\n")
                for i in itens:
                    print(
                        f"ID: {i['id']} | Pedido: {i['order_id']} | Produto: {i['nome_produto']} "
                        f"(ID {i['product_id']}) | Quantidade: {i['quantity']} | "
                        f"Preço: R$ {i['price']:.2f}"
                    )

        except Exception as e:
            print(f"Erro ao listar itens: {e}")

    @staticmethod
    def modificar(item_id, quantity=None, price=None):
        if not isinstance(item_id, int) or item_id <= 0:
            print("ID do item inválido.")
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
                return

        if price is not None:
            try:
                price = float(price)
                campos.append("price = %s")
                valores.append(price)
            except:
                print("Preço inválido.")
                return

        if not campos:
            print("Nenhum campo informado.")
            return

        valores.append(item_id)

        try:
            with Transições() as cursor:
                cursor.execute(
                    f"""
                    UPDATE order_items
                    SET {', '.join(campos)}
                    WHERE id = %s
                    """,
                    valores
                )

                if cursor.rowcount > 0:
                    print("Item atualizado com sucesso!")
                else:
                    print("Item não encontrado.")

        except Exception as e:
            print(f"Erro ao modificar item: {e}")

    @staticmethod
    def excluir(item_id):
        if not isinstance(item_id, int) or item_id <= 0:
            print("ID inválido.")
            return

        try:
            with Transições() as cursor:
                cursor.execute("DELETE FROM order_items WHERE id = %s", (item_id,))

                if cursor.rowcount > 0:
                    print("Item excluído com sucesso!")
                    Order.atualizar_total_pedido(item_id)  
                else:
                    print("Item não encontrado.")

        except Exception as e:
            print(f"Erro ao excluir item: {e}")
