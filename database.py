import sqlite3


class DatabaseManager:
    def __init__(self, database_filename) -> None:
        # added this to persist the name of the database file
        self.database_filename = database_filename
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()


def _execute(self, statement, values=None):

    with self.connection:  # https://www.pythonforbeginners.com/files/with-statement-in-python
        cursor = self.connection.cursor()
        cursor.execute(statement, values or [])
        return cursor


def create_table(self, table_name, columns):
    '''
    The method offers a flexible way to pass data definition:
    1. Accept two arguments: the name of the table to create, and a dictionary of column names mapped to their data types and constraints
    2. Construct a CREATE TABLE SQL statement like the one shown earlier
    3. Execute the statement using DatabaseManager._execute
    '''
    columns_with_types = [
        f'{column_name} {data_type}'
        # this loop reads all column information
        for column_name, data_type in columns.items()
    ]

    self._execute(
        f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({','.join(columns_with_types)});
            '''
    )


def drop_table(self, table_name):
    '''
    The method drops a table:
    1. Accept two arguments: the name of the table to create, and a dictionary of column names mapped to their data types and constraints
    2. Construct a DROP TABLE SQL statement like the one shown earlier
    3. Execute the statement using DatabaseManager._execute
    '''
    self._execute(
        f'''
            DROP TABLE {table_name};
            '''
    )


def add(self, table_name, data):
    '''
    Adding records using placeholders in SQL insert statements:
    INSERT INTO bookmarks
    (title, url, notes, date_added)
    VALUES (?, ?, ?, ?);
    This method: 
    1. Accepts two arguments: the name of the table, and a dictionary that maps column names to column values
    2. Constructs a placeholder string (a ? for each column specified)
    3. Constructs the string of the column names
    4. Gets the column values as a tuple (A dictionary’s .values() returns a dict_ values object, which happens not to work with sqlite3’s execute method.)
    5. Executes the statement with _execute, passing the SQL statement with placeholders and the column values as separate arguments
    '''
    placeholders = ', '.join('?' * len(data))
    column_names = ', '.join(data.keys())
    column_values = tuple(data.values())

    self._execute(
        f'''
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            ''',
        column_values,
    )


def delete(self, table_name, criteria):
    '''
    We delete a record from the database in SQL using:
    DELETE FROM bookmarks
    WHERE ID = 3;
    To do so, this method:
    1. Accepts two arguments: the table name to delete records from, and a dictionary mapping column names to the value to match on. The criteria should be a required argument, because you don’t want to delete all your records.
    2. Constructs a string of placeholders for the WHERE clause.
    3. Constructs the full DELETE FROM query and executes it with _execute.
    '''
    placeholders = [f'{column} = ?' for column in criteria.keys()]
    delete_criteria = ' AND '.join(placeholders)
    self._execute(
        f'''
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            ''',
        tuple(criteria.values()),  # https://www.w3schools.com/python/python_tuples.asp
    )


def select(self, table_name, criteria=None, order_by=None):
    '''
    we commonly need to find, select, and sort data
    SQL select:
    SELECT * FROM bookmarks
    WHERE ID = 3;
    SQL sort:
    SELECT * FROM bookmarks
    WHERE ID = ?
    ORDER BY title;
    '''
    criteria = criteria or {}

    query = f'SELECT * FROM {table_name}'
    if criteria:
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        select_criteria = ' AND '.join(placeholders)
        query += f' WHERE {select_criteria}'

    if order_by:
        query += f' ORDER BY {order_by}'

    return self._execute(
        query,
        tuple(criteria.values()),
    )
