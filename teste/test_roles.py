def test_insert_role(db_cursor):
    db_cursor.execute("INSERT INTO roles (name) VALUES ('tester_role')")
    db_cursor.execute("SELECT * FROM roles WHERE name = 'tester_role'")
    result = db_cursor.fetchone()
    assert result["name"] == "tester_role"