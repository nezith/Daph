import discord
import os
import requests
import json
from replit import db
from keep_alive import keep_alive
from discord.ext import commands
import youtube_dl
import os

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
  song_temp = os.path.isfile("song.mp3")
  try:
    if song_temp:
      os.remove("song.mp3")
  except PermissionError:
    await ctx.send("Wait for the current playing music to end or use the 'stop' command")
    return
  voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')

  await voiceChannel.connect()
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    

  ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192',
    }],
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
  for file in os.listdir("./"):
    if file.endswith(".mp3"):
      os.rename(file, "song.mp3")
  voice.play(discord.FFmpegPCMAudio("song.mp3"))

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

keep_alive()
client.run(os.environ['discord client secret key'])




