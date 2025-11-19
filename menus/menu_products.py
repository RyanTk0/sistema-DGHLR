from models.products import Product

def menu_products():
    while True:
        print("\n=============== MENU - PRODUTOS ===============")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Editar produto")
        print("4 - Excluir produto")
        print("0 - Voltar")

        opc = input("\nEscolha: ")

        if opc == "1":
            try:
                nome = input("Nome do produto: ")
                preco = float(input("Preço do produto (R$): "))
                estoque = int(input("Estoque: "))
                if preco <= 0 or estoque < 0:
                    print("O preço deve ser maior que zero e o estoque não pode ser negativo!")
                    continue
            except ValueError:
                print("Valores inválidos! O preço e estoque devem ser números válidos.")
                continue

            Product(nome, preco, estoque).salvar()
            input("\nPressione 'Enter' para continuar...")

        elif opc == "2":
            produtos = Product.listar()

            if isinstance(produtos, dict) and not produtos.get("success", True):
                print("\n Erro ao listar produtos:", produtos["error"])
            else:
                print("\n===== LISTA DE PRODUTOS =====\n")
                print(f"{'ID':<5} | {'Nome':<15} | {'Preço (R$)':<10} | {'Estoque':<10}")
                print("-" * 50)
                for p in produtos:
                    print(f"{p['id']:<5} | {p['name']:<15} | R$ {p['price']:<10.2f} | {p['stock']:<10}")
                print("=" * 50)

            input("\nPressione 'Enter' para continuar...")

        elif opc == "3":
            try:
                id_produto = int(input("ID do produto a modificar: "))
            except ValueError:
                print("ID inválido! O ID do produto deve ser um número inteiro.")
                continue

            novo_nome = input("Novo nome: ")
            novo_preco = input("Novo preço: ")
            novo_estoque = input("Novo estoque: ")

            nome_val = novo_nome if novo_nome.strip() else None
            preco_val = float(novo_preco) if novo_preco.strip() else None
            estoque_val = int(novo_estoque) if novo_estoque.strip() else None

            Product.editar(id_produto, nome_val, preco_val, estoque_val)
            input("\nPressione 'Enter' para continuar...")

        elif opc == "4":
            try:
                id_produto = int(input("ID do produto a excluir: "))
            except ValueError:
                print("ID inválido! O ID do produto deve ser um número inteiro.")
                continue

            Product.excluir(id_produto)
            input("\nPressione 'Enter' para continuar...")

        elif opc == "0":
            break

        else:
            print("Opção inválida!")
            input("\nEnter para continuar...")
