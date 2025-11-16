import os
import json
from menus.menu_users import menu_users
from menus.menu_products import menu_products
from menus.menu_roles import menu_roles
from menus.menu_tags import menu_tags
from menus.menu_product_tag import menu_product_tag
from menus.menu_orders import menu_orders
from menus.menu_order_items import menu_order_items
from menus.menu_relatorios import menu_relatorios
from menus.menu_relatorios_dinamicos import menu_relatorios_dinamicos
from banco_dados.reset_db import resetar_banco  

def menu_principal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n===== MENU PRINCIPAL =====")
        print("1 - Usuários")
        print("2 - Produtos")
        print("3 - Roles")
        print("4 - Tags")
        print("5 - Produto x Tag")
        print("6 - Orders (Pedidos)")
        print("7 - Order Items (Itens do Pedido)")
        print("8 - Relatórios Complexos")
        print("9 - Relatórios Dinâmicos")
        print("10 - Visualizar Relatórios Gerados")
        print("11 - Resetar Banco de Dados")  
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
        elif opcao == "9":
            menu_relatorios_dinamicos()
        elif opcao == "10":
            visualizar_relatorios()
        elif opcao == "11":
            resetar_banco()  
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

def visualizar_relatorios():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== VISUALIZAR RELATÓRIOS GERADOS ===\n")
    
    print("Escolha o relatório para visualizar:")
    print("1 - CSV")
    print("2 - JSON")
    print("3 - PDF")
    
    opcao = input("Escolha a opção: ")

    if opcao == "1":
        abrir_csv()
    elif opcao == "2":
        abrir_json()
    elif opcao == "3":
        abrir_pdf()
    else:
        print("Opção inválida!")
        input()

def abrir_csv():
    try:
        with open("relatorio_pedidos.csv", "r", encoding="utf-8") as file:
            print(file.read())
    except FileNotFoundError:
        print("Arquivo CSV não encontrado!")
    input()

def abrir_json():
    try:
        with open("relatorio_pedidos.json", "r", encoding="utf-8") as file:
            dados = json.load(file)
            print(json.dumps(dados, indent=4, default=str))
    except FileNotFoundError:
        print("Arquivo JSON não encontrado!")
    input()

def abrir_pdf():
    try:
        if os.name == 'nt':
            os.system("start relatorio_pedidos.pdf")
        else:
            os.system("xdg-open relatorio_pedidos.pdf")
    except FileNotFoundError:
        print("Arquivo PDF não encontrado!")
    input()

if __name__ == "__main__":
    menu_principal()
