# bot.py
import asyncio
from flask import Flask, jsonify, send_from_directory
from twitchio.ext import commands
import threading
import os
from db_manager import insert_chat_log  # Możesz używać insert_chat_log, jeśli chcesz wysyłać pojedyncze wiadomości
import aiohttp
from dotenv import load_dotenv
from collections import deque
import time

load_dotenv()

# Tworzenie aplikacji Flask
class Bot(commands.Bot):
    def __init__(self, match_id):
        super().__init__(
            token=os.getenv('BOT_TOKEN'),  # Zmienna środowiskowa
            prefix='!',
            initial_channels=['blejn_']
        )
        self.session = aiohttp.ClientSession()  # Tworzymy sesję HTTP
        self.message_buffer = deque()  # Bufor do przechowywania wiadomości
        self.last_flush_time = time.time()  # Czas ostatniego flush
        self.batch_size = 10  # Określamy, że wysyłamy zapytanie co 10 wiadomości
        self.match_id = match_id  # Przechowujemy ID meczu

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
        print(f"[Mecz ID: {self.match_id}] {message.author.name}: {message.content}")  # Używamy self.match_id

        # Dodajemy wiadomość do bufora
        self.message_buffer.append((message.author.name, message.content, self.match_id))

        # Jeśli bufor osiągnie 10 wiadomości, zapisujemy je do bazy
        if len(self.message_buffer) >= self.batch_size:
            await self.flush_messages()

    async def flush_messages(self):
        """Funkcja do zapisania wiadomości w bazie danych za jednym razem."""
        if self.message_buffer:
            # Zapisujemy wszystkie wiadomości do bazy
            insert_chat_log(list(self.message_buffer))
            print(f"Zapisano {len(self.message_buffer)} wiadomości do bazy.")
            self.message_buffer.clear()  # Wyczyść bufor po zapisaniu
            self.last_flush_time = time.time()  # Zaktualizuj czas flush
