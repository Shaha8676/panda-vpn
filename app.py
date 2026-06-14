"""
Flask server: vpn-app.html ni serve qiladi va aiogram botni
background thread'da ishga tushiradi (Railway uchun).
"""
import asyncio
import threading
import os
from flask import Flask, send_from_directory

import bot as bot_module

app = Flask(__name__, static_folder=".")


@app.route("/")
def index():
    return send_from_directory(".", "vpn-app.html")


@app.route("/vpn-app.html")
def vpn_app():
    return send_from_directory(".", "vpn-app.html")


def run_bot():
    asyncio.run(bot_module.main())


if __name__ == "__main__":
    # Botni alohida oqimda (thread) ishga tushiramiz
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Flask serverni ishga tushiramiz
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
