from models.order_items import OrderItem

def menu_order_items():
    while True:
        print("\n=============== MENU - ITENS DO PEDIDO ===============")
        print("1 - Cadastrar item")
        print("2 - Listar itens")
        print("3 - Modificar item")
        print("4 - Excluir item")
        print("0 - Voltar")

        opc = input("\nEscolha: ")

        if opc == "1":
            try:
                order_id = int(input("ID do pedido: "))
                product_id = int(input("ID do produto: "))
                quantity = int(input("Quantidade: "))
                price = float(input("Preço unitário (R$): "))
            except:
                print("Valores inválidos.")
                input("\nPressione 'Enter' para continuar...")
                continue

            OrderItem(order_id, product_id, quantity, price).salvar()

        elif opc == "2":
            OrderItem.listar()

        elif opc == "3":
            try:
                item_id = int(input("ID do item a modificar: "))
            except:
                print("ID inválido!")
                continue

            print("\n--- Campos para alterar ---")
            nova_qtd = input("Nova quantidade (Enter para manter): ")
            novo_preco = input("Novo preço (Enter para manter): ")

            qtd_val = int(nova_qtd) if nova_qtd.strip() else None
            preco_val = float(novo_preco) if novo_preco.strip() else None

            OrderItem.modificar(item_id, qtd_val, preco_val)

        elif opc == "4":
            try:
                item_id = int(input("ID do item a excluir: "))
            except:
                print("ID inválido!")
                continue

            OrderItem.excluir(item_id)

        elif opc == "0":
            break

        else:
            print("Opção inválida!")
            input("\nPressione 'Enter' para continuar...")
