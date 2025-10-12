import random
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import LOGGER_ID, SUPPORT_CHANNEL, SUPPORT_CHAT
from ShrutixMusic import nand
from ShrutixMusic.utils.database import add_served_chat, get_assistant, delete_served_chat

WELCOME_LINES = [
    "🎉 Woohoo! I'm here to make your group more musical! 🎶",
    "🔥 The vibe just got upgraded! Let’s rock together 🎧",
    "💫 Ready to fill your group with music magic ✨",
    "🎵 I’m tuned in! Let’s start the rhythm 😍",
    "🚀 Music bot successfully landed in your group 💥",
]

GOODBYE_LINES = [
    "👋 I’m leaving, but the music never dies 🎶",
    "😔 Seems like my rhythm wasn’t needed here anymore...",
    "💔 The stage goes silent as I exit...",
    "🌙 Time to take a musical break from this group 🎧",
    "🎵 I’m out, but your vibes will echo forever 💫",
]


@nand.on_message(filters.new_chat_members, group=-10)
async def join_watcher(_, message):
    try:
        userbot = await get_assistant(message.chat.id)
        for member in message.new_chat_members:
            if member.id == nand.id:
                count = await nand.get_chat_members_count(message.chat.id)
                username = message.chat.username if message.chat.username else "Private Group"

                invite_link = ""
                try:
                    if not message.chat.username:
                        link = await nand.export_chat_invite_link(message.chat.id)
                        invite_link = f"\n🔗 <b>Invite Link:</b> {link}" if link else ""
                except:
                    pass

                welcome_line = random.choice(WELCOME_LINES)

                caption = (
                    f"✨ <b>New Connection Established!</b>\n\n"
                    f"{welcome_line}\n\n"
                    f"🎶 <b>Bot Joined:</b> {message.chat.title}\n"
                    f"🆔 <b>Chat ID:</b> <code>{message.chat.id}</code>\n"
                    f"👥 <b>Total Members:</b> {count}\n"
                    f"🙋‍♂️ <b>Added By:</b> {message.from_user.mention}\n"
                    f"{invite_link}\n\n"
                    f"🚀 <b>Status:</b> <i>Activated & Ready!</i>\n"
                    f"#Added"
                )

                buttons = [
                    [
                        InlineKeyboardButton("🙋 Added By", url=f"tg://openmessage?user_id={message.from_user.id}")
                    ],
                    [
                        InlineKeyboardButton("🎧 Support Channel", url=SUPPORT_CHANNEL),
                        InlineKeyboardButton("💬 Support Chat", url=SUPPORT_CHAT),
                    ],
                ]

                await nand.send_message(
                    LOGGER_ID,
                    text=caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )

                await add_served_chat(message.chat.id)
                if username:
                    await userbot.join_chat(f"@{username}")

    except Exception as e:
        print(f"[JOIN ERROR] {e}")

@nand.on_message(filters.left_chat_member, group=-12)
async def on_left_chat_member(_, message):
    try:
        userbot = await get_assistant(message.chat.id)
        left_member = message.left_chat_member

        if left_member and left_member.id == (await nand.get_me()).id:
            removed_by = message.from_user.mention if message.from_user else "Unknown User"

            goodbye_line = random.choice(GOODBYE_LINES)

            caption = (
                f"❌ <b>Music Bot Removed!</b>\n\n"
                f"{goodbye_line}\n\n"
                f"🎶 <b>Group Name:</b> {message.chat.title}\n"
                f"🆔 <b>Chat ID:</b> <code>{message.chat.id}</code>\n"
                f"🙋‍♂️ <b>Removed By:</b> {removed_by}\n\n"
                f"💤 <b>Status:</b> <i>Disconnected & Sleeping...</i>\n"
                f"#Left"
            )

            buttons = [
                [
                    InlineKeyboardButton("🎧 Support Channel", url=SUPPORT_CHANNEL),
                    InlineKeyboardButton("💬 Support Chat", url=SUPPORT_CHAT),
                ]
            ]

            await nand.send_message(
                LOGGER_ID,
                text=caption,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            await delete_served_chat(message.chat.id)
            await userbot.leave_chat(message.chat.id)

    except Exception as e:
        print(f"[LEFT ERROR] {e}")
