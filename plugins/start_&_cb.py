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

 await add_sparkle_reaction(message)

 loading_msg = await message.reply_text("<b>Loading. ✨</b>")
 await asyncio.sleep(0.4)
 await loading_msg.edit_text("<b>Loading.. ✨</b>")
 
