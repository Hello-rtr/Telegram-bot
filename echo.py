import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = '8010459884:AAHM784b9ZjSE0IDNDpzUe6aiiuPA2AUFwY'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

user_games = {}

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Это игра 'Угадай число'!\nЯ загадаю число от 1 до 10, а ты должен его угадать.\nНапиши /play, чтобы начать!")

@dp.message(Command("play"))
async def start_game(message: types.Message):
    # Загадать число
    number_to_guess = random.randint(1, 10)
    user_games[message.from_user.id] = number_to_guess  # Сохранить загаднное число для пользователя
    await message.answer("Я загадал число от 1 до 10. Попробуй угадать!")

@dp.message()
async def guess_number(message: types.Message):
    user_id = message.from_user.id

    if user_id in user_games:
        try:
            guessed_number = int(message.text)
            if guessed_number < 1 or guessed_number > 10:
                await message.answer("Пожалуйста, введи число от 1 до 10.")
                return
            
            if guessed_number == user_games[user_id]:
                await message.answer("Поздравляю! Ты угадал число!")
                del user_games[user_id]  
            elif guessed_number < user_games[user_id]:
                await message.answer("Мое число больше! Попробуй снова.")
            else:
                await message.answer("Мое число меньше! Попробуй снова.")
        except ValueError:
            await message.answer("Пожалуйста, введи корректное число.")
    else:
        await message.answer("Чтобы начать игру, напиши /play.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())