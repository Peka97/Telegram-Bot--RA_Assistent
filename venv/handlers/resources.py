from create_bot import dp
from handlers import keyboards
from aiogram import types


@dp.callback_query_handler(lambda call: "btn_resourses" == call.data)
async def send_resourses(call: types.CallbackQuery) -> None:
    """Функция, ответственная за кнопку Ресурсы в главном меню"""
    with open('./data/macros.txt', 'r', encoding='utf-8') as file:
        rsc = file.read()
    await call.message.answer(text=rsc, parse_mode="Markdown",
                              reply_markup=keyboards.inline_keyboard_main)