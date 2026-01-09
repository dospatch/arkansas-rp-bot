import os
from dotenv import load_dotenv
import discord # or your specific bot library

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Use the TOKEN variable to run your bot
client.run(TOKEN)
