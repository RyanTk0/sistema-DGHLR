from menus.menu_users import menu_users
from menus.menu_products import menu_products
from menus.menu_roles import menu_roles
from menus.menu_tags import menu_tags
from menus.menu_product_tag import menu_product_tag
from menus.menu_orders import menu_orders
from menus.menu_order_items import menu_order_items
from menus.menu_relatorios import menu_relatorios  

def menu_principal():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Usuários")
        print("2 - Produtos")
        print("3 - Roles")
        print("4 - Tags")
        print("5 - Produto x Tag")
        print("6 - Orders (Pedidos)")
        print("7 - Order Items (Itens do Pedido)")
        print("8 - Relatórios")                        
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            menu_users()
        elif opcao == "2":
            menu_products()
        elif opcao == "3":
            menu_roles()
        elif opcao == "4":
            menu_tags()
        elif opcao == "5":
            menu_product_tag()
        elif opcao == "6":
            menu_orders()
        elif opcao == "7":
            menu_order_items()
        elif opcao == "8":
            menu_relatorios()                          
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_principal()