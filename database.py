# database.py
import sqlite3

# Funkcja do połączenia się z bazą danych
def connect_db():
    return sqlite3.connect("bot_data.db")

# Funkcja do inicjalizacji bazy danych
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Tworzenie tabeli logów
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tworzenie tabeli statusów bota
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bot_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            running BOOLEAN
        )
    """)
    
    # Ustawienie początkowego stanu bota
    cursor.execute("INSERT INTO bot_status (running) VALUES (0)")
    conn.commit()
    conn.close()

# Funkcja do zapisywania logów
def save_log(username, message):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (username, message) VALUES (?, ?)", (username, message))
    conn.commit()
    conn.close()

# Funkcja do zapisywania stanu bota
def update_bot_status(running):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE bot_status SET running = ? WHERE id = 1", (running,))
    conn.commit()
    conn.close()

# Funkcja do pobierania stanu bota
def get_bot_status():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT running FROM bot_status WHERE id = 1")
    status = cursor.fetchone()
    conn.close()
    return status[0] if status else None

# Funkcja do pobierania logów
def get_logs():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10")
    logs = cursor.fetchall()
    conn.close()
    return logs
