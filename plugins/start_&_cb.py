import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    CallbackQuery
)
from helper.database import db
from config import Config, Txt  

# Main Start Keyboard with fixed URL buttons
def build_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('• CLICK FOR MORE •', url='https://t.me/Lazzy_Bots_Official')],
        [
            InlineKeyboardButton("HELP", callback_data='help'), 
            InlineKeyboardButton("UPDATES ↗️", url='https://t.me/Lazzy_Bots_Official')
        ],
        [InlineKeyboardButton('DONATE', url='https://t.me/Lazzy_Bots_Support')]
    ])

# Sub Keyboard for navigation callbacks
def build_sub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❣️ Source Code", url="https://t.me/Minato_Assist_Bot")],
        [
            InlineKeyboardButton("🔒 Close", callback_data="close"),
            InlineKeyboardButton("⛔ Back", callback_data="start")
        ]
    ])

# Helper function to react with Twinkling Stars (✨)
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
   
    try:
        await db.add_user(client, message)
    except Exception as e:
        print(f"Database Error: {e}")

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

    # 3. Send photo/text message with fallback safety
    sent_msg = None
    if Config.START_PIC:
        try:
            sent_msg = await message.reply_photo(
                photo=Config.START_PIC, 
                caption=caption_text, 
                reply_markup=keyboard
            )
        except Exception as e:
            print(f"Photo sending failed, fallback to text: {e}")
            sent_msg = await message.reply_text(
                text=caption_text, 
                reply_markup=keyboard, 
                disable_web_page_preview=True
            )
    else:
        sent_msg = await message.reply_text(
            text=caption_text, 
            reply_markup=keyboard, 
            disable_web_page_preview=True
        )

    # 4. Add the twinkling star reaction to the photo/message timestamp
    if sent_msg:
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
        if query.message.photo:
            await query.message.edit_caption(
                caption=caption_text,
                reply_markup=build_start_keyboard()
            )
        else:
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
        caption_text = (
            f"<b>HEY, {user_mention}! WELCOME TO THE MOST ADVANCED RENAME BOT!</b>\n\n"
            f"<b>WITH MY POWERFUL FEATURES, YOU CAN:-</b>\n"
            f"<b>• AUTORENAME FILES WITH CUSTOM FORMATS.</b>\n"
            f"<b>• ADD CAPTIONS OR SELECT THUMBNAILS.</b>\n"
            f"<b>• PROCESS FILES SEQUENTIALLY FOR SMOOTH WORKFLOW.</b>\n\n"
            f"<b>🔷 READY TO BEGIN? JUST SEND ME ANY FILE!</b>\n"
            f"<b>🔷 FOR DETAILS, TAP THE HELP BUTTON BELOW.</b>"
        )
        if query.message.photo:
            await query.message.edit_caption(
                caption=caption_text,
                reply_markup=build_start_keyboard()
            )
        else:
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
