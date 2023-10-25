import os
from dotenv import load_dotenv
import asyncio
import discord
from discord import Embed
from discord.ext import commands
import websockets
import json
import logging
from config import API, MY_USER_ID
from chat_room_ids import CHANNEL_ROOM_MAP

# Load environment variables
load_dotenv()
AUTHORIZATION_TOKEN = os.getenv('AUTHORIZATION_TOKEN')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # This format is often cleaner.
    datefmt='%Y-%m-%d %H:%M:%S',  # Adding date format can make the logs easier to read.
)

logger = logging.getLogger('discord')
logger.propagate = False  # Prevents log messages from being propagated to the root logger

class APIBase:
    def __init__(self):
        self.session = None

    async def connect(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }
        self.session = await websockets.connect(f"wss://{API}/?authorization={AUTHORIZATION_TOKEN}", extra_headers=headers)

    async def disconnect(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def listen_for_messages(self, callback):
        while True:
            try:
                message = await self.session.recv()
                await callback(message)
            except websockets.ConnectionClosedError:
                logger.error("Connection closed. Reconnecting...")
                await self.connect()
            except Exception as e:
                logger.error(f"Error: {e}")

async def handle_incoming_app_message(message):
    # Try to parse the message
    try:
        parsed_message = json.loads(message)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse message as JSON: {e}")
        return

    # Check if the parsed message is a dictionary (as expected)
    if isinstance(parsed_message, dict):
        # Extract the fields from the parsed message
        sending_user_id = parsed_message.get("sendingUserId")
        twitter_name = parsed_message.get("twitterName")
        text = parsed_message.get("text")
        chat_room_id = parsed_message.get("chatRoomId")
        replying_to_message = parsed_message.get("replyingToMessage")

        # Check if this message is a reply to another message
        if replying_to_message:
            # It's a reply. Extract the original message details.
            original_text = replying_to_message.get('text')
            original_sender = replying_to_message.get('twitterName')  # Or the appropriate field for the original sender's name

            # Prepare extra information about the message being replied to
            reply_info = f"\n\n**Replying to {original_sender}:**\n{original_text}"
        else:
            # It's not a reply, so we don't need to add extra information.
            reply_info = ""

        # Here we check if the sending_user_id is your own user ID
        if sending_user_id == MY_USER_ID:
            logger.info("Ignoring message sent by myself.")
            return  # Ignore and return without processing the message

        # Log the specific fields
        logger.info(
            "Received parsed message:\n"
            f"'sendingUserId': {sending_user_id}\n"
            f"'twitterName': {twitter_name}\n"
            f"'text': {text}\n"
            f"'chatRoomId': {chat_room_id}\n"
            f"'replyingToMessage': {replying_to_message}"
        )

        # Find the corresponding Discord channel
        discord_channel_id = None
        for channel_id, room_id in CHANNEL_ROOM_MAP.items():
            if room_id == chat_room_id:
                discord_channel_id = channel_id
                break

        # Send the message to the Discord channel if found
        if discord_channel_id:
            channel = bot.get_channel(discord_channel_id)
            if channel:
                # Create the embed, including any reply info if present
                description_text = f"- {text}{reply_info}"  # This now includes the original message if it's a reply
                embed = discord.Embed(
                    title=f"{twitter_name} wrote...",
                    description=description_text,
                    color=0x0080c0
                )
                
                sender_url = f"https://www.friend.tech/rooms/{sending_user_id}"
                room_url = f"https://www.friend.tech/rooms/{chat_room_id}"

                # Adding hyperlinked fields
                embed.add_field(name="Room", value=f"[Link]({room_url})", inline=False)

                # Send the embed
                await channel.send(embed=embed)
            else:
                logger.error(f"Channel {discord_channel_id} not found.")
        else:
            logger.error(f"No mapping for chat room ID {chat_room_id}.")
    else:
        logger.error("Parsed message is not a dictionary")
        # No further processing since the message isn't the expected dictionary


intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} connected to Discord!')
    logger.info(f'Connected to guilds: {bot.guilds}')

    api_base = APIBase()
    await api_base.connect()
    asyncio.create_task(api_base.listen_for_messages(handle_incoming_app_message))

# Removed the on_message event as it's not needed for listening from the app

bot.run(DISCORD_BOT_TOKEN)
