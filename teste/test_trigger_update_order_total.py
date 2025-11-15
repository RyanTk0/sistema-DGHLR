def test_trigger_update_order_total(db_cursor):
    db_cursor.execute("INSERT INTO products (name, sku, price, stock) VALUES ('T', 'SKU-TG', 200, 10)")
    db_cursor.execute("SELECT id FROM products WHERE sku = 'SKU-TG'")
    product_id = db_cursor.fetchone()["id"]

    db_cursor.execute("INSERT INTO users (name, email, role_id) VALUES ('TR', 'trg@example.com', 1)")
    db_cursor.execute("SELECT id FROM users WHERE email = 'trg@example.com'")
    user_id = db_cursor.fetchone()["id"]

    db_cursor.execute("INSERT INTO orders (user_id) VALUES (%s)", (user_id,))
    db_cursor.execute("SELECT id FROM orders WHERE user_id = %s", (user_id,))
    order_id = db_cursor.fetchone()["id"]

    db_cursor.execute("""
        INSERT INTO order_items (order_id, product_id, quantity, price)
        VALUES (%s, %s, 2, 200)
    """, (order_id, product_id))

    db_cursor.execute("SELECT total FROM orders WHERE id = %s", (order_id,))
    total = db_cursor.fetchone()["total"]

    assert total == 400