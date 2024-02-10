#!/usr/bin/env python
## Based on https://medium.com/@kokhua81/how-to-send-messages-and-files-to-telegram-with-python-66c1abeea7a6
## Script sends file or/and text message to Telegramm Channel from commandline.
## 1. Create app configuration on https://my.telegram.org/apps , get 'api_id' and 'api_hash'
## 2. pip install -r requirements.txt
## 3. At first run the script asks for mobile or UID.. Need send your mobile associated with TG-account, bots access to API is restricted!!
## Subsequently to use backup, download all volumes adn run: cat *_part_* > backup.tar.bz2

import argparse, sys

## Instantiate the config parser
parser = argparse.ArgumentParser(description='''Snippet for tg file upload script..
If args consist path sign or space - doublequote them''')

## Optional positional argument - run without modifiers to upload file
parser.add_argument('filename', type=str, nargs='?', help='Single filename')

## Optional argument - run with modifiers to upload file or/and text (in separate post)
parser.add_argument('-f', '--file', type=str, help='Name of file to upload')
parser.add_argument('-t', '--text', type=str, help='Text to post')

## Without params gets help and quit
args = parser.parse_args(sys.argv[1:])
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)


from telethon import TelegramClient
import asyncio
import configparser

## Load params from config file
config = configparser.ConfigParser()
config.read("config.ini")

## Set variables from config
api_id       = config['Telegram']['api_id']
api_hash     = config['Telegram']['api_hash']
session_name = config['Telegram']['session_name']
channel      = config['TGGroup']['group']


async def func():
    entity = await client.get_entity(channel)
## Choose what we will post - file or/and text
    if args.text:
        await client.send_message(entity=entity, message=args.text)
    if args.filename or args.file:
        filename = args.filename or args.file
        await client.send_file(entity, filename)

## Connection
with TelegramClient(session_name, api_id, api_hash) as client:
    client.loop.run_until_complete(func())
