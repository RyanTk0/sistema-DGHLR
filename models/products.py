from dotenv import load_dotenv
load_dotenv()
import re
from banco_dados.connection import Transições

class Product:

    def __init__(self, name, price, stock):
        self.name = name.strip() if name else None
        self.price = price
        self.stock = stock

    def salvar(self):

        if not self.name:
            print("O nome do produto é obrigatório.")
            return

        if not isinstance(self.price, (int, float)) or self.price <= 0:
            print("O preço deve ser um número maior que zero.")
            return

        if not isinstance(self.stock, int) or self.stock < 0:
            print("O estoque deve ser um número inteiro maior ou igual a zero.")
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    """
                    INSERT INTO products (name, price, stock, sku)
                    VALUES (%s, %s, %s, CONCAT('SKU-', UUID()))
                    """,
                    (self.name, self.price, self.stock)
                )
                print("Produto cadastrado com sucesso!")

        except Exception as e:
            if "Duplicate entry" in str(e):
                print("Já existe um produto com esse nome.")
            else:
                print(f"Erro ao cadastrar produto: {e}")

    @staticmethod
    def listar():
        try:
            with Transições() as cursor:
                cursor.execute("""
                    SELECT id, name, price, stock, sku, created_at
                    FROM products
                    ORDER BY id ASC
                """)
                produtos = cursor.fetchall()

            if not produtos:
                print("Nenhum produto cadastrado.")
                return []  
            else:
                print("\n=========== PRODUTOS ===========\n")
                for p in produtos:
                    print(
                        f"{p['id']} - {p['name']} | SKU: {p['sku']} | "
                        f"R${p['price']} | Estoque: {p['stock']} "
                        f"| Criado em {p['created_at']}"
                    )
                return produtos  

        except Exception as e:
            print(f"Erro ao listar produtos: {e}")
            return []

    @staticmethod
    def editar(id_produto, novo_nome, novo_preco, novo_estoque):

        if not novo_nome:
            print("O nome do produto é obrigatório.")
            return

        if not isinstance(novo_preco, (int, float)) or novo_preco <= 0:
            print("Preço inválido.")
            return

        if not isinstance(novo_estoque, int) or novo_estoque < 0:
            print("Estoque inválido.")
            return

        novo_nome = novo_nome.strip()

        try:
            with Transições() as cursor:
                cursor.execute(
                    """
                    UPDATE products
                    SET name = %s,
                        price = %s,
                        stock = %s
                    WHERE id = %s
                    """,
                    (novo_nome, novo_preco, novo_estoque, id_produto)
                )

                if cursor.rowcount > 0:
                    print("Produto atualizado com sucesso!")
                else:
                    print("Produto não encontrado.")

        except Exception as e:
            if "Duplicate entry" in str(e):
                print("Já existe outro produto com esse nome.")
            else:
                print(f"Erro ao atualizar produto: {e}")

    @staticmethod
    def excluir(id_produto):
        try:
            with Transições() as cursor:
                cursor.execute("DELETE FROM products WHERE id = %s", (id_produto,))

                if cursor.rowcount > 0:
                    print("Produto excluído com sucesso!")
                else:
                    print("Produto não encontrado.")

        except Exception as e:
            if "foreign key constraint" in str(e).lower():
                print("Este produto está em algum pedido e não pode ser excluído.")
            else:
                print(f"Erro ao excluir produto: {e}")
