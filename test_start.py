import pytest
from unittest.mock import AsyncMock
from bot import shop, business_doner_kebab
from aiogram import types
import keyboards

@pytest.mark.asyncio
async def test_shop_handler():
    message = AsyncMock()
    await shop(message)
    
    message.answer.assert_called_with("Добро пожаловать в магазин!\nВыберите категорию товара", reply_markup=keyboards.shop_keyboard)
    
    
@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await business_doner_kebab(message)
    
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Купить \"Шаурмичную\"", "Назад"]
    keyboard.add(*buttons)
    
    message.answer.assert_called_with(f"Маленькая шаурмичная на окраине Москвы.\nСТОИМОСТЬ: 100000 рублей", reply_markup=keyboard)