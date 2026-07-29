import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    CallbackQuery, 
    WebAppInfo,
    Reaction
)
from helper.database import db
from config import Config, Txt  

def build_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
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
        [InlineKeyboardButton("❣️ Source Code", web_app=WebAppInfo(url="https://t.me/Minato_Assist_Bot/"))],
        [
            InlineKeyboardButton("🔒 Close", callback_data="close"),
            InlineKeyboardButton("⛔ Back", callback_data="start")
        ]
    ])

# மெசேஜ்க்கு ரியாக்ஷன் (Reaction Emoji) ஆட் செய்யும் ஹெல்பர் ஃபங்க்ஷன்
async def add_sparkle_reaction(message):
    try:
        # முதல் முயற்சி: நேரடி எமோஜி
        await message.react("✨")
    except Exception:
        try:
            # இரண்டாம் முயற்சி: Reaction Object
            await message.react(emoji="✨")
        except Exception:
            pass

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await db.add_user(client, message)

    # 1. பயனர் அனுப்பிய /start மெசேஜ்க்கு ✨ ரியாக்ஷன் தருவது
    await add_sparkle_reaction(message)

    # 2. லோடிங் மெசேஜ் அனிமேஷன்
    loading_msg = await message.reply_text("<b>Loading. ✨</b>")
    await asyncio.sleep(0.4)
    await loading_msg.edit_text("<b>Loading.. ✨</b>")
    await asyncio.sleep(0.4)
    await loading_msg.edit_text("<b>Loading... ✨</b>")
    await asyncio.sleep(0.4)

    await loading_msg.delete()

    keyboard = build_start_keyboard()
    caption_text = Txt.START_TXT.format(user.mention)

    # 3. ஸ்டார்ட் மெசேஜ் அனுப்புதல்
    if Config.START_PIC:
        sent_msg = await message.reply_photo(Config.START_PIC, caption=caption_text, reply_markup=keyboard)       
    else:
        sent_msg = await message.reply_text(text=caption_text, reply_markup=keyboard, disable_web_page_preview=True)

    # 4. பாட் அனுப்பிய போட்டோ/மெசேஜின் டைம் பக்கத்தில் ✨ ரியாக்ஷன் ஆட் செய்வது
    await add_sparkle_reaction(sent_msg)

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
