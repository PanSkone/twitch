# app.py
from flask import Flask, jsonify, request, send_from_directory
from bot_manager import start_bot, stop_bot, bot_running, current_match_id
from dotenv import load_dotenv
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Wczytanie zmiennych środowiskowych
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

API_KEY = os.getenv('API_KEY', 'default_api_key')  # Klucz do autoryzacji

limiter = Limiter(key_func=get_remote_address)  
limiter.init_app(app)  # Teraz poprawnie podpinamy do aplikacji Flask

def authenticate_request(req):
    """Prosta autoryzacja na podstawie klucza API."""
    auth_header = req.headers.get("Authorization")
    if not auth_header or auth_header.split(" ")[-1] != API_KEY:
        return False
    return True

@app.route('/')
def serve_html():
    return send_from_directory(".", "index.html")

@app.route('/start', methods=['GET'])
@limiter.limit("5 per minute")  # Limit 5 żądań na minutę na IP
def start():
    if not authenticate_request(request):
        return jsonify({"error": "Unauthorized"}), 403
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

# Trasa która będzie zwracać dane z tabeli matches
@app.route('/matches', methods=['GET'])
def matches():
    from db_manager import fetch_matches
    matches_data = fetch_matches()  # Pobieramy dane z tabeli matches
    return jsonify(matches_data)  # Zwracamy dane w formacie JSON

# Dodatkowy web który przenosi do szczegółu meczu
@app.route('/match/<int:match_id>', methods=['GET'])
def get_match(match_id):
    from db_manager import fetch_match_by_id
    match = fetch_match_by_id(match_id)
    if match:
        return jsonify({
            "id": match[0],
            "team1_id": match[1],
            "team2_id": match[2],
            "time_start_match": match[3]
        })
    return jsonify({"error": "Mecz nie znaleziony"}), 404

@app.route('/start_match/<int:match_id>', methods=['GET'])
def start_match(match_id):
    response = start_bot(match_id)
    return jsonify({"status": response})

@app.route('/stop_match/<int:match_id>', methods=['GET'])
def stop_match(match_id):
    response = stop_bot(match_id)
    return jsonify({"status": response})

@app.route('/status_match', methods=['GET'])
def status_match():
    return jsonify({"running": bot_running, "match_id": current_match_id})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

