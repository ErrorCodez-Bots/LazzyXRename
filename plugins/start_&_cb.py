import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    CallbackQuery, 
    WebAppInfo
)
from helper.database import db
from config import Config, Txt  


# பச்சைக் கலர் (Web App) மற்றும் சாதாரண பட்டன்கள் அமைக்கும் முறை
def build_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        # WebAppInfo கொடுத்தா டெலிகிராம்ல பட்டன் பச்சைக் கலர்ல (Green) மாறும்
        [InlineKeyboardButton('⚡ Updates Channel ⚡', web_app=WebAppInfo(url='https://t.me/Lazzy_Bots_Official/'))],
        [
            InlineKeyboardButton("About 😎", callback_data='about'), 
            InlineKeyboardButton("⚙️ Help", callback_data='help')
        ],
        [InlineKeyboardButton('❤️‍🔥 Support Group ❤️‍🔥', web_app=WebAppInfo(url='https://t.me/Lazzy_Bots_Support/'))],
        [InlineKeyboardButton("Admins 🧐", callback_data='admins')]
    ])

def build_sub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❣️ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", web_app=WebAppInfo(url="https://t.me/Minato_Assist_Bot/"))],
        [
            InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data="close"),
            InlineKeyboardButton("⛔ Bᴀᴄᴋ", callback_data="start")
        ]
    ])


@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await db.add_user(client, message)

    # 1. லோடிங் அனிமேஷன்
    loading_msg = await message.reply_text("<b>Lᴏᴀᴅɪɴɢ. ✨</b>")
    await asyncio.sleep(0.4)
    await loading_msg.edit_text("<b>Lᴏᴀᴅɪɴɢ.. ✨</b>")
    await asyncio.sleep(0.4)
    await loading_msg.edit_text("<b>Lᴏᴀᴅɪɴɢ... ✨</b>")
    await asyncio.sleep(0.4)

    # லோடிங் மெசேஜை நீக்குதல்
    await loading_msg.delete()

    keyboard = build_start_keyboard()
    caption_text = Txt.START_TXT.format(user.mention)

    # 2. மெசேஜ் அனுப்பிட்டு அதுக்கு ரியாக்ஷன் சேர்ப்பது
    if Config.START_PIC:
        sent_msg = await message.reply_photo(Config.START_PIC, caption=caption_text, reply_markup=keyboard)       
    else:
        sent_msg = await message.reply_text(text=caption_text, reply_markup=keyboard, disable_web_page_preview=True)

    # பயனர் மெசேஜ் & பாட் மெசேஜ் இரண்டிற்கும் ✨ ரியாக்ஷன்
    try:
        await message.react("✨")
        await sent_msg.react("✨")
    except Exception:
        pass


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
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
