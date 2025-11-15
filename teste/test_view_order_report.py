def test_view_order_report(db_cursor):
    db_cursor.execute("SELECT * FROM vw_order_report LIMIT 1")
    row = db_cursor.fetchone()

    assert "order_id" in row
    assert "customer_name" in row
    assert "product_name" in row
    assert "subtotal" in row