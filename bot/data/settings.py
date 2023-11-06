import psycopg2 as sql
import aiogram

base = sql.connect(database='onlineshopp', 
                   user='gaboom', 
                   host='localhost', 
                   password='0000')
cursor = base.cursor()



def get_product_id_by_name(product_name):
    global base, cursor
    try:
        cursor.execute("SELECT id FROM product WHERE title = %s;", (product_name, ))
        product_id = cursor.fetchone()
        if product_id:
            return product_id[0]
        else:
            return None
    except Exception as e:
        print('Ошибка при получении product_id:', str(e))


def get_product_by_uuid(uuid):
    global base, cursor
    try:
        cursor.execute("SELECT product.title, product.category, product.price FROM product WHERE id = %s;", (uuid, ))
        product = cursor.fetchall()
        return product
    except Exception as e:
        print('Ошибка при получении product:', str(e))



def update_product_by_uuid(uuid, title, category, price):
    global base, cursor
    try:
        cursor.execute(f'UPDATE product SET title=%s, category=%s, price=%s WHERE id=%s;', (title, category, price, uuid))
        base.commit()
    except Exception as e:
        print('Ошибка при обновлении product:', str(e))



def get_all_products():
    global base, cursor
    try:
        cursor.execute('SELECT product.title, product.category, product.price FROM product;')
        products = cursor.fetchall()
        return products
    except Exception as e:
        print('Ошибка при получении всех продуктов:', str(e))


def get_last_ten_products():
    global base, cursor
    try:
        cursor.execute('SELECT product.title, product.category, product.price FROM product;')
        products = cursor.fetchall()
        return products[-10::]
    except Exception as e:
        print('Ошибка при получении последних десяти продуктов:', str(e))



def delete_product_by_uuid(uuid):
    global base, cursor
    try:
        cursor.execute("DELETE from product WHERE id=%s", (uuid, ))
        base.commit()
    except Exception as e:
        print('Ошибка при удалении product:', str(e))



def get_all_categories():
    global base, cursor
    try:
        cursor.execute('SELECT categories.category_name FROM categories;')
        categories = cursor.fetchall()
        return categories
    except Exception as e:
        print('Ошибка при получении всех категорий:', str(e))


def inser_into_category(name):
    global base, cursor
    try:
        cursor.execute('INSERT INTO categories(category_name) VALUES(%s)', (name, ))
        base.commit()

    except Exception as e:
        print("Error inserting into category", str(e))


def inser_into_brands(name):
    global base, cursor
    try:
        cursor.execute('INSERT INTO brands(name) VALUES(%s)', (name, ))
        base.commit()

    except Exception as e:
        print("Error inserting into category", str(e))

def get_category_id_by_name(name):
    global base, cursor
    try:
        cursor.execute('SELECT category_id FROM categories WHERE category_name = %s', (name, ))
        category_id = cursor.fetchone()
        print(category_id)
        if category_id:
            return category_id[0]
        else:
            inser_into_category(name)
    except Exception as e:
        print('Ошибка при получении ID категории по имени:', str(e))



def get_brand_id_by_name(name):
    global base, cursor
    try:
        cursor.execute('SELECT brand_id FROM brands WHERE name = %s', (name, ))
        brand_id = cursor.fetchone()
        print(brand_id)
        if brand_id:
            return brand_id[0]
        else:
            inser_into_brands(name)
            
    except Exception as e:
        print('Ошибка при получении ID бренда по имени:', str(e))


def get_all_brands():
    global base, cursor
    try:
        cursor.execute('SELECT brands.name FROM brands;')
        brands = cursor.fetchall()
        return brands
    except Exception as e:
        print('Ошибка при получении всех брендов:', str(e))