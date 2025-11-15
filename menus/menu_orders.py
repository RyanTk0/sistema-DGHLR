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
                total = float(input("Total do pedido (R$): "))
            except:
                print("Valores inválidos!")
                continue

            Order(user_id, total).salvar()
            input("\nEnter para continuar...")

        elif opc == "2":
            pedidos = Order.listar()

            if isinstance(pedidos, dict) and not pedidos.get("success", True):
                print("\n❌ Erro ao listar pedidos:", pedidos["error"])
            else:
                print("\n===== LISTA DE PEDIDOS =====\n")
                print(f"{'ID':<5} | {'User ID':<8} | {'Cliente':<15} | {'Total (R$)':<10}")
                print("-" * 50)
                for p in pedidos:
                    print(f"{p['id']:<5} | {p['user_id']:<8} | {p['usuario']:<15} | R$ {p['total']:.2f}")
                print("=" * 50)

            input("\nEnter para continuar...")

        elif opc == "3":
            try:
                order_id = int(input("ID do pedido a modificar: "))
            except:
                print("ID inválido!")
                continue

            novo_user = input("Novo user_id (ou Enter p/ manter): ")
            novo_total = input("Novo total (ou Enter p/ manter): ")

            user_val = int(novo_user) if novo_user.strip() else None
            total_val = float(novo_total) if novo_total.strip() else None

            Order.modificar(order_id, user_val, total_val)
            input("\nEnter para continuar...")

        elif opc == "4":
            try:
                order_id = int(input("ID do pedido a excluir: "))
            except:
                print("ID inválido!")
                continue

            Order.excluir(order_id)
            input("\nEnter para continuar...")

        elif opc == "0":
            break

        else:
            print("Opção inválida!")
            input("\nEnter para continuar...")
