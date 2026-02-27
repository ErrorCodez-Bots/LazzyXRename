import re, os, time

id_pattern = re.compile(r'^.\d+$') 

class Config(object):
    # lazzy client config
    API_ID    = os.environ.get("API_ID", "20293219")
    API_HASH  = os.environ.get("API_HASH", "4aef7d9e065d92f4a95736eaeb93d3ac")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8605444314:AAHZxA7RHBZxBIzUPFlQFQiRYk16a77zldg") 
   
    # database config
    DB_NAME = os.environ.get("DB_NAME","Cluster0")     
    DB_URL  = os.environ.get("DB_URL", "mongodb+srv://kakashibot8:zenitsuchan@cluster0.h0hl0gc.mongodb.net/?retryWrites=true&w=majority")
 
    # other configs
    BOT_UPTIME  = time.time
    START_PIC   = os.environ.get("START_PIC", "https://telegra.ph/file/2fc36751a9123358476ff-5ca3e05fa627c79388.jpg")
    ADMIN       = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '6834180565').split()]
    FORCE_SUB   = os.environ.get("FORCE_SUB", "-1003322147522") 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003322147522"))
    MAX_CONCURRENT_TRANSMISSIONS = int(os.environ.get("MAX_CONCURRENT_TRANSMISSIONS", "2")) # Set the maximum amount of concurrent transmissions (uploads & downloads).
    
    # wes response configuration     
    WEB_SUPPORT = bool(os.environ.get("WEB_SUPPORT", "True"))



class Txt(object):
    # part of text configuration
    START_TXT = """<b>Hᴀɪ {} ♡゙,
    
◈ I Aᴍ A Pᴏᴡᴇʀғᴜʟ Fɪʟᴇ Rᴇɴᴀᴍᴇʀ Bᴏᴛ.
◈ I Cᴀɴ Rᴇɴᴀᴍᴇ Fɪʟᴇs, Cʜᴀɴɢᴇ Tʜᴜᴍʙɴᴀɪʟs, Cᴏɴᴠᴇʀᴛ Bᴇᴛᴡᴇᴇɴ Vɪᴅᴇᴏ Aɴᴅ Fɪʟᴇ, Aɴᴅ Sᴜᴘᴘᴏʀᴛ Cᴜsᴛᴏᴍ Tʜᴜᴍʙɴᴀɪʟs Aɴᴅ Cᴀᴘᴛɪᴏɴs.

• Mᴀɪɴᴛᴀɪɴᴇᴅ Bʏ : @ZxZenitsu</b>"""

    ABOUT_TXT = """<b>╭───────────⍟
├◈ ᴍy ɴᴀᴍᴇ : <a href='https://t.me/FilexRename_Bot'>FileXRename⚡️</a>
├◈ Dᴇᴠᴇʟᴏᴩᴇʀꜱ : <a href='https://t.me/ZxZenitsu'>Zenitsu✨</a>
├◈ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ: <a href='https://t.me/Lazzy_Bots_Official'>Lazzy Bots Official</a>
├◈ Lɪʙʀᴀʀy : <a href='https://github.com/pyrogram'>Pyʀᴏɢʀᴀᴍ</a>
├◈ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/'>Pʏᴛʜᴏɴ 𝟹</a>
├◈ Dᴀᴛᴀ Bᴀꜱᴇ: <a href='https://cloud.mongodb.com/>Mᴏɴɢᴏ DB</a>
├◈ Bᴜɪʟᴅ Vᴇʀꜱɪᴏɴ: <a href='https://t.me/Lazzy_Bots_Official'>Rᴇɴᴀᴍᴇʀ V4.0.0</a> 
╰───────────────⍟ </b>"""

    HELP_TXT = """
🌌 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ</u></b>
<b>•»</b> /start Tʜᴇ Bᴏᴛ Aɴᴅ Sᴇɴᴅ Aɴy Pʜᴏᴛᴏ Tᴏ Aᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟy Sᴇᴛ Tʜᴜᴍʙɴɪʟᴇ.
<b>•»</b> /del_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Oʟᴅ Tʜᴜᴍʙɴɪʟᴇ.
<b>•»</b> /view_thumb Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜʀʀᴇɴᴛ Tʜᴜᴍʙɴɪʟᴇ.
📑 <b><u>Hᴏᴡ Tᴏ Sᴇᴛ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ</u></b>
<b>•»</b> /set_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Sᴇᴛ ᴀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•»</b> /see_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Vɪᴇᴡ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
<b>•»</b> /del_caption - Uꜱᴇ Tʜɪꜱ Cᴏᴍᴍᴀɴᴅ Tᴏ Dᴇʟᴇᴛᴇ Yᴏᴜʀ Cᴜꜱᴛᴏᴍ Cᴀᴩᴛɪᴏɴ
Exᴀᴍᴩʟᴇ:- /set_caption 📕 Fɪʟᴇ Nᴀᴍᴇ: {filename}
<b>•»</b> Sᴇɴᴅ Aɴy Fɪʟᴇ Aɴᴅ Tyᴩᴇ Nᴇᴡ Fɪʟᴇ Nɴᴀᴍᴇ \nAɴᴅ Aᴇʟᴇᴄᴛ Tʜᴇ Fᴏʀᴍᴀᴛ [ document, video, audio ].           
ℹ️ 𝗔𝗻𝘆 𝗢𝘁𝗵𝗲𝗿 𝗛𝗲𝗹𝗽 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 :- <a href=https://t.me/Lazzy_Bots_Support>𝑺𝑼𝑷𝑷𝑶𝑹𝑻 𝑮𝑹𝑶𝑼𝑷</a>
"""

#⚠️ Dᴏɴ'ᴛ Rᴇᴍᴏᴠᴇ Oᴜʀ Cʀᴇᴅɪᴛꜱ @ᴩyʀᴏ_ʙᴏᴛᴢ🙏🥲
    ADMINS_TXT = """<b><u>Hɪ I'M <a href=https://t.me/FilexRename_Bot>FileXRename</a> ✨</b></u>

ᴛᴀʟᴋ ᴡɪᴛʜ ᴍᴇ : <a href='https://t.me/Satorux_Gojo'>Cʟɪᴄᴋ Hᴇʀᴇ</a>
ᴠɪsɪᴛ ᴍʏ ɢɪᴛʜᴜʙ : <a href='https://github.com/lazzyboybots'>Lazzy Boy Gɪᴛʜᴜʙ</a>
ᴍʏ Cʜᴀɴɴᴇʟ ғᴏʀ ʏᴏᴜ : <a href='https://t.me/Lazzy_Bots_Official'>Updates Channel</a>
ᴍʏ Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ ғᴏʀ ʏᴏᴜ : <a href='https://t.me/Lazzy_Bots_Support'>𝙎𝙪𝙥𝙥𝙤𝙧𝙩 𝙂𝙧𝙤𝙪𝙥</a> """

    PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""
