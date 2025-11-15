def test_insert_product(db_cursor):
    db_cursor.execute("""
        INSERT INTO products (name, sku, price, stock)
        VALUES ('Test Product', 'SKU-TEST', 10.50, 5)
    """)
    db_cursor.execute("SELECT * FROM products WHERE sku = 'SKU-TEST'")
    result = db_cursor.fetchone()

    assert result["price"] == 10.50
    assert result["stock"] == 5