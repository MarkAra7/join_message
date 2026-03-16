
from multiprocessing.util import info

import discord
from discord.ext import commands
import json
import os 

from discord.ui import View, Button
from discord import app_commands
from database import *


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
bot = commands.Bot(command_prefix='/', intents=intents)

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')

with open(config_path, 'r') as f:
    config = json.load(f)
BOT_TOKEN = config.get('TOKEN')
WELCOME_CHANNEL_ID = config.get('WELCOME_CHANNEL_ID') 
GUILD_ID = config.get('GUILD_ID')



@bot.event
async def on_member_join(member):
    print(f"{member} has joined the server.")
    guild = member.guild
    print(f"Guild: {guild}")
    channel = await guild.fetch_channel(WELCOME_CHANNEL_ID)
    print(f"Welcome channel: {channel}")
    if channel:
        embed = discord.Embed(
            title="Member Joined",
            description=f" Welcome {member.name}" ,
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow(),
        )
        embed.add_field(name="Welcome to the server!", value=member.mention, inline=False)
        embed.add_field(name="Member Count", value=str(guild.member_count), inline=False ,)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon.url if guild.icon else None)
        await channel.send(embed=embed)
        if not await player_exists(str(member.id)):
            await create_player(str(member.id))
    else:
        print(f"Welcome channel with ID {WELCOME_CHANNEL_ID} not found.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    synced = await bot.tree.sync()
    print(f'Synced {len(synced)} commands globally')
    
bot.run(BOT_TOKEN)