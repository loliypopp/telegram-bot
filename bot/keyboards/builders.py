from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from data.selects import get_all_categories, get_all_brands

def main_kb():
    items = [
        'Обновить продукт', "Посмотреть продукты",
        'Посмотреть продукт', 'Удалить продукт',
        'Добавить продукт', 'Личный кабинет',
        'Корзина', 'Статистика заказов',
        'Добавить продукт в корзину', 'Отмена'
    ]
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in items]
    builder.adjust(2, 2, 2,2)

    return builder.as_markup(resize_keyboard=True)

def products_kb():
    items = [
        'Все продукты', '10 последних добавленных',
        'Все продукты определ. категории', 'Все продукты определ. бренда',
        'Назад'
    ]
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in items]
    builder.adjust(2,2,1)
    return builder.as_markup(resize_keyboard=True)


def categories_kb():
    categories = get_all_categories()
    if categories is not None:
        items = []
        for select in categories:
            items.append(select[0])
        builder = ReplyKeyboardBuilder()
        [builder.button(text=item) for item in items]
        return builder.as_markup(resize_keyboard=True)
    else:
        return
    

    

def brands_kb():
    brands = get_all_brands()
    if brands is not None:
        items = []
        for select in brands:
            items.append(select[0])
        builder = ReplyKeyboardBuilder()
        [builder.button(text=item) for item in items]
        return builder.as_markup(resize_keyboard=True)
    else:
        return



def order_kb():
    items = ['Заказать', 'Назад']
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in items]
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def update_kb():
    items = ['Обновить себя', 'Назад']
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in items]
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

    
