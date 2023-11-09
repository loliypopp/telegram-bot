import psycopg2 as sql
from .settings import base, cursor
from .insertion import inser_into_brands, inser_into_category

def get_product_id_by_name(product_name):
    global base, cursor
    try:
        cursor.callproc('get_product_id_by_name', (product_name,))
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
        cursor.callproc('get_product_by_uuid', (uuid,))
        product = cursor.fetchall()
        return product
    except Exception as e:
        print('Ошибка при получении product:', str(e))



def get_all_products():
    global base, cursor
    try:
        cursor.callproc('get_all_products')
        products = cursor.fetchall()
        return products
    except Exception as e:
        print('Ошибка при получении всех продуктов:', str(e))


def get_last_ten_products():
    global base, cursor
    try:
        cursor.callproc('get_all_products')
        products = cursor.fetchall()
        return products[-10::]
    except Exception as e:
        print('Ошибка при получении последних десяти продуктов:', str(e))



def get_category_id_by_name(name):
    global base, cursor
    try:
        cursor.callproc('get_category_id_by_name', (name, ))
        category_id = cursor.fetchone()
        print(category_id)
        if category_id:
            return category_id[0]
        else:
            # Если категория не найдена, вставляем её в базу данных
            inser_into_category(name)
            # После вставки, повторно выполняем SELECT, чтобы получить ID
            cursor.callproc('get_category_id_by_name', (name, ))
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
        cursor.callproc('get_brand_id_by_name', (name, ))
        brand_id = cursor.fetchone()
        print(brand_id)
        if brand_id:
            return brand_id[0]
        else:
            inser_into_brands(name)
            cursor.callproc('get_brand_id_by_name', (name, ))
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
        cursor.callproc('get_all_brands')
        brands = cursor.fetchall()
        if not brands:
            base.commit()
            return None
        base.commit()
        return brands
    except Exception as e:
        print('Ошибка при получении всех брендов:', str(e))
        base.commit()
        return None


def get_all_categories():
    global base, cursor
    try:
        cursor.callproc('get_all_categories')
        categories = cursor.fetchall()
        if not categories:
            base.commit()
            return None
        base.commit()
        return categories
    except Exception as e:
        print('Ошибка при получении всех категорий:', str(e))
        base.commit()
        return None
    
    



def get_products_by_category(name):
    global base, cursor
    try:
        cursor.callproc('get_products_by_category', (name, ))
        products = cursor.fetchall()
        if not products:
            base.commit()
            return None
        base.commit()
        return products
    except Exception as e:
        print('Ошибка при получении товаров по категории:', str(e))
        base.commit()


def get_products_by_brands(name):
    global base, cursor
    try:
        cursor.callproc('get_products_by_brands', (name, ))
        products = cursor.fetchall()
        if not products:
            base.commit()
            return None
        base.commit()
        return products
    except Exception as e:
        print('Ошибка при получении товаров по бренду:', str(e))
        base.commit()


def get_user_info(chat_id):
    cursor.execute("SELECT name, phone, email, address FROM clients WHERE client_chat_id = %s", (str(chat_id),))
    user_info = cursor.fetchone()

    base.commit()

    return user_info


def get_user(chat_id):
    global base, cursor
    try:
        cursor.execute("SELECT client_chat_id FROM clients WHERE client_chat_id = %s;", (str(chat_id),))
        existing_user = cursor.fetchone()
        if existing_user:
            return existing_user
        else:
            return False

    except (Exception, sql.Error) as error:
        print("Ошибка при проверке существования пользователя в базе данных:", error)
        return False