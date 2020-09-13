from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon import functions, types

import asyncio
#import logging

#logging.basicConfig(filename='cctaxi.log', format='%(asctime)s %(message)s')

api_id = 1778565
api_hash = '32eb07d8b104c61f97bed842234174f2'

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

    if to_id['_'] != 'PeerChannel':
        return

    if to_id['channel_id'] == taxichan.id:
        return

    if any(s in event.raw_text.lower() for s in ('такси', 'uber', 'taxi', 'didi', 'яндекс.go', 'yandex.go', 'яндекс.лавк')):
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
