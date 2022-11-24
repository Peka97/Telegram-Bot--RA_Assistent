from create_bot import dp
from handlers import keyboards
from parsing import formatted_data, formatted_for_all

import json
import datetime
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


class GetData(StatesGroup):
    waiting_for_schedule_number = State()


@dp.callback_query_handler(lambda call: "btn_change_schedule_number" == call.data)
async def schedule_number_step_one(call: types.CallbackQuery) -> None:
    """Функция смены номера расписания, принимающая новый график"""

    await call.message.answer(text='Введите свой номер графика цифрой (0 для руководителей)',
                              reply_markup=keyboards.inline_keyboard_cancel)
    await GetData.waiting_for_schedule_number.set()


@dp.callback_query_handler(lambda call: 'btn_change_number_cancel' == call.data, state='*')
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.reply(text="Действие отменено. Возврат в 📁 Главное меню",
                             reply_markup=keyboards.inline_keyboard_main)


@dp.message_handler(state=GetData.waiting_for_schedule_number)
async def schedule_number_step_two(message: types.Message, state: FSMContext) -> None:
    """Фукнция смены номера расписания, которая редактирует файл БД"""
    if str(message.text).isdigit():
        with open('./data/users.json', 'r+', encoding='UTF-8') as json_file:
            data = json.load(json_file)
            data['users'][f'{message.from_user.username}']['schedule'] = f'{message.text}'
        with open('./data/users.json', 'w', encoding='UTF-8') as json_file:
            json.dump(data, json_file)
        await message.reply(
            text=f"График успешно изменён. Твой текущий график: {data['users'][f'{message.from_user.username}']['schedule']}",
            reply_markup=keyboards.inline_keyboard_main)
    else:
        await message.reply(text=f'Что то пошло не так')
    await state.finish()


@dp.callback_query_handler(lambda call: "btn_schedule_today" == call.data)
async def schedule_one_day(call: types.CallbackQuery) -> None:
    """Функция показывающая график на сегодняшний день. Часовой пояс - Moscow"""

    with open('./data/users.json', 'r', encoding="UTF-8") as json_file:
        data = json.load(json_file)
    number_of_schedule = data['users'][f'{call.message.chat.username}']['schedule']
    if number_of_schedule not in ('1', '2', '3', '4'):
        await call.message.answer(text=f'SheduleNumberOutOfList')
    else:
        check_date = (datetime.date.today()).strftime("%d.%m.%Y")
        reply = ''
        for el in formatted_data(number_of_schedule):
            if el.split(' ')[1] == check_date:
                reply = el
                break
        await call.message.answer(text=f'Твой график на сегодня:\n\n \t👉🏻 {reply}')
        await call.message.answer(text='📁 Главное меню', reply_markup=keyboards.inline_keyboard_main)


@dp.callback_query_handler(lambda call: "btn_schedule_week" == call.data)
async def schedule_seven_days(call: types.CallbackQuery) -> None:
    """Функция показывающая график на неделю. Часовой пояс - Moscow"""

    with open('./data/users.json', 'r', encoding="UTF-8") as json_file:
        data = json.load(json_file)
    number_of_schedule = data['users'][f'{call.message.chat.username}']['schedule']
    if number_of_schedule not in ('1', '2', '3', '4'):
        await call.message.answer(text=f'SheduleNumberOutOfList')
    else:
        check_date = (datetime.date.today()).strftime("%d.%m.%Y")
        idx_start = 0
        for idx, el in enumerate(formatted_data(number_of_schedule)):
            if el.split(' ')[1] == check_date:
                idx_start = idx
                break
        txt = '\n\t👉🏻 '.join(formatted_data(number_of_schedule)[idx_start:idx_start + 7])
        await call.message.answer(text=f'Твой график на неделю:\n\n\t👉🏻 {txt}')
        await call.message.answer(text='📁 Главное меню', reply_markup=keyboards.inline_keyboard_main)


@dp.callback_query_handler(lambda call: 'btn_schedule_general' == call.data)
async def show_schedule_general(call: types.CallbackQuery) -> None:
    """Функция, показывающая общее расписание. Часовой пояс - Moscow"""

    txt = '\n\t👉🏻 '.join(formatted_for_all())
    await call.message.answer(text=f'Общее расписание на неделю:\n\n\t👉🏻 {txt}')
    await call.message.answer(text='📁 Главное меню', reply_markup=keyboards.inline_keyboard_main)


