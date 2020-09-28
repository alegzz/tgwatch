from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon import functions, types
from telethon.tl.functions.channels import JoinChannelRequest

import re

#%%

import asyncio
#import logging

#logging.basicConfig(filename='cctaxi.log', format='%(asctime)s %(message)s')

api_id = 1778565
api_hash = '32eb07d8b104c61f97bed842234174f2'

admins = []

admins.append(919562137) 

pattern = re.compile(r'(такси|taxi|didi|(яндекс|yandex)\.go|(яндекс|yandex)\.лавк|gett|(uber(?!2))|сити.?мобил)')

client = TelegramClient('cctaxi', api_id, api_hash)

loop = asyncio.get_event_loop()

async def main():
    await client.get_dialogs()

    global taxichan
    taxichan = await client.get_entity('https://t.me/taxinewsb')

async def doit(event, is_album):
    if is_album:
        to_id = event.messages[1].to_dict()['to_id']
    else:
        to_id = event.message.to_dict()['to_id']

    if to_id['_'] == 'PeerUser':
        if to_id['user_id'] in admins:
            if is_album:
                chan_id = event.messages[1].to_dict()['from_id']
            else:
                chan_id = event.message.to_dict()['from_id']
            chan = client.get_entity(chan_id)
            client(JoinChannelRequest(channel))     

    if to_id['_'] != 'PeerChannel':
        return

    if to_id['channel_id'] == taxichan.id:
        return

    if pattern.findall(event.raw_text.lower()) != []:
         await event.forward_to(taxichan, as_album=True)

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

loop.run_until_complete(main())
client.run_until_disconnected()
