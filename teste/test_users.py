def test_insert_user(db_cursor):
    db_cursor.execute("""
        INSERT INTO users (name, email, role_id)
        VALUES ('Test User', 'pytest_user@example.com', 1)
    """)
    db_cursor.execute("SELECT * FROM users WHERE email = 'pytest_user@example.com'")
    result = db_cursor.fetchone()

    assert result["name"] == "Test User"
    assert result["role_id"] == 1