import json
import datetime
import pytz
from create_bot import dp
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from handlers import keyboards

tz_MOSCOW = pytz.timezone('Europe/Moscow')
check_date = datetime.date.strftime(datetime.datetime.now(tz_MOSCOW), '%m.%y')
check_date_2 = datetime.date.strftime(datetime.datetime.now(tz_MOSCOW), '%d/%m/%Y')



class GetData(StatesGroup):
    waiting_for_schedule_number = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message) -> None:
    """Стартовая команда. При наличии доступа обновляет меню Inline и BotCommand"""

    try:
        with open('./data/users.json', 'r', encoding="UTF-8") as file:
            data = json.load(file)
        if message.from_user.username not in data['users']:
            await message.reply(
                text="Привет! Я тебя не знаю. Если у тебя есть секретный код, то самое время его написать")
        else:
            await message.answer(text='📁 Главное меню', reply_markup=keyboards.inline_keyboard_main)
            await dp.bot.set_my_commands([
                types.BotCommand('start', 'Перезапустить бота'),
                types.BotCommand('profile', 'Посмотреть профиль'),
            ])
    except json.decoder.JSONDecodeError:
        with open('./data/users.json', 'r+', encoding="UTF-8") as file:
            json.dump({'users': {}}, file)
        await message.reply(text="Привет! Я тебя не знаю. Если у тебя есть секретный код, то самое время его написать")


@dp.message_handler(text='DrmCYS9GM6YZgsSR')
async def activate_secrete_code(message: types.Message) -> None:
    """Функция проверки секретного ключа"""

    try:
        with open('./data/users.json', 'r', encoding='UTF-8') as json_file:
            data = json.load(json_file)
        if message.from_user.username in data['users']:
            await message.reply(text="Ты уже есть в списках, более использовать код не нужно")
        else:
            data['users'][f'{message.from_user.username}'] = {"chat_id": message.from_user.id}
            with open('./data/users.json', 'w', encoding='UTF-8') as json_file:
                json.dump(data, json_file)
            await message.reply(text="Введи номер своего расписания (0 для руководителей)")
            await GetData.waiting_for_schedule_number.set()
    except json.decoder.JSONDecodeError:
        with open('./data/users.json', 'w', encoding='UTF-8') as json_file:
            json.dump({'users': {}}, json_file)


@dp.message_handler(commands='profile')
async def show_profile(call: types.CallbackQuery) -> None:
    """Функция, ответтвенная за команду, показывающую данные по логину в telegram"""

    with open('./data/users.json', 'r', encoding='UTF-8') as json_file:
        data_file = json.load(json_file)
        txt = data_file['users'][f'{call.chat.username}']
    await call.answer(text=f'Ваши текущие данные, {call.chat.username}: \n{txt}')
