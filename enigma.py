import discord
from markov import generate_chain, generate_message
import sys

datafile = sys.argv[1]

with open("token.ini", "r") as f:
    token = f.read()

t, s = generate_chain(datafile)

client = discord.Client()

def clean_message(message):
    text = message.content
    for m in message.mentions:
        text = text.replace(m.mention, '')
    for m in message.channel_mentions:
        text = text.replace(m.mention, '')
    for m in message.role_mentions:
        text = text.replace(m.mention, '')
    return text

def get_keyword(message):
    text = clean_message(message)
    key = text.split(None, 1)[0]
    return key

@client.event
async def on_message(message):
    for mention in message.mentions:
        if mention.id == client.user.id:
            key = get_keyword(message)
            if key and key in t:
                reply = ""
                while key not in reply:
                    reply = generate_message(t, s)
            else:
                reply = generate_message(t, s)
            await client.send_message(message.channel, reply)

client.run(token)