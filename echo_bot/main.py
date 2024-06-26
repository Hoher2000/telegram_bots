from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import sys

sys.path.insert(0, '/home/paulina/workspace/github.com/Hoher2000/telegram_bots')
from __token import token

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather

BOT_TOKEN = token

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
# @dp.message(Command(commands=["start"])) можно с декоратором
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
# @dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
# @dp.message()
async def send_echo(message: Message):
    try:
        print(message.model_dump_json(indent=4, exclude_none=True))
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text='Method "send_copy" is not support this update type')


dp.message.register(process_start_command, Command(commands=["start"]))
dp.message.register(process_help_command, Command(commands=["help"]))
dp.message.register(send_echo)


if __name__ == '__main__':
    dp.run_polling(bot)