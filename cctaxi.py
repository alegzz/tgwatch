#!/bin/env python3
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon import functions, types
from telethon.tl.functions.channels import JoinChannelRequest

import re

import asyncio
import systemd.daemon

from config import settings

pattern = re.compile(settings.pattern)

client = TelegramClient(settings.session, settings.api_id, settings.api_hash)

loop = asyncio.get_event_loop()

async def main():
    systemd.daemon.notify('READY=1')
    await client.get_dialogs()

    global taxichan
    taxichan = await client.get_entity(settings.channel)

async def doit(event, is_album):
    if is_album:
        to_id = event.messages[0].to_dict()['peer_id']
    else:
        to_id = event.message.to_dict()['peer_id']

    if to_id['_'] == 'PeerUser':
        if to_id['user_id'] in settings.admins:
            if is_album:
                chan_id = event.messages[0].fwd_from.to_dict()['from_id']
            else:
                chan_id = event.message.fwd_from.to_dict()['from_id']
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
async def handler(event):
    if event.message.to_dict()['grouped_id'] == None:
        await doit(event, False)
    return
   
client.start()

client.loop.run_until_complete(main())
client.run_until_disconnected()
