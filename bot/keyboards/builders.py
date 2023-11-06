from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_kb():
    items = [
        'Обновить продукт', "Посмотреть продукты", 
        'Посмотреть продукт', 'Удалить продукт',
        'Добавить продукт', 'Отмена'
    ]
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in items]
    builder.adjust(2,2,2)
    

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