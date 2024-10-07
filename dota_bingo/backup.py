import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import numpy as np
from prettytable import PrettyTable
from collections import defaultdict

# Get the token from .env file
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Check if TOKEN is not None
if not TOKEN:
    raise ValueError("TOKEN is not set in the environment")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


'''
# Event listener
@bot.event
async def on_message(message):
    specific_user_id = 181159715697328128
    if message.author.id != specific_user_id:  # Check if message is not from the specific user
        return

    emojis = ['🏳️‍⚧️', '🏳️‍🌈', '🍆', '💦']
    for emoji in emojis:
        try:
            await message.add_reaction(emoji)
        except discord.NotFound as e:
            print(f'Could not find emoji: {e}')
        except discord.HTTPException as e:
            print(f'HTTP error occurred while adding a reaction: {e}')
        except discord.InvalidArgument as e:
            print(f'Invalid argument provided: {e}')
'''

# Run the bot with the token
bot.run(TOKEN)