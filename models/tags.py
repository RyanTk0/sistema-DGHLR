from dotenv import load_dotenv
load_dotenv()
import re

from banco_dados.connection import Transições


class Tag:

    def __init__(self, name):
        self.name = name.strip() if name else None

    def salvar(self):

        if not self.name:
            print("O nome da tag é obrigatório.")
            input("\nPressione 'Enter' para continuar...")
            return

        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", self.name):
            print("Tag inválida. Use apenas letras.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    "INSERT INTO tags (name) VALUES (%s)",
                    (self.name,)
                )
                print("Tag cadastrada com sucesso!")

        except Exception as e:
            if "Duplicate entry" in str(e):
                print("Esta tag já está cadastrada.")
            else:
                print(f"Erro ao cadastrar tag: {e}")

        input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def listar():
        try:
            with Transições() as cursor:
                cursor.execute("SELECT id, name FROM tags ORDER BY id ASC")
                tags = cursor.fetchall()

            if not tags:
                print("Nenhuma tag cadastrada.")
            else:
                print("\n=========== TAGS CADASTRADAS ===========\n")
                for t in tags:
                    print(f"{t['id']} - {t['name']}")

        except Exception as e:
            print(f"Erro ao listar tags: {e}")

        input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def editar(id_tag, novo_nome):

        if not novo_nome:
            print("O nome da tag é obrigatório.")
            return

        novo_nome = novo_nome.strip()

        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", novo_nome):
            print("Nome inválido. Use apenas letras.")
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    "UPDATE tags SET name = %s WHERE id = %s",
                    (novo_nome, id_tag)
                )

                if cursor.rowcount > 0:
                    print("Tag atualizada com sucesso!")
                else:
                    print("Tag não encontrada.")

        except Exception as e:
            if "Duplicate entry" in str(e):
                print("Já existe uma tag com esse nome.")
            else:
                print(f"Erro ao atualizar tag: {e}")

        input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def excluir(id_tag):
        try:
            with Transições() as cursor:
                cursor.execute("DELETE FROM tags WHERE id = %s", (id_tag,))

                if cursor.rowcount > 0:
                    print("Tag excluída com sucesso!")
                else:
                    print("Tag não encontrada.")

        except Exception as e:
            print(f"Erro ao excluir tag: {e}")

        input("\nPressione 'Enter' para continuar...")
