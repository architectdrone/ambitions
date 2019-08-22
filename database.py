import sqlite3
import os

MOST_RECENT_DB_VERSION = 0

DB_NAME = 'ambition.db'

class database():
    def __init__(self):
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

        self.connection = sqlite3.connect(DB_NAME)
        self.crsr = self.connection.cursor()

        #Make sure the database is up to date.
        self.crsr.execute("PRAGMA user_version")
        current_db_version = self.crsr.fetchone()[0]
        print(f"You are on DB version {current_db_version}. Most recent DB version: {MOST_RECENT_DB_VERSION}")
        if current_db_version != MOST_RECENT_DB_VERSION:
            print("Updating to most recent version...")
            distance = MOST_RECENT_DB_VERSION - current_db_version
            for i in range(distance):
                current = i+1+current_db_version
                with open(f'schemas\\{current}.sql', 'r') as f:
                    self.crsr.executescript(f.read())
            print("Okay, done.")
            self.crsr.execute(f"PRAGMA user_version = {MOST_RECENT_DB_VERSION}")
            self.connection.commit()
    
    def get(self, command):
        '''
        Runs command and returns the result
        '''

        self.crsr.execute(command)
        return self.crsr.fetchall()
    
    def run(self, command):
        '''
        Runs command, but doesn't return a result
        '''

        self.crsr.execute(command)
        self.connection.commit()

    def __del__(self):
        self.connection.commit()
        self.connection.close()

class databaseWrapper():
    def __init__(self):
        self.database = database()

    def search(self, table, search = (), limit = -1):
        '''
        Searches a table. If query is not specified, return all records. If it is, return only those records that match the query.
        @param table The table to search in.
        @param search A tuple that specifies a search query. The first element is the key, the second element is the value.
        @param limit The limit.
        @return A list of dictionaries that matches the query.
        '''

        query = f"SELECT * FROM {table} "
        if search != ():
            query += f'WHERE {search[0]} = '
            if type(search[1]) is str:
                query += f'"{search[1]}" '
            else:
                query += f'{search[1]} '
        if limit > 0:
            query+=f"LIMIT {limit}"
        return self._parseQuery(query, table)

    def getColumnNames(self, table):
        return [i[1] for i in self.database.get(f"PRAGMA table_info({table});")]

    def _parse(self, list_to_parse, table):
        '''
        Takes in a single db record. Returns a dictionary with the same information.
        @param list_to_parse A single DB record.
        @param table The table from which list_to_parse came.
        @return A dictionary. The keys are the names of the columns, the values are the values from the record.
        '''

        to_return = {}
        for key, value in zip(self.getColumnNames(table), list_to_parse):
            to_return[key] = value
        return to_return

    def _parseQuery(self, query, table):
        '''
        Takes in a query, returns results.
        @param list_to_parse A single DB record.
        @param table The table from which list_to_parse came.
        @return A list of dictionaries.
        '''
        to_return = []
        for i in self.database.get(query):
            to_return.append(self._parse(i, table))
        return to_return