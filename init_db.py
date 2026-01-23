import sqlite3

DATABASE = "incidentdesk.db"

conn = sqlite3.connect(DATABASE)
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        severity TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """
)
conn.commit()
conn.close()

print("Database initialised.")
