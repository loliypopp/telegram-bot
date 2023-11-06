from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.context import FSMContext
from data.settings import base, cursor
from aiogram import F

router = Router()


class Product:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

    def get_data_for_insert_query(self):
        return (self.name, self.category, self.price)


class AddProductForm(StatesGroup):
    enter_name = State()
    enter_category = State()
    enter_price = State()


@router.message(F.text.lower()=='добавить продукт')
async def add_product_script(message: Message, state: FSMContext):
    await state.set_state(AddProductForm.enter_name)
    await message.answer('Сценарий добавления продукта!\nВведи название продукта!')


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
    await message.answer('Товар добавлен успешно!')