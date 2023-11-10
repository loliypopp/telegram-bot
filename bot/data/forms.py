from aiogram.fsm.state import StatesGroup, State

class AddProductForm(StatesGroup):
    enter_name = State()
    enter_price = State()
    enter_category = State()
    enter_brand = State()
    enter_descr = State()
    enter_quantity = State()    


class UpdateProductForm(StatesGroup):
    uuid = State()
    edit_name = State()
    edit_price = State()
    edit_category = State()
    edit_brand = State()
    edit_descr = State()
    edit_quantity = State()  


class DeleteProductForm(StatesGroup):
    delete_uuid = State()


class FindTables(StatesGroup):
    enter_product_name= State()
    enter_category_name = State()
    enter_brand_name = State()


class UserState(StatesGroup):
    name = State()
    phone = State()
    email = State()
    address = State()


class UpdateUserState(StatesGroup):
    name = State()
    phone = State()
    email = State()
    address = State()

    