from handlers import meetings, schedule, resources, keyboards, basic
from aiogram.utils import executor
from create_bot import dp
import logging

#logging.basicConfig(filename='log.log', datefmt="%H%M%S", level=logging.ERROR)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
