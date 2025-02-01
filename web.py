from flask import jsonify, request, send_from_directory
from bot_manager import start_bot, stop_bot, bot_running, current_match_id
from db_manager import fetch_matches, fetch_match_by_id
from flask_limiter import Limiter

def authenticate_request(req):
    """Prosta autoryzacja na podstawie klucza API."""
    auth_header = req.headers.get("Authorization")
    if not auth_header or auth_header.split(" ")[-1] != os.getenv('API_KEY'):
        return False
    return True

def configure_routes(app, limiter):
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

    @app.route('/matches', methods=['GET'])
    def matches():
        matches_data = fetch_matches()
        return jsonify(matches_data)

    @app.route('/match/<int:match_id>', methods=['GET'])
    def get_match(match_id):
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
