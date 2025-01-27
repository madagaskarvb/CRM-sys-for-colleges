import sqlite3

# Подключение к базе данных
connection = sqlite3.connect('nn.db')
cursor = connection.cursor()

# Создание таблицы users (если нет)
def create_baza():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name VARCHAR(150) NOT NULL,
        login VARCHAR(150) NOT NULL UNIQUE,
        email VARCHAR(150) NOT NULL,
        status VARCHAR(150) NOT NULL DEFAULT "Активный",  
        level VARCHAR(150) NOT NULL DEFAULT "user",      
        password VARCHAR(150) NOT NULL
    );""")
    connection.commit()

create_baza()