DROP DATABASE IF EXISTS shopdb;
CREATE DATABASE shopdb;
USE shopdb;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS product_tags;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    role_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) NOT NULL UNIQUE,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    stock INT NOT NULL CHECK (stock >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE product_tags (
    product_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (product_id, tag_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_orders_date ON orders(created_at);
CREATE INDEX idx_order_items_product ON order_items(product_id);

INSERT INTO roles (name) VALUES ('cliente'), ('admin');

INSERT INTO users (name, email, role_id) VALUES
('Alice', 'alice@example.com', 1),
('Bob', 'bob@example.com', 2),
('Carlos', 'carlos@example.com', 1),
('Diana', 'diana@example.com', 1);

INSERT INTO products (name, sku, price, stock) VALUES
('Notebook Gamer', 'NTBK-001', 5999.90, 10),
('Mouse Sem Fio', 'MSE-002', 99.90, 50),
('Teclado Mecânico RGB', 'KEY-003', 299.90, 30),
('Monitor 27" 144Hz', 'MON-004', 1899.90, 15);

INSERT INTO tags (name) VALUES ('Informática'), ('Gamer'), ('Acessórios');

INSERT INTO product_tags (product_id, tag_id) VALUES
(1, 1), (1, 2),
(2, 3),
(3, 2),
(4, 1), (4, 2);

DELIMITER //
CREATE PROCEDURE sp_recalculate_order_total(IN p_order_id INT)
BEGIN
    DECLARE v_total DECIMAL(10,2);
    SELECT SUM(quantity * price) INTO v_total FROM order_items WHERE order_id = p_order_id;
    UPDATE orders SET total = IFNULL(v_total, 0) WHERE id = p_order_id;
END //
DELIMITER ;

INSERT INTO orders (user_id) VALUES (1), (2), (3), (4);

INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 5999.90),
(1, 2, 2, 99.90),
(2, 3, 1, 299.90),
(3, 4, 1, 1899.90),
(4, 2, 3, 99.90);

CALL sp_recalculate_order_total(1);
CALL sp_recalculate_order_total(2);
CALL sp_recalculate_order_total(3);
CALL sp_recalculate_order_total(4);

CREATE OR REPLACE VIEW vw_order_report AS
SELECT o.id AS order_id, u.name AS customer_name, p.name AS product_name,
       oi.quantity, oi.price, oi.quantity * oi.price AS subtotal, o.total, o.created_at
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
ORDER BY o.id;

CREATE OR REPLACE VIEW vw_total_gasto_por_cliente AS
SELECT u.name AS cliente, COUNT(o.id) AS total_pedidos, SUM(o.total) AS total_gasto
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id
ORDER BY total_gasto DESC;

CREATE OR REPLACE VIEW vw_produtos_nunca_vendidos AS
SELECT p.id, p.name, p.price, p.stock
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.id
WHERE oi.product_id IS NULL;

CREATE OR REPLACE VIEW vw_top_produtos_vendidos AS
SELECT p.name AS produto, SUM(oi.quantity) AS total_vendido, SUM(oi.quantity * oi.price) AS valor_total
FROM order_items oi
JOIN products p ON p.id = oi.product_id
GROUP BY p.id
ORDER BY total_vendido DESC;

DELIMITER //
CREATE TRIGGER trg_update_order_total
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    CALL sp_recalculate_order_total(NEW.order_id);
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_update_stock
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE products SET stock = stock - NEW.quantity WHERE id = NEW.product_id;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_prevent_negative_stock
BEFORE INSERT ON order_items
FOR EACH ROW
BEGIN
    DECLARE v_stock INT;
    SELECT stock INTO v_stock FROM products WHERE id = NEW.product_id;
    IF v_stock < NEW.quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Estoque insuficiente';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_update_order_total_on_update
AFTER UPDATE ON order_items
FOR EACH ROW
BEGIN
    CALL sp_recalculate_order_total(NEW.order_id);
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_restore_stock_on_delete
AFTER DELETE ON order_items
FOR EACH ROW
BEGIN
    UPDATE products SET stock = stock + OLD.quantity WHERE id = OLD.product_id;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_adjust_stock_on_update
BEFORE UPDATE ON order_items
FOR EACH ROW
BEGIN
    UPDATE products SET stock = stock + OLD.quantity - NEW.quantity WHERE id = NEW.product_id;
    IF (SELECT stock FROM products WHERE id = NEW.product_id) < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Estoque insuficiente após alteração';
    END IF;
END //
DELIMITER ;

CREATE TABLE IF NOT EXISTS orders_backup LIKE orders;

SET GLOBAL event_scheduler = ON;

DELIMITER $$
CREATE EVENT IF NOT EXISTS ev_backup_orders
ON SCHEDULE EVERY 1 DAY
DO
BEGIN
    INSERT INTO orders_backup SELECT * FROM orders;
END$$
DELIMITER ;
