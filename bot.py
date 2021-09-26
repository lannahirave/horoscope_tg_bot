#!/usr/bin/python3
import logging
import asyncio
import parse
import config
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types import InputFile
from aiogram.utils import executor


storage = MemoryStorage()


class Form(StatesGroup):
    type = State()  # Will be represented in storage as 'Form:type'
    sign = State()  # Will be represented in storage as 'Form:sign'
    day = State()  # Will be represented in storage as 'Form:day'


async def zodiac(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in config.types:
        keyboard.add(name)
    await message.answer("Выберите тип гороскопа:", reply_markup=keyboard)
    await Form.type.set()

# Обратите внимание: есть второй аргумент


async def type_chosen(message: types.Message, state: FSMContext):
    """
    FSM MACHINE START
    If user input for type is not correct, awaits new input
    then goes to choosing sign
    """
    if message.text not in config.types:
        await message.answer("Пожалуйста, выберите гороскоп, используя клавиатуру ниже.")
        return
    await state.update_data(type=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for sign in config.signs_zodiac:
        keyboard.add(sign)
    await Form.next()
    await message.answer("Теперь выберите знак:", reply_markup=keyboard)


async def type_sign_chosen(message: types.Message, state: FSMContext):
    """
    If user input for sign is not correct, await new input
    then goes to choosing time
    """
    if message.text not in config.signs_zodiac:
        await message.answer("Пожалуйста, выберите размер знак, используя клавиатуру ниже.")
        return
    await state.update_data(sign=message.text)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for day in config.days:
        keyboard.add(day)
    await Form.next()
    await message.answer("Теперь выберите время:", reply_markup=keyboard)


async def type_sign_day_chosen(message: types.Message, state: FSMContext):
    """
    if user input for time is not correct, awaits new input
    """
    if message.text not in config.days:
        await message.answer("Пожалуйста, выберите время, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    print(user_data, f"{'day:', message.text}")
    type, sign, day = parse.translate_ru_to_eng(
        user_data.get('type'), user_data.get('sign'), message.text)
    
    #get image for specified sign
    png = InputFile(f"images/{sign}.png")
    await message.answer_photo(photo=png, caption=f"{parse.parse_zodiac1(type, sign, day)}\nНовый гороскоп с помощью /start",
                               reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_zodiac(dp: Dispatcher):
    dp.register_message_handler(zodiac, commands="start", state="*")
    dp.register_message_handler(type_chosen, state=Form.type)
    dp.register_message_handler(type_sign_chosen, state=Form.sign)
    dp.register_message_handler(type_sign_day_chosen, state=Form.day)


"""
    Добавить комманду для ежедневного повтора событий
"""
logger = logging.getLogger(__name__)


async def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    bot = Bot(token=config.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_zodiac(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
