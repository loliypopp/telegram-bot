CREATE OR REPLACE FUNCTION get_product_id_by_name(p_name VARCHAR(255))
RETURNS UUID
AS $$
    SELECT uuid FROM products WHERE product_name = p_name LIMIT 1;
$$
LANGUAGE SQL;


-- get_product_by_uuid
CREATE OR REPLACE FUNCTION get_product_by_uuid(p_uuid UUID)
RETURNS TABLE (
    name VARCHAR(255),
    price DECIMAL(10, 2),
    category_id INT,
    brand_id INT,
    descr TEXT,
    stock_quantity INT
)
AS $$
    SELECT
        products.product_name,
        products.price,
        products.category_id,
        products.brand_id,
        products.descr,
        products.stock_quantity
    FROM
        products
    WHERE
        uuid = p_uuid;
$$
LANGUAGE SQL;


-- GET ALL PRODUCTS
CREATE OR REPLACE FUNCTION get_all_products()
RETURNS TABLE (
    product_uuid UUID,
    product_name VARCHAR(255),
    price DECIMAL(10, 2),
    category_name VARCHAR(255),
    brand_name VARCHAR(255),
    descr TEXT,
    stock_quantity INT
)
AS $$
    SELECT
        products.uuid AS product_uuid,
        products.product_name AS product_name,
        products.price,
        categories.category_name AS category_name,
        brands.name AS brand_name,
        products.descr,
        products.stock_quantity
    FROM
        products
    JOIN
        categories ON products.category_id = categories.category_id
    JOIN
        brands ON products.brand_id = brands.brand_id;
$$
LANGUAGE SQL;

-- get category_name_by_id
CREATE OR REPLACE FUNCTION get_category_name_by_id(p_category_id INT)
RETURNS VARCHAR(255)
AS $$
    SELECT category_name FROM categories WHERE category_id = p_category_id;
$$
LANGUAGE SQL;


-- get all brands
CREATE OR REPLACE FUNCTION get_all_brands()
RETURNS TABLE (name VARCHAR(255))
AS $$
    SELECT name FROM brands;
$$
LANGUAGE SQL;


-- get all categories
CREATE OR REPLACE FUNCTION get_all_categories()
RETURNS TABLE (name VARCHAR(255))
AS $$
    SELECT category_name FROM categories;
$$
LANGUAGE SQL;


-- get user info
CREATE OR REPLACE FUNCTION get_user_info(p_chat_id VARCHAR(255))
RETURNS TABLE (name VARCHAR(255), phone VARCHAR(255), email VARCHAR(255), address TEXT)
AS $$
    SELECT name, phone, email, address FROM clients WHERE client_chat_id = p_chat_id;
$$
LANGUAGE SQL;


-- get products by category
CREATE OR REPLACE FUNCTION get_products_by_category(p_name VARCHAR(255))
RETURNS TABLE (
    uuid UUID,
    name VARCHAR(255),
    price NUMERIC(10, 2),
    category_id INT,
    brand_id INT,
    descr TEXT,
    stock_quantity INT
)
AS $$
    SELECT 
        products.uuid, 
        products.product_name, 
        products.price, 
        products.category_id, 
        products.brand_id, 
        products.descr, 
        products.stock_quantity
    FROM 
        products 
    JOIN 
        categories ON products.category_id = categories.category_id
    WHERE 
        categories.category_name = p_name;
$$
LANGUAGE SQL;


-- get products by brands
CREATE OR REPLACE FUNCTION get_products_by_brands(p_name VARCHAR(255))
RETURNS TABLE (
    uuid UUID,
    name VARCHAR(255),
    price NUMERIC(10, 2),
    category_id INT,
    brand_id INT,
    descr TEXT,
    stock_quantity INT
)
AS $$
    SELECT 
        products.uuid, 
        products.product_name, 
        products.price, 
        products.category_id, 
        products.brand_id, 
        products.descr, 
        products.stock_quantity
    FROM 
        products 
    JOIN 
        brands ON products.brand_id = brands.brand_id
    WHERE 
        brands.name = p_name;
$$
LANGUAGE SQL;



-- get products by name
CREATE OR REPLACE FUNCTION get_product_by_name(p_product_name VARCHAR(255))
RETURNS TABLE (
    uuid UUID,
    product_name VARCHAR(255),
    price NUMERIC(10, 2),
    category_id INT,
    brand_id INT,
    descr TEXT,
    stock_quantity INT
)
AS $$
    SELECT 
        uuid, 
        product_name, 
        price, 
        category_id, 
        brand_id, 
        descr, 
        stock_quantity
    FROM 
        products 
    WHERE 
        product_name = p_product_name;
$$
LANGUAGE SQL;


-- get category id by name
CREATE OR REPLACE FUNCTION get_category_id_by_name(p_name VARCHAR(255))
RETURNS INT
AS $$
    SELECT category_id FROM categories WHERE category_name = p_name LIMIT 1;

$$
LANGUAGE SQL;



-- get brand id by name
CREATE OR REPLACE FUNCTION get_brand_id_by_name(p_name VARCHAR(255))
RETURNS INT
AS $$
    SELECT brand_id FROM brands WHERE name = p_name LIMIT 1;
$$
LANGUAGE SQL;

-- get_user
CREATE OR REPLACE FUNCTION get_user(chat_id VARCHAR) 
RETURNS TABLE(client_chat_id VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT client_chat_id FROM clients WHERE client_chat_id = chat_id;
END;
$$ LANGUAGE plpgsql;
