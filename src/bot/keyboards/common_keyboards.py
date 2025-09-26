from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Список команд")],
            [KeyboardButton(text="Добавить команду")],
            [KeyboardButton(text="Обновить команду"), KeyboardButton(text="Удалить команду")]
        ],
        resize_keyboard=True
    )

    return kb

def get_cancel_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Отмена")]
        ],
        resize_keyboard=True
    )

    return kb