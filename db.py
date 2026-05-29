import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY)")
    cursor.execute("CREATE TABLE IF NOT EXISTS balances(user_id INTEGER PRIMARY KEY, amount REAL DEFAULT 0)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            status TEXT DEFAULT 'pending',
            created_at INTEGER
        )
    """)
    conn.commit()
