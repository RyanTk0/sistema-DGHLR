from models.products import Product

def menu_products():
    while True:
        print("\n===== MENU DE PRODUTOS =====")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Editar produto")
        print("4 - Excluir produto")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            nome = input("Nome: ")
            descricao = input("Descrição: ")

            try:
                preco = float(input("Preço: "))
            except:
                print("Preço inválido!")
                input("\nPressione ENTER para continuar...")
                continue

            try:
                estoque = int(input("Estoque: "))
            except:
                print("Estoque inválido!")
                input("\nPressione ENTER para continuar...")
                continue

            Product(nome, descricao, preco, estoque).salvar()

        elif opcao == "2":
            Product.listar()

        elif opcao == "3":
            try:
                id_prod = int(input("ID do produto a editar: "))
            except:
                print("ID inválido!")
                input("\nPressione ENTER para continuar...")
                continue

            novo_nome = input("Novo nome: ")
            nova_desc = input("Nova descrição: ")

            try:
                novo_preco = float(input("Novo preço: "))
            except:
                print("Preço inválido!")
                input("\nPressione ENTER para continuar...")
                continue

            try:
                novo_estoque = int(input("Novo estoque: "))
            except:
                print("Estoque inválido!")
                input("\nPressione ENTER para continuar...")
                continue

            Product.editar(id_prod, novo_nome, nova_desc, novo_preco, novo_estoque)

        elif opcao == "4":
            try:
                id_prod = int(input("ID do produto a excluir: "))
            except:
                print("ID inválido!")
                input("\nPressione ENTER para continuar...")
                continue

            Product.excluir(id_prod)

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")
