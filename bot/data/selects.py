import psycopg2 as sql
from .settings import base, cursor
from .insertion import inser_into_brands, inser_into_category

def get_product_id_by_name(product_name):
    global base, cursor
    try:
        cursor.execute("SELECT uuid FROM products WHERE product_name = %s;", (product_name, ))
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

    
def get_category_id_by_name(name):
    global base, cursor
    try:
        cursor.execute('SELECT category_id FROM categories WHERE category_name = %s', (name, ))
        category_id = cursor.fetchone()
        print(category_id)
        if category_id:
            return category_id[0]
        else:
            # Если категория не найдена, вставляем её в базу данных
            inser_into_category(name)
            # После вставки, повторно выполняем SELECT, чтобы получить ID
            cursor.execute('SELECT category_id FROM categories WHERE category_name = %s', (name, ))
            category_id = cursor.fetchone()
            if category_id:
                return category_id[0]
            else:
                print('Категория не была найдена после вставки.')
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
            cursor.execute('SELECT brand_id FROM brands WHERE name = %s', (name, ))
            brand_id = cursor.fetchone()
            if brand_id:
                return brand_id[0]
            else:
                print('Категория не была найдена после вставки.')
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

def get_all_categories():
    global base, cursor
    try:
        cursor.execute('SELECT categories.category_name FROM categories;')
        categories = cursor.fetchall()
        return categories
    except Exception as e:
        print('Ошибка при получении всех категорий:', str(e))
