from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup()
main_keyboard.add(*["Бизнес", "Работа","Магазин","Казино", 'Лидербоард', 'Получить мой id', 'Перевести другу'])

business_keyboard = ReplyKeyboardMarkup()
business_keyboard.add(*["Купить бизнес", "Управление бизнесом","Выйти в главное меню"])

work_keyboard = ReplyKeyboardMarkup()
work_keyboard.add(*["Пропустить задание", "Я устал, Босс"])

back_keyboard = ReplyKeyboardMarkup()
back_keyboard.add(*["Выйти в главное меню"])

casion_keyboard = ReplyKeyboardMarkup()
casion_keyboard.add(*["Изменить ставку", "Красное", "Черное", "Zero", "Чётное", "Нечётное",
                "1st", "2nd", "3rd", "Выйти в главное меню"])

shop_keyboard = ReplyKeyboardMarkup()
shop_keyboard.add(*['Обувь', 'Футболки', 'Шапки', 'Дома', "Выйти в главное меню"])

businesses_keyboard = ReplyKeyboardMarkup()
businesses_keyboard.add(*["Шаурмичная", "Завод пива", "Крупнейшая IT-компания"])

start_work_keyboard = ReplyKeyboardMarkup()
start_work_keyboard.add(*["Приступить к работе", "Выйти в главное меню"])

work_types_keyboard = ReplyKeyboardMarkup()
work_types_keyboard.add(*["Препод по линалу"])

business_manage_keyboard = ReplyKeyboardMarkup()
business_manage_keyboard.add(*["Продать бизнес", "Информация о бизнесе","Купить сырьё на все деньги","Вывести деньги", "Напасть на чужой бизнес", "Назад"])

sell_business_keyboard = ReplyKeyboardMarkup()
sell_business_keyboard.add(*["Да, я хочу продать свой бизнес", "Нет, я передумал"])

attack_business_keyboard = ReplyKeyboardMarkup()
attack_business_keyboard.add(*["Выстрелить"])