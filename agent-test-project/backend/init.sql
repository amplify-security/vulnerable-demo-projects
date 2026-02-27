CREATE TABLE IF NOT EXISTS juices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    juice_type ENUM('orange', 'apple') NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    in_stock BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO juices (name, description, juice_type, price, in_stock) VALUES
    ('Fresh Orange Squeeze', 'Freshly squeezed orange juice with pulp', 'orange', 4.99, TRUE),
    ('Apple Cider', 'Classic apple cider made from local apples', 'apple', 3.99, TRUE),
    ('Valencia Orange', 'Sweet Valencia orange juice', 'orange', 5.49, TRUE);
