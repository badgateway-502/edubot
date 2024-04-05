from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text, Bold

from bot import future_api
from bot.keyboards import keyboard_go_to_menu, keyboard_for_subject
from bot.states import AFKState, SubjectState

lecture_router = Router()

@lecture_router.message(SubjectState.current_lecture, F.text == "Текущая лекция")
async def my_subjects_button(message: types.Message, state: FSMContext):
    await message.answer_video('text', reply_markup=keyboard_go_to_menu())
    await state.set_state(SubjectState.current_lecture)