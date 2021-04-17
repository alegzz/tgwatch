#!/bin/env python3
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from telethon import functions, types
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sessions import StringSession

import re2 as re
import asyncio

from systemd.daemon import notify, Notification

from psutil import Process
from os import getpid

from config import Settings
from sessions import Session
from opts import Options

options = Options()
settings = Settings(options.configname)
session = Session(settings.sessionfile)
client = TelegramClient(StringSession(session.string), settings.api_id, settings.api_hash)
client.start()
string = StringSession.save(client.session)
if string != session.string:
    session.save(string)

is_systemd = Process(getpid()).ppid() == 1

pattern = re.compile(settings.pattern, re.IGNORECASE)

admins = [settings.admins[admin]['id'] for admin in settings.admins]

async def doit(event, is_album):
    to_id = event.messages[0].to_dict()['peer_id'] if is_album else event.message.to_dict()['peer_id']

    to_peer = to_id['_']

    if to_peer == 'PeerUser':
        if to_id['user_id'] in admins:
            chan_id = event.messages[0].fwd_from.to_dict()['from_id'] if is_album else event.message.fwd_from.to_dict()['from_id']
            if chan_id['_'] == 'PeerChannel':
                channel = await client.get_entity(chan_id['channel_id'])
                await client(JoinChannelRequest(channel))     

    if to_peer != 'PeerChannel' or to_id['channel_id'] == fwd_channel.id:
        return

    if pattern.search(event.raw_text):
         await event.forward_to(fwd_channel)

@client.on(events.Album)
async def handler(event):
    await doit(event, True)

@client.on(events.NewMessage)
async def handler(event):
    if event.message.to_dict()['grouped_id'] == None:
        await doit(event, False)

async def main():
    if is_systemd:
        notify(Notification.READY)
    await client.get_dialogs()
    global fwd_channel
    fwd_channel = await client.get_entity(settings.forward_channel)

    while client.is_connected():
        if is_systemd:
            notify(Notification.STATUS, "I'm fine")
            await asyncio.sleep(10)
        else:
            await asyncio.sleep(3600)

client.loop.run_until_complete(main())
