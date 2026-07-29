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
        [InlineKeyboardButton('• ᴄʟɪᴄᴋ ғᴏʀ ᴍᴏʀᴇ •', url='https://t.me/Lazzy_Bots_Official')],
        [
            InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'), 
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs ↗️", url='https://t.me/Lazzy_Bots_Official')
        ],
        [InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ', url='https://t.me/Lazzy_Bots_Support')]
    ])

# Sub Keyboard for navigation callbacks
def build_sub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ", url="https://t.me/Minato_Assist_Bot")],
        [
            InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
            InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="start")
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
    loading_msg = await message.reply_text("<b>Lᴏᴀᴅɪɴɢ. </b>")
    await asyncio.sleep(0.4)
    await loading_msg.edit_text("<b>Lᴏᴀᴅɪɴɢ.. </b>")
    await asyncio.sleep(0.4)
    await loading_msg.edit_text("<b>Lᴏᴀᴅɪɴɢ... </b>")
    await asyncio.sleep(0.4)

    await loading_msg.delete()

    keyboard = build_start_keyboard()

    # Blockquote வடிவில் வடிவமைக்கப்பட்ட மெசேஜ் (user.mention என சரி செய்யப்பட்டது)
    caption_text = (
        f"<blockquote><b>Hᴇʏ, {user.mention}! Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴍᴏsᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ʀᴇɴᴀᴍᴇ ʙᴏᴛ!</b></blockquote>\n\n"
        f"<blockquote expandable><b>Wɪᴛʜ ᴍʏ ᴘᴏᴡᴇʀғᴜʟ ғᴇᴀᴛᴜʀᴇs, ʏᴏᴜ ᴄᴀɴ:-\n"
        f"• Aᴜᴛᴏʀᴇɴᴀᴍᴇ ғɪʟᴇs ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ғᴏʀᴍᴀᴛs.\n"
        f"• Aᴅᴅ ᴄᴀᴘᴛɪᴏɴs ᴏʀ sᴇʟᴇᴄᴛ ᴛʜᴜᴍʙɴᴀɪʟs.\n"
        f"• Pʀᴏᴄᴇss ғɪʟᴇs sᴇǫᴜᴇɴᴛɪᴀʟʟʏ ғᴏʀ sᴍᴏᴏᴛʜ ᴡᴏʀᴋғʟᴏᴡ.</b></blockquote>\n\n"
        f"<blockquote><b>🔷 Rᴇᴀᴅʏ ᴛᴏ ʙᴇɢɪɴ? ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴀɴʏ ғɪʟᴇ!\n"
        f"🔷 Fᴏʀ ᴅᴇᴛᴀɪʟs, ᴛᴀᴘ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ.</b></blockquote>"
    )

    # 3. Send photo with Spoiler (has_spoiler=True)
    sent_msg = None
    if Config.START_PIC:
        try:
            sent_msg = await message.reply_photo(
                photo=Config.START_PIC, 
                caption=caption_text, 
                reply_markup=keyboard,
                has_spoiler=True
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

    # 4. Add sparkle reaction
    if sent_msg:
        await add_sparkle_reaction(sent_msg)

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    user_mention = query.from_user.mention
    sub_keyboard = build_sub_keyboard()

    if data == "start":
        caption_text = (
            f"<blockquote><b>Hᴇʏ, {user_mention}! Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴍᴏsᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ʀᴇɴᴀᴍᴇ ʙᴏᴛ!</b></blockquote>\n\n"
            f"<blockquote expandable><b>Wɪᴛʜ ᴍʏ ᴘᴏᴡᴇʀғᴜʟ ғᴇᴀᴛᴜʀᴇs, ʏᴏᴜ ᴄᴀɴ:-\n"
            f"• Aᴜᴛᴏʀᴇɴᴀᴍᴇ ғɪʟᴇs ᴡɪᴛʜ ᴄᴜsᴛᴏᴍ ғᴏʀᴍᴀᴛs.\n"
            f"• Aᴅᴅ ᴄᴀᴘᴛɪᴏɴs ᴏʀ sᴇʟᴇᴄᴛ ᴛʜᴜ姆ɴᴀɪʟs.\n"
            f"• Pʀᴏᴄᴇss ғɪʟᴇs sᴇǫᴜᴇɴᴛɪᴀʟʟʏ ғᴏʀ sᴍᴏᴏᴛʜ ᴡᴏʀᴋғʟᴏᴡ.</b></blockquote>\n\n"
            f"<blockquote><b>🔷 Rᴇᴀᴅʏ ᴛᴏ ʙᴇɢɪɴ? ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴀɴʏ ғɪʟᴇ!\n"
            f"🔷 Fᴏʀ ᴅᴇᴛᴀɪʟs, ᴛᴀᴘ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ.</b></blockquote>"
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
        help_text = f"<blockquote>{Txt.HELP_TXT}</blockquote>"
        if query.message.photo:
            await query.message.edit_caption(
                caption=help_text,
                reply_markup=sub_keyboard
            )
        else:
            await query.message.edit_text(
                text=help_text, 
                disable_web_page_preview=True,
                reply_markup=sub_keyboard
            )    
            
    elif data == "about":
        about_text = f"<blockquote>{Txt.ABOUT_TXT.format(client.mention)}</blockquote>"
        if query.message.photo:
            await query.message.edit_caption(
                caption=about_text,
                reply_markup=sub_keyboard
            )
        else:
            await query.message.edit_text(
                text=about_text,
                disable_web_page_preview=True,
                reply_markup=sub_keyboard
            )
            
    elif data == "admins":
        admins_text = f"<blockquote>{Txt.ADMINS_TXT}</blockquote>"
        if query.message.photo:
            await query.message.edit_caption(
                caption=admins_text,
                reply_markup=sub_keyboard
            )
        else:
            await query.message.edit_text(
                text=admins_text,
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
