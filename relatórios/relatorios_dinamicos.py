import os
import json
import csv
from reportlab.pdfgen import canvas
from banco_dados.connection import Transições

def relatorios_dinamicos():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIOS DINÂMICOS ===\n")

    data_inicio = input("Informe a data inicial (YYYY-MM-DD): ")
    data_fim = input("Informe a data final (YYYY-MM-DD): ")

    print("\nEscolha o formato de exportação:")
    print("1 - CSV")
    print("2 - JSON")
    print("3 - PDF")

    formato = input("Opção: ")

    query = """
        SELECT o.id AS pedido, u.name AS cliente, o.total, o.created_at
        FROM orders o
        JOIN users u ON u.id = o.user_id
        WHERE o.created_at BETWEEN %s AND %s
        ORDER BY o.created_at DESC;
    """

    try:
        with Transições() as cursor:
            cursor.execute(query, (data_inicio, data_fim))
            dados = cursor.fetchall()

            if not dados:
                print("Nenhum pedido encontrado no período informado.")
                input()
                return

            if formato == "1":
                exportar_csv(dados)
            elif formato == "2":
                exportar_json(dados)
            elif formato == "3":
                exportar_pdf(dados)
            else:
                print("Opção inválida.")

            print("\nRelatório gerado com sucesso!")
            input()

    except Exception as e:
        print(f"Erro: {e}")
        input()


def exportar_csv(dados):
    with open("relatorio_pedidos.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=dados[0].keys())
        writer.writeheader()
        writer.writerows(dados)


def exportar_json(dados):
    with open("relatorio_pedidos.json", "w", encoding="utf-8") as file:
        json.dump(dados, file, indent=4, default=str)


def exportar_pdf(dados):
    pdf = canvas.Canvas("relatorio_pedidos.pdf")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 800, "Relatório de Pedidos por Período")

    y = 770
    for item in dados:
        texto = f"Pedido {item['pedido']} | Cliente: {item['cliente']} | Total: R$ {item['total']:.2f} | Data: {item['created_at']}"
        pdf.drawString(50, y, texto)
        y -= 20

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y = 800

    pdf.save()
