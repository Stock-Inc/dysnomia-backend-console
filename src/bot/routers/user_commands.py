from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.fsm import CommandsFSM
from src.bot.keyboards.common_keyboards import get_main_kb, get_cancel_kb
from src.database.requests import select_commands, insert_command


router = Router(name=__name__)

@router.message(F.text == "Список команд")
@router.message(Command("list"))
async def cmd_show(message: types.Message):
    commands = await select_commands()

    response = [
        f"Команды: ({len(commands)})", *[
            f"{cmd.name} {cmd.description} {cmd.result}" for cmd in commands
        ]
    ]

    return await message.answer(
        text="\n".join(response),
        reply_markup=get_main_kb(),
        disable_web_page_preview=True,
    )

@router.message(F.text == "Добавить команду")
@router.message(Command("add"))
async def cmd_add(message: types.Message, state: FSMContext):
    await state.set_state(CommandsFSM.WAITING_FOR_ADD_COMMAND)

    add_text = "Формат: <команда> <описание> <результат>"

    #command already exist
    ...

    return await message.answer(
        text=add_text,
        reply_markup=get_cancel_kb(),
        disable_web_page_preview=True
    )

@router.message(F.text == "Обновить команду")
@router.message(Command("update"))
async def cmd_update(message: types.Message, state: FSMContext):
    ...



@router.message(F.text == "Удалить команду")
async def cmd_delete(message: types.Message, state: FSMContext):
    ...

@router.message(F.text == "Отмена")
@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    if await state.get_state() is None:
        return None

    await state.clear()

    return await message.answer(
        text="Операция отменена",
        reply_markup=get_main_kb()
    )

@router.message(CommandsFSM.WAITING_FOR_ADD_COMMAND)
async def on_command_add(message: types.Message, state: FSMContext):
    text = [word.strip() for word in message.text.split(" ")]

    await insert_command(text[0], text[1], text[2])

    response = f"Команда <{text[0]}> успешно добавлена"

    await message.answer(
        text=response,
        reply_markup=get_main_kb(),
        disable_web_page_preview=True
    )

    await state.clear()