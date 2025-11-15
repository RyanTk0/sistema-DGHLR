from models.users import User


def menu_users():
    while True:
        print("\n===== MENU DE USUÁRIOS =====")
        print("1 - Cadastrar usuário")
        print("2 - Listar usuários")
        print("3 - Editar usuário")
        print("4 - Excluir usuário")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            role_id = input("Role ID: ")

            try:
                role_id = int(role_id)
            except:
                print("Role ID deve ser número inteiro.")
                input("\nPressione ENTER para continuar...")
                continue

            User(nome, email, role_id).salvar()

        elif opcao == "2":
            User.listar()

        elif opcao == "3":
            try:
                id_user = int(input("ID do usuário a editar: "))
            except:
                print("ID inválido!")
                continue

            novo_nome = input("Novo nome: ")
            novo_email = input("Novo email: ")

            novo_role_id = input("Novo role_id: ")
            try:
                novo_role_id = int(novo_role_id)
            except:
                print("role_id inválido!")
                input("\nPressione ENTER para continuar...")
                continue

            User.editar(id_user, novo_nome, novo_email, novo_role_id)

        elif opcao == "4":
            try:
                id_user = int(input("ID do usuário a excluir: "))
            except:
                print("ID inválido!")
                continue

            User.excluir(id_user)

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")
