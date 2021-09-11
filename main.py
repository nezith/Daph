from discord.ext import commands
from keep_alive import keep_alive
import os


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

bot.load_extension("music")


keep_alive()
bot.run(os.environ['discord client secret key'])
    
