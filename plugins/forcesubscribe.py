from config import AUTH_CHANNEL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

async def check_force_sub(bot, message):
    btn = []

    for channel_id in AUTH_CHANNEL:
        chat = await bot.get_chat(int(channel_id))

        try:
            await bot.get_chat_member(channel_id, message.from_user.id)

        except UserNotParticipant:
            btn.append([
                InlineKeyboardButton(
                    f"📢 Join {chat.title}",
                    url=chat.invite_link
                )
            ])

    # ❌ NOT JOINED
    if btn:
        username = (await bot.get_me()).username

        file_param = message.command[1] if len(message.command) > 1 else "start"

        btn.append([
            InlineKeyboardButton(
                "♻️ Try Again",
                url=f"https://t.me/{username}?start={file_param}"
            )
        ])

        await message.reply_text(
            f"👋 Hello {message.from_user.mention}\n\n"
            "⚠️ Please join all required channels to continue.",
            reply_markup=InlineKeyboardMarkup(btn)
        )

        return False  # ❗ important

    return True  # ✅ joined
