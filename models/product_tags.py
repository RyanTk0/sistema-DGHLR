from dotenv import load_dotenv
load_dotenv()

from banco_dados.connection import Transições


class ProductTag:

    def __init__(self, product_id, tag_id):
        self.product_id = product_id
        self.tag_id = tag_id

    def salvar(self):

        if not isinstance(self.product_id, int) or self.product_id <= 0:
            print("O ID do produto é inválido.")
            input("\nPressione 'Enter' para continuar...")
            return
        
        if not isinstance(self.tag_id, int) or self.tag_id <= 0:
            print("O ID da tag é inválido.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    """
                    INSERT INTO product_tags (product_id, tag_id)
                    VALUES (%s, %s)
                    """,
                    (self.product_id, self.tag_id)
                )

                print("Relação produto ↔ tag cadastrada com sucesso!")

        except Exception as e:
            if "Duplicate entry" in str(e):
                print("Esta relação já existe.")
            elif "foreign key constraint" in str(e).lower():
                print("O product_id ou tag_id informado não existe.")
            else:
                print(f"Erro ao cadastrar a relação: {e}")

        input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def listar():
        try:
            with Transições() as cursor:
                cursor.execute("""
                    SELECT 
                        pt.product_id,
                        p.name AS product_name,
                        pt.tag_id,
                        t.name AS tag_name
                    FROM product_tags pt
                    JOIN products p ON p.id = pt.product_id
                    JOIN tags t ON t.id = pt.tag_id
                    ORDER BY pt.product_id ASC;
                """)
                relacoes = cursor.fetchall()

            if not relacoes:
                print("Nenhuma relação produto ↔ tag cadastrada.")
            else:
                print("\n=========== PRODUTO x TAG ===========\n")
                for r in relacoes:
                    print(
                        f"Produto {r['product_id']} - {r['product_name']} "
                        f"<--> Tag {r['tag_id']} - {r['tag_name']}"
                    )

        except Exception as e:
            print(f"Erro ao listar relações: {e}")

        input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def excluir(product_id, tag_id):

        if not isinstance(product_id, int) or product_id <= 0:
            print("product_id inválido.")
            return

        if not isinstance(tag_id, int) or tag_id <= 0:
            print("tag_id inválido.")
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    """
                    DELETE FROM product_tags
                    WHERE product_id = %s AND tag_id = %s
                    """,
                    (product_id, tag_id)
                )

                if cursor.rowcount > 0:
                    print("Relação excluída com sucesso!")
                else:
                    print("Relação não encontrada.")

        except Exception as e:
            print(f"Erro ao excluir relação: {e}")

        input("\nPressione 'Enter' para continuar...")
