import config
import logging
import time
from db import DB
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from random import randint
from task_generator import generate_task
from PIL import Image
import keyboards

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)

db = DB()


class FSMBet(StatesGroup):
    bet = State()

class FSMWork(StatesGroup):
    task = State()
    
class FSMTransaction(StatesGroup):
    get_id = State()
    get_amount = State()

def get_my_photo(user_id):
    user = db.get_user(user_id)
    shoes_id = user[3]
    tshort_id = user[4]
    hat_id = user[5]
    house_id = user[6]

    
    if house_id != -1:
        house_id = db.get_shop_item(house_id)[-1]
        img = Image.open(f'shop_items/house/{house_id}.png')
    else:
        img = Image.new("RGB", (1920, 1080), (255, 255, 255))
    
    man = Image.open('shop_items/man.png')
    img.paste(man, (0, 200), man)
    
    if shoes_id != -1:
        shoes_id = db.get_shop_item(shoes_id)[-1]
        shoes = Image.open(f'shop_items/shoes/{shoes_id}.png')
        img.paste(shoes, (0, 200), shoes)
    
    if tshort_id != -1:
        tshort_id = db.get_shop_item(tshort_id)[-1]
        tshort = Image.open(f'shop_items/tshort/{tshort_id}.png')
        img.paste(tshort, (0, 200), tshort)
    
    if hat_id != -1:
        hat_id = db.get_shop_item(hat_id)[-1]
        hat = Image.open(f'shop_items/hat/{hat_id}.png')
        img.paste(hat, (0, 200), hat)

    
    img.save(f"shop_items/result/{house_id}_{shoes_id}_{tshort_id}_{hat_id}.png")
    return f"shop_items/result/{house_id}_{shoes_id}_{tshort_id}_{hat_id}.png"


