import os  # Dodaj ten import
from flask import Flask
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from web import configure_routes  # Zaimportowanie funkcji do konfiguracji tras

# Wczytanie zmiennych środowiskowych
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

# Konfiguracja tras
configure_routes(app, limiter)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
