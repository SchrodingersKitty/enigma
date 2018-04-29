import discord
import logging
import sys
import json
import argparse
import traceback
from datetime import datetime, date, time

# deal with command line args
arg_parser = argparse.ArgumentParser(description='Discord chat history scraper')
arg_parser.add_argument('channel', type=str, help='channel name or id')
args = arg_parser.parse_args()

# set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler("info.log"),
        logging.StreamHandler(sys.stdout)
    ])
log = logging.info
err = logging.error

# get bot token
with open("token.ini", "r") as f:
    token = f.read()

# initialize Discord client
client = discord.Client()

def get_last_timestamp(datafile):
    """Return the last timestamp on file or the beginning of Discord epoch if none is found."""
    line = ''
    with open(datafile, 'r') as data:
        # unwind to EOF
        for line in data:
            pass
    if not line:
        return datetime.combine(date(2015, 1, 1), time.min)
    time_string = json.loads(line)[0]
    timestamp = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S.%f')
    return timestamp

@client.event
async def on_ready():
    log("Logged in as {}".format(client.user))
    # find channel
    chan = None
    for c in client.get_all_channels():
        if c.id == args.channel or c.name == args.channel:
            chan = client.get_channel(c.id)
    if not chan:
        err("Channel {} not found".format(args.channel))
        await client.logout()
        return
    log("Beginning history scan of channel {} with id {}".format(chan.name, chan.id))
    # touch channel data file
    datafile = args.channel + '.json'
    open(datafile, 'a').close()
    # resume from last timestamp
    timestamp = get_last_timestamp(datafile)
    with open(datafile, 'a', 1) as data:
        while True:
            log("Getting history after {}".format(timestamp))
            history = client.logs_from(chan, limit=500, after=timestamp, reverse=True)
            count = 0
            async for msg in history:
                timestamp = msg.timestamp
                msg_scrape = [datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S.%f'), msg.author.id, msg.clean_content]
                json.dump(msg_scrape, data)
                data.write('\n')
                count += 1
            if count == 0:
                break
    await client.logout()

@client.event
async def on_error(event, *args, **kwargs):
    err(traceback.format_exc())
    await client.logout()

client.run(token)