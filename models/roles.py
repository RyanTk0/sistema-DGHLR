from dotenv import load_dotenv
load_dotenv()
import re

from banco_dados.connection import Transições


class Role:

    def __init__(self, name):
        self.name = name.strip() if name else None

    def salvar(self):

        if not self.name:
            print("O nome da role é obrigatório.")
            input("\nPressione 'Enter' para continuar...")
            return

        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", self.name):
            print("Nome inválido. Use apenas letras.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    "INSERT INTO roles (name) VALUES (%s)",
                    (self.name,)
                )
                print("Role cadastrada com sucesso!")

        except Exception as e:
            if "Duplicate entry" in str(e):
                print("Já existe uma role com esse nome.")
            else:
                print(f"Erro ao cadastrar role: {e}")

        input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def listar():
        try:
            with Transições() as cursor:
                cursor.execute("SELECT id, name FROM roles ORDER BY id ASC")
                roles = cursor.fetchall()

            if not roles:
                print("Nenhuma role cadastrada.")
            else:
                print("\n=========== ROLES CADASTRADAS ===========\n")
                for r in roles:
                    print(f"{r['id']} - {r['name']}")

        except Exception as e:
            print(f"Erro ao listar roles: {e}")

        input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def editar(id_role, novo_nome):

        if not novo_nome:
            print("O nome da role é obrigatório.")
            return

        novo_nome = novo_nome.strip()

        if not re.match(r"^[A-Za-zÀ-ÿ\s]+$", novo_nome):
            print("Nome inválido. Use apenas letras.")
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    "UPDATE roles SET name = %s WHERE id = %s",
                    (novo_nome, id_role)
                )

                if cursor.rowcount > 0:
                    print("Role atualizada com sucesso!")
                else:
                    print("Role não encontrada.")

        except Exception as e:
            if "Duplicate entry" in str(e):
                print("Já existe uma role com esse nome.")
            else:
                print(f"Erro ao atualizar role: {e}")

        input("\nPressione 'Enter' para continuar...")

    @staticmethod
    def excluir(id_role):
        try:
            with Transições() as cursor:
                cursor.execute("DELETE FROM roles WHERE id = %s", (id_role,))

                if cursor.rowcount > 0:
                    print("Role excluída com sucesso!")
                else:
                    print("Role não encontrada.")

        except Exception as e:

            if "foreign key constraint" in str(e).lower():
                print("Esta role está associada a um usuário e não pode ser excluída.")
            else:
                print(f"Erro ao excluir role: {e}")

        input("\nPressione 'Enter' para continuar...")
