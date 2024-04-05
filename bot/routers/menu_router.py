from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.keyboards import keyboard_for_menu
from bot.states import Subject, AFKState

menu_router = Router()


@menu_router.message(Subject.choosing_subject, F.text == 'В меню')
@menu_router.message(Subject.chosen_subject, F.text == 'В меню')
@menu_router.message(AFKState.logged, F.text == 'В меню')
async def my_subjects_button(message: types.Message, state: FSMContext):
    await message.answer("Меню", reply_markup=keyboard_for_menu())
    await state.set_state(AFKState.logged)
