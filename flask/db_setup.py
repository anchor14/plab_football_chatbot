import sqlite3
# from sqlite3 imp


db_filename = '/tmp/sample.db'
connection = sqlite3.connect(db_filename)


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

# def update_table(conn, return_json):


def main():
    database = "pythonsqlite.db"

    sql_create_sessions_table = """CREATE TABLE IF NOT EXISTS times (
    id integer PRIMARY KEY,
    Loc text NOT NULL,
    Sessions text not null
    );
    """


    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_sessions_table)
        print("DB created")
    else:
        print("Error! cannot create db connection")

if __name__ == '__main__':
    main()
