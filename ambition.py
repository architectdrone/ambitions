import sqlite3
import os

MOST_RECENT_DB_VERSION = 0

DB_NAME = 'ambition.db'

# If database doesn't exist, create it
if not os.path.exists(DB_NAME):
    print(f"Creating Database, and updating it to version {MOST_RECENT_DB_VERSION}")
    connection = sqlite3.connect(DB_NAME)
    crsr = connection.cursor()
    for i in range(MOST_RECENT_DB_VERSION+1):
        with open(f'schemas\\{i}.sql', 'r') as f:
            crsr.executescript(f.read())
    print("Okay, Done.")
    connection.close()

