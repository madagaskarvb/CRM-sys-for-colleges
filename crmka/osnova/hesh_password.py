import hashlib
import sqlite3

password = 'admin'
hashed_password = hashlib.sha256(password.encode()).hexdigest()

# Подключение к базе данных 
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL
)
''')

# Вставка данных в таблицу
username = 'admin_user'  # ЗАМЕНИТЬ на нужное имя пользователя
cursor.execute('''
INSERT INTO users (username, password_hash) VALUES (?, ?)
''', (username, hashed_password))

conn.commit()
conn.close()

print(f'Пользователь {username} успешно добавлен с хешированным паролем.')