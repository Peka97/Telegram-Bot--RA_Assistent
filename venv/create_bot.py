import json

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

with open('config.json', 'r', encoding='utf-8') as file:
    API_TOKEN = json.load(file)['API_TOKEN']

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
