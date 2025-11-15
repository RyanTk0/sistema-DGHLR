def test_insert_tag(db_cursor):
    db_cursor.execute("INSERT INTO tags (name) VALUES ('pytest_tag')")
    db_cursor.execute("SELECT * FROM tags WHERE name = 'pytest_tag'")
    result = db_cursor.fetchone()
    assert result["name"] == "pytest_tag"