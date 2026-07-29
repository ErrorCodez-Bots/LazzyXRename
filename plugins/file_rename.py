from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db

from asyncio import sleep
from PIL import Image
import os
import time

MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_handler(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name or "file"

    if file.file_size > MAX_FILE_SIZE:
        return await message.reply_text("Sᴏʀʀy Bʀᴏ, Tʜɪꜱ Bᴏᴛ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 4GB.")

    try:
        await message.reply_text(
            text=f"**__Pʟᴇᴀꜱᴇ Eɴᴛᴇʀ NᴇW FɪʟᴇNᴀMᴇ...__**\n\n**Oʟᴅ Fɪʟᴇ Nᴀᴍᴇ** :- `{filename}`",
            reply_to_message_id=message.id,
            reply_markup=ForceReply(True)
        )
    except FloodWait as e:
        await sleep(e.value)
        await message.reply_text(
            text=f"**__Pʟᴇᴀꜱᴇ Eɴᴛᴇʀ NᴇW FɪʟᴇNᴀMᴇ...__**\n\n**Oʟᴅ Fɪʟᴇ Nᴀᴍᴇ** :- `{filename}`",
            reply_to_message_id=message.id,
            reply_markup=ForceReply(True)
        )
    except Exception:
        pass


async def force_reply_filter(_, client, message):
    if message.reply_to_message and message.reply_to_message.reply_markup:
        return isinstance(message.reply_to_message.reply_markup, ForceReply)
    return False


@Client.on_message(filters.private & filters.reply & filters.create(force_reply_filter))
async def rename_selection(client, message):
    reply_message = message.reply_to_message
    new_name = message.text.strip()
    await message.delete()

    msg = await client.get_messages(message.chat.id, reply_message.id)
    file = msg.reply_to_message
    if not file or not file.media:
        return await message.reply("Oʀɪɢɪɴᴀʟ ᴍᴇssᴀGᴇ ɴᴏᴛ Fᴏᴜɴᴅ.")

    media = getattr(file, file.media.value)

    if "." not in new_name:
        extn = media.file_name.rsplit('.', 1)[-1] if media.file_name and "." in media.file_name else "mkv"
        new_name = f"{new_name}.{extn}"

    await reply_message.delete()

    button = [[InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ", callback_data="upload_document")]]
    if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
        button.append([InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data="upload_video")])
    elif file.media == MessageMediaType.AUDIO:
        button.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data="upload_audio")])

    await message.reply(
        text=f"**Sᴇʟᴇᴄᴛ Tʜᴇ OᴜᴛPᴜT Fɪʟᴇ TʏPᴇ**\n**• Fɪʟᴇ NᴀMᴇ :-** `{new_name}`",
        reply_to_message_id=file.id,
        reply_markup=InlineKeyboardMarkup(button)
    )


@Client.on_callback_query(filters.regex("^upload_"))
async def rename_callback(bot, query):
    user_id = query.from_user.id
    raw_text = query.message.text
    
    if ":-" in raw_text:
        file_name = raw_text.split(":-", 1)[1].strip(" `")
    else:
        file_name = "renamed_file"

    download_dir = f"downloads/{user_id}_{int(time.time())}"
    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, file_name)

    file = query.message.reply_to_message
    if not file or not file.media:
        return await query.message.edit("Oʀɪɢɪɴᴀʟ mᴇᴅɪᴀ ɴᴏᴛ Fᴏᴜɴᴅ.")

    sts = await query.message.edit("TʀyɪɴG Tᴏ Dᴏᴡɴʟᴏᴀᴅ....")
    ph_path = None

    try:
        path = await file.download(
            file_name=file_path,
            progress=progress_for_pyrogram,
            progress_args=("Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time())
        )

        duration = 0
        try:
            metadata = extractMetadata(createParser(file_path))
            if metadata and metadata.has("duration"):
                duration = metadata.get('duration').seconds
        except Exception:
            pass

        media = getattr(file, file.media.value)
        db_caption = await db.get_caption(user_id)
        db_thumb = await db.get_thumbnail(user_id)

        if db_caption:
            try:
                caption = db_caption.format(
                    filename=file_name,
                    filesize=humanbytes(media.file_size),
                    duration=convert(duration)
                )
            except KeyError:
                caption = f"**{file_name}**"
        else:
            caption = f"**{file_name}**"

        if db_thumb:
            ph_path = await bot.download_media(db_thumb)
        elif getattr(media, "thumbs", None):
            ph_path = await bot.download_media(media.thumbs[0].file_id)

        if ph_path and os.path.exists(ph_path):
            img = Image.open(ph_path).convert("RGB")
            img.resize((320, 320))
            img.save(ph_path, "JPEG")

        await sts.edit("TʀyɪɴG Tᴏ UPLᴏᴀᴅ....")
        upload_type = query.data.split("_")[1]

        if upload_type == "document":
            await sts.reply_document(
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("UPLᴏᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time())
            )
        elif upload_type == "video":
            await sts.reply_video(
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("UPLᴏᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time())
            )
        elif upload_type == "audio":
            await sts.reply_audio(
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("UPLᴏᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time())
            )

        await sts.delete()

    except Exception as e:
        await sts.edit(f"**ERRᴏʀ:** `{e}`")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if ph_path and os.path.exists(ph_path):
            os.remove(ph_path)
        if os.path.exists(download_dir) and not os.listdir(download_dir):
            os.rmdir(download_dir)
 
    if (media.thumbs or db_thumb):
        if db_thumb:
            ph_path = await bot.download_media(db_thumb) 
        else:
            ph_path = await bot.download_media(media.thumbs[0].file_id)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")

    await sts.edit("Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....")
    type = query.data.split("_")[1]
    try:
        if type == "document":
            await sts.reply_document(
                document=file_path,
                thumb=ph_path, 
                caption=caption, 
                progress=progress_for_pyrogram,
                progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time())
            )
        elif type == "video": 
            await sts.reply_video(
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time())
            )
        elif type == "audio": 
            await sts.reply_audio(
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=("Uᴩʟᴏᴅ Sᴛᴀʀᴛᴇᴅ....", sts, time.time())
            )
    except Exception as e:          
        try: 
            os.remove(file_path)
            os.remove(ph_path)
            return await sts.edit(f" Eʀʀᴏʀ {e}")
        except: pass
        
    try: 
        os.remove(file_path)
        os.remove(ph_path)
        await sts.delete()
    except: pass
