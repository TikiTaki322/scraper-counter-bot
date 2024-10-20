import psycopg2

from core.settings import settings


def create_db():
    connection = psycopg2.connect(user=settings.bots.db_user, password=settings.bots.db_password, database='postgres',
                                  host=settings.bots.host)
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (f'{settings.bots.db_name}',))
        exists = cursor.fetchone() is not None
        if exists is False:
            cursor.execute(f"CREATE DATABASE {settings.bots.db_name}")


def create_table():
    connection = psycopg2.connect(user=settings.bots.db_user, password=settings.bots.db_password, database=settings.bots.db_name,
                                  host=settings.bots.host)
    connection.autocommit = True
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
            user_id BIGINT PRIMARY KEY,
            user_name VARCHAR(50));"""
        )