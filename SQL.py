import sqlite3


class Database:

    def __init__(self):
        self.connect = sqlite3.connect('Users_DB')
        self.cursor = self.connect.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                ID TEXT,
                PAUSE INT DEFAULT 0,
                CHALLENGE INT  DEFAULT 0,
                LITRES INT DEFAULT 0,
                RECOMMENDATION INT DEFAULT 0
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bag_words(
                MAIN_MENU TEXT,
                RECOMMENDATION TEXT,
                LITRES TEXT
            )
        """)

    def insert_data(self, table, column, data):
        self.cursor.execute(f"SELECT {column} FROM {table} WHERE {column}='{data}'")
        if not self.cursor.fetchone():
            self.cursor.execute(f"INSERT INTO {table}({column}) VALUES (?)", (data,))
        self.connect.commit()

    def update_data(self, table, column, data, user_id):
        self.cursor.execute(f"UPDATE {table} SET {column} = {data} WHERE ID={user_id}")
        self.connect.commit()

    def find_data(self, table, column, data):
        self.cursor.execute(f"SELECT {column} FROM {table} WHERE {column}='{data}'")
        if self.cursor.fetchone():
            return True
        else:
            return False

