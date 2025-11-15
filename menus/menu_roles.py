from models.roles import Role

def menu_roles():
    while True:
        print("\n===== MENU DE ROLES =====")
        print("1 - Cadastrar role")
        print("2 - Listar roles")
        print("3 - Editar role")
        print("4 - Excluir role")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome da role: ")
            Role(nome).salvar()

        elif opcao == "2":
            Role.listar()

        elif opcao == "3":
            try:
                id_role = int(input("ID da role a editar: "))
            except:
                print("ID inválido! Use apenas números.")
                input("\nPressione ENTER para continuar...")
                continue

            novo_nome = input("Novo nome da role: ")
            Role.editar(id_role, novo_nome)

        elif opcao == "4":
            try:
                id_role = int(input("ID da role a excluir: "))
            except:
                print("ID inválido! Use apenas números.")
                input("\nPressione ENTER para continuar...")
                continue

            Role.excluir(id_role)

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")
