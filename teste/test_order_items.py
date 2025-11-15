def test_insert_order_item(db_cursor):
    db_cursor.execute("INSERT INTO products (name, sku, price, stock) VALUES ('Prod', 'SKU-OI', 50, 10)")
    db_cursor.execute("SELECT id FROM products WHERE sku = 'SKU-OI'")
    prod_id = db_cursor.fetchone()["id"]

    db_cursor.execute("INSERT INTO users (name, email, role_id) VALUES ('Client OI', 'clientoi@example.com', 1)")
    db_cursor.execute("SELECT id FROM users WHERE email = 'clientoi@example.com'")
    user_id = db_cursor.fetchone()["id"]

    db_cursor.execute("INSERT INTO orders (user_id) VALUES (%s)", (user_id,))
    db_cursor.execute("SELECT id FROM orders WHERE user_id = %s", (user_id,))
    order_id = db_cursor.fetchone()["id"]

    db_cursor.execute("""
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES (%s, %s, 2, 50)
    """, (order_id, prod_id))

    db_cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
    oi = db_cursor.fetchone()

    assert oi["quantity"] == 2
    assert oi["price"] == 50
