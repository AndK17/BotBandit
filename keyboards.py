from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup()
main_keyboard.add(*["Бизнес", "Работа","Магазин","Казино", 'Лидербоард'])

business_keyboard = ReplyKeyboardMarkup()
business_keyboard.add(*["Купить бизнес", "Управление бизнесом","Выйти в главное меню"])

work_keyboard = ReplyKeyboardMarkup()
work_keyboard.add(*["Пропустить задание", "Я устал, Босс"])

back_keyboard = ReplyKeyboardMarkup()
back_keyboard.add(*["Выйти в главное меню"])

casion_keyboard = ReplyKeyboardMarkup()
casion_keyboard.add(*["Изменить ставку", "Красное", "Черное", "Zero", "Чётное", "Нечётное",
                "1st", "2nd", "3rd", "Выйти в главное меню"])