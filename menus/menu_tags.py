from models.tags import Tag

def menu_tags():
    while True:
        print("\n===== MENU DE TAGS =====")
        print("1 - Cadastrar tag")
        print("2 - Listar tags")
        print("3 - Editar tag")
        print("4 - Excluir tag")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome da tag: ")
            Tag(nome).salvar()

        elif opcao == "2":
            Tag.listar()

        elif opcao == "3":
            try:
                id_tag = int(input("ID da tag a editar: "))
            except:
                print("ID inválido! Use apenas números.")
                input("\nPressione ENTER para continuar...")
                continue

            novo_nome = input("Novo nome da tag: ")
            Tag.editar(id_tag, novo_nome)

        elif opcao == "4":
            try:
                id_tag = int(input("ID da tag a excluir: "))
            except:
                print("ID inválido! Use apenas números.")
                input("\nPressione ENTER para continuar...")
                continue

            Tag.excluir(id_tag)

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")
