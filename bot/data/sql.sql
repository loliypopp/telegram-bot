CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE clients (
    client_id SERIAL PRIMARY KEY,
    client_chat_id VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    phone VARCHAR(255),
    email VARCHAR(255),
    address TEXT,
    cart_id INT
);

CREATE TABLE brands (
    brand_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE products (
    uuid UUID DEFAULT uuid_generate_v4(),
    product_name VARCHAR(255),
    price NUMERIC(10, 2),
    category_id INT,
    brand_id INT,
    descr TEXT,
    creation_date DATE,
    stock_quantity INT
);

CREATE TABLE cart (
    cart_id SERIAL PRIMARY KEY
);


CREATE TABLE cart_products (
    cart_id INT,
    product_uuid UUID,
    quantity INT,
    FOREIGN KEY (cart_id) REFERENCES cart(cart_id),
    FOREIGN KEY (product_uuid) REFERENCES products(uuid)
);


CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY
);