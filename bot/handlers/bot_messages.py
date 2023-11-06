from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from data.settings import base, cursor, get_product_id_by_name, get_product_by_uuid, update_product_by_uuid
from aiogram import F


router = Router()


class AddProductForm(StatesGroup):
    enter_name = State()
    enter_category = State()
    enter_price = State()


class UpdateProductForm(StatesGroup):
    uuid = State()
    edit_name = State()
    edit_category = State()
    edit_price = State()


class FindTables(StatesGroup):
    enter_product_name= State()


''' REQUEST STARTS '''
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



''' CREATION '''
@router.message(AddProductForm.enter_name)
async def process_product_name(message: Message, state: FSMContext):
   
    await state.update_data(enter_name=message.text)
    await state.set_state(AddProductForm.enter_category)
    await message.answer(
        'Отлично!\nТеперь напиши категорию товаров:'
    )

@router.message(AddProductForm.enter_category)
async def process_product_category(message: Message, state: FSMContext):
    await state.update_data(enter_category=message.text)
    await state.set_state(AddProductForm.enter_price)
    await message.answer(
        'Отлично!\nТеперь укажи цену на товар!'
    )
@router.message(AddProductForm.enter_price)
async def process_commit(message: Message, state: FSMContext):


    data = await state.update_data(enter_price=int(message.text))

    name = data['enter_name']
    category = data['enter_category']
    price = data['enter_price']

    await state.clear()
    value = (name, category, price)
    query = 'INSERT INTO product(title, category, price) VALUES (%s, %s, %s);'

    cursor.execute(query, value)
    base.commit()
    await message.answer(f'Товар добавлен успешно!\nTitle: {name} - Category: {category} - Price: {price}')



''' SHOW PRODUCT(S) '''
@router.message(FindTables.enter_product_name)
async def show_product(message: Message, state: FSMContext):
    data = await state.update_data(enter_product_name=message.text)
    name =  data['enter_product_name'].capitalize()

    uuid = get_product_id_by_name(name)
    value = get_product_by_uuid(uuid)
    print(value)
    title, category, price = value[0]

    await message.answer(f'Вот данные о продукте\n\nНазвание: {title}\nКатегория:{category}\nЦена:{price}')


''' UPDATE PRODUCT '''
@router.message(UpdateProductForm.uuid)
async def find_product_procces(message: Message, state: FSMContext):
    await state.update_data(uuid=message.text)
    await state.set_state(UpdateProductForm.edit_name)
    await message.answer('Укажи новый заголовок для товара!')

@router.message(UpdateProductForm.edit_name)
async def edit_name_proccess(message: Message, state: FSMContext):
    await state.update_data(edit_name=message.text)
    await state.set_state(UpdateProductForm.edit_category)
    await message.answer('Укажи новую категорию товара!')

@router.message(UpdateProductForm.edit_category)
async def edit_category_proccess(message: Message, state: FSMContext):
    await state.update_data(edit_category = message.text)
    await state.set_state(UpdateProductForm.edit_price)
    await message.answer('Укажи новую цену товара!')


@router.message(UpdateProductForm.edit_price)
async def proccess_commit_update(message: Message, state: FSMContext):
    data = await state.update_data(edit_price = int(message.text))
      
    uuid = data['uuid'].capitalize()
    uuid = get_product_id_by_name(uuid)

    title,category,price = data['edit_name'], data['edit_category'], data['edit_price'] 

    change = update_product_by_uuid(uuid, title, category, price)
    
    print(change)
    state.clear()
    await message.answer('Продукт успешно обновлен!')