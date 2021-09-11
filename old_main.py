import discord
import os
import requests
import json
from replit import db
from keep_alive import keep_alive
from discord.ext import commands
import youtube_dl
import asyncio


client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")

  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + "\n -" + json_data[0]['a']
  return (quote)

def update_user_messages(user_input):
  if "user_messages" in db.keys():
    user_messages = db["user_messages"]
    user_messages.append(user_input)
    db["user_messages"] = user_messages
  else:
    db["user_messages"] = [user_input]

def delete_user_message(index):
  user_messages = db["user_messages"]
  if len(user_messages) > index:
    del user_messages[index]
    db["user_messages"] = user_messages

@client.event
async def on_ready():
  print ('{0.user} is online!'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if message.content.startswith('!hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith("!add"):
    user_input = msg.split("!add ",1)[1]
    update_user_messages(user_input)
    await message.channel.send("New message added.")

  if msg.startswith("!del"):
    user_messages = []
    if "user_messages" in db.keys():
      index = int(msg.split("!del",1)[1])
      delete_user_message(index)
      user_messages = db["user_messages"]
    await message.channel.send(user_messages)

  if msg.startswith("!list"):
    user_messages = []
    if "user_messages" in db.keys():
      user_messages = db["user_messages"]
    await message.channel.send(user_messages)






client = commands.Bot(command_prefix="!")

@client.command()
async def play (ctx, url: str):
  song_temp = os.path.isfile("song.webm")
  try:
    if song_temp:
      os.remove("song.webm")
  except PermissionError:
    await ctx.send("Wait for the current playing music to end or use the 'stop' command")
    return
  #voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')

  await ctx.author.voice.channel.connect()
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    

  ydl_opts = {
    'format': '249/250/251',
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  for file in os.listdir("./"):
    if file.endswith(".webm"):
      os.rename(file, "song.webm")
  voice.play(discord.FFmpegOpusAudio("song.webm"))

@client.command()
async def leave(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_connected():
    await voice.disconnect()
  else:
    await ctx.send("{0.user} is not connected to a voice channel ")

@client.command()
async def pause(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_playing():
    voice.pause()
  else:
    await ctx.send("No audio is currently playing")

@client.command()
async def resume(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_paused():
    voice.resume()
  else:
    await ctx.send("The audio is not paused")

@client.command()
async def stop(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  voice.stop()


ytdl_format_options = {
    'format': '249/250/251',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegOpusAudio(filename, **ffmpeg_options), data=data)




@client.command()
async def stream(self, ctx, url:str):
  """Streams from a url (same as yt, but doesn't predownload)"""
  async with ctx.typing():
    player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
    ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
    await ctx.send(f'Now playing: {player.title}')




keep_alive()
client.run(os.environ['discord client secret key'])




