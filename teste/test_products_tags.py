def test_product_tag_relation(db_cursor):
    db_cursor.execute("INSERT INTO products (name, sku, price, stock) VALUES ('P1', 'SKU-P1', 10, 2)")
    db_cursor.execute("INSERT INTO tags (name) VALUES ('TAG1')")

    db_cursor.execute("SELECT id FROM products WHERE sku = 'SKU-P1'")
    prod_id = db_cursor.fetchone()["id"]

    db_cursor.execute("SELECT id FROM tags WHERE name = 'TAG1'")
    tag_id = db_cursor.fetchone()["id"]

    db_cursor.execute("INSERT INTO product_tags (product_id, tag_id) VALUES (%s, %s)", (prod_id, tag_id))

    db_cursor.execute("""
        SELECT * FROM product_tags WHERE product_id = %s AND tag_id = %s
    """, (prod_id, tag_id))

    rel = db_cursor.fetchone()
    assert rel is not None