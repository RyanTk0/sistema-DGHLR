from models.order_items import OrderItem
from models.products import Product
from models.orders import Order


def menu_order_items():
    while True:
        print("\n=========== MENU - ITENS DO PEDIDO ===========")
        print("1 - Adicionar item ao pedido")
        print("2 - Listar TODOS os pedidos com itens")
        print("3 - Modificar item do pedido")
        print("4 - Excluir item do pedido")
        print("0 - Voltar")

        opc = input("\nEscolha: ").strip()

        if opc in ["1", "3", "4"]:
            try:
                order_id = int(input("ID do pedido: "))
            except ValueError:
                print("ID inválido!")
                continue

        if opc == "1":
            produtos = Product.listar()
            if not produtos:
                print("Nenhum produto disponível.")
                continue

            print("\nProdutos disponíveis:")
            print(f"{'ID':<5} | {'Nome':<20} | {'Preço'}")
            print("-" * 40)
            for p in produtos:
                print(f"{p['id']:<5} | {p['name']:<20} | R$ {p['price']:.2f}")

            try:
                product_id = int(input("\nID do produto: "))
                quantidade = int(input("Quantidade: "))
            except ValueError:
                print("Valores inválidos!")
                continue

            produto = next((p for p in produtos if p["id"] == product_id), None)

            if not produto:
                print("Produto não encontrado!")
                continue

            preco = produto["price"]

            OrderItem(order_id, product_id, quantidade, preco).salvar()
            input("\nPressione 'Enter' para continuar...")

        elif opc == "2":
            pedidos = Order.listar()

            if not pedidos:
                print("Nenhum pedido encontrado.")
                input("\nPressione 'Enter' para continuar...")
                continue

            print("\n=========== LISTA DE TODOS OS PEDIDOS ==========\n")

            for pedido in pedidos:
                print(f"Pedido ID: {pedido['id']}  |  Usuário: {pedido['usuario']}  |  Data: {pedido['data_pedido']}")
                print("-" * 60)

                itens = OrderItem.listar(pedido['id'])

                if not itens:
                    print("  Nenhum item neste pedido.")
                else:
                    total_pedido = 0
                    print(f"{'Produto':<20} | {'Qtd':<5} | {'Preço':<10} | Subtotal")
                    print("-" * 60)

                    for item in itens:
                        subtotal = item['quantity'] * item['price']
                        total_pedido += subtotal
                        print(f"{item['produto']:<20} | {item['quantity']:<5} | R$ {item['price']:<10.2f} | R$ {subtotal:.2f}")

                    print(f"\nTOTAL DO PEDIDO: R$ {total_pedido:.2f}")

                print("\n" + "=" * 60 + "\n")

            input("\nPressione 'Enter' para continuar...")

        elif opc == "3":
            itens = OrderItem.listar(order_id)

            if not itens:
                print("Nenhum item nesse pedido.")
                continue

            print("\nItens disponíveis:")
            for i in itens:
                print(f"ID Item: {i['item_id']} | Produto: {i['produto']} | Qtd: {i['quantity']} | Preço: R$ {i['price']:.2f}")

            try:
                item_id = int(input("\nID do item a modificar: "))
            except ValueError:
                print("ID inválido!")
                continue

            print("\n1 - Alterar quantidade")
            print("2 - Alterar produto")
            print("3 - Alterar pedido")
            print("4 - Alterar quantidade e produto")
            print("0 - Cancelar")

            escolha = input("\nEscolha: ").strip()

            nova_qtd = None
            novo_produto = None
            novo_order = None

            if escolha in ["1", "4"]:
                try:
                    nova_qtd = int(input("Nova quantidade: "))
                except ValueError:
                    print("Quantidade inválida!")
                    continue

            if escolha in ["2", "4"]:
                produtos = Product.listar()
                print("\nProdutos disponíveis:")
                for p in produtos:
                    print(f"{p['id']} - {p['name']} (R$ {p['price']:.2f})")
                try:
                    novo_produto = int(input("Novo ID de produto: "))
                except ValueError:
                    print("Produto inválido!")
                    continue

            if escolha == "3":
                try:
                    novo_order = int(input("Novo ID do pedido: "))
                except ValueError:
                    print("Pedido inválido!")
                    continue

            OrderItem.modificar(
                item_id,
                quantity=nova_qtd,
                product_id=novo_produto,
                order_id=novo_order
            )

            input("\nPressione 'Enter' para continuar...")

        elif opc == "4":
            itens = OrderItem.listar(order_id)

            if not itens:
                print("Nenhum item nesse pedido.")
                continue

            print("\nItens disponíveis:")
            for i in itens:
                print(f"ID Item: {i['item_id']} | Produto: {i['produto']} | Qtd: {i['quantity']}")

            try:
                item_id = int(input("\nID do item a excluir: "))
            except ValueError:
                print("ID inválido!")
                continue

            OrderItem.excluir(item_id)
            input("\nPressione 'Enter' para continuar...")

        elif opc == "0":
            break

        else:
            print("Opção inválida!")
            input("\nPressione 'Enter' para continuar...")
