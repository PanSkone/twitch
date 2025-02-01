# bot_manager.py
from bot import Bot
import asyncio
from flask import Flask, jsonify, send_from_directory
from twitchio.ext import commands
import threading
import os
import asyncio
import time

bot_running = False
bot_instance = None
current_match_id = None  # ID meczu, dla którego działa bot
loop = None  # Globalna pętla zdarzeń

async def run_bot():
    global bot_instance
    bot_instance = Bot(current_match_id)  # Przekazujemy current_match_id do instancji Bota
    await bot_instance.start()

# Funkcja startująca bota
def start_bot(match_id):
    global bot_instance, bot_running, current_match_id, loop  # Zmienna globalna

    if bot_running:
        return f"Bot jest już uruchomiony dla meczu ID {current_match_id}. Zatrzymaj go przed uruchomieniem nowego."

    bot_running = True
    current_match_id = match_id

    loop = asyncio.new_event_loop()  
    asyncio.set_event_loop(loop)
    bot_task = loop.create_task(run_bot())  # Tworzymy zadanie
    thread = threading.Thread(target=loop.run_forever, daemon=True)
    thread.start()

    return f"Bot uruchomiony dla meczu ID {match_id}"

# Funkcja zatrzymująca bota
def stop_bot(match_id):
    global bot_instance, bot_running, current_match_id, loop  # Zmienna globalna

    if not bot_running or current_match_id != match_id:
        return f"Bot nie jest uruchomiony dla meczu ID {match_id}"

    bot_running = False
    current_match_id = None  # Resetujemy ID meczu

    if bot_instance:
        future = asyncio.run_coroutine_threadsafe(bot_instance.close(), loop)  
        future.result()  # Czekamy na zamknięcie bota
        bot_instance = None

    if loop:
        loop.call_soon_threadsafe(loop.stop)  # Zatrzymujemy pętlę asyncio
        loop = None

    return f"Bot zatrzymany dla meczu ID {match_id}"
