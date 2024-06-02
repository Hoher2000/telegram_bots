import sys
from dataclasses import dataclass
from random import randint
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
sys.path.insert(0, '/home/paulina/workspace/github.com/Hoher2000/telegram_bots')
from __token import token

@dataclass
class User:
    id: int = id
    in_game: bool = False
    secret_number: int | None = None
    attempts: int | None = None
    total_games: int = 0
    wins: int = 0

users = dict()
user_id = lambda message: message.from_user.id
bot = Bot(token)
dp = Dispatcher()
attempts = 5

@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )

    if message.from_user.id not in users:
        users[user_id(message)] = User(user_id(message))

@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {attempts} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )

    if message.from_user.id not in users:
        users[user_id(message)] = User(user_id(message))

@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    if message.from_user.id not in users:
        users[user_id(message)] = User(user_id(message))

    await message.answer(
        f'Всего игр сыграно: {users[user_id(message)].total_games}\n'
        f'Игр выиграно: {users[user_id(message)].wins}'
    )

@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if message.from_user.id not in users:
        users[user_id(message)] = User(user_id(message))
    if users[user_id(message)].in_game:
        users[user_id(message)].in_game= False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )

@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if message.from_user.id not in users:
        users[user_id(message)] = User(user_id(message))

    if not users[user_id(message)].in_game:
        users[user_id(message)].in_game = True
        users[user_id(message)].secret_number = randint(1, 100)
        users[user_id(message)].attempts = attempts
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )

@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if message.from_user.id not in users:
        users[user_id(message)] = User(user_id(message))

    if not users[user_id(message)].in_game:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )

@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if message.from_user.id not in users:
        users[user_id(message)] = User(user_id(message))

    if users[user_id(message)].in_game:
        if int(message.text) == users[user_id(message)].secret_number:
            users[user_id(message)].in_game = False
            users[user_id(message)].total_games += 1
            users[user_id(message)].wins += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[user_id(message)].secret_number:
            users[user_id(message)].attempts -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < users[user_id(message)].secret_number:
            users[user_id(message)].attempts -= 1
            await message.answer('Мое число больше')

        if users[user_id(message)].attempts == 0:
            users[user_id(message)].in_game = False
            users[user_id(message)].total_games += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[user_id(message)].secret_number}\n\nДавайте '
                f'сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')

@dp.message()
async def process_other_answers(message: Message):
    if message.from_user.id not in users:
        users[user_id(message)] = User(user_id(message))

    if users[user_id(message)].in_game:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )


if __name__ == '__main__':
    dp.run_polling(bot)