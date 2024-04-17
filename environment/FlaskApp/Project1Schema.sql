-- Create ProjectOneStore database
CREATE DATABASE IF NOT EXISTS ProjectOneStore;
USE ProjectOneStore;

-- Create Category table
CREATE TABLE IF NOT EXISTS Category (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

-- Create inventory table
CREATE TABLE IF NOT EXISTS Inventory (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255),
    price FLOAT,
    categoryID INT,
    FOREIGN KEY (categoryID) REFERENCES Category(CategoryID),
    CONSTRAINT fk_inventory_category FOREIGN KEY (categoryID) REFERENCES Category(CategoryID) -- Unique foreign key constraint name
);

-- Populate Category table
INSERT INTO Category (name) VALUES
('toys'),
('kitchen'),
('furniture');

-- Populate inventory table with 10 different examples
INSERT INTO Inventory (description, price, categoryID) VALUES
('Toy 1', 10.50, 1),
('Toy 2', 15.75, 1),
('Kitchen Item 1', 20.00, 2),
('Kitchen Item 2', 25.50, 2),
('Furniture Item 1', 100.00, 3),
('Furniture Item 2', 150.00, 3),
('Toy 3', 12.25, 1),
('Kitchen Item 3', 22.75, 2),
('Furniture Item 3', 125.00, 3),
('Toy 4', 18.99, 1);

