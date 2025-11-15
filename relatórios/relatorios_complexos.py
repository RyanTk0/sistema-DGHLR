import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from banco_dados.connection import Transições


def r_produtos_nunca_vendidos():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIO: PRODUTOS NUNCA VENDIDOS ===\n")

    try:
        with Transições() as cursor:
            query = """
                SELECT p.id, p.name, p.price
                FROM products p
                WHERE NOT EXISTS (
                    SELECT 1 FROM order_items oi
                    WHERE oi.product_id = p.id
                )
                ORDER BY p.name;
            """

            cursor.execute(query)
            dados = cursor.fetchall()

            print(f"{'Produto':<30} | {'Preço (R$)':<15}")
            print("-" * 50)

            for linha in dados:
                print(f"{linha['name']:<30} | {linha['price']:>10.2f}")

            print("=" * 50)
            input()

    except Exception as e:
        print(f"Erro: {e}")
        input()


def r_clientes_com_pedidos():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIO: CLIENTES QUE POSSUEM PEDIDOS ===\n")

    try:
        with Transições() as cursor:
            query = """
                SELECT u.id, u.name
                FROM users u
                WHERE EXISTS (
                    SELECT 1 FROM orders o
                    WHERE o.user_id = u.id
                )
                ORDER BY u.name;
            """

            cursor.execute(query)
            dados = cursor.fetchall()

            print(f"{'Cliente':<30}")
            print("-" * 30)

            for linha in dados:
                print(f"{linha['name']:<30}")

            print("=" * 30)
            input()

    except Exception as e:
        print(f"Erro: {e}")
        input()


def r_total_gasto_por_cliente():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIO: TOTAL GASTO POR CLIENTE ===\n")

    try:
        with Transições() as cursor:
            query = """
                SELECT
                    u.name AS cliente,
                    SUM(o.total) AS total_gasto
                FROM users u
                JOIN orders o ON o.user_id = u.id
                GROUP BY u.id
                ORDER BY total_gasto DESC;
            """

            cursor.execute(query)
            dados = cursor.fetchall()

            print(f"{'Cliente':<25} | {'Total Gasto (R$)':<15}")
            print("-" * 45)

            for linha in dados:
                print(f"{linha['cliente']:<25} | {linha['total_gasto']:>10.2f}")

            print("=" * 45)
            input()

    except Exception as e:
        print(f"Erro: {e}")
        input()


def r_total_vendido_por_produto():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIO: TOTAL VENDIDO POR PRODUTO ===\n")

    try:
        with Transições() as cursor:
            query = """
                SELECT 
                    p.name AS produto,
                    SUM(oi.quantity) AS total_unidades,
                    SUM(oi.quantity * oi.price) AS valor_total
                FROM order_items oi
                JOIN products p ON p.id = oi.product_id
                GROUP BY p.id
                ORDER BY valor_total DESC;
            """

            cursor.execute(query)
            dados = cursor.fetchall()

            print(f"{'Produto':<30} | {'Unidades':<10} | {'Total (R$)':<15}")
            print("-" * 65)

            for linha in dados:
                print(f"{linha['produto']:<30} | {linha['total_unidades']:<10} | {linha['valor_total']:>10.2f}")

            print("=" * 65)
            input()

    except Exception as e:
        print(f"Erro: {e}")
        input()


def r_ticket_medio_por_cliente():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIO: TICKET MÉDIO POR CLIENTE ===\n")

    try:
        with Transições() as cursor:
            query = """
                SELECT
                    u.name AS cliente,
                    AVG(o.total) AS ticket_medio
                FROM users u
                JOIN orders o ON o.user_id = u.id
                GROUP BY u.id
                ORDER BY ticket_medio DESC;
            """

            cursor.execute(query)
            dados = cursor.fetchall()

            print(f"{'Cliente':<25} | {'Ticket Médio (R$)':<15}")
            print("-" * 45)

            for linha in dados:
                print(f"{linha['cliente']:<25} | {linha['ticket_medio']:>10.2f}")

            print("=" * 45)
            input()

    except Exception as e:
        print(f"Erro: {e}")
        input()


def r_media_preco_por_tag():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n=== RELATÓRIO: MÉDIA DE PREÇO POR TAG ===\n")

    try:
        with Transições() as cursor:
            query = """
                SELECT 
                    t.name AS tag,
                    AVG(p.price) AS preco_medio
                FROM tags t
                JOIN product_tags pt ON pt.tag_id = t.id
                JOIN products p ON p.id = pt.product_id
                GROUP BY t.id
                ORDER BY preco_medio DESC;
            """

            cursor.execute(query)
            dados = cursor.fetchall()

            print(f"{'Tag':<20} | {'Preço Médio (R$)':<20}")
            print("-" * 40)

            for linha in dados:
                print(f"{linha['tag']:<20} | {linha['preco_medio']:>10.2f}")

            print("=" * 40)
            input()

    except Exception as e:
        print(f"Erro: {e}")
        input()
