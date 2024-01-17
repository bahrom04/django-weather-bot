import os
import sys

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from tg_bot import config
from tg_bot.db import DataBaseManager
from tg_bot.weather import Weather

sys.path.insert(1, os.getcwd())

try:
    db = DataBaseManager()
except Exception as ex:
    print('[INFO] Error while working with SQL', ex)

bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

weather = Weather()


class Form(StatesGroup):
    reg = State()


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if str(user_id) in db.get_user(user_id):
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True,
            input_field_placeholder='Введите название города: '
        )
        button = ['Москва','Tashkent','Paris']
        keyboard.add(*button)
        await message.answer('В каком городе Вы хотите узнать погоду?',
                             reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True
        )
        buttons = ['Согласен', 'Не согласен']
        keyboard.add(*buttons)
        await message.answer('Сначала нужно зарегистрироваться.')
        await message.answer('Вы согласны на обработку персональных данных?',
                             reply_markup=keyboard)
        await Form.reg.set()


@dp.message_handler(state=Form.reg)
async def register(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['reg'] = message.text
        if proxy['reg'] == 'Согласен':
            db.add_user(message.from_user.id, message.from_user.first_name,
                        message.from_user.username)
            await message.reply('Всё готово, Вы зарегистрированы!\n'
                                'Выполните комманду /start ещё раз.')
            await state.finish()
        elif proxy['reg'] == 'Не согласен':
            await message.reply('В таком случае, Вы не можете узнать погоду.\n'
                                'Если передумаете, повторно введите /start')
            await state.finish()
        else:
            await message.reply('Введите "Согласен", либо "Не согласен"')



   
@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        await message.reply(weather.get_weather(message.text))
    except Exception as e:
        print('[INFO] The user entered an invalid city name', e)
        await message.reply("\U00002620 Проверьте название города \U00002620")


async def send_weather(id_user, text):
    await bot.send_message(id_user, weather.get_weather(text))


if __name__ == '__main__':
    executor.start_polling(dp)
