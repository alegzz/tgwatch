from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon import functions, types
from telethon.tl.functions.channels import JoinChannelRequest

import re

import asyncio
#import logging
import systemd.daemon

#logging.basicConfig(level=logging.WARNING, filename='cctaxi.log', format='%(asctime)s %(message)s\n-------------------------------------------------------------')

api_id = 1778565
api_hash = '32eb07d8b104c61f97bed842234174f2'

admins = []

admins.append(125875021) 

pattern = re.compile(r'т[аa][kк][сc]и|taxi|didi|(яндекс|yandex)\.go|(яндекс|yandex)\.лавк|gett|\buber\b|сити.?мобил|\bубер([уе]|\b)')

client = TelegramClient('cctaxi', api_id, api_hash)

loop = asyncio.get_event_loop()

async def main():
    systemd.daemon.notify('READY=1')
    await client.get_dialogs()

    global taxichan
    taxichan = await client.get_entity('https://t.me/taxinewsb')

async def doit(event, is_album):
    if is_album:
        to_id = event.messages[0].to_dict()['peer_id']
    else:
        to_id = event.message.to_dict()['peer_id']

    if pattern.findall(event.raw_text.lower()) != []:
        logging.warning(event)
        logging.warning(to_id)

    if to_id['_'] == 'PeerUser':
        if to_id['user_id'] in admins:
            if is_album:
                chan_id = event.messages[0].fwd_from.to_dict()['from_id']
            else:
                chan_id = event.message.fwd_from.to_dict()['from_id']
            logging.warning(chan_id)
            if chan_id['_'] == 'PeerChannel':
                channel = await client.get_entity(chan_id['channel_id'])
                await client(JoinChannelRequest(channel))     

    if to_id['_'] != 'PeerChannel':
        return

    if to_id['channel_id'] == taxichan.id:
        return

    if pattern.findall(event.raw_text.lower()) != []:
         await event.forward_to(taxichan)

@client.on(events.Album)
async def handler(event):
    await doit(event, True)
    return

@client.on(events.NewMessage)
async def normal_handler(event):
    if event.message.to_dict()['grouped_id'] == None:
        await doit(event, False)
    return
   
client.start()

#with client:
#loop.run_until_complete(main())
#with client:
client.loop.run_until_complete(main())
client.run_until_disconnected()
