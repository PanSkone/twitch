import asyncio
from flask import Flask, jsonify, send_from_directory
from twitchio.ext import commands
import threading
import os

#  Tworzenie aplikacji Flask
# bot.py

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token='oauth:a0yvoysbq9ox6dhj9f7smiinqckw51',  # Twój token
            prefix='!',
            initial_channels=['caedrel']
        )

    async def event_message(self, message):
        if message.echo:
            return
        print(f"{message.author.name}: {message.content}")
        with open("chat_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{message.author.name}: {message.content}\n")
