# app.py
from flask import Flask, jsonify, send_from_directory
from bot_manager import start_bot, stop_bot, bot_running

app = Flask(__name__)

@app.route('/')
def serve_html():
    return send_from_directory(".", "index.html")

@app.route('/start', methods=['GET'])
def start():
    if not bot_running:
        start_bot()
        return jsonify({"status": "Bot uruchomiony"})
    return jsonify({"status": "Bot już działa"})

@app.route('/stop', methods=['GET'])
def stop():
    result = stop_bot()
    return jsonify({"status": result})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"running": bot_running})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
