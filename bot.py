import config
import logging
from db import DB
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from random import randint
from task_generator import generate_task

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)

db = DB()

task = 0


class FSMBet(StatesGroup):
    bet = State()

class FSMWork(StatesGroup):
    task = State()

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
    await message.answer(f"Ты в главном меню, {str(message.chat.first_name)}. У тебя на счету {balance} рублей", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Бизнес")
async def business(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Купить бизнес", "Управление бизнесом","Выйти в главное меню"]
    keyboard.add(*buttons)
    await message.answer(f"Привет, {str(message.chat.first_name)}!\nТы находишься в меню управления бизнесом. ", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Купить бизнес")
async def business(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Шаурмичная", "Завод пива", "Крупнейшая IT-компания"]
    keyboard.add(*buttons)
    if db.get_business_id(message.from_user.id) == -1:
        await message.answer(f"Какой бизнес хочешь купить?", reply_markup=keyboard)
    else:
        await message.answer(f"У тебя уже есть бизнес")


@dp.message_handler(lambda message: message.text == "Работа")
async def work(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Препод по линалу"]
    keyboard.add(*buttons)
    await message.answer(f"Выбери кем ты хочешь работать", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Препод по линалу")
async def teacher(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Приступить к работе", "Выйти в главное меню"]
    keyboard.add(*buttons)
    balance = db.get_balance(message.from_user.id)
    await message.answer(f"Привет, твоя задача считать опредеители матриц, справишься? За каждую правильно решённую задачу будешь получать по 1000 рублей. Твой баланс: {balance} рублей", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Приступить к работе")
async def start_work(message: types.Message):
    global task 
    task = generate_task()
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Пропустить задание", "Я устал, Босс"]
    keyboard.add(*buttons)
    await FSMWork.task.set()
    await message.answer(f"Найди определитель матрицы: {task}", reply_markup=keyboard) 

@dp.message_handler(lambda message: message.text == "Пропустить задание")
async def skip_work(message: types.Message):
    global task 
    task = generate_task()
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Пропустить задание", "Я устал, Босс"]
    keyboard.add(*buttons)
    await FSMWork.task.set()
    await message.answer(f"Найди определитель матрицы: {task}", reply_markup=keyboard) 

@dp.message_handler(content_types=["text"], state=FSMWork.task)
async def get_bet(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Пропустить задание", "Я устал, Босс"]
    keyboard.add(*buttons)
    balance = db.get_balance(message.from_user.id)
    global task
    if message.text == "Пропустить задание":
        task = generate_task()
        await message.answer(f"Найди определитель матрицы: {task}", reply_markup=keyboard)
    elif message.text.isdigit():
        if task[1] == int(message.text):
            task = generate_task()
            db.set_balance(message.from_user.id, balance + 1000)
            balance += 1000
            await message.answer(f"Правильно! Ваш баланс: {balance} рублей", reply_markup=keyboard)
            await message.answer(f"Найди определитель матрицы: {task}", reply_markup=keyboard)
        else:
            await message.answer(f"Увы, это неверный ответ. Попробуй ещё раз", reply_markup=keyboard)
    elif message.text == "Я устал, Босс":
        await state.finish()
        keyboard = types.ReplyKeyboardMarkup()
        buttons = ["Выйти в главное меню"]
        keyboard.add(*buttons)
        await message.answer(f"Вы точно хотите уйти?", reply_markup=keyboard)
    else:
        await message.answer(f"Решай задачу или иди отсюда, бездарь!", reply_markup=keyboard)
    
@dp.message_handler(lambda message: message.text == "Магазин")
async def shop(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ['Обувь', 'Штаны', 'Футболки', 'Шапки', "Выйти в главное меню"]
    keyboard.add(*buttons)
    await message.answer("Добро пожаловать в магазин!\nВыберите категорию товара", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Казино")
async def casino(message: types.Message):
    db.set_bet(message.from_user.id, 0)
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Рулетка","Выйти в главное меню"]
    keyboard.add(*buttons)
    await message.answer("...", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Рулетка")
async def roulette(message: types.Message):
    bet = db.get_bet(message.from_user.id)
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Изменить ставку", "Красное", "Черное", "Zero", "Чётное", "Нечётное",
               "1st", "2nd", "3rd", "Выйти в главное меню"]
    keyboard.add(*buttons)
    balance = db.get_balance(message.from_user.id)
    await message.answer(f"Ваш баланс: {balance} рублей\nВаша ставка: {bet} рублей", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Изменить ставку")
async def change_bet(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add("Выйти в главное меню")
    await FSMBet.bet.set()
    await message.answer("Введите ставку (натуральное число):", reply_markup=keyboard)


@dp.message_handler(content_types=["text"], state=FSMBet.bet)
async def get_bet(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Изменить ставку", "Красное", "Черное", "Zero", "Чётное", "Нечётное",
               "1st", "2nd", "3rd", "Выйти в главное меню"]
    keyboard.add(*buttons)
    balance = db.get_balance(message.from_user.id)
    if message.text.isdigit():
        bet = int(message.text)
        if bet <= balance:
            db.set_bet(message.from_user.id, int(message.text))
            await message.answer(f"Ваш баланс: {balance} рублей\nВаша ставка: {bet} рублей", reply_markup=keyboard)
            await state.finish()
        else:
            await message.answer("Ставка не может быть больше баланса\nПожалуйста, введите ставку снова:")
    elif message.text == "Выйти в главное меню":
        await state.finish()
        await cmd_start(message)
    else:
        await message.answer("Ставка должна быть натуральным числом\nПожалуйста, введите ставку снова:")


@dp.message_handler(lambda message: message.text in ["Красное", "Черное", "Zero", "Чётное", "Нечётное", "1st", "2nd", "3rd"] and db.get_bet(message.from_user.id) > db.get_balance(message.from_user.id))
async def bet_problem(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    bet = db.get_bet(message.from_user.id)
    await message.answer(f"Вы не можете играть со ставкой превышающей баланс\n"
                         f"Ваш баланс: {balance}\n"
                         f"Ваша ставка: {bet}")


@dp.message_handler(lambda message: message.text == "Красное")
async def casino_red(message: types.Message):
    bet = db.get_bet(message.from_user.id)
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
    bet = db.get_bet(message.from_user.id)
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
    bet = db.get_bet(message.from_user.id)
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
    bet = db.get_bet(message.from_user.id)
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
    bet = db.get_bet(message.from_user.id)
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
    bet = db.get_bet(message.from_user.id)
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
    bet = db.get_bet(message.from_user.id)
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
    bet = db.get_bet(message.from_user.id)
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