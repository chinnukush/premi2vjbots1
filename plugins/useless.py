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
from plugins.dbusers import db

admin = filters.user(ADMINS)


#=====================================================================================##

START_TIME = datetime.now()

@Client.on_message(filters.command("stats") & admin)
async def stats(client, message: Message):
    total = await db.total_users_count()

    now = datetime.now()
    delta = now - START_TIME
    uptime = get_readable_time(int(delta.total_seconds()))

    await message.reply(
        f"""📊 **BOT STATISTICS**

👥 Total Users : {total}
⏰ Uptime : {uptime}
🤖 Pyrogram : {__version__}""")


#=====================================================================================##

WAIT_MSG = "<b>Working....</b>"

#=====================================================================================##


@Client.on_message(filters.command("users") & filters.private & admin)
async def get_users(client, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users_cursor = await db.get_all_users()
    users = await users_cursor.to_list(length=None)  # convert cursor to list
    await msg.edit(f"{len(users)} users are using this bot")
