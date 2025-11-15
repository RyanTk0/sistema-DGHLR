from models.product_tags import ProductTag

def menu_product_tag():
    while True:
        print("\n========= MENU - RELAÇÃO PRODUTO x TAG =========")
        print("1 - Cadastrar relação (product_id ↔ tag_id)")
        print("2 - Listar relações")
        print("3 - Excluir relação")
        print("0 - Voltar")

        opc = input("\nEscolha: ")

        if opc == "1":
            try:
                product_id = int(input("ID do produto: "))
                tag_id = int(input("ID da tag: "))
            except:
                print("Valores inválidos! Use apenas números inteiros.")
                input("\nPressione 'Enter' para continuar...")
                continue

            ProductTag(product_id, tag_id).salvar()

        elif opc == "2":
            ProductTag.listar()

        elif opc == "3":
            try:
                product_id = int(input("ID do produto da relação: "))
                tag_id = int(input("ID da tag da relação: "))
            except:
                print("Valores inválidos! Use apenas números inteiros.")
                input("\nPressione 'Enter' para continuar...")
                continue

            ProductTag.excluir(product_id, tag_id)

        elif opc == "0":
            break

        else:
            print("Opção inválida!")
            input("\nPressione 'Enter' para continuar...")
