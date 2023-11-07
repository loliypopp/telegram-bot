import psycopg2 as sql
from .settings import base, cursor


def update_product_by_uuid(uuid, name, price, category, brand, descr, quantity):
    global base, cursor
    try:
        cursor.execute(f'UPDATE products SET product_name=%s, price=%s, category_id=%s, brand_id=%s, descr =%s, stock_quantity =%s  WHERE uuid=%s;', (name, price, category, brand, descr, quantity, uuid))
        base.commit()
    except Exception as e:
        print('Ошибка при обновлении product:', str(e))


def delete_product_by_uuid(uuid):
    global base, cursor
    try:
        cursor.execute("DELETE from products WHERE uuid=%s", (uuid, ))
        base.commit()
    except Exception as e:
        print('Ошибка при удалении product:', str(e))



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
