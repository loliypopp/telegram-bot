import psycopg2 as sql
import aiogram

base = sql.connect(database='onlineshop', 
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