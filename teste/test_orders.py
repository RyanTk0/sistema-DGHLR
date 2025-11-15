def test_insert_order(db_cursor):
    db_cursor.execute("INSERT INTO users (name, email, role_id) VALUES ('Client', 'client_pytest@example.com', 1)")
    db_cursor.execute("SELECT id FROM users WHERE email = 'client_pytest@example.com'")
    user_id = db_cursor.fetchone()["id"]

    db_cursor.execute("INSERT INTO orders (user_id) VALUES (%s)", (user_id,))
    db_cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))

    order = db_cursor.fetchone()
    assert order["user_id"] == user_id