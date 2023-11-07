import psycopg2 as sql
from .settings import base, cursor


def update_product_by_uuid(uuid, title, category, price):
    global base, cursor
    try:
        cursor.execute(f'UPDATE product SET title=%s, category=%s, price=%s WHERE id=%s;', (title, category, price, uuid))
        base.commit()
    except Exception as e:
        print('Ошибка при обновлении product:', str(e))


def delete_product_by_uuid(uuid):
    global base, cursor
    try:
        cursor.execute("DELETE from product WHERE id=%s", (uuid, ))
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
