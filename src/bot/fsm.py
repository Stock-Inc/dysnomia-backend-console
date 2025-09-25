from aiogram.fsm.state import StatesGroup, State

class CommandsFSM(StatesGroup):
    WAITING_FOR_ADD_COMMAND = State()
    WAITING_FOR_UPDATE_COMMAND = State()
    WAITING_FOR_DELETE_COMMAND = State()