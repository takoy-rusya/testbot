from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    """Хэндлер срабатывает на команду /start"""
    await message.answer('Здарова, заебал. Чё надо?')


@dp.message(Command(commands=['settings']))
async def process_settings_command(message: Message):
    """Хэндлер срабатывает на команду /settings"""
    await message.answer("Я подскажу тебе с настройками")


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    """Хэндлер срабатывает на команду /help"""
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
        print(message.model_dump_json(indent=1, exclude_none=True))     #Печатает в терминал JSON
    except TypeError:
        await message.reply(
            text="Неподдерживаемый формат для send_copy"
        )


if __name__ == '__main__':
    dp.run_polling(bot)
