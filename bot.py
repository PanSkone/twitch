import asyncio
from flask import Flask, jsonify, send_from_directory
from twitchio.ext import commands
import threading
import os
from db_manager import insert_chat_log
import aiohttp

# Tworzenie aplikacji Flask
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token='oauth:a0yvoysbq9ox6dhj9f7smiinqckw51',  # Twój token
            prefix='!',
            initial_channels=['zackrawrr']
        )
        self.session = aiohttp.ClientSession()  # Tworzymy sesję HTTP

    async def close(self):
        if not self.session.closed:
            await self.session.close()  # Zamykamy sesję HTTP
        await super().close()  # Zamykamy bota poprawnie

    async def is_valid_message(self, message):
        """Funkcja sprawdzająca, czy wiadomość jest dokładnie '#kmt'."""
        print(f"{message.author.name}: {message.content}")

        return message.content.strip() == "#kmt"

    async def event_message(self, message):
        if message.echo:
            return

        # Sprawdzamy poprawność wiadomości
        if not await self.is_valid_message(message):  # UŻYWAMY self.is_valid_message()
            return  # Odrzucamy wiadomość, jeśli nie spełnia warunku

        print(f"{message.author.name}: {message.content}")

        # Zapisujemy wiadomość w bazie danych
        insert_chat_log(message.author.name, message.content)