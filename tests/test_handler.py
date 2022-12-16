import pytest
from unittest.mock import AsyncMock
from bot import business_doner_kebab, shop, attack_business, sell_business, work
from aiogram import types
import keyboards


@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await business_doner_kebab(message)
    
    keyboard = types.ReplyKeyboardMarkup()
    buttons = ["Купить \"Шаурмичную\"", "Назад"]
    keyboard.add(*buttons)
    
    message.answer.assert_called_with(f"Маленькая шаурмичная на окраине Москвы.\nСТОИМОСТЬ: 100000 рублей", reply_markup=keyboard)
    
    
@pytest.mark.asyncio
async def test_shop_handler():
    message = AsyncMock(text = AsyncMock())
    await shop(message)
    
    message.answer.assert_called_with("Добро пожаловать в магазин!\nВыберите категорию товара", reply_markup=keyboards.shop_keyboard)


@pytest.mark.asyncio
async def test_attack_business():
    message = AsyncMock()
    await attack_business(message)
    
    message.answer.assert_called_with("Выбери откуда хочешь напасть:", reply_markup=keyboards.attack_business_keyboard)
    
    
@pytest.mark.asyncio
async def test_sell_business():
    message = AsyncMock()
    await sell_business(message)
    
    message.answer.assert_called_with(f"Ты уверен, что хочешь продать свой бизнес?\nТы получишь только 75% от стоимости бизнеса", reply_markup=keyboards.sell_business_keyboard)
    
    
@pytest.mark.asyncio
async def test_work():
    message = AsyncMock()
    await work(message)
    
    message.answer.assert_called_with(f"Выбери кем ты хочешь работать", reply_markup=keyboards.work_types_keyboard)