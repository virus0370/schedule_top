import sqlite3


DATABASE_NAME = "database.db"


def create_database_and_table():
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT NOT NULL UNIQUE
                )
                ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL UNIQUE,
                    login TEXT,
                    password TEXT,
                    group_name TEXT
                )
                ''')
        connection.commit()


def fetch_all_groups():
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM groups')
        rows = cursor.fetchall()

        return rows


def fetch_all_group_tokens_and_names():
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT group_name FROM groups')
        rows = cursor.fetchall()

        return rows


def user_exists(telegram_id):
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM users WHERE telegram_id = ?
            ''', (telegram_id,))

        result = cursor.fetchone()
        return result[0] > 0


def add_or_update_user(telegram_id, login, password, group_name):
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()

        if user_exists(telegram_id):
            cursor.execute('''
                UPDATE users SET login = ?, password = ?, group_name = ? WHERE telegram_id = ?
                ''', (login, password, telegram_id, group_name))
        else:
            cursor.execute('''
                INSERT INTO users (telegram_id, login, password, group_name) 
                VALUES (?, ?, ?, ?)
                ''', (telegram_id, login, password, group_name))

        connection.commit()


def add_group(group_name):
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute('''
                INSERT INTO groups (group_name) 
                VALUES (?)
                ''', (group_name,))
        except sqlite3.IntegrityError:
            pass

        connection.commit()


def get_login_and_password(group_name):
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.cursor()

        cursor.execute('''
            SELECT login, password FROM users WHERE group_name = ?
            ''', (group_name,))

        result = cursor.fetchall()
        return result
