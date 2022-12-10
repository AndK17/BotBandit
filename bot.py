import config
import logging
from db import DB
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from random import randint

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)

db = DB()

bet = 0


class FSMBet(StatesGroup):
    bet = State()

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
    global bet
    bet = 0
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Рулетка","Выйти в главное меню"]
    keyboard.add(*buttons)
    await message.answer("...", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Рулетка")
async def roulette(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Изменить ставку", "Красное", "Черное", "Zero", "Чётное", "Нечётное",
               "1st", "2nd", "3rd", "Выйти в главное меню"]
    keyboard.add(*buttons)
    balance = db.get_balance(message.from_user.id)
    await message.answer(f"Ваш баланс: {balance} рублей\nВаша ставка: {bet} рублей", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Изменить ставку")
async def change_bet(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Изменить ставку", "Красное", "Черное", "Zero", "Чётное", "Нечётное",
               "1st", "2nd", "3rd", "Выйти в главное меню"]
    keyboard.add(*buttons)
    await FSMBet.bet.set()
    await message.answer("Введите ставку (натуральное число):", reply_markup=keyboard)


@dp.message_handler(content_types=["text"], state=FSMBet.bet)
async def get_bet(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Изменить ставку", "Красное", "Черное", "Zero", "Чётное", "Нечётное",
               "1st", "2nd", "3rd", "Выйти в главное меню"]
    keyboard.add(*buttons)
    global bet
    balance = db.get_balance(message.from_user.id)
    if message.text.isdigit():
        bet = int(message.text)
        if bet <= balance:
            await message.answer(f"Ваш баланс: {balance} рублей\nВаша ставка: {bet} рублей", reply_markup=keyboard)
            await state.finish()
        else:
            await message.answer("Ставка не может быть больше баланса\nПожалуйста, введите ставку снова:")
    else:
        await message.answer("Ставка должна быть натуральным числом\nПожалуйста, введите ставку снова:")


@dp.message_handler(lambda message: message.text == "Красное")
async def casino_red(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    result = randint(0, 36)
    reds = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
    if result == 0:
        result_color = "зеро"
    else:
        if result in reds:
            result_color = "красное"
        else:
            result_color = "чёрное"

    if result_color == "красное":
        db.set_balance(message.from_user.id, balance + bet)
        balance += bet
        await message.answer(f"Выпало {result} - красное :)\n"
                             f"Вы выиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")
    else:
        db.set_balance(message.from_user.id, balance - bet)
        balance -= bet
        await message.answer(f"Выпало {result} - {result_color}  :(\n"
                             f"Вы проиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")


@dp.message_handler(lambda message: message.text == "Черное")
async def casino_black(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    result = randint(0, 36)
    reds = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
    if result == 0:
        result_color = "зеро"
    else:
        if result in reds:
            result_color = "красное"
        else:
            result_color = "чёрное"

    if result_color == "чёрное":
        db.set_balance(message.from_user.id, balance + bet)
        balance += bet
        await message.answer(f"Выпало {result} - чёрное :)\n"
                             f"Вы выиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")
    else:
        db.set_balance(message.from_user.id, balance - bet)
        balance -= bet
        await message.answer(f"Выпало {result} - {result_color}  :(\n"
                             f"Вы проиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")


@dp.message_handler(lambda message: message.text == "Zero")
async def casino_zero(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    result = randint(0, 36)
    reds = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
    if result == 0:
        result_color = "зеро"
    else:
        if result in reds:
            result_color = "красное"
        else:
            result_color = "чёрное"

    if result_color == "зеро":
        db.set_balance(message.from_user.id, balance + bet*36)
        balance += bet*36
        await message.answer(f"Выпало 0 - зеро :)\n"
                             f"Вы выиграли {bet*36} рублей\n"
                             f"Ваш баланс: {balance}")
    else:
        db.set_balance(message.from_user.id, balance - bet)
        balance -= bet
        await message.answer(f"Выпало {result} - {result_color}  :(\n"
                             f"Вы проиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")


@dp.message_handler(lambda message: message.text == "Чётное")
async def casino_even(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    result = randint(0, 36)
    reds = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
    if result == 0:
        result_color = "зеро"
    else:
        if result in reds:
            result_color = "красное"
        else:
            result_color = "чёрное"

    if result % 2 == 0:
        db.set_balance(message.from_user.id, balance + bet)
        balance += bet
        await message.answer(f"Выпало {result} - {result_color} :)\n"
                             f"Вы выиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")
    else:
        db.set_balance(message.from_user.id, balance - bet)
        balance -= bet
        await message.answer(f"Выпало {result} - {result_color} :(\n"
                             f"Вы проиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")


@dp.message_handler(lambda message: message.text == "Нечётное")
async def casino_not_even(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    result = randint(0, 36)
    reds = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
    if result == 0:
        result_color = "зеро"
    else:
        if result in reds:
            result_color = "красное"
        else:
            result_color = "чёрное"

    if result % 2 != 0:
        db.set_balance(message.from_user.id, balance + bet)
        balance += bet
        await message.answer(f"Выпало {result} - {result_color} :)\n"
                             f"Вы выиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")
    else:
        db.set_balance(message.from_user.id, balance - bet)
        balance -= bet
        await message.answer(f"Выпало {result} - {result_color} :(\n"
                             f"Вы проиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")


@dp.message_handler(lambda message: message.text == "1st")
async def casino_1st(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    result = randint(0, 36)
    reds = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
    if result == 0:
        result_color = "зеро"
    else:
        if result in reds:
            result_color = "красное"
        else:
            result_color = "чёрное"

    if result <= 12 and result != 0:
        db.set_balance(message.from_user.id, balance + bet*3)
        balance += bet*3
        await message.answer(f"Выпало {result} - {result_color} :)\n"
                             f"Вы выиграли {bet*3} рублей\n"
                             f"Ваш баланс: {balance}")
    else:
        db.set_balance(message.from_user.id, balance - bet)
        balance -= bet
        await message.answer(f"Выпало {result} - {result_color} :(\n"
                             f"Вы проиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")


@dp.message_handler(lambda message: message.text == "2nd")
async def casino_2nd(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    result = randint(0, 36)
    reds = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
    if result == 0:
        result_color = "зеро"
    else:
        if result in reds:
            result_color = "красное"
        else:
            result_color = "чёрное"

    if result >= 13 and result <= 24:
        db.set_balance(message.from_user.id, balance + bet * 3)
        balance += bet * 3
        await message.answer(f"Выпало {result} - {result_color} :)\n"
                             f"Вы выиграли {bet * 3} рублей\n"
                             f"Ваш баланс: {balance}")
    else:
        db.set_balance(message.from_user.id, balance - bet)
        balance -= bet
        await message.answer(f"Выпало {result} - {result_color} :(\n"
                             f"Вы проиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")


@dp.message_handler(lambda message: message.text == "3rd")
async def casino_3rd(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    result = randint(0, 36)
    reds = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
    if result == 0:
        result_color = "зеро"
    else:
        if result in reds:
            result_color = "красное"
        else:
            result_color = "чёрное"

    if result >= 25:
        db.set_balance(message.from_user.id, balance + bet * 3)
        balance += bet * 3
        await message.answer(f"Выпало {result} - {result_color} :)\n"
                             f"Вы выиграли {bet * 3} рублей\n"
                             f"Ваш баланс: {balance}")
    else:
        db.set_balance(message.from_user.id, balance - bet)
        balance -= bet
        await message.answer(f"Выпало {result} - {result_color} :(\n"
                             f"Вы проиграли {bet} рублей\n"
                             f"Ваш баланс: {balance}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)