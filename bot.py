#!/usr/bin/python3
# bot.py
from query import search, parse_results
from discord import Color
from discord.ext import commands
import discord
import bot_vars
from itertools import takewhile

bot = commands.Bot(command_prefix='!')

''' 
Formats a search term to the appropriate result.
e.g. if your search term is fsscanf, it will likely
be formatted to fscanf, as that is what matches the
existing search result.
'''
async def get_term(url: str):
    url = ''.join(reversed(url))
    term = ''.join([letter for letter in takewhile(lambda letter: letter != '/', url)])
    return ''.join(reversed(term))

@bot.event
async def on_ready(): 
    print(f'{bot.user} is online!')

'''
Usage: !cpp [term]

Accepts a single argument which is the term
to query a search for cppreference.com.

Responds to the command sender with an embedded
message to the reference link.
'''
@bot.command('cpp')
async def cpp(ctx: commands.Context, *, term: str):
    member = ctx.author

    if str == None:
        await ctx.send(f'{member.mention} `!cpp` usage: ```!cpp [SearchTerm] // without brackets```')
        return

    site = 'cppreference.com'
    ref_link = parse_results(search(term, bot_vars.cppref))
    if ref_link == None or ref_link == '':
        ref_link = parse_results(search(term), bot_vars.man7)
        site = 'man7.org'
        return

    term = await get_term(ref_link)
    embed_msg = discord.Embed(
        title=f'{site} - {term}', 
        description=f'{member.mention} I found a reference to `{term}` in {site}!\n[Click me or the title]({ref_link})!',
        url=ref_link,
        colour=Color.blue()
    )
    embed_msg.set_thumbnail(url="https://apastyle.apa.org/images/references-page-category_tcm11-282727_w1024_n.jpg"
    ).set_author(name='CPP Ref Bot', url=ref_link, icon_url="https://docs.microsoft.com/cs-cz/windows/images/c-logo.png"
    ).add_field(name='GitHub', value='https://github.com/Ethan0429/discord-cppref', inline=False
    ).add_field(name='Created By', value='Ethan Rickert', inline=False)
    await ctx.send(content=f'{member.mention}', embed=embed_msg)

bot.run(bot_vars.TOKEN)