-- Create database
CREATE DATABASE testdb;

-- Connect to the database
\c testdb;

-- Create the items table (if the app hasn't already created it)
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data
INSERT INTO items (name, description, price) VALUES
    ('Laptop', 'High-performance laptop with 16GB RAM', 1299.99),
    ('Smartphone', 'Latest model with 5G capabilities', 899.50),
    ('Headphones', 'Noise-cancelling wireless headphones', 249.99),
    ('Monitor', '27-inch 4K display', 399.00),
    ('Keyboard', 'Mechanical RGB keyboard', 129.95);