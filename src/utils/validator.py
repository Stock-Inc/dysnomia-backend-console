from aiogram import types

from src.bot.keyboards.common_keyboards import get_cancel_kb


class InputValidator:
    @staticmethod
    async def is_valid(message: types.Message) -> bool:
        user_input = message.text.split(" ", 2)
        answer_text = "Следуйте формату"
        if len(user_input) < 3:
            await message.answer(
                text=answer_text,
                reply_markup=get_cancel_kb(),
                disable_web_page_preview=True
            )
            return False
        return True