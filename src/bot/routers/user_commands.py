from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.utils.validator import InputValidator
from src.bot.fsm import CommandsFSM
from src.bot.keyboards.common_keyboards import get_main_kb, get_cancel_kb
from src.database.requests import select_one_command, select_commands
from src.database.requests import insert_command, delete_command, update_command


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

    return await message.answer(
        text=add_text,
        reply_markup=get_cancel_kb(),
        disable_web_page_preview=True
    )

@router.message(F.text == "Обновить команду")
@router.message(Command("update"))
async def cmd_update(message: types.Message, state: FSMContext):
    await state.set_state(CommandsFSM.WAITING_FOR_UPDATE_COMMAND)

    update_text = "Формат: <название команды> <новое описание> <новый результат>"

    await message.answer(
        text=update_text,
        reply_markup=get_cancel_kb(),
        disable_web_page_preview=True
    )



@router.message(F.text == "Удалить команду")
@router.message(Command("delete"))
async def cmd_delete(message: types.Message, state: FSMContext):
    await state.set_state(CommandsFSM.WAITING_FOR_DELETE_COMMAND)

    delete_text = "Формат: <название команды>"

    await message.answer(
        text=delete_text,
        reply_markup=get_cancel_kb(),
        disable_web_page_preview=True
    )

@router.message(F.text == "Отмена")
@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()

    return await message.answer(
        text="Операция отменена",
        reply_markup=get_main_kb()
    )

@router.message(CommandsFSM.WAITING_FOR_ADD_COMMAND)
async def on_command_add(message: types.Message, state: FSMContext):
    if not await InputValidator.is_valid(message):
        return

    command, description, result = map(str.strip, message.text.split(" ", 2))

    if await select_one_command(command) is not None:
        await message.answer(
            text="Команда с таким именем уже существует!",
            reply_markup=get_cancel_kb(),
            disable_web_page_preview=True
        )
        return await state.set_state(CommandsFSM.WAITING_FOR_ADD_COMMAND)
    else:
        await insert_command(command, description, result)

        response = f"Команда <{command}> успешно добавлена"

        await message.answer(
            text=response,
            reply_markup=get_main_kb(),
            disable_web_page_preview=True
        )

    return await state.clear()

@router.message(CommandsFSM.WAITING_FOR_UPDATE_COMMAND)
async def on_command_update(message: types.Message, state: FSMContext):
    if not await InputValidator.is_valid(message):
        return

    command, n_description, n_result = map(str.strip, message.text.split(" ", 2))

    if await select_one_command(command) is None:
        await message.answer(
            text="Команды с таким именем не существует!",
            reply_markup=get_cancel_kb(),
            disable_web_page_preview=True
        )
        return await state.set_state(CommandsFSM.WAITING_FOR_UPDATE_COMMAND)
    else:
        await update_command(command, n_description, n_result)
        await message.answer(
            text=f"Успешно: {command} {n_description} {n_result}",
            reply_markup=get_main_kb(),
            disable_web_page_preview=True
        )

    return await state.clear()

@router.message(CommandsFSM.WAITING_FOR_DELETE_COMMAND)
async def on_command_delete(message: types.Message, state: FSMContext):
    command = message.text.split(" ")[0]

    if await select_one_command(command) is None:
        await message.answer(
            text="Команды с таким именем не существует!",
            reply_markup=get_cancel_kb(),
            disable_web_page_preview=True
        )
        return await state.set_state(CommandsFSM.WAITING_FOR_DELETE_COMMAND)
    else:
        await delete_command(command)
        await message.answer(
            text=f"Команда {command} успешно удалена!",
            reply_markup=get_main_kb(),
            disable_web_page_preview=True
        )

    return await state.clear()