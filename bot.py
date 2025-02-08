# bot.py
import asyncio
from flask import Flask, jsonify, send_from_directory
from twitchio.ext import commands
import threading
import os
from db_manager import insert_chat_log, fetch_team_tags_by_match
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
        self.batch_size = 5  # Określamy, że wysyłamy zapytanie co 5 wiadomości
        self.match_id = match_id  # Przechowujemy ID meczu

    async def close(self):
        if not self.session.closed:
            await self.session.close()  # Zamykamy sesję HTTP
        await super().close()  # Zamykamy bota poprawnie

    # Sprawdza, czy wiadomość pasuje do tagów drużyn w danym meczu.
    async def is_valid_message(self, message):
        team1_tag, team2_tag = fetch_team_tags_by_match(self.match_id)
        return message.content.strip().lower() in {team1_tag.lower(), team2_tag.lower()}

    async def event_message(self, message):
        print(f"[Mecz ID: {self.match_id}] {message.author.name}: {message.content}")

        if message.echo:
            return

        if not await self.is_valid_message(message):
            return

        print(f"✅ [Dodano do bufora] {self.match_id}] {message.author.name}: {message.content}")
        # Dodajemy wiadomość do bufora
        self.message_buffer.append((message.author.name, message.content, self.match_id))

        # Jeśli bufor osiągnie 10 wiadomości, zapisujemy je do bazy
        if len(self.message_buffer) >= self.batch_size:
            await self.flush_messages()

    # Funkcja do zapisania wiadomości w bazie danych za jednym razem.
    async def flush_messages(self):
        if self.message_buffer:
            # Zapisujemy wszystkie wiadomości do bazy
            insert_chat_log(list(self.message_buffer))
            print(f"Zapisano {len(self.message_buffer)} wiadomości do bazy.")
            self.message_buffer.clear()  # Wyczyść bufor po zapisaniu
            self.last_flush_time = time.time()  # Zaktualizuj czas flush
