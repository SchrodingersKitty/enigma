import discord
import logging
import sys
import json
import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler("info.log"),
        logging.StreamHandler(sys.stdout)
    ])
log = logging.info

datafile = sys.argv[1]

with open("token.ini", "r") as f:
    token = f.read()

client = discord.Client()

def load_progress(filename):
    with open("temp.ini", "r+") as temp:
        chan_id = temp.readline().strip()
        msg_id = temp.readline().strip()
    return chan_id, msg_id

def save_progress(filename, chan_id, msg_id):
    with open(filename, "w") as temp:
        temp.write(chan_id)
        temp.write('\n')
        temp.write(msg_id)

@client.event
async def on_ready():
    log("Connected as {}".format(client.user))
    temp = "temp.ini"
    chan_id, msg_id = load_progress(temp)
    chan = client.get_channel(chan_id)
    log("Beginning history scan of channel {}".format(chan.name))
    with open(datafile, "a", 1, encoding="utf-8") as data:
        msg = await client.get_message(chan, msg_id)
        count = 100
        while count > 1:
            log("Getting history from {}".format(msg.timestamp))
            history = client.logs_from(chan, limit=100, before=msg)
            count = 0
            async for msg in history:
                count += 1
                msg_scrape = [datetime.datetime.strftime(msg.timestamp, '%Y%m%d%H%M%S'), msg.author.id, msg.clean_content]
                #datetime.datetime.strptime(DATESTRING, '%Y%m%d%H%M%S')
                json.dump(msg_scrape, data)
                data.write('\n')
            save_progress(temp, chan.id, msg.id)
    await client.logout()

client.run(token)