import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import numpy as np
from prettytable import PrettyTable
from collections import defaultdict
from discord.errors import NotFound

class BingoBot(commands.Bot):
    card_list = ['Wick AFK first minute', 'Metta goes mute', 'Harri clicks E randomly', 'Longo says he is bored', 'Edgar is farming not fighting',
                      'Chris falls asleep', 'Nick 15 deaths', 'Alec jungling pre 5min', 'Harder games with worse heros', 'Metta MageSlayer or Linkin',
                      'Longo spergs out', 'Harri Pango or similar', 'GAMER WORDS USED', 'Smurf stack gets paused on', 'Colton sighs sadly',
                      'Chin Abyssal on Ogre', 'We pause, then lose', 'Anyone muted for rest of match', 'Netta lane', 'Enemy Sniper or Viper mid',
                      'Complaints about supports', 'Kener safelane', 'Wick\'s mom yelling', 'Complaining about detection',
                      'They have sentries everywhere', '60 minute L', 'The rando goes core and feeds']
    # the bingo cards of the players, {player id (str) : bingo card (2D list)}
    bingo_cards = defaultdict(list)
    bingo_card_message_ids = defaultdict(int)

    def create_card(self, player_id):
        if player_id in self.bingo_cards:
            return False  # Already have a card
        random.shuffle(self.card_list)
        card = [[0] * 5 for _ in range(5)]  # Change made here
        for i in range(5):
            for j in range(5):
                card[i][j] = self.card_list[i * 5 + j]  # Change made here
        self.bingo_cards[player_id] = card  # store it as 2D list directly

    def cross_off(self, player_id, item):
        if player_id not in self.bingo_cards:
            return False
        card = self.bingo_cards[player_id]
        for i in range(5):  # Changed here
            for j in range(5):  # Changed here
                if card[i][j] == item:
                    card[i][j] = 'X'
                    self.bingo_cards[player_id] = card
                    return True
        return False

    def check_bingo(self, player_id):
        if player_id not in self.bingo_cards:
            return False
        card = self.bingo_cards[player_id]
        # check rows and columns
        for i in range(5):  # Change made here
            if all(card[i][j] == 'X' for j in range(5)):  # Change made here
                return True
            if all(card[j][i] == 'X' for j in range(5)):  # Change made here
                return True
        # check diagonals
        if all(card[i][i] == 'X' for i in range(5)):  # Change made here
            return True
        if all(card[i][4-i] == 'X' for i in range(5)):  # Change made here
            return True
        return False

intents = discord.Intents.all()

bot = BingoBot(command_prefix='!', intents=intents)

# for ease of our example, we put your card_list directly into the bot class
BingoBot.card_list = ['Wick AFK first minute', 'Metta goes mute', 'Harri clicks E randomly', 'Longo says he is bored', 'Edgar is farming not fighting',
                      'Chris falls asleep', 'Nick 15 deaths', 'Alec jungling pre 5min', 'Harder games with worse heros', 'Metta MageSlayer or Linkin',
                      'Longo spergs out', 'Harri Pango or similar', 'GAMER WORDS USED', 'Smurf stack gets paused on', 'Colton sighs sadly',
                      'Chin Abyssal on Ogre', 'We pause, then lose', 'Anyone muted for rest of match', 'Netta lane', 'Enemy Sniper or Viper mid',
                      'Complaints about supports', 'Kener safelane', 'Wick\'s mom yelling', 'Complaining about detection',
                      'They have sentries everywhere', '60 minute L', 'The rando goes core and feeds']

@bot.command(name='newcard')
async def new_card(ctx):
    bot.create_card(str(ctx.message.author.id))
    card_table = PrettyTable()
    card = bot.bingo_cards[str(ctx.message.author.id)]
    # Set field names before adding rows
    card_table.field_names = ["B", "I", "N", "G", "O"]
    for row in card:
        card_table.add_row(row)
    await ctx.send(f"New bingo card created for {ctx.message.author.mention}. Here it is:\n```\n{card_table}\n```")
    # save the message id
    bot.bingo_card_message_ids[str(ctx.message.author.id)] = sent_message.id

# in cross_item command
@bot.command(name='cross')
async def cross_item(ctx, *, item):
    if bot.cross_off(str(ctx.message.author.id), item):
        message_id = bot.bingo_card_message_ids[str(ctx.message.author.id)]
        # delete the original message
        try:
            message_to_delete = await ctx.channel.fetch_message(message_id)
            await message_to_delete.delete()
        except NotFound:  # if the message has already been deleted
            pass
        # print the updated bingo card
        card_table = PrettyTable()
        card_table.field_names = ["B", "I", "N", "G", "O"]
        for row in bot.bingo_cards[str(ctx.message.author.id)]:
            card_table.add_row(row)
        sent_message = await ctx.send(f"Bingo card of {ctx.message.author.mention} after an item has been crossed off:\n```\n{card_table}\n```")
        # update the message id
        bot.bingo_card_message_ids[str(ctx.message.author.id)] = sent_message.id
        if bot.check_bingo(str(ctx.message.author.id)):
            await ctx.send(f"{ctx.message.author.mention} got a bingo!")
    else:
        await ctx.send(f"Item not found in the bingo card of {ctx.message.author.mention}.")

@bot.command(name='reset_harri')
async def reset_bot(ctx):
    # Reset class variables
    bot.card_list = ['Wick AFK first minute', 'Metta goes mute', 'Harri clicks E randomly', 'Longo says he is bored', 'Edgar is farming not fighting',
                      'Chris falls asleep', 'Nick 15 deaths', 'Alec jungling pre 5min', 'Harder games with worse heros', 'Metta MageSlayer or Linkin',
                      'Longo spergs out', 'Harri Pango or similar', 'GAMER WORDS USED', 'Smurf stack gets paused on', 'Colton sighs sadly',
                      'Chin Abyssal on Ogre', 'We pause, then lose', 'Anyone muted for rest of match', 'Netta lane', 'Enemy Sniper or Viper mid',
                      'Complaints about supports', 'Kener safelane', 'Wick\'s mom yelling', 'Complaining about detection',
                      'They have sentries everywhere', '60 minute L', 'The rando goes core and feeds']
    bot.bingo_cards = defaultdict(list)
    bot.bingo_card_message_ids = defaultdict(int)
    await ctx.send(f"All variables in the bot have been reset.")

# set bot token and ensure it's not None
load_dotenv()
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    raise ValueError("TOKEN is not set in the environment")

try:
    bot.run(TOKEN)
except Exception as e:
    print(f"An error occurred: {e}")