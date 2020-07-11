from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import sys
import json
from colorama import init
from termcolor import colored, cprint

init()

args = sys.argv[1:]
api_id = 0
api_hash = "0"
name = 'Spotigram'
chat = args[0]
playlist_name = args[1]
songs = []
performer = 'artist'
title = 'track'
test = 0
broken_songs = []

print_red_onwhite  = lambda x: cprint(x, 'red', 'on_white')
print_green_onwhite = lambda x: cprint(x, 'green', 'on_white')
print_red = lambda x: cprint(x, 'red')

def format_for_spotify(query_str):
    return query_str.replace("&", ",").replace("feat.", ",").replace("feat", ",").replace("...", "").replace("..", "").replace("•", "").replace("/","").replace(".", " .")

def save_file(songs, filename):
    with open(filename + ".json", "w", encoding="utf-8") as file:
        json.dump(songs, file, ensure_ascii=False, separators=(",\n", ": "))

with TelegramClient(name, api_id, api_hash) as client:
    for message in client.iter_messages(chat):
        media = message.media
        if media:
            if hasattr(media, 'document'):
                attributes = media.document.attributes[0]
                performers, title = "", ""
                try:
                    if hasattr(attributes, 'performer') and attributes.performer != "" and attributes.performer:
                        if attributes.title:
                            title = attributes.title
                        search_str = title + ' ' + performers
                        search_str = format_for_spotify(search_str)
                        if search_str == " " or not search_str:
                            search_str = message.message.split("\n")[-1]
                        songs.append(search_str)
                except Exception as ex:
                    broken_str = performers + ' ' + title
                    broken_songs.append(broken_str)
                    print_red_onwhite("Failed to get song %s from telegram" %broken_str)
                    
save_file(broken_songs, "tele_fail")
