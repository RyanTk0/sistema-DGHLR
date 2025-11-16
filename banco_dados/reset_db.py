import mysql.connector

def resetar_banco():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="151252",
            database="shopdb"
        )
        
        cursor = conn.cursor()

        cursor.execute("SET foreign_key_checks = 0;")

        reset_queries = [
            "TRUNCATE TABLE order_items;",
            "TRUNCATE TABLE orders;",
            "TRUNCATE TABLE product_tags;",
            "TRUNCATE TABLE products;",
            "TRUNCATE TABLE tags;",
            "TRUNCATE TABLE users;",
            "TRUNCATE TABLE roles;"
        ]

        for query in reset_queries:
            cursor.execute(query)
        
        conn.commit()

        cursor.execute("SET foreign_key_checks = 1;")
        
        create_queries = [
            """
            CREATE TABLE IF NOT EXISTS roles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                role_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (role_id) REFERENCES roles(id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                sku VARCHAR(100) NOT NULL UNIQUE,
                price DECIMAL(10,2) NOT NULL CHECK (price > 0),
                stock INT NOT NULL CHECK (stock >= 0),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS tags (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL UNIQUE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS product_tags (
                product_id INT NOT NULL,
                tag_id INT NOT NULL,
                PRIMARY KEY (product_id, tag_id),
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                total DECIMAL(10,2) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT NOT NULL,
                product_id INT NOT NULL,
                quantity INT NOT NULL CHECK (quantity > 0),
                price DECIMAL(10,2) NOT NULL CHECK (price > 0),
                FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
            """
        ]

        for query in create_queries:
            cursor.execute(query)
        
        conn.commit()

        insert_queries = [
            "INSERT INTO roles (name) VALUES ('cliente'), ('admin');",
            "INSERT INTO users (name, email, role_id) VALUES "
            "('Alice', 'alice@example.com', 1), "
            "('Bob', 'bob@example.com', 2), "
            "('Carlos', 'carlos@example.com', 1), "
            "('Diana', 'diana@example.com', 1);",
            "INSERT INTO products (name, sku, price, stock) VALUES "
            "('Notebook Gamer', 'NTBK-001', 5999.90, 10), "
            "('Mouse Sem Fio', 'MSE-002', 99.90, 50), "
            "('Teclado Mecânico RGB', 'KEY-003', 299.90, 30), "
            "('Monitor 27\" 144Hz', 'MON-004', 1899.90, 15);",
            "INSERT INTO tags (name) VALUES ('Informática'), ('Gamer'), ('Acessórios');",
            "INSERT INTO product_tags (product_id, tag_id) VALUES "
            "(1, 1), (1, 2), "
            "(2, 3), "
            "(3, 2), "
            "(4, 1), (4, 2);",
            "INSERT INTO orders (user_id) VALUES (1), (2), (3), (4);",
            "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES "
            "(1, 1, 1, 5999.90), "
            "(1, 2, 2, 99.90), "
            "(2, 3, 1, 299.90), "
            "(3, 4, 1, 1899.90), "
            "(4, 2, 3, 99.90);"
        ]

        for query in insert_queries:
            cursor.execute(query)
        
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Erro ao conectar ou executar comandos no banco de dados: {err}")
    
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexão com o banco de dados fechada.")

resetar_banco()
