# import pytest

# from aiogram import Bot, Dispatcher
# from mocked_bot import MockedBot


# @pytest.fixture()
# def bot():
#     bot = MockedBot()
#     token = Bot.set_current(bot)
#     try:
#         yield bot
#     finally:
#         Bot.reset_current(token)


# @pytest.fixture()
# async def dispatcher():
#     dp = Dispatcher()
#     await dp.emit_startup()
#     try:
#         yield dp
#     finally:
#         await dp.emit_shutdown()