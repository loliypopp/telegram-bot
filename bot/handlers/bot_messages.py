from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Router
from aiogram.fsm.context import FSMContext
from data.settings import base, cursor
from aiogram import F
from keyboards.builders import *
from data.forms import *
from data.insertion import *
from data.selects import *


router = Router()

''' REQUEST STARTS '''


# CLIENT 







# c
@router.message(F.text.lower()=='добавить продукт')
async def add_product_script(message: Message, state: FSMContext):
    await state.set_state(AddProductForm.enter_name)
    await message.answer('Сценарий добавления продукта!\nВведи название продукта!')
    

# u
@router.message(F.text.lower()=='обновить продукт')
async def update_product_script(message: Message, state: FSMContext):
    await state.set_state(UpdateProductForm.uuid)
    await message.answer('Сценари изменения продукта!\nВведите название продукта которого вы хотите изменить!')

# r
@router.message(F.text.lower()=='посмотреть продукт')
async def product_details_script(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(FindTables.enter_product_name)
    await message.answer('Введите название продукта, которого\nвы хотите посмотреть!')


@router.message(F.text.lower()=='посмотреть продукты')
async def show_products_script(message: Message):
    await message.answer('Выбери что вы хотите вывести:', reply_markup=products_kb())

@router.message(F.text.lower()=='назад')
async def go_back_script(message: Message):
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







''' CREATION '''
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
    
    category = data['enter_category'].capitalize()
    brand = data['enter_brand'].capitalize()

    category = get_category_id_by_name(category)
    brand = get_brand_id_by_name(brand)


    
    descr = data['enter_descr']
    quantity = data['enter_quantity']
    


    await state.clear()
    value = (name, price, category, brand, descr, quantity)
    query = 'INSERT INTO products(product_name, price, category_id, brand_id, descr, stock_quantity) VALUES (%s, %s, %s, %s, %s, %s);'

    cursor.execute(query, value)
    base.commit()
    await message.answer(f'Товар добавлен успешно!\nTitle: - {name},  Price: - {price}, Category: - {category}, Brand: - {brand},\nDescription: - {descr}, Quantity: - {quantity} ', 
                         reply_markup=main_kb())








''' SHOW PRODUCT(S) '''
@router.message(FindTables.enter_product_name)
async def show_product(message: Message, state: FSMContext):
    data = await state.update_data(enter_product_name=message.text)
    name =  data['enter_product_name'].capitalize()

    uuid = get_product_id_by_name(name)
    value = get_product_by_uuid(uuid)
    print(value)
    name, price, category, brand, descr, quantity  = value[0]

    await message.answer(f'Title: - {name},  Price: - {price}, Category: - {category}, Brand: - {brand},\nDescription: - {descr}, Quantity: - {quantity}')


@router.message(F.text.lower()=='все продукты')
async def show_products_script(message: Message):
    data = get_all_products()
    count = 0

    for select in data:
        count+=1
        await message.answer(f'{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]}.')
        


@router.message(F.text.lower()=='10 последних добавленных')
async def show_last10_products_script(message: Message):
    data = get_last_ten_products()
    print(data)
    count = 0
    for select in data:
        count+=1
        await message.answer(f'{count}.\nUUID: - {select[0]}\nTitle: - {select[1]},\nPrice: - {select[2]},\nCategory: - {select[3]},\nBrand: - {select[4]},\nDescription: - {select[5]},\nQuantity: - {select[6]}.')
        







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

    

    name = data['edit_name'].capitalize()
    uuid = get_product_id_by_name(name)


    price = data['edit_price']
    
    category = data['edit_category'].capitalize()
    brand = data['edit_brand'].capitalize()

    category = get_category_id_by_name(category)
    brand = get_brand_id_by_name(brand)


    
    descr = data['edit_descr']
    quantity = data['edit_quantity']
    
    await state.clear()

    change = update_product_by_uuid(uuid, name, price, category, brand, descr, quantity)
    await message.answer('Продукт успешно обновлен!')





'''DELETE PRODUCT'''
@router.message(DeleteProductForm.delete_uuid)
async def delete_process(message: Message, state: FSMContext):
    data = await state.update_data(delete_uuid=message.text)
    uuid = data['delete_uuid']

    delete_product_by_uuid(uuid)
    await message.answer('Продукт успешно был удален!')

