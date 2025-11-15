from dotenv import load_dotenv
load_dotenv()
import re

from banco_dados.connection import Transições


class User:

    def __init__(self, name, email, role_id):
        self.name = name.strip() if name else None
        self.email = email.strip().lower() if email else None
        self.role_id = role_id

    def salvar(self):

        if not self.name:
            print("O nome é obrigatório.")
            input("\nPressione 'Enter' para continuar...")
            return
        
        if not self.email:
            print("O email é obrigatório.")
            input("\nPressione 'Enter' para continuar...")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            print("Email inválido.")
            input("\nPressione 'Enter' para continuar...")
            return

        if not isinstance(self.role_id, int):
            print("role_id inválido. Ele deve ser um número inteiro.")
            input("\nPressione 'Enter' para continuar...")
            return

        try:
            with Transições() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email, role_id) VALUES (%s, %s, %s)",
                    (self.name, self.email, self.role_id)
                )
                print("Usuário cadastrado com sucesso!")
                input("\nPressione 'Enter' para continuar...")

        except Exception as e:
            if "Duplicate entry" in str(e):
                print("Já existe um usuário com esse email.")
            elif "foreign key constraint" in str(e).lower():
                print("O role_id informado não existe na tabela roles.")
            else:
                print(f"Erro ao cadastrar usuário: {e}")
            input("\nPressione 'Enter' para continuar...")


    @staticmethod
    def listar():
        try:
            with Transições() as cursor:
                cursor.execute("SELECT id, name, email, role_id, created_at FROM users ORDER BY id ASC")
                users = cursor.fetchall()

            if not users:
                print("Nenhum usuário cadastrado.")
            else:
                print("\n=========== USUÁRIOS CADASTRADOS ===========\n")
                for u in users:
                    print(
                        f"{u['id']} - {u['name']} | {u['email']} | role_id={u['role_id']} "
                        f"| criado em {u['created_at']}"
                    )

        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
        input("\nPressione 'Enter' para continuar...")


    @staticmethod
    def editar(id_user, novo_nome, novo_email, novo_role_id):

        if not novo_nome:
            print("O nome é obrigatório.")
            return

        if not novo_email or not re.match(r"[^@]+@[^@]+\.[^@]+", novo_email):
            print("Email inválido.")
            return

        if not isinstance(novo_role_id, int):
            print("role_id inválido.")
            return

        novo_email = novo_email.lower().strip()

        try:
            with Transições() as cursor:
                cursor.execute(
                    """
                    UPDATE users 
                    SET name = %s, email = %s, role_id = %s
                    WHERE id = %s
                    """,
                    (novo_nome, novo_email, novo_role_id, id_user)
                )

                if cursor.rowcount > 0:
                    print("Usuário atualizado com sucesso!")
                else:
                    print("Usuário não encontrado.")

        except Exception as e:
            if "Duplicate entry" in str(e):
                print("Já existe outro usuário usando esse email.")
            elif "foreign key constraint" in str(e).lower():
                print("O role_id não existe na tabela roles.")
            else:
                print(f"Erro ao atualizar usuário: {e}")
        input("\nPressione 'Enter' para continuar...")


    @staticmethod
    def excluir(id_user):
        try:
            with Transições() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (id_user,))

                if cursor.rowcount > 0:
                    print("Usuário excluído com sucesso!")
                else:
                    print("Usuário não encontrado.")

        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")

        input("\nPressione 'Enter' para continuar...")
