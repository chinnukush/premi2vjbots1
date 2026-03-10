import asyncio
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from config import ADMINS
from pyrogram import filters

admin = filters.user(ADMINS)


#=====================================================================================##

@Client.on_message(filters.command('stats') & admin)
async def stats(bot: Bot, message: Message):

    users = await db.full_userbase()
    total = len(users)

    now = datetime.now()
    delta = now - bot.uptime
    uptime = get_readable_time(delta.seconds)

    await message.reply(f"""📊 **BOT STATISTICS**

👥 Total Users : {total}
⏰ Uptime : {uptime}
🤖 Pyrogram : {__version__}""")

#=====================================================================================##

WAIT_MSG = "<b>Working....</b>"

#=====================================================================================##


@Client.on_message(filters.command('users') & filters.private & admin)
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await db.full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

