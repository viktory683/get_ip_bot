import subprocess

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor as ex
from requests import get

from private_variables import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

admins = {
    '389026886': 'bzglve'
}


@dp.message_handler(commands=['start'])
async def welcome_message(msg: types.Message):
    await msg.answer('Oh hi Mark')


@dp.message_handler(commands=['help'])
async def help_message(msg: types.Message):
    await msg.answer('Type \'ip\' to get your remote machine ip addresses')


@dp.message_handler(commands=['ip'], user_id=list(admins))
async def ip_message(msg: types.Message):
    ip_ext = get('https://api.ipify.org').content.decode('utf8')
    ip_loc = subprocess.run('ip a | grep \'[i]net \'', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').split(
            '\n')[1].strip().split()[1].split('/')[0]
    await msg.answer(f'Here is your ip\n{ip_loc}\n{ip_ext}')


@dp.message_handler(content_types=['text'])
async def text_message(msg: types.Message):
    print(list(admins), type(msg.from_user.id))
    if 'ip' in msg.text.lower():
        if str(msg.from_user.id) in list(admins):
            await ip_message(msg)
        else:
            await msg.answer('You are not authorized to perform this operation')
    else:
        await msg.answer('I don\'t understand')


if __name__ == '__main__':
    ex.start_polling(dp)
