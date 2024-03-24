import psycopg2

from contextlib import contextmanager

database = './postgres.db'

@contextmanager
def create_connection(db_file):
    """ create a database connection to a Postgras database """
    conn = psycopg2.connect(host = "localhost", dbname = "postgres", user = "postgres", password = "123456789", port = "5432")
    yield conn
    conn.rollback()
    conn.close()
