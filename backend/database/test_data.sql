-- Auto Parts System
-- Sample data for databse testing 

PRAGMA foreign_keys = ON; -- Enforces foreign key relationships, preventing records from referencing nonexistent parent records.

-- Temporary Information for testing -- 

-- Part Info -- 

INSERT OR IGNORE INTO Part (part_id, name, description, price, category)
VALUES (1, 'Oil Filter', 'Engine oil filter', 12.99, 'Filters'); 

INSERT OR IGNORE INTO Part (part_id, name, description, price, category)
VALUES (2, 'Brake Pads', 'Front ceramic brake pads', 49.99, 'Brakes');

-- Store Info -- 

INSERT OR IGNORE INTO Store (store_id, street_address, city, state, zip, phone_number)
VALUES (1, '123 Main Street', 'Fort Worth', 'TX', '76102', 8175550001);

INSERT OR IGNORE INTO Store (store_id, street_address, city, state, zip, phone_number)
VALUES (2, '123 Main Street', 'Denton', 'TX', '76201', '940-555-0102');

INSERT OR IGNORE INTO StoreInventory (
    store_id, part_id, stock_quantity
)
VALUES
    (2, 1, 35),
    (2, 2, 15);

-- User Info -- 

INSERT OR IGNORE INTO User (user_id, email, password_hash, fname, lname, phone_number)
VALUES (1, 'JohnDoe@yahoo.com', 'demo_hash_customer_001', 'John', 'Doe', '8175551000');

INSERT OR IGNORE INTO User (user_id, email, password_hash, fname, lname, phone_number)
VALUES (2, 'JaneDoe@yahoo.com', 'demo_hash_customer_002', 'Jane', 'Doe', '8175551001');

INSERT OR IGNORE INTO User (user_id, email, password_hash, fname, lname, phone_number)
VALUES (3, 'manager@test.com', 'demo_hash_employee_003', 'Test', 'Manager', '8175551002');

-- Customer Info -- 

INSERT OR IGNORE INTO Customer (customer_id, user_id)
VALUES (1, 1);

INSERT OR IGNORE INTO Customer (customer_id, user_id)
VALUES (2, 2);

-- Employee Info -- 

INSERT OR IGNORE INTO Employee (employee_id, user_id, store_id)
VALUES (1, 3, 1);

-- Store Inventory Info --

INSERT OR IGNORE INTO StoreInventory (store_id, part_id, stock_quantity)
VALUES (1, 1, 25);

INSERT OR IGNORE INTO StoreInventory (store_id, part_id, stock_quantity)
VALUES (1, 2, 15);

INSERT OR IGNORE INTO StoreInventory (store_id, part_id, stock_quantity)
VALUES (2, 1, 35), (2, 2, 5);

-- Order Info -- 

INSERT OR IGNORE INTO "Order" (order_id, customer_id, store_id, order_date, status)
VALUES (1,1,1, '2026-10-20', 'Pending'); -- Order #1 for John Doe(customer_id = 1) at Store #1

-- OrderItem Info --

INSERT OR IGNORE INTO OrderItem (order_item_id, order_id, part_id, quantity, unit_price)
VALUES (1, 1, 1, 2, 12.99);  --- Order #1 for John Doe contains 2 Oil Filters at $12.99 each.

INSERT OR IGNORE INTO OrderItem (order_item_id, order_id, part_id, quantity, unit_price)
VALUES (2, 1, 2, 1, 49.99); -- Order #1 for John Doe contains 1 set of Brake Pads at $49.99.

