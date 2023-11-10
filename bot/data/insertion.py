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

def add_product_to_user_cart(cart_id, product_uuid):
    try:
        cursor.execute("INSERT INTO cart_products (cart_id, product_uuid, quantity) VALUES (%s, %s, 1);",
                       (cart_id, product_uuid))
        base.commit()
    except Exception as e:
        print('Ошибка при добавлении продукта в корзину пользователя:', str(e))

def create_user_cart(user_id):
    try:
        cursor.execute("INSERT INTO cart DEFAULT VALUES RETURNING cart_id;")
        cart_id = cursor.fetchone()[0]

        cursor.execute("UPDATE clients SET cart_id = %s WHERE client_chat_id = %s;", (cart_id, str(user_id)))
        base.commit()
        return cart_id
    except Exception as e:
        print('Ошибка при создании корзины пользователя:', str(e))
        return None



def user_exists(chat_id):
    global base, cursor
    try:

        cursor.execute("SELECT client_chat_id FROM clients WHERE client_chat_id = %s;", (str(chat_id),))
        existing_user = cursor.fetchone()
        print(existing_user)
        if existing_user:
            return True
            
        else:
            return False

    except (Exception, sql.Error) as error:
        print("Ошибка при проверке существования пользователя в базе данных:", error)
        return False
    

def insert_into_clien(client_chat_id,name, phone, email, address):
    try:

        cursor = base.cursor()

        insert_query = """INSERT INTO clients (client_chat_id, name, phone, email, address)
                                 VALUES (%s, %s, %s, %s, %s)"""

        record_to_insert = (client_chat_id,name, phone, email, address)

        cursor.execute(insert_query, record_to_insert)
        base.commit()
        print("Запись о пользователе успешно добавлена в базу данных")

    except (Exception, sql.Error) as error:
        print("Ошибка при добавлении записи о пользователе в базу данных:", error)


def update_product_by_uuid(uuid, name, price, category, brand, descr, quantity):
    global base, cursor
    try:
        cursor.execute(f'UPDATE products SET product_name=%s, price=%s, category_id=%s, brand_id=%s, descr =%s, stock_quantity =%s  WHERE uuid=%s;', (name, price, category, brand, descr, quantity, uuid))
        base.commit()
    except Exception as e:
        print('Ошибка при обновлении product:', str(e))




def update_user(chat_id, name, phone, email, address):
    global base, cursor
    try:
        cursor.execute("UPDATE clients SET name = %s, phone = %s, email = %s, address = %s WHERE client_chat_id = %s;", (name, phone, email, address, chat_id))
    except Exception as e:
        print('Ошибка при обновлении user:', str(e))



def insert_into_order(client_id):
    global base, cursor
    try:
        cursor.execute('INSERT INTO orderss (client_id) VALUES (%s);', (client_id, ))
        base.commit()
    except Exception as e:
        print('Ошибка при создании нового ордера:', str(e))




def cart_to_fart_transfer(cart_id):
    global base, cursor
    try:
        cursor.execute('SELECT product_uuid FROM cart_products WHERE cart_id = %s;', (cart_id, ))
        tupl = cursor.fetchone()
        print(tupl)
        # cursor.execute('INSERT INTO orders_products (order_id, product_id) SELECT order_id, product_id FROM cart_products WHERE cart_id = %s;', (cart_id, ))
        base.commit()
    except Exception as e:
        print('Ошибка при переводе корзины в фарт:', str(e))


def clear_cart(cart_id):
    global base, cursor
    try:
        cursor.execute('DELETE FROM cart WHERE cart_id = %s;', (cart_id, ))
        base.commit()
    except Exception as e:
        print('Ошибка при удалении всех товаров из корзины:', str(e))