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

# Main Start Keyboard with WebApp buttons matching your layout
def build_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('• CLICK FOR MORE •', web_app=WebAppInfo(url='https://t.me/Lazzy_Bots_Official/'))],
        [
            InlineKeyboardButton("HELP", callback_data='help'), 
            InlineKeyboardButton("UPDATES ↗️", web_app=WebAppInfo(url='https://t.me/Lazzy_Bots_Official/'))
        ],
        [InlineKeyboardButton('DONATE', web_app=WebAppInfo(url='https://t.me/Lazzy_Bots_Support/'))]
    ])

# Sub Keyboard for navigation callbacks
def build_sub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❣️ Source Code", web_app=WebAppInfo(url="https://t.me/Minato_Assist_Bot/"))],
        [
            InlineKeyboardButton("🔒 Close", callback_data="close"),
            InlineKeyboardButton("⛔ Back", callback_data="start")
        ]
    ])

# Helper function to react with Twinkling Stars (✨) near the timestamp
async def add_sparkle_reaction(message):
    try:
        await message.react("✨")
    except Exception:
        try:
            await message.react(emoji="✨")
        except Exception:
            pass

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user = message.from_user
    await db.add_user(client, message)

    # 1. Add reaction to user's /start command message
    await add_sparkle_reaction(message)

    # 2. Loading animation
    loading_msg = await message.reply_text("<b>Loading. ✨</b>")
    await asyncio.sleep(0.4)
    await loading_msg.edit_text("<b>Loading.. ✨</b>")
    await asyncio.sleep(0.4)
    await loading_msg.edit_text("<b>Loading... ✨</b>")
    await asyncio.sleep(0.4)

    await loading_msg.delete()

    keyboard = build_start_keyboard()

    caption_text = (
        f"<b>HEY, {user.mention}! WELCOME TO THE MOST ADVANCED RENAME BOT!</b>\n\n"
        f"<b>WITH MY POWERFUL FEATURES, YOU CAN:-</b>\n"
        f"<b>• AUTORENAME FILES WITH CUSTOM FORMATS.</b>\n"
        f"<b>• ADD CAPTIONS OR SELECT THUMBNAILS.</b>\n"
        f"<b>• PROCESS FILES SEQUENTIALLY FOR SMOOTH WORKFLOW.</b>\n\n"
        f"<b>🔷 READY TO BEGIN? JUST SEND ME ANY FILE!</b>\n"
        f"<b>🔷 FOR DETAILS, TAP THE HELP BUTTON BELOW.</b>"
    )

    # 3. Send photo/text message
    if Config.START_PIC:
        sent_msg = await message.reply_photo(
            photo=Config.START_PIC, 
            caption=caption_text, 
            reply_markup=keyboard
        )       
    else:
        sent_msg = await message.reply_text(
            text=caption_text, 
            reply_markup=keyboard, 
            disable_web_page_preview=True
        )

    # 4. Add the twinkling star reaction to the photo/message timestamp
    await add_sparkle_reaction(sent_msg)

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    user_mention = query.from_user.mention
    sub_keyboard = build_sub_keyboard()

    if data == "start":
        caption_text = (
            f"<b>HEY, {user_mention}! WELCOME TO THE MOST ADVANCED RENAME BOT!</b>\n\n"
            f"<b>WITH MY POWERFUL FEATURES, YOU CAN:-</b>\n"
            f"<b>• AUTORENAME FILES WITH CUSTOM FORMATS.</b>\n"
            f"<b>• ADD CAPTIONS OR SELECT THUMBNAILS.</b>\n"
            f"<b>• PROCESS FILES SEQUENTIALLY FOR SMOOTH WORKFLOW.</b>\n\n"
            f"<b>🔷 READY TO BEGIN? JUST SEND ME ANY FILE!</b>\n"
            f"<b>🔷 FOR DETAILS, TAP THE HELP BUTTON BELOW.</b>"
        )
        await query.message.edit_text(
            text=caption_text,
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
