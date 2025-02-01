# db_manager.py
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
connection = None  # Globalna zmienna połączenia

def create_connection():
    global connection
    if connection is None or not connection.is_connected():
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                database=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            if connection.is_connected():
                print("Połączono z bazą danych")
        except Error as e:
            print(f"Błąd połączenia z bazą danych: {e}")
            connection = None
    return connection

def insert_chat_log(logs):
    """Funkcja do wstawiania wielu wiadomości do bazy danych za jednym razem."""
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
            INSERT INTO chat_logs (username, message)
            VALUES (%s, %s)
        """
        # Wykorzystujemy executemany do dodania wielu rekordów
        cursor.executemany(query, logs)
        connection.commit()  # Zatwierdzamy zmiany w bazie danych
        cursor.close()  # Zamykamy kursor


# Funkcja do pobierania danych z bazy
def fetch_matches():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, team1_id, team2_id, time_start_match FROM matches")  # Pobieramy dane z tabeli matches
        rows = cursor.fetchall()  # Pobieramy wszystkie wyniki zapytania
        cursor.close()
        return rows
    return []

# Pobiera dane tylko jednego konkretnego meczu
def fetch_match_by_id(match_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, team1_id, team2_id, time_start_match FROM matches WHERE id = %s", (match_id,))
        match = cursor.fetchone()
        cursor.close()
        return match
    return None
