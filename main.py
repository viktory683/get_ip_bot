import contextlib
import subprocess

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand, Message
from aiogram.utils import executor as ex
from aiogram.utils.exceptions import NetworkError
from environs import Env
from requests import get

env = Env()
env.read_env(".env")

BOT_TOKEN: str = env.str("BOT_TOKEN")
admins_raw = env.list("ADMINS")
admins = list(map(int, admins_raw))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def welcome_message(msg: Message):
    await msg.answer("Oh hi Mark")


@dp.message_handler(commands=["help"])
async def help_message(msg: Message):
    await msg.answer("Type '/ip' or 'ip' to get your remote machine ip addresses")


@dp.message_handler(commands=["ip"], user_id=admins)
async def ip_message(msg: Message):
    ip_ext = get("https://api.ipify.org").content.decode("utf8")
    ip_loc = (
        subprocess.run("ip a | grep '[i]net '", shell=True, stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .splitlines()[1]
        .strip()
        .split()[1]
        .split("/")[0]
    )
    await msg.answer(f"`{ip_loc}`\n`{ip_ext}`", parse_mode="Markdown")


@dp.message_handler(content_types=["text"])
async def text_message(msg: Message):
    if "ip" in msg.text.lower():
        if msg.from_user.id in admins:
            await ip_message(msg)
        else:
            await msg.answer("You are not authorized to perform this operation")
    else:
        await msg.answer("I don't understand")


async def set_commands(*args, **kwargs):
    await dp.bot.set_my_commands([BotCommand("ip", "Get IP")])


if __name__ == "__main__":
    # while True:
    with contextlib.suppress(NetworkError):
        ex.start_polling(dp, on_startup=set_commands)
