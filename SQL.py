import sqlite3


def createDB(cursor):
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    user_id TEXT,
                    name TEXT DEFAULT 1,
                    new_user INT DEFAULT 1,
                    pause_pos INT DEFAULT 0,
                    challenge_pos INT  DEFAULT 0,
                    litres_pos INT DEFAULT 0,
                    recommendation_pos INT DEFAULT 0,
                    quiz_pos INT DEFAULT 0
                )
            """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS bad_words(
                    main_menu TEXT,
                    recommendation TEXT,
                    litres TEXT
                )
            """)

    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS quiz(
                            user_id TEXT,
                            question INT DEFAULT 1,
                            correct_answer INT DEFAULT 0,
                            time INT DEFAULT 0
                        )
                    """)

    cursor.execute("""
                            CREATE TABLE IF NOT EXISTS message_text(
                                trigger TEXT,
                                value TEXT
                            )
                        """)

    cursor.execute("""
                            CREATE TABLE IF NOT EXISTS media(
                                media TEXT,
                                value TEXT
                            )
                        """)


def renameColumn(cursor, table, columns):
    for column in columns:
        stmt = "ALTER TABLE {table} RENAME COLUMN {oldname} TO {newname}".format(
            table=table,
            oldname=column[0],
            newname=column[1]
        )
        cursor.execute(stmt)


if __name__ == '__main__':
    connect = sqlite3.connect('Users_DB')
    cursor = connect.cursor()
    # func
    connect.commit()


class Database:

    def __init__(self):
        self.connect = sqlite3.connect('Users_DB')
        self.cursor = self.connect.cursor()
        self.SQLRequest = SQLReuest(self.connect, self.cursor)


class Record:

    def _select(self, tables: list):
        localSelect = 'SELECT '
        localFrom = ' FROM '
        for table in tables:
            localSelect += '{table}, '.format(table=table)
            point = table.find('.')
            localFrom += table[:point] + ', '
        localSelect, localFrom = localSelect[:-2], localFrom[:-2]
        return localSelect + localFrom

    def _where(self, conds):
        localWhere = 'WHERE '
        stmt = ' AND '.join(conds)
        return localWhere + stmt

    def _update(self, table, value):
        localUpdate = 'UPDATE '
        localSet = ' SET '
        point = table.find('.')
        return localUpdate + table[:point] + localSet + '{column}={value}'.format(column=table[point + 1:], value=value)

    def _insert(self, table, value):
        table, value = str(table[0]), str(value[0])
        localInsert = 'INSERT INTO '
        localValue = ' VALUES '
        return localInsert + table.replace('.', '(') + ')' + localValue + '({value})'.format(value=value)

    def _count(self, table):
        point = table.find('.')
        return 'SELECT COUNT({column}) FROM {table}'.format(
            table=table[:point],
            column=table[point+1:]
        )

    def createSQL(self, method, where: str = ''):
        return '{method} {where}'.format(method=method, where=where)


class Inquiry:

    def _eq(self, tables, values):
        conds = ['{column}={value}'.format(column=column, value=value)
                 for column, value in zip(tables, values)]
        return conds

    def _neq(self, tables, values):
        conds = ['{column}!={value}'.format(column=column, value=value)
                 for column, value in zip(tables, values)]
        return conds

    def _ge(self, tables, values):
        conds = ['{column}>={value}'.format(column=column, value=value)
                 for column, value in zip(tables, values)]
        return conds

    def _le(self, tables, values):
        conds = ['{column}<={value}'.format(column=column, value=value)
                 for column, value in zip(tables, values)]
        return conds

    def _ge(self, tables, values):
        conds = ['{column}>{value}'.format(column=column, value=value)
                 for column, value in zip(tables, values)]
        return conds

    def _le(self, tables, values):
        conds = ['{column}<{value}'.format(column=column, value=value)
                 for column, value in zip(tables, values)]
        return conds

    def _isNot(self, tables, values):
        conds = ['{column} IS NOT {value}'.format(column=column, value=value)
                 for column, value in zip(tables, values)]
        return conds

    def _is(self, tables, values):
        conds = ['{column} IS {value}'.format(column=column, value=value)
                 for column, value in zip(tables, values)]
        return conds


class SQLReuest(Inquiry, Record):

    def __init__(self, connect, cursor):
        self.connect = connect
        self.cursor = cursor

    def insert_data(self, tables: list, value: list):
        SQLSelect = self.createSQL(
            self._select(tables),
            self._where(self._eq(tables, value))
        )
        SQLInsert = self.createSQL(
            self._insert(tables, value)
        )
        self.cursor.execute(SQLSelect)
        if not self.cursor.fetchone():
            self.cursor.execute(SQLInsert)
        self.connect.commit()

    def update_data(self, table, column, data, user_id):
        SQLUpdate = self.createSQL(
            self._update()
        )
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
