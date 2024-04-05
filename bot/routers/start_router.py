from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot import future_api, validate
from bot.main import keyboard_for_menu
from bot.states import AFKState, SignInState

start_router = Router()


@start_router.message(StateFilter(None))
async def cmd_start(message: types.Message, state: FSMContext):
    if await future_api.check_user_db(message.from_user.id):
        await message.answer("Меню", reply_markup=keyboard_for_menu())
        await state.set_state(AFKState.logged)
    else:
        await message.answer("Пожалуйста, зарегестрируйтесь. Введите ваше имя и фамилию.")
        await state.set_state(SignInState.signing_in)

@start_router.message(SignInState.signing_in)
async def signing_in(message: types.Message, state: FSMContext):
    try:
        if validate.validate_name(message.text):
            name = message.text.split()
            await future_api.create_new_student_db(name[0], name[1], message.from_user.id)
            await message.answer("Меню", reply_markup=keyboard_for_menu())
            await state.set_state(AFKState.logged)
    except ValueError as e:
        await message.answer(f'{e}')
