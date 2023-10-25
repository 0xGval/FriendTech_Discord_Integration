# FriendTech_Discord_Integration
Set of scripts to map a dedicated discord to the rooms of the keys you own on friendtech and auto forward messages in both directions through your own discord bot.

The mapping requires you to have n° discord channels to map each channel to a specific room of a key you own on Friend Tech.

***This is the first version and even if it is pretty stable and support filters for avoiding forwarding bots messages etc, it still a v1.  Logs needs to be cleaned and structured and sending or receiving pictures isn't supported yet.**

### Prerequisites

1. This project requires Python 3.11.5 or newer. If you haven't already installed Python, download and install it from [python.org](https://www.python.org/downloads/).
2. A discord account and a server where you have administrative privileges. Consider creating a dedicated new one.
3. A friend tech account and your JWT authorization token
 
## Discord Bot Setup

1. **Create a New Application**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Click on the "New Application" button. Name your application and click "Create".
   
2. **Set up a Bot**:
   - On the left side panel, click on "Bot".
   - Click "Add Bot" and confirm.
   - Toggle the buttons under the Privileged Intents section.
   
3. **Get Your Bot Token**:
   - Under the "TOKEN" section, click "Copy" to copy your bot token. Save this token carefully as it will be used in the `config.py` file.

4. **Invite the Bot to Your Server**:
   - On the left side panel, click on "OAuth2".
   - Under "OAuth2 URL Generator", select "bot" in the scopes section.
   - Choose the desired permissions for your bot (It needs AT LEAST to be able to read messages and send embedded).
   - Copy the generated URL and open it in your browser to invite the bot to your server.
   - Make sure the bot has access to the channels (or the whole category) that you will use to map the FT rooms.

## Installation

1. **Git**:
   - If you haven't already installed Git, you can find download and installation instructions on the Git official site.

3. **Clone the Repository**: 
   ```bash
   git clone https://github.com/giovall/FriendTech_Discord_Integration.git
   cd FriendTech_Discord_Integration

 > Tip: Alternativly you can manually download the Repository from github.

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

  ## Configuration

1. **sample.env**:
   - Rename sample.env to .env
   - Open the .env file in a text editor and replace PASTE_YOUR_FRIEND_TECH_JWT_AUTHORIZATION_TOKEN_HERE with your Friend Tech JWT token.
 > **REMEMBER: your JWT token is EXTREMELY confidential as gives access to your Friend Tech account. The script stores it in a .env file that ALWAYS stays on your local machine. It is YOUR responsibility to ensure the .env file is protected adequately**
   - Replace PASTE_YOUR_DISCORD_BOT_TOKEN with your Discord Bot token you saved earlier.
  
2. **sample.config**:
   - Rename sample.config.py to config.py
   - Open the config.py file in a text editor and replace PASTE_YOUR_FRIEND_TECH_ADDRESS with your Friend Tech wallet address.
  
2. **sample.chat_room_ids**:
   - Rename sample.chat_room_ids.py to chat_room_ids.py
   - Open the chat_room_ids.py file in a text editor and replace the placeholders according to the example provided.
     > Tip: In Discord, enable Developer Mode in Settings to easily copy IDs by right-clicking on channels.

  
     ## How It Works
1. **Initialization**: On startup, the scripts initialize the Discord bot and establish WebSocket connections to the Friend Tech API.
2. **autod.py**: The autod.py script listens for messages on Discord, forwarding any received messages to the corresponding Friend Tech rooms.
3. **listen.py**: Conversely, listen.py monitors for messages from Friend Tech rooms, relaying them back to the appropriate Discord channels.
4. **Running the Scripts**: The run.py script is used to launch both listeners simultaneously, allowing for real-time, two-way communication between platforms.
5. **Secure Closure**: After message transmission, WebSocket connections are responsibly closed, maintaining security.

## Usage

1. **Run the bot**:
   ```bash
   python run.py

 ### **Disclaimer: Please interact with the software at your own risk, I am not responsible for any loss or any downside caused by it. I cannot guarantee any results from it. The software is not an offering from me. I share no responsibility for the usage and outcome of this now open-sourced software.**

