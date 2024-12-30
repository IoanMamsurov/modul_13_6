import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

api = '8089127395:AAHteEiAwWpG-JiYyw3VjIGS39mG8Qv58dE'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
button = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(button, button_2)
in_kb = InlineKeyboardMarkup(resize_keyboard=True)
in_button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
in_kb.add(in_button_1, in_button_2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию: ', reply_markup=in_kb)

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст: ')
    await call.answer()
    await UserState.age.set()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(f"Ваша норма каллорий:"
                         f" {float(data['age']) * 10 + 6.25 * float(data['growth']) - 5 * float(data['weight']) + 5}")
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Информация')
async def start(message):
    await message.answer('Здесь может быть любой текст')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)