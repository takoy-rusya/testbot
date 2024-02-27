from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import F
import random
from dotenv import load_dotenv
import os
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

ATTEMPTS = 5

user = {
    'in_game': False,
    'secret_number': None,
    'attempts': None,
    'total_games': 0,
    'wins': 0
}
positive_answer_list = ['да', 'давай', 'играем', 'сыграем', 'погнали']
negative_answer_list = ['не', 'не хочу', 'не буду', 'нет', 'не сегодня', 'не в этот раз', 'иди нахуй', 'иди на хуй',
                        'пошел в жопу', 'пошел на хуй', 'пошел нахуй']


def get_random_number() -> int:
    """Возвращает случайное число от 1 до 100"""
    return random.randint(1, 100)


def input_number_filter(message: Message):
    """Проверка нахождения вводимого числа в диапазоне от 1 до 100"""
    return message.text and message.text.isdigit() and 1 <= int(message.text) <= 100


@dp.message(CommandStart())
async def process_start_command(message: Message):
    """Хэндлер срабатывает на команду /start"""
    await message.answer(
        'Ещё один кожаный\nКороче я играю в игру "Угадай число"\n\n'
        'Если ты тупой и не понял из названия смысл игры, то жми /help, '
        'я там всё расскажу\n'
        'Будешь играть?'
    )


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    """Хэндлер срабатывает на команду /help"""
    await message.answer(
        f'Правила игры такие:\n\nЯ загадываю число от 1 до 100,'
        f'а тебе нужно его угадать\nУ тебя есть {ATTEMPTS} попыток\n\n'
        f'Доступные команды :\n/help - узнать правила\n/start - начать игру\n'
        f'/stat - узнать статистику\n/cancel - завершить игру\n\n'
        f'Сыграем, пёс?'
    )


@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    """Хэндлер срабатывает на команду /stat и возвращает статистику игры"""
    await message.answer(
        f'Всего завершенных игр: {user["total_games"]}\n'
        f'Количество побед:{user["wins"]}'
    )


@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    """Хэндлер срабатывает на команду /cancel и завершает игру"""
    if user['in_game']:
        user['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Жду возвращения'
        )
    else:
        await message.answer(
            'Ты и так не в игре. Не хочешь сыграть?'
        )


@dp.message(F.text.lower().in_(positive_answer_list))
async def process_positive_anser(message: Message):
    """Хэндлер срабатывает на позитивный ответ"""
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        user['attempts'] = ATTEMPTS
        await message.answer(
            'Ну что ж...\n\nЯ загадал число\n'
            'Докажи, что ты Ванга'
        )
    else:
        await message.answer(
            'В игре я могу реагировать только на твоё число,'
            'а так же на команды /stat и /cancel'
        )


@dp.message(F.text.lower().in_(negative_answer_list))
async def process_negativ_answer(message: Message):
    """Хэндлер срабатывает на негативный ответ"""
    if not user['in_game']:
        await message.answer(
            'Я знал, что ты слабак и тряпка\n'
            'Вернёшся, если захочешь доказать обратное'
        )
    else:
        await message.answer(
            'Ты долго будешь ещё гадать?\n'
            'Вводи число от 1 до 100'
        )


@dp.message(input_number_filter)
async def process_number_answer(message: Message):
    """Хэндлер обрабатывает вводимое число и возвращает ответ"""
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            user['in_game'] = False
            user['wins'] += 1
            user['total_games'] += 1
            await message.answer(
                'Дуракам везёт\n'
                'Ещё раз сыграем? Не боишься облажаться?'
            )

        elif int(message.text) < user['secret_number']:
            user['attempts'] -= 1
            await message.answer('Моё число больше')
        elif int(message.text) > user['secret_number']:
            user['attempts'] -= 1
            await message.answer('Моё число меньше')

        if user['attempts'] == 0:
            user['in_game'] = False
            user['total_games'] += 1
            await message.answer(
                f'Что ж... Я знал, что ты дно и не сможешь угадать\n'
                f'Я загадал {user["secret_number"]}\n\n'
                f'Докажешь, что ты не шелудивый пёс?'
            )
    else:
        await message.answer(
            'Мы ещё не играем, если ты не заметил'
        )


@dp.message()
async def process_another_answer(message: Message):
    """Хэндлер срабатывает на другие сообщения"""
    if user['in_game']:
        if input_number_filter:
            await message.answer("Ты что, дурак?\nДолжно быть число от 1 до 100")

    else:
        await message.answer(
            'Я такой же ограниченный бот, как и твой кругозор\n'
            'Может уже начнём играть и я тебе покажу твоё место?'
        )
if __name__ == '__main__':
    dp.run_polling(bot)
