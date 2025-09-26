from aiogram import types

from src.bot.keyboards.common_keyboards import get_cancel_kb

class InputValidator:
    @staticmethod
    async def is_add_valid(message: types.Message) -> bool:
        if "|" not in message.text or message.text.count("|") != 1:
            await message.answer(
                text="Используйте: <команда> <описание> | <результат>",
                reply_markup=get_cancel_kb(),
                disable_web_page_preview=True
            )
            return False

        command_desc, result = map(str.strip, message.text.split("|", 1))
        parts = command_desc.split(" ", 1)

        if len(parts) < 2 or not result:
            await message.answer(
                text="Используйте: <команда> <описание> | <результат>",
                reply_markup=get_cancel_kb(),
                disable_web_page_preview=True
            )
            return False

        return True

    @staticmethod
    async def is_update_valid(message: types.Message) -> bool:
        if "|" not in message.text or message.text.count("|") != 1:
            await message.answer(
                text="Используйте: <команда> <новое_описание> | <новый_результат>",
                reply_markup=get_cancel_kb(),
                disable_web_page_preview=True
            )
            return False

        command_desc, result = map(str.strip, message.text.split("|", 1))
        parts = command_desc.split(" ", 1)

        if len(parts) < 2 or not result:
            await message.answer(
                text="Используйте: <команда> <новое_описание> | <новый_результат>",
                reply_markup=get_cancel_kb(),
                disable_web_page_preview=True
            )
            return False

        return True