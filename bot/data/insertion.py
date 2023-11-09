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

