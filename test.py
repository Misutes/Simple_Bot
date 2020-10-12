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
        return 'SELECT COUNT(*) FROM {table}'.format(table=table)

    def createSQL(self, method, where: str = None):
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

    def insert_data(self, tables: list, value: list):
        SQLSelect = self.createSQL(
            self._select(tables),
            self._where(self._eq(tables, value))
        )
        SQLInsert = self.createSQL(
            self._insert(tables, value),
            where=''
        )
        print(SQLSelect)

        print(SQLInsert)


a = SQLReuest()

a.insert_data(['users.id'], [5595812])
