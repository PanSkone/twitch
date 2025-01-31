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

async def run_bot():
    global bot_instance
    bot_instance = Bot()
    await bot_instance.start()

def start_bot():
    global bot_running
    if not bot_running:
        bot_running = True
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_bot())

def stop_bot():
    global bot_instance, bot_running

    if not bot_running:
        return "Bot nie jest uruchomiony"

    bot_running = False
    try:
        if bot_instance:
            asyncio.run(bot_instance.close())  # Zamykamy bota poprawnie
            bot_instance = None
        print("Bot został zatrzymany. Zaczekaj 10 sekund przed ponownym uruchomieniem.")
        asyncio.sleep(10)  # Oczekiwanie 10 sekund
    except RuntimeError as e:
        return f"Błąd podczas zatrzymywania bota: {str(e)}"

    return "Bot zatrzymany. Możesz uruchomić go ponownie."