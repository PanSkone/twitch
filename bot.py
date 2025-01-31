import asyncio
from flask import Flask, jsonify, send_from_directory
from twitchio.ext import commands
import threading
import os
from db_manager import insert_chat_log  # Importujemy funkcję zapisu do bazy danych

# Tworzenie aplikacji Flask
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token='oauth:a0yvoysbq9ox6dhj9f7smiinqckw51',  # Twój token
            prefix='!',
            initial_channels=['rybsonlol_']
        )

    async def event_message(self, message):
        if message.echo:
            return
        print(f"{message.author.name}: {message.content}")
        
        # Zapisujemy wiadomość w bazie danych
        insert_chat_log(message.author.name, message.content)
