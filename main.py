import socket
import logging

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import BotCommand, Message
from aiogram.utils import executor as ex
from environs import Env
import aiohttp


logging.basicConfig(level=logging.INFO)

env = Env()
env.read_env(".env")

BOT_TOKEN: str = env.str("BOT_TOKEN")
admins_raw = env.list("ADMINS")
admins = list(map(int, admins_raw))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


async def get_ext_ip() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.ipify.org") as resp:
            return await resp.text()


@dp.message_handler(commands=["start"])
async def welcome_message(msg: Message):
    await msg.answer("Oh hi Mark")


@dp.message_handler(Text(equals="ip", ignore_case=True), user_id=admins)
@dp.message_handler(commands=["ip"], user_id=admins)
async def ip_handler(msg: Message):
    ip_msg = await msg.answer("Please wait\nGetting my ip...")

    ip_loc = get_local_ip()
    ip_ext = await get_ext_ip()

    await bot.edit_message_text(
        text=f"`{ip_loc}`\n`{ip_ext}`",
        message_id=ip_msg.message_id,
        chat_id=ip_msg.chat.id,
        parse_mode="Markdown",
    )


@dp.message_handler(content_types=["text"], user_id=admins)
async def text_handler(msg: Message):
    await msg.answer("I don't understand")


async def set_commands(_):
    await dp.bot.set_my_commands([BotCommand("ip", "Get IP")])


if __name__ == "__main__":
    ex.start_polling(dp, on_startup=set_commands)
