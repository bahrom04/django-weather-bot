import os
import sys
import random
import requests

from aiogram import Bot, types, filters
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

kb = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
buttons = [types.reply_keyboard.KeyboardButton('Manzil'),
            types.reply_keyboard.KeyboardButton('Contact'),
                 types.reply_keyboard.KeyboardButton("Biz haqimizda")]

kb.add(*buttons)


class Form(StatesGroup):
    name = State()
    phone = State()



@dp.message_handler(filters.Text(contains='Biz haqimizda'))
async def about_us(message: types.Message):
    path = open(file=path, mode='rb')
    template = types.InputFile(path)
    await message.answer("biz haqimizda", reply_markup=kb)
    
@dp.message_handler(filters.Text(contains="Contact"))
async def contact(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text="contact",
        reply_markup=kb
    )

# Buxoro locatsiyasi
@dp.message_handler(filters.Text(contains="📍 Buxoro"))
async def contact(message: types.Message):
    path = 'buxoro.jpg'
    path = open(file=path, mode='rb')
    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=path,
        reply_markup=kb,
        caption="buxoro"
    )
    longitude =  64.4024167
    latitude = 39.7471944
    await bot.send_location(chat_id=message.from_user.id, 
        latitude=latitude, 
        longitude=longitude)
@dp.message_handler(commands=['random'])
async def random_jokes(message:types.Message):
    res = requests.get("https://api.chucknorris.io/jokes/random").json()
    context = res["value"]
    print(res)
    await message.answer(res)
    
    
@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await Form.name.set()

    user_id = message.from_user.id
    # if str(user_id) in db.get_user(user_id):
    #     keyboard = types.ReplyKeyboardMarkup(
    #         resize_keyboard=True,
    #         input_field_placeholder='Ismingizni kiriting:'
    #     )
    #     # button = ['Москва','Tashkent','Paris']
    #     # keyboard.add(*button)
    await message.answer('Ismiz:',
                            reply_markup=kb)
    # else:
    #     keyboard = types.ReplyKeyboardMarkup(
    #         resize_keyboard=True, one_time_keyboard=True
    #     )
    #     buttons = ['Согласен', 'Не согласен']
    #     keyboard.add(*buttons)
    #     await message.answer('Сначала нужно зарегистрироваться.')
    #     await message.answer('Вы согласны на обработку персональных данных?',
    #                          reply_markup=keyboard)


@dp.message_handler(state=Form.name)
async def register(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['name'] = message.text
        await message.answer("tel number:")

        # if proxy['name'] == 'Согласен':
        #     db.add_user(message.from_user.id, message.from_user.first_name,
        #                 message.from_user.username)
        #     await message.reply('Всё готово, Вы зарегистрированы!\n'
        #                         'Выполните комманду /start ещё раз.')
        #     await state.finish()
        # elif proxy['reg'] == 'Не согласен':
        #     await message.reply('В таком случае, Вы не можете узнать погоду.\n'
        #                         'Если передумаете, повторно введите /start')
        #     await state.finish()
        # else:
        #     await message.reply('Введите "Согласен", либо "Не согласен"')

@dp.message_handler(state=Form.phone)
async def register(message: types.Message, state: FSMContext):
    async with state.proxy() as proxy:
        proxy['phone'] = message.text
        await message.answer(f"raxmat:")
        await Form.finish()


   
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
