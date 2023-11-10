from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router
from aiogram.fsm.context import FSMContext
from data.settings import base, cursor
from aiogram import F
from keyboards.builders import *
from data.forms import *
from data.insertion import *
from data.selects import *
from aiogram.filters import CommandStart

router = Router()

''' REQUEST STARTS '''


# CLIENT 
@router.message(CommandStart())
async def add_user(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    print(chat_id)
    await message.answer(f"Привет!, @{message.from_user.username}\nЭто Онлайн-магазин продуктов, что хотите сделать?",
                         reply_markup=main_kb())
    if user_exists(str(chat_id)):
        await message.answer("Вы уже зарегистрированы в системе.")
    else:
        await state.set_state(UserState.name)
        await message.answer(f"Доувай регатся\nЕсли ты не хочешь то просто пиши пропустит\nВведи своё имя")
        



@router.message(F.text.lower() == 'пропустить')
async def skip(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы решили не регатся попуск', reply_markup=main_kb())


# c
@router.message(F.text.lower()=='добавить продукт')
async def add_product_script(message: Message, state: FSMContext):
    await state.set_state(AddProductForm.enter_name)
    await message.answer('Сценарий добавления продукта!\nВведи название продукта!')
    

# u
@router.message(F.text.lower()=='обновить продукт')
async def update_product_script(message: Message, state: FSMContext):
    await state.clear()
    products = get_all_products()
    count = 0

    for select in products:
        count+=1
        await message.answer(f'{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]}')
    await state.set_state(UpdateProductForm.uuid)
    await message.answer('Сценари изменения продукта!\nВведите UUID продукта которого вы хотите изменить!')


# r
@router.message(F.text.lower()=='посмотреть продукт')
async def product_details_script(message: Message, state: FSMContext):
    await state.clear()
    data = get_all_products()
    count = 0

    for select in data:
        count+=1
        await message.answer(f'{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]}')
    await state.set_state(FindTables.enter_product_name)
    await message.answer('Введите UUID продукта, которого\nвы хотите посмотреть!')


@router.message(F.text.lower()=='посмотреть продукты')
async def show_products_script(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Выбери что вы хотите вывести:', reply_markup=products_kb())

@router.message(F.text.lower()=='назад')
async def go_back_script(message: Message, state: FSMContext):
     await state.clear()
     await message.answer(f"@{message.from_user.username} - вы вернулись назад,\n что хотите сделать?", reply_markup=main_kb())


# d
@router.message(F.text.lower()=='удалить продукт')
async def del_product_script(message: Message, state: FSMContext):
    products = get_all_products()
    count = 0
    print(products)
    for select in products:
        count+=1
        await message.answer(f'{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]} ')
  
    await state.set_state(DeleteProductForm.delete_uuid)
    await message.answer('Укажи UUID товара которого хотите удалить!')


# orders
@router.message(F.text.lower() == 'статистика заказов')
async def order_statistics(message:Message):
    products = get_products_in_orders()
    count = 0
    if  products is not None:
        await message.answer('Вот ваши заказы', reply_markup=order_kb())
        for select in products:
            count+=1
            await message.answer(f"{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]}", reply_markup=main_kb())
    else:

        await message.answer('Заказов нет', reply_markup=main_kb())




# cart
@router.message(F.text.lower() == 'корзина')
async def order_order_scripts(message: Message, ):
    
    products = get_products_in_cart()
    count = 0
    if  products is not None:
        await message.answer('Вот ваши продукты', reply_markup=order_kb())
        for select in products:
            count+=1
            await message.answer(f"{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]}")
        await message.answer('Хотите заказать?')
    else:

        await message.answer('Корзина пустая', reply_markup=main_kb())


@router.message(F.text.lower() == 'заказать')
async def order_order_start(message:Message, state: FSMContext):
    if user_exists(str(message.from_user.id)):
        chat_id = str(message.from_user.id)
        client_id = get_client_id_by_chat_id(chat_id)

        order_id = insert_into_order(client_id)
        cart_id = get_user_cart_id(chat_id)
        cart_to_fart_transfer(cart_id, order_id)
        clear_cart(cart_id)

        await message.answer("Заказ создан", reply_markup=main_kb())
    else:
        await state.set_state(UserCartState.name)
        await message.answer('Вы не регестрированы\nВведите имя')


@router.message(UserCartState.name)
async def process_user_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserCartState.phone)
    await message.answer(
        'теперь введи свой номер телефона'
    )


@router.message(UserCartState.phone)
async def process_user_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(UserCartState.email)
    await message.answer(
        'теперь введи свой email телефона')


@router.message(UserCartState.email)
async def process_user_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(UserCartState.address)
    await message.answer(
        'теперь введи свой адресс ')


@router.message(UserCartState.address)
async def prcess_user_address(message: Message, state: FSMContext):
    data = await state.update_data(address=message.text)
    chat_id = message.chat.id
    name = data['name']
    phone = data['phone']
    email = data['email']
    address = data['address']
    await state.clear()
    insert_into_clien(str(chat_id),name, phone, email, address)
    if insert_into_clien:
        await message.answer('Успешно зарегался чел')
        if user_exists(str(message.from_user.id)):
            chat_id = str(message.from_user.id)
            client_id = get_client_id_by_chat_id(chat_id)

            order_id = insert_into_order(client_id)
            cart_id = get_user_cart_id(chat_id)
            cart_to_fart_transfer(cart_id, order_id)
            clear_cart(cart_id)

            await message.answer("Заказ создан", reply_markup=main_kb())
    else:
        await message.answer('Ошибка при регистрации')








"""CLIENT"""
@router.message(F.text =='Личный кабинет')
async def personal_area(message: Message):
    chat_id = message.from_user.id
    user_info = get_user_info(chat_id)

    if user_info:
        user_name = user_info[0]
        user_phone = user_info[1]
        user_email = user_info[2]
        user_address = user_info[3]

        response_message = f"Имя: {user_name}\nТелефон: {user_phone}\nEmail: {user_email}\nАдрес: {user_address}"
        await message.answer(response_message, reply_markup=update_kb())
    else:
        await message.answer("Пользователь не найден.")






@router.message(F.text.lower()=='обновить себя')
async def update_client_script(message: Message, state: FSMContext):
    await state.set_state(UpdateUserState.name)
    await message.answer('Введи новое свое название(СЛАВА СССР)')


@router.message(UpdateUserState.name)
async def update_client_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UpdateUserState.phone)
    await message.answer('Введи новый свой номер телефона(СЛАВА СССР)')



@router.message(UpdateUserState.phone)
async def update_client_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(UpdateUserState.email)
    await message.answer('Введи новый свой эмейл(СЛАВА СССР)')


@router.message(UpdateUserState.email)
async def update_client_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(UpdateUserState.address)
    await message.answer('Введи новый свой адрес(СЛАВА СССР)')

@router.message(UpdateUserState.address)
async def update_client_proccess(message: Message, state: FSMContext):
    await state.update_data(chat_id = message.from_user.id)
    data = await state.update_data(address = message.text)
    
    chat_id = data['chat_id']
    name = data['name']
    phone = data['phone']
    email = data['email']
    address = data['address']
    
    get_user(str(chat_id))
    update_user(str(chat_id), name, phone, email, address)
    await state.clear()
    await message.answer('Ты успешно обновился!!!', reply_markup=main_kb())



@router.message(UserState.name)
async def process_user_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UserState.phone)
    await message.answer(
        'теперь введи свой номер телефона'
    )


