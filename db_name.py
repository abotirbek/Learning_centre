import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname = 'learning_centre',
        user = 'postgres',
        password = 'MILM1234',
        host = 'localhost',
        port = 5432
    )
get_connection()
