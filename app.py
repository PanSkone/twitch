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



if __name__ == '__main__':
    app.run(debug=True, port=5000)

