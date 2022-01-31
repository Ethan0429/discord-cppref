#!/usr/bin/python3
# bot.py
from discord.ext import commands
import bot_vars

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready(): 
    print(f'{bot.user} is online!')

@bot.command('cpp')
async def cpp(ctx: commands.Context):
    pass
bot.run(bot_vars.TOKEN)

