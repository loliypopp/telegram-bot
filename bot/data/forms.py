from aiogram.fsm.state import StatesGroup, State

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


class DeleteProductForm(StatesGroup):
    delete_uuid = State()