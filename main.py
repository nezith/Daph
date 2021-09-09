import discord
import os
import requests
import json
from replit import db
from keep_alive import keep_alive


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

keep_alive()
client.run(os.environ['discord client secret key'])




