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