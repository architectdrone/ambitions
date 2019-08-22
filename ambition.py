import sqlite3
import os

MOST_RECENT_DB_VERSION = 1

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
    crsr.execute(f"PRAGMA user_version = {MOST_RECENT_DB_VERSION}")
    connection.commit()
    connection.close()

connection = sqlite3.connect(DB_NAME)
crsr = connection.cursor()

#Make sure the database is up to date.
crsr.execute("PRAGMA user_version")
current_db_version = crsr.fetchone()[0]
print(f"You are on DB version {current_db_version}. Most recent DB version: {MOST_RECENT_DB_VERSION}")
if current_db_version != MOST_RECENT_DB_VERSION:
    print("Updating to most recent version...")
    distance = MOST_RECENT_DB_VERSION - current_db_version
    for i in range(distance):
        current = i+1+current_db_version
        with open(f'schemas\\{current}.sql', 'r') as f:
            crsr.executescript(f.read())
    print("Okay, done.")
    crsr.execute(f"PRAGMA user_version = {MOST_RECENT_DB_VERSION}")
    connection.commit()