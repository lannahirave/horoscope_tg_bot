#!/usr/bin/python3
import logging, asyncio
import parse, config
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()

# States
class Form(StatesGroup):
    type = State()  # Will be represented in storage as 'Form:gender'
    sign = State()  # Will be represented in storage as 'Form:name'
    day = State()  # Will be represented in storage as 'Form:age'


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
    if message.text.lower() not in config.types:
        await message.answer("Пожалуйста, выберите гороскоп, используя клавиатуру ниже.")
        return
    await state.update_data(type=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for sign in config.signs_zodiac:
        keyboard.add(sign)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await Form.next()
    await message.answer("Теперь выберите знак:", reply_markup=keyboard)
    
async def type_sign_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in config.signs_zodiac:
        await message.answer("Пожалуйста, выберите размер знак, используя клавиатуру ниже.")
        return
    await state.update_data(sign=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for day in config.days:
        keyboard.add(day)
    # Для последовательных шагов можно не указывать название состояния, обходясь next()
    await Form.next()
    await message.answer("Теперь выберите время:", reply_markup=keyboard)


async def type_sign_day_chosen(message: types.Message, state: FSMContext):
    if message.text.lower() not in config.days:
        await message.answer("Пожалуйста, выберите время, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    print(user_data)
    await message.answer(f"{parse.parse_zodiac1(user_data.get('type'), user_data.get('sign'), message.text.lower())}\n\
                           Новый гороскоп с помощью /start", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()

def register_handlers_zodiac(dp: Dispatcher):
    dp.register_message_handler(zodiac, commands="start", state="*")
    dp.register_message_handler(type_chosen, state=Form.type)
    dp.register_message_handler(type_sign_chosen, state=Form.sign)
    dp.register_message_handler(type_sign_day_chosen, state=Form.day)




logger = logging.getLogger(__name__)

# Регистрация команд, отображаемых в интерфейсе Telegram
# async def set_commands(bot: Bot):
#     commands = [
#         BotCommand(command="/start", description="Получить гороскоп "),
#     ]
#     await bot.set_my_commands(commands)


async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хэндлеров
    register_handlers_zodiac(dp)

    # Установка команд бота
    # await set_commands(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
