-- Relational Database Schema - Auto Parts System
-- David Jason Bowlby

-- CREATE TABLE IF NOT EXISTS name (
--    column name  data type CONSTRAINTS, 
-- );
-- IF NOT EXISTS prevents errors when creating an
-- already-existing table. It does NOT update its structure.
-- Use ALTER TABLE to add columns to existing tables.

-- REFERENCES is the shorter, column-level way to declare a FOREIGN KEY.
-- FOREIGN KEY (...) REFERENCES ... is the explicit, table-level way.
-- Both create a foreign-key relationship.


CREATE TABLE IF NOT EXISTS Part (  -- "IF NOT EXISTS" is a safety check to make sure the table doesn't already exist
    part_id INTEGER PRIMARY KEY,  -- use INTEGER and not INT for PRIMARY KEY this will automatically generate the ID when you insert a new part
    name TEXT NOT NULL,
    description TEXT, 
    price REAL NOT NULL CHECK (price >= 0),  -- REAL = SQL data type for floating point numbers
    category TEXT  -- does not need a coma since it's the last column 
);

CREATE TABLE IF NOT EXISTS Store (
    store_id INTEGER PRIMARY KEY,
    street_address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    zip TEXT NOT NULL,
    phone_number TEXT 
);

CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY,
    login TEXT UNIQUE NOT NULL,  -- "UNIQUE" = prevents duplicate values in a column
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Employee (
    employee_id INTEGER PRIMARY KEY,
    user_id INT UNIQUE NOT NULL REFERENCES User(user_id), -- REFERENCES table(primary key) syntax is a shortcut for FOREIGN KEY
    store_id INT NOT NULL REFERENCES Store(store_id), -- Foreign Key
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Customer (
    customer_id INTEGER PRIMARY KEY,
    user_id INT UNIQUE NOT NULL REFERENCES User(user_id), -- Foreign Key
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    phone_number TEXT
);

CREATE TABLE IF NOT EXISTS StoreInventory (
    store_id INTEGER NOT NULL REFERENCES Store(store_id), -- Foreign Key
    part_id INTEGER NOT NULL REFERENCES Part(part_id), -- Foreign Key
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),

    PRIMARY KEY (store_id, part_id)  -- correct syntax for a composite PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS "Order" (  -- use "..." because ORDER is a keyword ex. ORDER BY, this tells SQL it's not the keyword
    order_id INTEGER PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES Customer(customer_id), -- Foreign Key
    store_id INT NOT NULL REFERENCES Store(store_id), -- Foreign Key
    order_date TEXT,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS OrderItem (
    order_item_id INTEGER PRIMARY KEY,
    order_id INT NOT NULL REFERENCES "Order"(order_id), -- Foreign Key
    part_id INT NOT NULL REFERENCES Part(part_id),  -- Foreign Key
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0)
);