@router.message(UserState.phone)
async def process_user_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(UserState.email)
    await message.answer(
        'теперь введи свой email телефона')


@router.message(UserState.email)
async def process_user_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(UserState.address)
    await message.answer(
        'теперь введи свой адресс ')


@router.message(UserState.address)
async def prcess_user_address(message: Message, state: FSMContext):
    data = await state.update_data(address=message.text)
    chat_id = message.chat.id
    name = data['name']
    phone = data['phone']
    email = data['email']
    address = data['address']
    await state.clear()
    insert_into_clien(str(chat_id),name, phone, email, address)
    if insert_into_clien:
        await message.answer('Успешно зарегался чел')

@router.message(F.text.lower() == 'пропустить')
async def skip(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы решили не регатся попуск', reply_markup=main_kb())


''' CREATION '''
@router.message(F.text.lower() == 'добавить продукт в корзину')
async def add_product_to_cart_script(message:Message):
    data = get_all_products()
    count = 0

    for select in data:
        count+=1
        await message.answer(f'{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]}.')
    await message.answer('Если хотите добавить продукт в корзину\nНапишите:"Добавить {Название продукта}"')


@router.message(F.text.startswith('добавить'))
async def add_product_to_cart(message: Message, state: FSMContext):
    product_name = message.text[8:].strip().capitalize()

    product = get_product_by_name(product_name)

    if product:

        user_id = message.from_user.id
        cart_id = get_user_cart_id(user_id)

        if not cart_id:
            create_user_cart(user_id)

            cart_id = get_user_cart_id(user_id)

        add_product_to_user_cart(cart_id, product['uuid'])

        await message.answer(f'Продукт "{product_name}" добавлен в вашу корзину.')
    else:
        await message.answer(f'Продукт "{product_name}" не найден.')




@router.message(AddProductForm.enter_name)
async def process_product_name(message: Message, state: FSMContext):
   
    await state.update_data(enter_name=message.text)
    await state.set_state(AddProductForm.enter_price)
    await message.answer(
        'Отлично!\nТеперь укажи цену на товар!:'
    )


@router.message(AddProductForm.enter_price)
async def process_product_price(message: Message, state: FSMContext):
    await state.update_data(enter_price=int(message.text))
    await state.set_state(AddProductForm.enter_category)
    await message.answer(
        'Отлично!\nТеперь выберите категорию товаров!', reply_markup=categories_kb()
    )


@router.message(AddProductForm.enter_category)
async def process_product_category(message: Message, state: FSMContext):
    await state.update_data(enter_category=message.text)
    await state.set_state(AddProductForm.enter_brand)
    await message.answer(
        'Отлично!\nТеперь выберите бренд товара!', reply_markup=brands_kb()
    )

@router.message(AddProductForm.enter_brand)
async def process_product_category(message: Message, state: FSMContext):
    await state.update_data(enter_brand=message.text)
    await state.set_state(AddProductForm.enter_descr)
    await message.answer(
        'Отлично!\nТеперь напишите описание товара!', reply_markup=ReplyKeyboardRemove()
    )

@router.message(AddProductForm.enter_descr)
async def process_product_category(message: Message, state: FSMContext):
    await state.update_data(enter_descr=message.text)
    await state.set_state(AddProductForm.enter_quantity)
    await message.answer(
        'Отлично!\nТеперь количество товара!'
    )


@router.message(AddProductForm.enter_quantity)
async def process_commit(message: Message, state: FSMContext):
    data = await state.update_data(enter_quantity=int(message.text))

    name = data['enter_name'].capitalize()
    price = data['enter_price']

    category_name = data['enter_category'].capitalize()
    brand_name = data['enter_brand'].capitalize()

    try:
        category_id = get_category_id_by_name(category_name)
        brand_id = get_brand_id_by_name(brand_name)
        if category_id is None:
            inser_into_category(category_name)
            category_id = get_category_id_by_name(category_name)
        if brand_id is None:
            inser_into_brands(brand_name)
            brand_id = get_brand_id_by_name(brand_name)
        descr = data['enter_descr']
        quantity = data['enter_quantity']

        await state.clear()
        value = (name, price, category_id, brand_id, descr, quantity)
        query = 'INSERT INTO products(product_name, price, category_id, brand_id, descr, stock_quantity) VALUES (%s, %s, %s, %s, %s, %s);'

        cursor.execute(query, value)
        base.commit()
        await message.answer(
            f'Товар добавлен успешно!\nTitle: - {name},  Price: - {price}, Category: - {category_name}, Brand: - {brand_name},\nDescription: - {descr}, Quantity: - {quantity} ',
            reply_markup=main_kb())

    except Exception as e:

        base.rollback()
        print(f"Ошибка при добавлении продукта: {str(e)}")
        await message.answer("Произошла ошибка при добавлении продукта. Пожалуйста, попробуйте еще раз.")






''' SHOW PRODUCT(S) '''
@router.message(FindTables.enter_product_name)
async def show_product(message: Message, state: FSMContext):
    data = await state.update_data(enter_product_name=message.text)
    name =  data['enter_product_name']
    await state.clear()
    value = get_product_by_uuid(name)

    name, price, category, brand, descr, quantity  = value[0]
    
    await message.answer(f'PRODUCT DETAILS:\nTitle: - {name},\nPrice: - {price},\nCategory: - {category},\nBrand: - {brand},\nDescription: - {descr},\nQuantity: - {quantity}')
    await message.answer('Что вы хотите сделать?', reply_markup=main_kb()) 


@router.message(F.text.lower()=='все продукты')
async def show_products_script(message: Message, state: FSMContext):
    await state.clear()
    data = get_all_products()
    count = 0

    for select in data:
        count+=1
        await message.answer(f'{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]}.')
    await message.answer('Что вы хотите сделать?', reply_markup=main_kb())    


@router.message(F.text.lower()=='10 последних добавленных')
async def show_last10_products_script(message: Message, state: FSMContext):
    await state.clear()
    data = get_last_ten_products()
    print(data)
    count = 0
    for select in data:
        count+=1
        await message.answer(f'{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]}.')
    await message.answer('Что вы хотите сделать?', reply_markup=main_kb())  




@router.message(F.text.lower()=='все продукты определ. категории')
async def show_products_by_category(message: Message, state: FSMContext):
    data = get_all_categories()
    count = 0
    if data is not None:
        for select in data:
            count +=1
            await message.answer(f'{count}.\nTitle: {select[0]}')
        await state.set_state(FindTables.enter_category_name)
        await message.answer('Введите название категории по которому вы хотите получить продукты!')
    else:
        await message.answer('Нет категорий')
        await state.clear()
    



@router.message(FindTables.enter_category_name)
async def proccess_products_by_category(message: Message, state: FSMContext):
    data = await state.update_data(name=message.text)
    name = data['name']
    
    products = get_products_by_category(name)
    count = 0
    await state.clear()
    if products is not None:
        for select in products:
            count+=1
            await message.answer(f'{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]}.')
    else:
        await message.answer('По данному категорию товаров не существует.')
    await message.answer('Что вы хотите сделать?', reply_markup=main_kb())  




@router.message(F.text.lower()=='все продукты определ. бренда')
async def show_products_by_brand(message: Message, state: FSMContext):
    await state.clear()
    data = get_all_brands()
    count = 0
    
    for select in data:
        count +=1
        await message.answer(f'{count}.\nTitle: {select[0]}')
    await state.set_state(FindTables.enter_brand_name)
    await message.answer('Введите название бренда по которому вы хотите получить продукты!')



@router.message(FindTables.enter_brand_name)
async def proccess_products_by_brand(message: Message, state: FSMContext):
    data = await state.update_data(name=message.text)
    name = data['name']
    products = get_products_by_brands(name)
    count = 0
    if products is not None:
        for select in products:
            count+=1
            await message.answer(f'{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]}.')
    else:
        await message.answer('По данному бренду товаров не существует.')
    await message.answer('Что вы хотите сделать?', reply_markup=main_kb())  
    await state.clear()





''' UPDATE PRODUCT '''
@router.message(UpdateProductForm.uuid)
async def find_product_procces(message: Message, state: FSMContext):
    await state.update_data(uuid=message.text)
    await state.set_state(UpdateProductForm.edit_name)
    await message.answer('Укажи новый заголовок для товара!')


@router.message(UpdateProductForm.edit_name)
async def edit_name_proccess(message: Message, state: FSMContext):
    await state.update_data(edit_name=message.text)
    await state.set_state(UpdateProductForm.edit_price)
    await message.answer('Укажи новую цену товара!')


@router.message(UpdateProductForm.edit_price)
async def edit_category_proccess(message: Message, state: FSMContext):
    await state.update_data(edit_price = int(message.text))
    await state.set_state(UpdateProductForm.edit_category)
    await message.answer('Укажи новую категорию товара!', reply_markup=categories_kb())


@router.message(UpdateProductForm.edit_category)
async def edit_category_proccess(message: Message, state: FSMContext):
    await state.update_data(edit_category = message.text)
    await state.set_state(UpdateProductForm.edit_brand)
    await message.answer('Укажи новый бренд товара!', reply_markup=brands_kb())

@router.message(UpdateProductForm.edit_brand)
async def edit_category_proccess(message: Message, state: FSMContext):
    await state.update_data(edit_brand = message.text)
    await state.set_state(UpdateProductForm.edit_descr)
    await message.answer('Укажи новое описание товара!', reply_markup=ReplyKeyboardRemove())


@router.message(UpdateProductForm.edit_descr)
async def edit_category_proccess(message: Message, state: FSMContext):
    await state.update_data(edit_descr = message.text)
    await state.set_state(UpdateProductForm.edit_quantity)
    await message.answer('Укажи новое количество товаров!')


@router.message(UpdateProductForm.edit_quantity)
async def proccess_commit_update(message: Message, state: FSMContext):
    data = await state.update_data(edit_quantity = int(message.text))

    uuid = data['uuid']
    name = data['edit_name'].capitalize()
    price = data['edit_price']
    
    category = data['edit_category'].capitalize()
    brand = data['edit_brand'].capitalize()

    category = get_category_id_by_name(category)
    brand = get_brand_id_by_name(brand)


    
    descr = data['edit_descr']
    quantity = data['edit_quantity']
    
    await state.clear()

    update_product_by_uuid(uuid, name, price, category, brand, descr, quantity)
    await message.answer('Продукт успешно обновлен!', reply_markup=main_kb())





'''DELETE PRODUCT'''
@router.message(DeleteProductForm.delete_uuid)
async def delete_process(message: Message, state: FSMContext):
    data = await state.update_data(delete_uuid=message.text)
    uuid = data['delete_uuid']
    await state.clear()
    delete_product_by_uuid(uuid)
    await message.answer('Продукт успешно был удален!')