@dp.message_handler(lambda message: message.text == "Выйти в главное меню")
async def main_menu(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    photo = open(get_my_photo(message.from_user.id), 'rb')
    await bot.send_photo(message.from_user.id, photo, 
                         caption=f"Ты в главном меню, {str(message.chat.first_name)}. У тебя на счету {balance} рублей", reply_markup=keyboards.main_keyboard)
    
    
@dp.message_handler(commands = "start")
async def cmd_start(message: types.Message):
    db.append_user(message.from_user.id)
    await main_menu(message)


@dp.message_handler(lambda message: message.text == "Получить мой id")
async def get_my_id(message: types.Message):
    await message.answer(message.from_user.id)

@dp.message_handler(lambda message: message.text == "Перевести другу")
async def transact_to_friend(message: types.Message):
    await FSMTransaction.get_id.set()
    await message.answer('Введи id друга, он может его получить в главном меню', reply_markup=keyboards.back_keyboard)

@dp.message_handler(lambda message: message.text == "Выйти в главное меню", state=FSMTransaction.all_states)
async def out_fsm(message: types.Message, state: FSMContext):
    await state.finish()
    await main_menu(message)
            
@dp.message_handler(content_types=["text"], state=FSMTransaction.get_id)
async def input_id(message: types.Message, state: FSMContext):
    if message.text.isdigit() == False:
        await message.answer('Id болжен быть натуральное число')
    else:
        user = db.get_user(message.text)
        if user == None:
            await message.answer('Пользователем с таким id не найден. Попробуйте еще раз')
        else:
            async with state.proxy() as data:
                data['to_user'] = int(message.text)
            await FSMTransaction.get_amount.set()
            await message.answer('Сколько ты хочешь перевести?')

@dp.message_handler(state=FSMTransaction.get_amount)
async def input_amount(message: types.Message, state: FSMContext):
    if message.text.isdigit() == True:
        balance = db.get_balance(message.from_user.id)
        if int(message.text) > balance:
            await message.answer(f'У вас недостаточно средств. Ваш баланс {balance}')
        else:
            async with state.proxy() as data:
                db.set_balance(data['to_user'], db.get_balance(data['to_user'])+int(message.text))
                db.set_balance(message.from_user.id, db.get_balance(message.from_user.id)-int(message.text))
                
            await message.answer(f'Средства успено переведены')
            await state.finish()
            await main_menu(message)
    else:
        await message.answer('Введите натуральное число')
    
@dp.message_handler(lambda message: message.text =='Лидербоард')
async def business(message: types.Message):
    msg = ''
    c = 1
    for i in db.get_liderboard():
        usr = await bot.get_chat(i[0])
        msg += f'{c}. {usr.username} - {i[1]}\n'
        c += 1
    await message.answer(msg, reply_markup=keyboards.main_keyboard)
    

@dp.message_handler(lambda message: message.text == message.text in ["Бизнес", "Назад"])
async def business(message: types.Message):
    await message.answer(f"Привет, {str(message.chat.first_name)}!\nТы находишься в меню управления бизнесом\n"
                        f"У тебя на счету {db.get_balance(message.from_user.id)} рублей.", reply_markup=keyboards.business_keyboard)


@dp.message_handler(lambda message: message.text == "Купить бизнес")
async def business(message: types.Message):
    business = db.get_business_id(message.from_user.id)
    if business in [-1, None]:
        await message.answer(f"Какой бизнес хочешь купить?", reply_markup=keyboards.businesses_keyboard)
    else:
        await message.answer(f"У тебя уже есть свой бизнес")


@dp.message_handler(lambda message: message.text == "Шаурмичная")
async def business_doner_kebab(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Купить \"Шаурмичную\"", "Назад"]
    keyboard.add(*buttons)
    await message.answer(f"Маленькая шаурмичная на окраине Москвы.\nСТОИМОСТЬ: 100000 рублей", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Завод пива")
async def business_factory(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Купить \"Завод пива\"", "Назад"]
    keyboard.add(*buttons)
    await message.answer(f"Завод пива в Подмосковье.\nСТОИМОСТЬ: 5000000 рублей", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Крупнейшая IT-компания")
async def business_IT(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Купить \"Крупнейшая IT-компания\"", "Назад"]
    keyboard.add(*buttons)
    await message.answer(f"Крупнейшая IT-компания основанная в Москве.\nСТОИМОСТЬ: 100000000 рублей", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Купить \"Шаурмичную\"")
async def buy_business_doner_kebab(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    if balance >= 100000:
        db.set_balance(message.from_user.id, balance - 100000)
        db.set_business_id(message.from_user.id, 1)
        await message.answer(f"Поздравляю с покупкой!\nУ тебя на счету осталось {db.get_balance(message.from_user.id)} рублей", reply_markup=keyboards.business_keyboard)
    else:
        await message.answer(f"У тебя не хватает средств :(", reply_markup=keyboards.business_keyboard)


@dp.message_handler(lambda message: message.text == "Купить \"Завод пива\"")
async def buy_business_factory(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    if balance >= 5000000:
        db.set_balance(message.from_user.id, balance - 5000000)
        db.set_business_id(message.from_user.id, 2)
        await message.answer(f"Поздравляю с покупкой!\nУ тебя на счету осталось {db.get_balance(message.from_user.id)}  рублей", reply_markup=keyboards.business_keyboard)
    else:
        await message.answer(f"У тебя не хватает средств :(", reply_markup=keyboards.business_keyboard)


@dp.message_handler(lambda message: message.text == "Купить \"Крупнейшая IT-компания\"")
async def buy_business_IT(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    if balance >= 100000000:
        db.set_balance(message.from_user.id, balance - 100000000)
        db.set_business_id(message.from_user.id, 3)
        await message.answer(f"Поздравляю с покупкой!\nУ тебя на счету осталось {db.get_balance(message.from_user.id)}  рублей", reply_markup=keyboards.business_keyboard)
    else:
        await message.answer(f"У тебя не хватает средств :(", reply_markup=keyboards.business_keyboard)


@dp.message_handler(lambda message: message.text in ["Управление бизнесом", "Нет, я передумал"])
async def lead(message: types.Message):
    if db.get_business_id(message.from_user.id) == 1:
        await message.answer(f"Привет, здесь ты можешь управлять своим бизнеcом:\nШаурмичная\nБаланс бизнеса: {db.get_business_balance(message.from_user.id)}\n"
                             f"Занято мест на складе: {db.get_business_raw_materials(message.from_user.id)}/100", reply_markup=keyboards.business_manage_keyboard)
    elif db.get_business_id(message.from_user.id) == 2:
        await message.answer(f"Привет, здесь ты можешь управлять своим бизнеcом:\nЗавод пива\nБаланс бизнеса: {db.get_business_balance(message.from_user.id)}\n"
                             f"Занято мест на складе: {db.get_business_raw_materials(message.from_user.id)}/300", reply_markup=keyboards.business_manage_keyboard) 
    elif db.get_business_id(message.from_user.id) == 3:
        await message.answer(f"Привет, здесь ты можешь управлять своим бизнеcом:\nКрупнейшая IT-компания\nБаланс бизнеса: {db.get_business_balance(message.from_user.id)}\n"
                             f"Занято мест на складе: {db.get_business_raw_materials(message.from_user.id)}/1000", reply_markup=keyboards.business_manage_keyboard)
    else:
        await message.answer(f"У тебя ещё нет своего бизнеса")

@dp.message_handler(lambda message: message.text == "Вывести деньги")
async def take_money(message: types.Message):
    if db.get_business_balance(message.from_user.id) > 0:
        db.set_balance(message.from_user.id, db.get_balance(message.from_user.id) + db.get_business_balance(message.from_user.id))
        await message.answer(f"Тебе на счёт поступило {db.get_business_balance(message.from_user.id)} рублей.\nУ тебя на счету {db.get_balance(message.from_user.id)} рублей")
        db.set_business_balance(message.from_user.id, 0)
    else:
        await message.answer(f"На счету твоего бизнеса нет денег")

@dp.message_handler(lambda message: message.text == "Информация о бизнесе")
async def business_info(message: types.Message):
    Time = time.time()
    if db.get_business_id(message.from_user.id) == 1:
        if Time - db.get_last_online(message.from_user.id) >= 100:
            db.set_business_balance(message.from_user.id, db.get_business_balance(message.from_user.id) + db.get_business_raw_materials(message.from_user.id)*100)
            db.set_business_raw_materials(message.from_user.id, 0)
            await message.answer(f"Информация о твоём бизнесе\nБизнес: Шаурмичная\nБаланс бизнеса: {db.get_business_balance(message.from_user.id)}\nЗанятых мест на складе: {db.get_business_raw_materials(message.from_user.id)}")
        else:
            await message.answer(f"Информация о твоём бизнесе\nБизнес: Шаурмичная\nБаланс бизнеса: {db.get_business_balance(message.from_user.id)}\nЗанятых мест на складе: {db.get_business_raw_materials(message.from_user.id)}\nДо получения прибыли осталось {round(100 - Time + db.get_last_online(message.from_user.id))} секунд")
    elif db.get_business_id(message.from_user.id) == 2:
        if Time - db.get_last_online(message.from_user.id) >= 300:
            db.set_business_balance(message.from_user.id, db.get_business_balance(message.from_user.id) + db.get_business_raw_materials(message.from_user.id)*100)
            db.set_business_raw_materials(message.from_user.id, 0)
            await message.answer(f"Информация о твоём бизнесе\nБизнес: Завод пива\nБаланс бизнеса: {db.get_business_balance(message.from_user.id)}\nЗанятых мест на складе: {db.get_business_raw_materials(message.from_user.id)}")
        else:
            await message.answer(f"Информация о твоём бизнесе\nБизнес: Завод пива\nБаланс бизнеса: {db.get_business_balance(message.from_user.id)}\nЗанятых мест на складе: {db.get_business_raw_materials(message.from_user.id)}\nДо получения прибыли осталось {round(300 - Time + db.get_last_online(message.from_user.id))} секунд")
    else:
        if Time - db.get_last_online(message.from_user.id) >= 1000:
            db.set_business_balance(message.from_user.id, db.get_business_balance(message.from_user.id) + db.get_business_raw_materials(message.from_user.id)*100)
            db.set_business_raw_materials(message.from_user.id, 0)
            await message.answer(f"Информация о твоём бизнесе\nБизнес: Крупнейшая IT-компания\nБаланс бизнеса: {db.get_business_balance(message.from_user.id)}\nЗанятых мест на складе: {db.get_business_raw_materials(message.from_user.id)}")
        else:
            await message.answer(f"Информация о твоём бизнесе\nБизнес: Крупнейшая IT-компания\nБаланс бизнеса: {db.get_business_balance(message.from_user.id)}\nЗанятых мест на складе: {db.get_business_raw_materials(message.from_user.id)}\nДо получения прибыли осталось {round(1000 - Time + db.get_last_online(message.from_user.id))} секунд")



@dp.message_handler(lambda message: message.text == "Купить сырьё на все деньги")
async def buy_materials(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    Time = time.time()
    if db.get_business_id(message.from_user.id) == 1:
        if db.get_business_raw_materials(message.from_user.id) == 100:
            await message.answer(f"У тебя забит склад! Подожди пока склад освободится")
        elif db.get_balance(message.from_user.id) >= 10000:
            db.set_balance(message.from_user.id, balance - 10000)
            db.set_last_online(message.from_user.id, Time)
            db.set_business_raw_materials(message.from_user.id, 100)
            await message.answer(f"Ты успешно купил сырьё!\nУ тебя на счету осталось {db.get_balance(message.from_user.id)}  рублей")
        else:
            await message.answer(f"У тебя не хватает средств :(")
    elif db.get_business_id(message.from_user.id) == 2:
        if db.get_business_raw_materials(message.from_user.id) == 300:
            await message.answer(f"У тебя забит склад! Подожди пока склад освободится")
        elif db.get_balance(message.from_user.id) >= 60000:
            db.set_balance(message.from_user.id, balance - 60000)
            db.set_last_online(message.from_user.id, Time)
            db.set_business_raw_materials(message.from_user.id, 300)
            await message.answer(f"Ты успешно купил сырьё!\nУ тебя на счету осталось {db.get_balance(message.from_user.id)}  рублей")
        else:
            await message.answer(f"У тебя не хватает средств :(")
    else:
        if db.get_business_raw_materials(message.from_user.id) == 1000:
            await message.answer(f"У тебя забит склад! Подожди пока склад освободится")
        elif db.get_balance(message.from_user.id) >= 500000:
            db.set_balance(message.from_user.id, balance - 500000)
            db.set_last_online(message.from_user.id, Time)
            db.set_business_raw_materials(message.from_user.id, 1000)
            await message.answer(f"Ты успешно купил сырьё!\nУ тебя на счету осталось {db.get_balance(message.from_user.id)}  рублей")
        else:
            await message.answer(f"У тебя не хватает средств :(")


@dp.message_handler(lambda message: message.text == "Напасть на чужой бизнес")
async def attack_business(message: types.Message):
    if db.get_balance(message.from_user.id) >= 100:
        await message.answer(f"Выбери откуда хочешь напасть:", reply_markup=keyboards.attack_business_keyboard)
    else:
        await message.answer(f"У тебя не хватает денег, на проведение операции")
    

@dp.message_handler(lambda message: message.text in ["Зайти с черного хода", "Высадиться на крышу"])
async def shoot(message: types.Message):
    if randint(1, 3) == 1:
        aim = db.get_random_user(message.from_user.id)
        user = await bot.get_chat(aim[0])
        db.set_balance(message.from_user.id, db.get_balance(message.from_user.id) + round(db.get_business_balance(aim[0])*0.05))
        db.set_business_balance(aim[0], round(db.get_business_balance(aim[0])*0.95))
        await message.answer(f"Ты успешно атаковал бизнес игрока {user.username}!\nТы заработал {round(db.get_business_balance(aim[0])*0.05)} рублей",  reply_markup=keyboards.business_manage_keyboard)
    else:
        db.set_balance(message.from_user.id, db.get_balance(message.from_user.id) - 100)
        await message.answer(f"Задание провалено!\nРасходы на операцию составили {100} рублей",  reply_markup=keyboards.business_manage_keyboard)


@dp.message_handler(lambda message: message.text == "Продать бизнес")
async def sell_business(message: types.Message):
    await message.answer(f"Ты уверен, что хочешь продать свой бизнес?\nТы получишь только 75% от стоимости бизнеса", reply_markup=keyboards.sell_business_keyboard)


@dp.message_handler(lambda message: message.text == "Да, я хочу продать свой бизнес")
async def sell_business1(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    if db.get_business_id(message.from_user.id) == 1:
        db.set_balance(message.from_user.id, balance + 0.75*100000 + db.get_business_balance(message.from_user.id))
        db.set_business_raw_materials(message.from_user.id, 0)
        db.set_business_id(message.from_user.id, -1)
        await message.answer(f"Привет, {str(message.chat.first_name)}!\nТы находишься в меню управления бизнесом.\n"
                            f"У тебя на счету {db.get_balance(message.from_user.id)} рублей.", reply_markup=keyboards.business_keyboard)
    elif db.get_business_id(message.from_user.id) == 2:
        db.set_balance(message.from_user.id, balance + 0.75*5000000 + db.get_business_balance(message.from_user.id))
        db.set_business_raw_materials(message.from_user.id, 0)
        db.set_business_id(message.from_user.id, -1)
        await message.answer(f"Привет, {str(message.chat.first_name)}!\nТы находишься в меню управления бизнесом.\n"
                            f"У тебя на счету {db.get_balance(message.from_user.id)} рублей.", reply_markup=keyboards.business_keyboard)
    else:
        db.set_balance(message.from_user.id, balance + 0.75*100000000 + db.get_business_balance(message.from_user.id))
        db.set_business_raw_materials(message.from_user.id, 0)
        db.set_business_id(message.from_user.id, -1)
        await message.answer(f"Привет, {str(message.chat.first_name)}!\nТы находишься в меню управления бизнесом.\n"
                            f"У тебя на счету {db.get_balance(message.from_user.id)} рублей.", reply_markup=keyboards.business_keyboard)


@dp.message_handler(lambda message: message.text == "Работа")
async def work(message: types.Message):
    await message.answer(f"Выбери кем ты хочешь работать", reply_markup=keyboards.work_types_keyboard)


@dp.message_handler(lambda message: message.text == "Препод по линалу")
async def teacher(message: types.Message):
    balance = db.get_balance(message.from_user.id)
    await message.answer(f"Привет, твоя задача считать опредеители матриц, справишься?"
                         f"За каждую правильно решённую задачу будешь получать по 1000 рублей. Твой баланс: {balance} рублей", reply_markup=keyboards.start_work_keyboard)


@dp.message_handler(lambda message: message.text == "Приступить к работе")
async def start_work(message: types.Message):
    Task = generate_task()
    db.set_work_answer(message.from_user.id, Task[1])
    db.set_start_work_time(message.from_user.id, time.time())
    await FSMWork.task.set()
    await message.answer(f"Найди определитель матрицы: {Task}", reply_markup=keyboards.work_keyboard) 


@dp.message_handler(lambda message: message.text == "Пропустить задание")
async def skip_work(message: types.Message):
    Task = generate_task()
    db.set_work_answer(message.from_user.id, Task[1])
    db.set_start_work_time(message.from_user.id, time.time())
    await FSMWork.task.set()
    await message.answer(f"Найди определитель матрицы: {Task}", reply_markup=keyboards.work_keyboard) 


@dp.message_handler(content_types=["text"], state=FSMWork.task)
async def get_bet(message: types.Message, state: FSMContext):
    if message.text == "Пропустить задание":
        Task = generate_task()
        db.set_work_answer(message.from_user.id, Task[1])
        db.set_start_work_time(message.from_user.id, time.time())
        await message.answer(f"Найди определитель матрицы: {Task}", reply_markup=keyboards.work_keyboard)
    elif str(message.text) == str(db.get_work_answer(message.from_user.id)):
        Task = generate_task()
        db.set_work_answer(message.from_user.id, Task[1])
        c = 1
        len_lid = len(db.get_liderboard_work())
        for i in db.get_liderboard_work():
            if i[0] == message.from_user.id:
                place = c
            c += 1
        db.set_balance(message.from_user.id, db.get_balance(message.from_user.id) + round(1000*(1 + place/len_lid)))
        db.set_average_work_time(message.from_user.id, (db.get_average_work_time(message.from_user.id)*db.get_done_work_count(message.from_user.id) + (time.time() - db.get_start_work_time(message.from_user.id))) / (db.get_done_work_count(message.from_user.id) + 1))
        db.set_done_work_count(message.from_user.id, db.get_done_work_count(message.from_user.id) + 1)
        await message.answer(f"Правильно! Ваш баланс: {db.get_balance(message.from_user.id)} рублей", reply_markup=keyboards.work_keyboard)
        await message.answer(f"Найди определитель матрицы: {Task}", reply_markup=keyboards.work_keyboard)
    elif message.text == "Я устал, Босс":
        await state.finish()
        await message.answer(f"Вы точно хотите уйти?", reply_markup=keyboards.back_keyboard)
    else:
        await message.answer(f"Увы, это неверный ответ. Попробуй ещё раз", reply_markup=keyboards.work_keyboard)


@dp.message_handler(lambda message: message.text == "Магазин")
async def shop(message: types.Message):
    await message.answer("Добро пожаловать в магазин!\nВыберите категорию товара", reply_markup=keyboards.shop_keyboard)

@dp.message_handler(lambda message: message.text in ['Обувь', 'Футболки', 'Шапки', 'Дома'])
async def shoes_shop(message: types.Message):
    item_type = {'Обувь':'shoes',
                 'Футболки':'tshort',
                 'Шапки':'hat', 
                 'Дома': 'house'}
    items = db.get_shop_item_by_type(item_type[message.text])
    await message.answer("В наличие имеются следующие товары:", reply_markup=keyboards.back_keyboard)
    for item in items:
        buy_kb = InlineKeyboardMarkup(row_width=1)
        buy_kb.add(InlineKeyboardButton(text='Купить', callback_data=f'buy{item[0]}'))
        photo = open(f'shop_items/{item_type[message.text]}/{item[-1]}.png', 'rb')
        await bot.send_photo(message.from_user.id, photo, 
                         caption=f"{item[1]}. Цена: {item[-2]}", reply_markup=buy_kb)

@dp.callback_query_handler(Text(startswith='buy'))
async def buy_item(callback: types.CallbackQuery):
    item_id = int(callback.data[3:])
    item = db.get_shop_item(item_id)
    user_balance = db.get_balance(callback.from_user.id)
    if item[-2] > user_balance:
        await callback.message.answer('У вас не достаточно средств')
    else:
        if item[2] == 'hat':
            db.set_hat(callback.from_user.id, item_id)
        elif item[2] == 'shoes':
            db.set_shoes(callback.from_user.id, item_id)
        elif item[2] == 'tshort':
            db.set_tshort(callback.from_user.id, item_id)
        else:
            db.set_house(callback.from_user.id, item_id)

        db.set_balance(callback.from_user.id, user_balance-item[-2])
        photo = open(get_my_photo(callback.from_user.id), 'rb')
        await bot.send_photo(callback.from_user.id, photo, 
                            caption=f"Покупка упешно совершена. У тебя на счету {user_balance-item[-2]} рублей", reply_markup=keyboards.main_keyboard)


@dp.message_handler(lambda message: message.text == "Казино")
async def roulette(message: types.Message):
    bet = db.get_bet(message.from_user.id)
    balance = db.get_balance(message.from_user.id)
    await message.answer(f"Ваш баланс: {balance} рублей\nВаша ставка: {bet} рублей", reply_markup=keyboards.casion_keyboard)


@dp.message_handler(lambda message: message.text == "Изменить ставку")
async def change_bet(message: types.Message):
    await FSMBet.bet.set()
    await message.answer("Введите ставку (натуральное число):", reply_markup=keyboards.back_keyboard)


@dp.message_handler(content_types=["text"], state=FSMBet.bet)
async def get_bet(message: types.Message, state: FSMContext):
    balance = db.get_balance(message.from_user.id)
    if message.text.isdigit():
        bet = int(message.text)
        if bet <= balance:
            db.set_bet(message.from_user.id, int(message.text))
            await message.answer(f"Ваш баланс: {balance} рублей\nВаша ставка: {bet} рублей", reply_markup=keyboards.casion_keyboard)
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