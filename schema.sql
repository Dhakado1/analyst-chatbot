CREATE TABLE IF NOT EXISTS business_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    retailer VARCHAR(100),
    city VARCHAR(100),
    product VARCHAR(100),
    category VARCHAR(100),
    osa DECIMAL(5,2),
    sales DECIMAL(12,2),
    units_sold INT,
    date DATE
);

-- Sample Data
INSERT INTO business_data (retailer, city, product, category, osa, sales, units_sold, date) VALUES
('Blinkit', 'Mumbai', 'Amul Milk 500ml', 'Dairy', 87.40, 15000.00, 500, '2023-10-01'),
('Blinkit', 'Delhi', 'Amul Milk 500ml', 'Dairy', 84.90, 18000.00, 600, '2023-10-01'),
('Zepto', 'Mumbai', 'Amul Milk 500ml', 'Dairy', 90.10, 12000.00, 400, '2023-10-01'),
('Instamart', 'Mumbai', 'Amul Milk 500ml', 'Dairy', 85.50, 14000.00, 450, '2023-10-01'),
('Blinkit', 'Pune', 'Amul Milk 500ml', 'Dairy', 88.20, 10000.00, 300, '2023-10-01'),
('Zepto', 'Delhi', 'Britannia Bread', 'Bakery', 92.00, 8000.00, 200, '2023-10-01'),
('Blinkit', 'Bangalore', 'Nandini Milk 500ml', 'Dairy', 89.50, 25000.00, 1000, '2023-10-01'),
('Instamart', 'Hyderabad', 'Aashirvaad Atta 5kg', 'Staples', 95.00, 45000.00, 150, '2023-10-01')
ON DUPLICATE KEY UPDATE id=id;