from create_bot import dp
from handlers import keyboards
from aiogram import types

# Main Menu
inline_btn_schedule = types.InlineKeyboardButton('📅 Расписание', callback_data='btn_schedule')
inline_btn_resourse = types.InlineKeyboardButton('🗄 Ресурсы', callback_data='btn_resourses')
inline_btn_help = types.InlineKeyboardButton('🙋🏼‍♂️ Помощь', callback_data='btn_help')
inline_btn_meetings = types.InlineKeyboardButton('🧑🏼‍💻 Встречи', callback_data='btn_meetings')
inline_keyboard_main = types.InlineKeyboardMarkup().add(inline_btn_schedule, inline_btn_resourse,
                                                        inline_btn_meetings, inline_btn_help)

# Schedule Menu
inline_btn_schedule_one_day = types.InlineKeyboardButton('📆 На сегодня', callback_data='btn_schedule_today')
inline_btn_schedule_seven_days = types.InlineKeyboardButton('🗓 На 7 дней', callback_data='btn_schedule_week')
inline_btn_schedule_general = types.InlineKeyboardButton('👨‍👩‍👦 Общее', callback_data='btn_schedule_general')
inline_btn_schedule_link = types.InlineKeyboardButton('📎 Excel',
                                                      url='https://docs.google.com/spreadsheets/d'
                                                          '/16bqjSnz6IWeGpG1OSyFHuG2iSb-fspuOqnhgnQ9YN9k/edit#gid=0')
inline_btn_schedule_change_number = types.InlineKeyboardButton('✏️ Изменить номер',
                                                               callback_data='btn_change_schedule_number')

# Meetings Menu
inline_btn_create_meeting = types.InlineKeyboardButton('🎙 Создать', callback_data='btn_create_meeting')
inline_btn_show_meetings = types.InlineKeyboardButton('🗒 Список', callback_data='btn_show_meetings')

# Functional Buttons
inline_btn_cancel = types.InlineKeyboardButton("❌ Отменить", callback_data='btn_change_number_cancel')
inline_btn_confirm_users = types.InlineKeyboardButton("Подтвердить", callback_data='btn_confirm_users')
inline_btn_send_links = types.InlineKeyboardButton("Отправить", callback_data='btn_send_links')
inline_btn_return = types.InlineKeyboardButton('🏠 На главную', callback_data='btn_main')
########################################################################################################################
# Init. MenuBars
inline_keyboard_schedule = types.InlineKeyboardMarkup().add(inline_btn_schedule_one_day, inline_btn_schedule_seven_days,
                                                            inline_btn_schedule_general, inline_btn_schedule_link,
                                                            inline_btn_schedule_change_number, inline_btn_return)
inline_keyboard_meetings = types.InlineKeyboardMarkup().add(inline_btn_create_meeting, inline_btn_show_meetings,
                                                            inline_btn_return)
inline_keyboard_cancel = types.InlineKeyboardMarkup().add(inline_btn_cancel)
inline_keyboard_confirm = types.InlineKeyboardMarkup().add(inline_btn_confirm_users)


@dp.callback_query_handler(lambda call: 'btn_main' == call.data)
async def show_main_keyboard(call: types.CallbackQuery) -> None:
    """Функция, ответственная за смену меню на главне меню"""

    await call.message.edit_text(text='📁 Главное меню', reply_markup=keyboards.inline_keyboard_main)


@dp.callback_query_handler(lambda call: "btn_schedule" == call.data)
async def show_schedule_keyboard(call: types.CallbackQuery) -> None:
    """Функция, ответственная за кнопку Расписание в главном меню"""

    await call.message.edit_text(text='📁 Расписание', reply_markup=inline_keyboard_schedule)


@dp.callback_query_handler(lambda call: "btn_meetings" == call.data)
async def show_meets_keyboard(call: types.CallbackQuery) -> None:
    await call.message.edit_text(text='📁 Встречи', reply_markup=inline_keyboard_meetings)


@dp.callback_query_handler(lambda call: "btn_help" == call.data)
async def send_help(call: types.CallbackQuery) -> None:
    """Функция, ответственная за кнопку Помощь в главном меню"""

    await call.message.answer(text="По всем вопросам обращайтесь к моему создателю: @loner97",
                              reply_markup=inline_keyboard_main)
