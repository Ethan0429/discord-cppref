#!/usr/bin/python3
# bot.py
from tracemalloc import stop
from query import search, parse_results
from discord import Color
from discord.ext import commands
import discord
import bot_vars
from itertools import takewhile

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

'''
Formats a search term to the appropriate result.
e.g. if your search term is fsscanf, it will likely
be formatted to fscanf, as that is what matches the
existing search result.
'''


async def get_term(url: str, mode: str):
    if mode == 'cpp':
        url = ''.join(reversed(url))
        term = ''.join([letter for letter in takewhile(
            lambda letter: letter != '/', url)])
        return ''.join(reversed(term))
    elif mode == 'man':
        for i in range(1, 9):
            url = url.replace(f'.{i}.html', '')

        url = ''.join(reversed(url))
        term = ''.join([letter for letter in takewhile(
            lambda letter: letter != '/', url)])
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
async def cpp(ctx: commands.Context, term: str):
    member = ctx.author

    if str == None:
        await ctx.send(f'{member.mention} `!cpp` usage: ```!cpp [SearchTerm] // without brackets```')
        return

    cpp_link = parse_results(search(term, bot_vars.cppref))
    man_link = parse_results(search(term, bot_vars.man))

    # if neither cpp nor man has a valid link
    if (cpp_link == None or cpp_link == '') and (man_link == None or man_link == ''):
        await ctx.send(f'{member.mention} could not find `{term}` in cppreference.com or man.org!')
        return

    # if only cpp link is available
    elif cpp_link == None or cpp_link == '':
        term = await get_term(man_link, 'man')
        embed_msg = discord.Embed(
            title=f'{bot_vars.man_alias} - {term}',
            description=f'{member.mention} I found a reference to `{term}` in {bot_vars.man_alias}!\n[Click me or the title]({man_link})!',
            url=man_link,
            colour=Color.blue()
        )
        embed_msg.set_thumbnail(url="https://apastyle.apa.org/images/references-page-category_tcm11-282727_w1024_n.jpg"
                                ).set_author(name='CPP Ref Bot', url=man_link, icon_url="https://docs.microsoft.com/cs-cz/windows/images/c-logo.png"
                                             ).add_field(name='GitHub', value='https://github.com/Ethan0429/discord-cppref', inline=False)
        await ctx.send(content=f'{member.mention}', embed=embed_msg)

    # if only man page link is available
    elif man_link == None or man_link == '':
        term = await get_term(cpp_link, 'cpp')
        embed_msg = discord.Embed(
            title=f'{bot_vars.cppref} - {term}',
            description=f'{member.mention} I found a reference to `{term}` in {bot_vars.cppref}!\n[Click me or the title]({cpp_link})!',
            url=cpp_link,
            colour=Color.blue()
        )
        embed_msg.set_thumbnail(url="https://apastyle.apa.org/images/references-page-category_tcm11-282727_w1024_n.jpg"
                                ).set_author(name='CPP Ref Bot', url=cpp_link, icon_url="https://docs.microsoft.com/cs-cz/windows/images/c-logo.png"
                                             ).add_field(name='GitHub', value='https://github.com/Ethan0429/discord-cppref', inline=False)
        await ctx.send(content=f'{member.mention}', embed=embed_msg)

    # if both links are available
    else:
        cpp_term = await get_term(cpp_link, 'cpp')
        man_term = await get_term(man_link, 'man')
        embed_msg = discord.Embed(
            title=f'{bot_vars.cppref} - {term}',
            description=f'''
            {member.mention} I found a reference to `{term}` in {bot_vars.cppref}!\n[Click me or the title]({cpp_link})!\n
            **Man Link**\nAlternatively, [here is the Linux man link to {man_term}]({man_link})''',
            url=cpp_link,
            colour=Color.blue()
        )
        embed_msg.set_thumbnail(url="https://apastyle.apa.org/images/references-page-category_tcm11-282727_w1024_n.jpg"
                                ).set_author(name='CPP Ref Bot', url=man_link, icon_url="https://docs.microsoft.com/cs-cz/windows/images/c-logo.png"
                                             ).add_field(name='GitHub', value='https://github.com/Ethan0429/discord-cppref', inline=False)
        await ctx.send(content=f'{member.mention}', embed=embed_msg)

bot.run(bot_vars.TOKEN)
