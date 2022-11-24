from create_bot import dp, bot
from handlers import keyboards
from handlers.basic import tz_MOSCOW
from parsing import schedule_for_transfer_of_shifts, formatted_for_meets
from handlers.basic import check_date_2

import asyncio
import json
import datetime
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

with open('./config.json', 'r', encoding='utf-8') as file:
    MEET_CHAT_ID = json.load(file)['MEET_CHAT_ID']


class ChannelInfo(StatesGroup):
    name_link = State()
    invoke_date = State()
    member_limit = State()


def add_members_to_turple(agent_info_1: tuple, agent_info_2: tuple) -> tuple:
    members = [1973622999]  # Добавлены Саша Инякин и дубль меня
    with open('./data/users.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for user_name, user_data in data['users'].items():
        if agent_info_1[1] == user_data['schedule'] or agent_info_2[1] == user_data['schedule']:
            members.append(user_data['chat_id'])
    return tuple(members)


@dp.message_handler(commands='auto_meets_force')
async def automatic_send_link_for_meets(message: types.Message) -> None:
    last_check = datetime.datetime.now(tz_MOSCOW).date() - datetime.timedelta(days=1)
    while True:
        if last_check < datetime.datetime.now(tz_MOSCOW).date():
            last_check = datetime.datetime.now(tz_MOSCOW).date()
            users = formatted_for_meets(last_check)
            date = (datetime.datetime.now(tz_MOSCOW).date() + datetime.timedelta(days=1)).strftime('%d/%m/%Y')
            morning = add_members_to_turple(users[1], users[2])
            night = add_members_to_turple(users[2], users[3])
            meet_morning = await bot.create_chat_invite_link(chat_id=-1001561208078,
                                                             name=f'AUTO {users[1]} to {users[2]}',
                                                             expire_date=datetime.timedelta(hours=24),
                                                             member_limit=6)
            meet_night = await bot.create_chat_invite_link(chat_id=-1001561208078,
                                                           name=f'AUTO {users[2]} to {users[3]}',
                                                           expire_date=datetime.timedelta(hours=24),
                                                           member_limit=6)
            txt_morning = f"{date} 09:00 MSC\n{users[1][0].split()[0]} ➡ {users[2][0].split()[0]}\nПерейдите по " \
                          f"[ссылке]({meet_morning['invite_link']}) или нажмите на кнопку ниже"
            txt_night = f"{date} 21:00 MSC\n{users[2][0].split()[0]} ➡ {users[3][0].split()[0]}\nПерейдите по " \
                        f"[ссылке]({meet_night['invite_link']}) или нажмите на кнопку ниже"
            for user_chat_id in morning:
                await bot.send_message(chat_id=user_chat_id, text=txt_morning, parse_mode='MarkdownV2',
                                       reply_markup=types.InlineKeyboardMarkup().add(
                                           types.InlineKeyboardButton("Присоединиться",
                                                                      url=meet_morning['invite_link'])))
            for user_chat_id in night:
                await bot.send_message(chat_id=user_chat_id, text=txt_night, parse_mode='MarkdownV2',
                                       reply_markup=types.InlineKeyboardMarkup().add(
                                           types.InlineKeyboardButton("Присоединиться", url=meet_night['invite_link'])))
        else:
            await asyncio.sleep(3600)

#######################################################################################################################
# Далее расположен не законченный код для реализации кастомных собраний
#######################################################################################################################
# @dp.message_handler(commands='cancel', state='*')
# async def delete_states(message: types.Message, state: FSMContext) -> None:
#     await state.finish()
#     await message.answer(text="Действие отменено. Память очищена")
#
#
# @dp.callback_query_handler(lambda call: 'btn_create_meeting' in call.data)
# async def create_meeting_start(call: types.CallbackQuery) -> None:
#     await call.message.reply(text='Введите название своего собрания')
#     await ChannelInfo.name_link.set()
#
#
# @dp.message_handler(state=ChannelInfo.name_link)
# async def create_meeting_get_invokedate(message: types.Message, state: FSMContext) -> None:
#     await state.update_data(name_link=message.text)
#     await message.answer(text='Введите "username" участников, отправляя их имена одно за другим. '
#                               'По окончанию нажмите на кнопку "Подтвердить"',
#                          reply_markup=keyboards.inline_keyboard_confirm)
#     await ChannelInfo.member_limit.set()
#
#
# @dp.message_handler(state=ChannelInfo.member_limit)
# async def create_meeting_get_memberlimit(message: types.Message, state: FSMContext) -> None:
#     if 'member_limit' in (await state.get_data()).keys():
#         data = await state.get_data('members')
#         await state.update_data(member_limit=data['members'] + message.text + ", ")
#     else:
#         await state.update_data(member_limit=message.text + ", ")
#     await message.answer(text=f'Пользователь {message.text} добавлен. При необходимости введите дополнительный '
#                               f'"username" участника или нажмите на кнопку "Подтвердить"',
#                          reply_markup=keyboards.inline_keyboard_confirm)
#     await ChannelInfo.member_limit.set()
#
#
# @dp.callback_query_handler(lambda call: 'btn_confirm_users' in call.data, state='*')
# async def confirm_members(call: types.CallbackQuery, state: FSMContext) -> None:
#     data = await state.get_data()
#     try:
#         with open('./data/links.json', 'r+', encoding="UTF-8") as file:
#             json.dump({check_date_2: {'info': data}}, file)
#         await state.finish()
#     except FileNotFoundError:
#         with open('./data/links.json', 'w+', encoding="UTF-8") as file:
#             json.dump({check_date_2: {'info': data}}, file)
#         await state.finish()
#     await call.message.reply(text=f"Всю информацию я собрал. Вот она:\n\n{data}\n\n Отправить приглашение?",
#                              reply_markup=types.InlineKeyboardMarkup().add(keyboards.inline_btn_send_links))
#
#
# @dp.callback_query_handler(lambda call: 'btn_send_links' in call.data)
# @dp.message_handler(commands='send_link')
# async def send_link_to_members(message: types.Message) -> None:
#     users = []
#     with open("./data/links.json", 'r', encoding="UTF-8") as file:
#         data: dict = json.load(file)
#         for meet_time, info in data.items():
#             if meet_time.split()[0] == check_date_2:
#                 meet_info = info['info']
#         for key, value in data.items():
#             if key == "members":
#                 for username in value.split(', '):
#                     users.append(username)
#         print("Start")
#         print(MEET_CHAT_ID)
#         meet = await bot.create_chat_invite_link(chat_id=-1001561208078,
#                                                  name=meet_info['name_link'],
#                                                  expire_date=datetime.timedelta(hours=24),
#                                                  member_limit=len(users))
#     print("Done")
#     with open('./data/links.json', 'r+', encoding='UTF-8') as json_file_data:
#         links = json.load(json_file_data)
#         links['links'].append(meet['invite_link'])
#     with open('./data/links.json', 'w', encoding='UTF-8') as json_file_data:
#         json.dump(links, json_file_data)
#     with open('./data/users.json', 'r', encoding='UTF-8') as json_file:
#         info = json.load(json_file)
#         for user in info['users']:
#             print(user['username'])
#             if f"@{user['username']}" in users:
#                 await bot.send_message(chat_id=user['chat_id'], text=f"Новое собрание: {meet['name']}\n"
#                                                                      f"Ссылка на собрание: {meet['invite_link']}")
#
#
# @dp.message_handler(commands='clear_links')
# async def clear_links(message: types.Message) -> None:
#     if message.from_user.username == 'loner97':
#         with open('./data/links.json', 'r', encoding='UTF-8') as json_file:
#             data = json.load(json_file)
#             for link in data['links']:
#                 await bot.revoke_chat_invite_link(chat_id=MEET_CHAT_ID, invite_link=link)
#         with open('./data/links.json', 'w', encoding='UTF-8') as json_file:
#             json.dump({'links': []}, json_file)
#             await bot.send_message(text='Ссылки очищены')
#
#
# @dp.message_handler(commands='kick')
# async def kick_chat_members(message: types.Message) -> None:
#     with open('./data/users.json', 'r', encoding='UTF-8') as json_file:
#         data = json.load(json_file)
#     for user in data['users']:
#         if user['chat_id'] == 1387411715:  # Except for chat owner
#             continue
#         await bot.kick_chat_member(chat_id=MEET_CHAT_ID, user_id=user['chat_id'])
#         await bot.unban_chat_member(chat_id=MEET_CHAT_ID, user_id=user['chat_id'], only_if_banned=True)
#
#
# @dp.message_handler(commands='regular')
# async def transfer_of_shifts(
#         message: types.Message):  # Сдать автоматическую рассылку в зависимости от того кто выходит на смену
#     morning = schedule_for_transfer_of_shifts()['09:00']
#     night = schedule_for_transfer_of_shifts()['21:00']
#     print(morning, night)
#     meeting_morning = []  # Добавить сюда изначальные chat_id Барковской и Инякина
#     meeting_night = []  # Добавить сюда изначальные chat_id Барковской и Инякина
#     with open('./data/users.json', 'r', encoding='UTF-8') as f_users:
#         f_users_data: dict = json.load(f_users)
#     for user, info in f_users_data['users'].items():
#         print(info)
#         if info['schedule'] in morning:
#             meeting_morning.append(info['chat_id'])
#         if info['schedule'] in night:
#             meeting_night.append(info['chat_id'])
#     print(meeting_morning)
#     print(meeting_night)

# meet_morning = await bot.create_chat_invite_link(chat_id=MEET_CHAT_ID,
#                                          name=data['name_link'],
#                                          expire_date=datetime.timedelta(hours=24),
#                                          member_limit=len(users))
