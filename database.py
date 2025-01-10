import sqlite3
import json

def create_local_db():
    # Подключаемся к SQLite
    conn = sqlite3.connect('telegram.db')
    cur = conn.cursor()
    
    # Создаем таблицу users
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            language VARCHAR(2) DEFAULT 'en',
            appearance_settings TEXT DEFAULT NULL
        )
    ''')
    
    # Добавляем тестового пользователя
    try:
        cur.execute('''
            INSERT INTO users (username, email, password, language, appearance_settings)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            'lol',
            'lol@lol.com',
            '$2y$10$J1fFAe4RHJAfivxmr7S4NeUGgt/s/vV5pWLyH9/WPX2ZSXmvJZkkm',
            'ru',
            '{"theme":"light","messageSize":"small","backgroundColor":"#e8f5e9","backgroundImage":"pattern1.png"}'
        ))
    except sqlite3.IntegrityError:
        print("Пользователь уже существует")
    
    conn.commit()
    conn.close()

def show_users():
    conn = sqlite3.connect('telegram.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    print("\nСписок пользователей:")
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, Email: {user[2]}")
    conn.close()

if __name__ == '__main__':
    create_local_db()
    show_users()