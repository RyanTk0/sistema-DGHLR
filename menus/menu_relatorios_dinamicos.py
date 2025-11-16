from relatórios.relatorios_dinamicos import relatorios_dinamicos
import os

def menu_relatorios_dinamicos():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\n===== RELATÓRIOS — DINÂMICOS =====")
        print("1 - Exportar pedidos por período (CSV / JSON / PDF)")
        print("0 - Voltar")

        opc = input("Escolha a opção desejada: ")

        if opc == "1":
            relatorios_dinamicos()
        elif opc == "0":
            break
        else:
            print("\nOpção inválida!")
            input("Pressione Enter para continuar...")
