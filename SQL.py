import sqlite3


class Database:

    def __init__(self):
        self.connect = sqlite3.connect('Users_DB')
        self.cursor = self.connect.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                ID TEXT,
                NAME_ TEXT DEFAULT 1,
                NEW INT DEFAULT 1,
                PAUSE INT DEFAULT 0,
                CHALLENGE INT  DEFAULT 0,
                LITRES INT DEFAULT 0,
                RECOMMENDATION INT DEFAULT 0,
                QUIZ INT DEFAULT 0
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bag_words(
                MAIN_MENU TEXT,
                RECOMMENDATION TEXT,
                LITRES TEXT
            )
        """)

        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quiz(
                        ID TEXT,
                        QUESTION INT DEFAULT 1,
                        CORR_ANS INT DEFAULT 0,
                        TIME_ INT DEFAULT 0
                    )
                """)

        # self.cursor.execute("""ALTER TABLE users ADD COLUMN QUIZ """)

    def insert_data(self, table, column, data):
        self.cursor.execute(f"SELECT {column} FROM {table} WHERE {column}='{data}'")
        if not self.cursor.fetchone():
            self.cursor.execute(f"INSERT INTO {table}({column}) VALUES (?)", (data,))
        self.connect.commit()

    def update_data(self, table, column, data, user_id):
        self.cursor.execute(f"UPDATE {table} SET {column} = {data} WHERE ID={user_id}")
        self.connect.commit()

    def update_name(self, table, column, data, user_id):
        self.cursor.execute(f"UPDATE {table} SET {column} = '{data}' WHERE ID={user_id}")
        self.connect.commit()

    def find_data(self, table, column_1, column_2, data):
        self.cursor.execute(f"SELECT {column_1} FROM {table} WHERE {column_2}='{data}'")
        if self.cursor.fetchone():
            self.cursor.execute(f"SELECT {column_1} FROM {table} WHERE {column_2}='{data}'")
            return self.cursor.fetchone()
        else:
            return False

    def check_position(self, table, column, data, user_id):
        self.cursor.execute(f"SELECT {column} FROM {table} WHERE {column}='{data}' and ID={user_id}")
        if self.cursor.fetchone():
            return True
        else:
            return False

    def count_data(self, table, column, data):
        self.cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {column}={data}")
        if self.cursor.fetchone():
            self.cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {column}={data}")
            return self.cursor.fetchone()
        else:
            return False

