import config
import logging
from db import DB
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

db = DB()


@dp.message_handler(commands = "start")
async def cmd_start(message: types.Message):
    db.append_user(message.from_user.id)
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Бизнес", "Работа","Магазин","Казино"]
    keyboard.add(*buttons)
    balance = db.get_balance(message.from_user.id)
    await message.answer(f"Ты в главном меню, {str(message.chat.first_name)}. У тебя на счету {balance} рублей", reply_markup=keyboard) #здесь на месте звёздочек должен появлятся баланс

@dp.message_handler(lambda message: message.text == "Выйти в главное меню")
async def teacher(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Бизнес", "Работа","Магазин","Казино"]
    keyboard.add(*buttons)
    balance = db.get_balance(message.from_user.id)
    await message.answer(f"Ты в главном меню, {str(message.chat.first_name)}. У тебя на счету {balance} рублей", reply_markup=keyboard) #здесь на месте звёздочек должен появлятся баланс

@dp.message_handler(lambda message: message.text == "Бизнес")
async def buisness(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Купить бизнес", "Управление бизнесом","Выйти в главное меню"]
    keyboard.add(*buttons)
    await message.answer("...", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Работа")
async def work(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Учитель"]
    keyboard.add(*buttons)
    await message.answer("...", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Учитель")
async def teacher(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Приступить к работе", "Выйти в главное меню"]
    keyboard.add(*buttons)
    balance = db.get_balance(message.from_user.id)
    await message.answer(f"Привет, твоя задача.... Твой баланс: {balance} рублей", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Приступить к работе")
async def start_work(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Пропустить задание", "Выйти в главное меню"]
    keyboard.add(*buttons)
    await message.answer("Расшифруй слово " + "***", reply_markup=keyboard) #здесь берутся слова из заданий

@dp.message_handler(lambda message: message.text == "Пропустить задание")
async def start_work(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Пропустить задание", "Выйти в главное меню"]
    keyboard.add(*buttons)
    await message.answer("Расшифруй слово " + "***", reply_markup=keyboard) #здесь берутся слова из заданий

#@dp.message_handler(lambda message: message.text == ???) #здесь нужно подумать как считывать правильный ответ и зачислять баланс

@dp.message_handler(lambda message: message.text == "Магазин")
async def shop(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Выйти в главное меню"]
    keyboard.add(*buttons)
    await message.answer("Тут пока ничего нет...", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Казино")
async def casino(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Рулетка","Выйти в главное меню"]
    keyboard.add(*buttons)
    await message.answer("...", reply_markup=keyboard)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)