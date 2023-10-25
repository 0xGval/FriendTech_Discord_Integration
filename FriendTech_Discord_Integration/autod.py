import os
from dotenv import load_dotenv
import asyncio
import discord
from discord.ext import commands
import websockets
import traceback 
import json
import logging
import aiohttp
from pythonjsonlogger import jsonlogger
from config import API
from chat_room_ids import CHANNEL_ROOM_MAP  # updated from CHAT_ROOM_IDS

# Load environment variables
load_dotenv()
AUTHORIZATION_TOKEN = os.getenv('AUTHORIZATION_TOKEN')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Custom formatter class
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        # Correcting the timestamp formatting
        log_record['time'] = self.formatTime(record, self.datefmt)

# Set up logging with the custom formatter
logHandler = logging.StreamHandler()
# Initialize the formatter without the custom format string
formatter = CustomJsonFormatter()  # No arguments here
logHandler.setFormatter(formatter)

logger = logging.getLogger('discord')
logger.addHandler(logHandler)
logger.setLevel(logging.DEBUG)  # Change to DEBUG for detailed logs

class APIBase:
    def __init__(self):
        self.session = aiohttp.ClientSession()  # session is now an HTTP session

    async def send_message(self, chat_room_id, text):
        url = f"https://prod-api.kosetto.com/messages/{chat_room_id}"  # adjust as necessary
        headers = {
            'Content-Type': 'application/json',
            'Authorization': AUTHORIZATION_TOKEN,  # assuming this is the correct token
            # add other headers as shown in your working example
        }
        payload = {
            "clientMessageId": "some_unique_id",  # generate or get this from somewhere as needed
            "text": text,
            # add other payload fields as shown in your working example
        }

        async with self.session.post(url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                print(await resp.json())  # or handle the response as you need
            else:
                print(f"Received bad response code: {resp.status}")  # or handle this as you need

    async def close(self):
        await self.session.close()  # don't forget to close the session

class NonRest:
    def __init__(self, api_base: APIBase):
        self.api_base = api_base

    async def sendMessage(self, text: str):
        for chat_room_id in CHAT_ROOM_IDS:
            await self.api_base.session.send(json.dumps({
                "action": "sendMessage",
                "text": text,
                "imagePaths": [],
                "chatRoomId": chat_room_id,
                "clientMessageId": "some_client_msg_id"
            }))

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    


@bot.event
async def on_message(message):
    # Log the message first (optional, but useful for debugging)
    logger.info(f"Message from {message.author.name}: {message.content}")

    # Check if the message is from a bot
    if message.author.bot:
        # If the message is from a bot, we don't proceed further
        return

    # If the channel is in the map, and the message is not from a bot, proceed to send
    if message.channel.id in CHANNEL_ROOM_MAP:
        associated_chat_room_id = CHANNEL_ROOM_MAP[message.channel.id]

        api_base = APIBase()
        try:
            await api_base.send_message(associated_chat_room_id, message.content)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
        finally:
            await api_base.close()  # Make sure to close the session

    # Process other potential bot commands
    await bot.process_commands(message)


bot.run(DISCORD_BOT_TOKEN)
