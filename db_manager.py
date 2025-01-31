# db_manager.py
import mysql.connector
from mysql.connector import Error

connection = None  # Globalna zmienna połączenia

def create_connection():
    global connection
    if connection is None or not connection.is_connected():
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='chat_db',  # Twoja baza danych
                user='root',  # Twoje dane logowania do MySQL
                password=''  # Twoje hasło (jeśli masz ustawione)
            )
            if connection.is_connected():
                print("Połączono z bazą danych")
        except Error as e:
            print(f"Błąd połączenia z bazą danych: {e}")
            connection = None
    return connection

# Usuwamy funkcję create_table, ponieważ tabela już istnieje w bazie danych

def insert_chat_log(username, message):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO chat_logs (username, message)  # Zakładamy, że tabela chat_logs już istnieje
            VALUES (%s, %s)
        """, (username, message))
        connection.commit()  # Zatwierdzamy zmiany w bazie danych
        cursor.close()  # Zamykamy kursor
