from aiogram.fsm.state import StatesGroup, State


class AFKState(StatesGroup):
    logged = State()


class SignInState(StatesGroup):
    signing_in = State()
