#!/usr/bin/python3
import logging
import asyncio

from aiogram.types.reply_keyboard import KeyboardButton
import parse
import config
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile


class horoscope(Bot):
    def __init__(self, Bot):
        logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )
        logger.error("Starting bot")
        storage = MemoryStorage()
        dp = Dispatcher(Bot, storage=MemoryStorage())

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
            btns_array = []
            for name in config.types:
                btns_array.append(name)
                if len(btns_array) == 3:
                    keyboard.row(btns_array[0], btns_array[1], btns_array[2],)
                    btns_array.clear()
            keyboard.row(btns_array[0], btns_array[1])
            await message.answer("Выберите тип гороскопа:", reply_markup=keyboard)
            await Form.type.set()

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
            btns_array = []
            for name in config.signs_zodiac:
                btns_array.append(name)
                if len(btns_array) == 3:
                    keyboard.row(btns_array[0], btns_array[1], btns_array[2],)
                    btns_array.clear()
            keyboard.row(*btns_array)
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
            btns_array = []
            days = config.days
            user_data = await state.get_data()
            if user_data.get('type') in 'Тинейджер Флирт Амигос':
                days = days[:-2]
            for name in days:
                btns_array.append(name)
                if len(btns_array) == 3:
                    keyboard.row(btns_array[0], btns_array[1], btns_array[2],)
                    btns_array.clear()
            keyboard.row(*btns_array)
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

            # get image for specified sign
            png = InputFile(f"images/{sign}.png")
            self.png = png
            await message.answer_photo(photo=self.png, caption=f"{parse.parse_zodiac1(type, sign, day)}\nНовый гороскоп с помощью /start",
                                       reply_markup=types.ReplyKeyboardRemove())
            await state.finish()

        def register_handlers_zodiac(dp: Dispatcher):
            dp.register_message_handler(zodiac, commands="start", state="*")
            dp.register_message_handler(type_chosen, state=Form.type)
            dp.register_message_handler(type_sign_chosen, state=Form.sign)
            dp.register_message_handler(type_sign_day_chosen, state=Form.day)

        self.storage = storage
        self.Form = Form
        self.dp = dp
        register_handlers_zodiac(self.dp)


"""
    Добавить комманду для ежедневного повтора событий
"""


async def main():
    bot = horoscope(Bot(token=config.token))
    await bot.dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
