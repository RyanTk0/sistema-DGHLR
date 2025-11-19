from models.orders import Order

def menu_orders():
    while True:
        print("\n=============== MENU - PEDIDOS ===============")
        print("1 - Cadastrar pedido")
        print("2 - Listar pedidos")
        print("3 - Modificar pedido")
        print("4 - Excluir pedido")
        print("0 - Voltar")

        opc = input("\nEscolha: ")

        if opc == "1":
            try:
                user_id = int(input("ID do usuário: "))
                if user_id <= 0:
                    print("O ID do usuário deve ser maior que zero!")
                    continue
            except ValueError:
                print("Valores inválidos! O ID do usuário deve ser um número inteiro.")
                continue

            result = Order(user_id).salvar()
            if result.get("success"):
                print(f"Pedido cadastrado com sucesso! ID do pedido: {result['order_id']}")
            else:
                print(f"Erro ao cadastrar pedido: {result['error']}")
            input("\nPressione 'Enter' para continuar...")

        elif opc == "2":
            pedidos = Order.listar()
            if pedidos:
                print("\n==== LISTA DE PEDIDOS ====")
                print(f"{'ID':<5} | {'User ID':<8} | {'Cliente':<15} | {'Data do Pedido'}")
                print("-" * 50)
                for p in pedidos:
                    print(f"{p['id']:<5} | {p['user_id']:<8} | {p['usuario']:<15} | {p['data_pedido']}")
                print("=" * 50)
            else:
                print("Nenhum pedido encontrado.")
            input("\nPressione 'Enter' para continuar...")

        elif opc == "3":
            try:
                order_id = int(input("ID do pedido a modificar: "))
            except ValueError:
                print("ID inválido! O ID do pedido deve ser um número inteiro.")
                continue

            novo_user = input("Novo user_id: ")
            user_val = int(novo_user) if novo_user.strip() else None

            Order.modificar(order_id, user_val)
            input("\nPressione 'Enter' para continuar...")

        elif opc == "4":
            try:
                order_id = int(input("ID do pedido a excluir: "))
            except ValueError:
                print("ID inválido! O ID do pedido deve ser um número inteiro.")
                continue

            Order.excluir(order_id)
            input("\nPressione 'Enter' para continuar...")

        elif opc == "0":
            break

        else:
            print("Opção inválida! Tente novamente.")
            input("\nPressione 'Enter' para continuar...")
