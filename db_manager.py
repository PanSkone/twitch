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
            INSERT INTO chat_logs (username, message, match_id)
            VALUES (%s, %s, %s)
        """
        # Wykorzystujemy executemany do dodania wielu rekordów
        cursor.executemany(query, logs)
        connection.commit()  # Zatwierdzamy zmiany w bazie danych
        cursor.close()  # Zamykamy kursor

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

# Pobiera tagi drużyn na podstawie match_id
def fetch_team_tags_by_match(match_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
            SELECT t1.tag, t2.tag 
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.id
            JOIN teams t2 ON m.team2_id = t2.id
            WHERE m.id = %s
        """
        cursor.execute(query, (match_id,))
        result = cursor.fetchone()  # Pobieramy pierwszy wynik
        cursor.close()
        return result if result else (None, None)  # Zwracamy tagi lub None
    return None, None

# Wypisanie meczy na podstawie daty z DB
def fetch_matches_by_date(date_str):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        query = """
            SELECT m.id, m.team1_id, t1.name AS team1_name, m.team2_id, t2.name AS team2_name, m.time_start_match
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.id
            JOIN teams t2 ON m.team2_id = t2.id
            WHERE DATE(m.time_start_match) = %s
        """
        cursor.execute(query, (date_str,))
        matches = cursor.fetchall()
        cursor.close()

        # Przekształcamy dane w listę słowników
        match_list = [
            {"id": match[0], "team1_id": match[1], "team1_name": match[2], "team2_id": match[3], "team2_name": match[4], "time_start_match": match[5]}
            for match in matches
        ]
        return match_list
    return []
