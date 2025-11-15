from relatórios.relatorios_complexos import (
    r_produtos_nunca_vendidos,
    r_clientes_com_pedidos,
    r_total_gasto_por_cliente,
    r_total_vendido_por_produto,
    r_ticket_medio_por_cliente,
    r_media_preco_por_tag
)
import os


def menu_relatorios():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n===== RELATÓRIOS — CONSULTAS COMPLEXAS =====")
        print("1 - Produtos nunca vendidos")
        print("2 - Clientes que possuem pedidos")
        print("3 - Total gasto por cliente")
        print("4 - Total vendido por produto")
        print("5 - Ticket médio por cliente")
        print("6 - Média de preço por tag")
        print("0 - Voltar")

        opc = input("Escolha a opção desejada: ")

        if opc == "1":
            r_produtos_nunca_vendidos()
        elif opc == "2":
            r_clientes_com_pedidos()
        elif opc == "3":
            r_total_gasto_por_cliente()
        elif opc == "4":
            r_total_vendido_por_produto()
        elif opc == "5":
            r_ticket_medio_por_cliente()
        elif opc == "6":
            r_media_preco_por_tag()
        elif opc == "0":
            break
        else:
            print("\nOpção inválida!")
            input("Pressione Enter para continuar...")
