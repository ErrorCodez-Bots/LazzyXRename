import asyncio
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from helper.database import db
from config import Config, Txt

# Helper function to generate standard navigation keymaps
def build_sub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❣️ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", url="https://t.me/Minato_Assist_Bot/")],
        [
            InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data="close"),
            InlineKeyboardButton("⛔ Bᴀᴄᴋ", callback_data="start")
        ]
    ])

# Helper function for main menu keymap
def build_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Updates Channel ⚡", url="https://t.me/Lazzy_Bots_Official/")],
        [
            InlineKeyboardButton("About 😎", callback_data="about"),
            InlineKeyboardButton("⚙️ Help", callback_data="help")
        ],
        [InlineKeyboardButton("❤️‍🔥 Support Group ❤️‍🔥", url="https://t.me/Lazzy_Bots_Support/")],
        [InlineKeyboardButton("Admins 🧐", callback_data="admins")]
    ])


@Client.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    user = message.from_user
    await db.add_user(client, message)

    # Animated loading effect
    loading_msg = await message.reply_text("<b>Lᴏᴀᴅɪɴɢ. ✨</b>")
    for dots in ["..", "..."]:
        await asyncio.sleep(0.4)
        await loading_msg.edit_text(f"<b>Lᴏᴀᴅɪɴɢ{dots} ✨</b>")
    await asyncio.sleep(0.4)

    # Optional reaction
    try:
        await message.react("✨")
    except Exception:
        pass

    # Clean up loading message
    await loading_msg.delete()

    # Send start response
    keyboard = build_start_keyboard()
    caption_text = Txt.START_TXT.format(user.mention)

    if Config.START_PIC:
        await message.reply_photo(photo=Config.START_PIC, caption=caption_text, reply_markup=keyboard)
    else:
        await message.reply_text(text=caption_text, reply_markup=keyboard, disable_web_page_preview=True)


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
    user_mention = query.from_user.mention
    sub_keyboard = build_sub_keyboard()

    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(user_mention),
            disable_web_page_preview=True,
            reply_markup=build_start_keyboard()
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=sub_keyboard
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=sub_keyboard
        )
    elif data == "admins":
        await query.message.edit_text(
            text=Txt.ADMINS_TXT,
            disable_web_page_preview=True,
            reply_markup=sub_keyboard
        )
    elif data == "close":
        try:
            await query.message.delete()
            if query.message.reply_to_message:
                await query.message.reply_to_message.delete()
        except Exception:
            pass
        except Exception:
            pass
