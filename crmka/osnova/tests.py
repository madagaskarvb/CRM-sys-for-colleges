import unittest
import sqlite3
import hashlib
from datetime import datetime, timedelta
import json
import os
from main import cleanup_deleted_users, is_valid_email

# Включим в тестирование функции
# Для тестов мы добавим сюда только основные функции программы.

def create_baza(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name VARCHAR(150) NOT NULL,
        login VARCHAR(150) NOT NULL UNIQUE,
        email VARCHAR(150) NOT NULL,
        status VARCHAR(150) NOT NULL DEFAULT "Активный",  
        level VARCHAR(150) NOT NULL DEFAULT "user",      
        password VARCHAR(150) NOT NULL
    );""")

def add_user(cursor, name, login, email, password, role='user'):
    if not is_valid_email(email):
        raise ValueError("Некорректный формат email")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        "INSERT INTO users(name, login, email, password, level) VALUES (?,?,?,?,?)",
        (name, login, email, hashed_password, role)
    )

def delete_user(cursor, login):
    cursor.execute("UPDATE users SET status = 'Удалён' WHERE login = ?", (login,))
    
def change_user_status(cursor, login, new_status):
    cursor.execute("UPDATE users SET status = ? WHERE login = ?", (new_status, login))

def reincornation_user(cursor, login):
    cursor.execute("UPDATE users SET status = 'Активный' WHERE login = ?", (login,))

# Тестирование
class TestUserManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Подготовка базы данных для тестов"""
        # создаём подключение к базе данных в памяти
        cls.connection = sqlite3.connect(":memory:")
        cls.cursor = cls.connection.cursor()
        create_baza(cls.cursor)

    @classmethod
    def tearDownClass(cls):
        """Закрытие соединения с базой данных"""
        cls.connection.close()
    
    def setUp(self):
        self.cursor.execute("DELETE FROM users")
        self.connection.commit()

        if os.path.exists('deleted_users.json'):
            os.remove('deleted_users.json')

    def test_add_user(self):
        """Тестирование добавления нового пользователя"""
        add_user(self.cursor, "Test User", "test_user", "test@example.com", "password123")
        
        self.cursor.execute("SELECT * FROM users WHERE login = ?", ("test_user",))
        user = self.cursor.fetchone()

        self.assertIsNotNone(user)
        self.assertEqual(user[2], "test_user")  # login
        self.assertEqual(user[3], "test@example.com")  # email
        self.assertEqual(user[4], "Активный")  # status
        self.assertEqual(user[5], "user")  # level

    def test_delete_user(self):
        """Тестирование удаления (пометка на удаление) пользователя"""
        # Добавляем пользователя
        add_user(self.cursor, "Test User", "test_user", "test@example.com", "password123")
        
        # Выполняем удаление
        delete_user(self.cursor, "test_user")
        
        self.cursor.execute("SELECT status FROM users WHERE login = ?", ("test_user",))
        user = self.cursor.fetchone()

        self.assertEqual(user[0], "Удалён")

    def test_change_user_status(self):
        """Тестирование изменения статуса пользователя"""
        # Добавляем пользователя
        add_user(self.cursor, "Test User", "test_user", "test@example.com", "password123")
        
        # Меняем статус
        change_user_status(self.cursor, "test_user", "Не активен")
        
        self.cursor.execute("SELECT status FROM users WHERE login = ?", ("test_user",))
        user = self.cursor.fetchone()

        self.assertEqual(user[0], "Не активен")

    def test_reincornation_user(self):
        """Тестирование восстановления пользователя"""
        # Добавляем пользователя и помечаем его как удалённого
        add_user(self.cursor, "Test User", "test_user", "test@example.com", "password123")
        delete_user(self.cursor, "test_user")
        
        # Восстанавливаем пользователя
        reincornation_user(self.cursor, "test_user")
        
        self.cursor.execute("SELECT status FROM users WHERE login = ?", ("test_user",))
        user = self.cursor.fetchone()

        self.assertEqual(user[0], "Активный")

    def test_invalid_email(self):
            """Тестирование неправильного email при добавлении пользователя"""
            # Попытка добавления с неверным email
            with self.assertRaises(ValueError):
                add_user(self.cursor, "Test User", "test_user", "invalid_email", "password123")

    def test_empty_deleted_users_json(self):
        """Тестируем, что файл deleted_users.json создаётся пустым, если его нет"""
        if os.path.exists('deleted_users.json'):
            os.remove('deleted_users.json')
        
        self.assertFalse(os.path.exists('deleted_users.json'))  # файл должен быть создан пустым
        # Пытаемся сохранить в пустой файл
        user_data = {"login": "test_user", "name": "Test User", "deleted_at": datetime.now().isoformat()}
        with open('deleted_users.json', 'w', encoding='utf-8') as f:
            json.dump([user_data], f, ensure_ascii=False, indent=4)
        
        # Проверяем, что файл существует и не пуст
        self.assertTrue(os.path.exists('deleted_users.json'))
        with open('deleted_users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertEqual(len(data), 1)

    def test_cleanup_deleted_users(self):
        """Тест очистки deleted_users.json"""
        if os.path.exists('deleted_users.json'):
            os.remove('deleted_users.json')

        # Создаём файл с пользователем, который был удалён более 14 дней назад
        user_data = {"login": "test_user", "name": "Test User", "deleted_at": (datetime.now() - timedelta(days=15)).isoformat()}
        with open('deleted_users.json', 'w', encoding='utf-8') as f:
            json.dump([user_data], f, ensure_ascii=False, indent=4)

        # Теперь проверим, что старые записи удаляются
        cleanup_deleted_users()

        with open('deleted_users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(len(data), 0)  # После очистки данных не должно быть


def check_database_connection(connection):
    """Проверяет подключение к базе данных."""
    try:
        cursor = connection.cursor()
        # Проверим, существует ли таблица users
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        table = cursor.fetchone()
        if table is None:
            raise RuntimeError("Таблица 'users' отсутствует в базе данных.")
        return True
    except sqlite3.Error as e:
        raise RuntimeError(f"Ошибка подключения к базе данных: {e}")
    
class TestDatabaseConnection(unittest.TestCase):
    
    def setUp(self):
        """Создание временной базы данных перед каждым тестом."""
        self.connection = sqlite3.connect(":memory:")  # Используем новую базу данных для каждого теста
        self.cursor = self.connection.cursor()
        create_baza(self.cursor)  # Создаём таблицу users для тестов
        self.connection.commit()

    def tearDown(self):
        """Закрытие соединения после каждого теста."""
        if self.connection:
            self.connection.close()

    def test_successful_connection(self):
        """Тест успешного подключения к базе данных"""
        # Проверяем, что функция успешно подтверждает подключение
        self.assertTrue(check_database_connection(self.connection))
    
    def test_missing_table(self):
        """Тест ошибки при отсутствии таблицы в базе данных"""
        # Удаляем таблицу users, чтобы проверить поведение
        self.cursor.execute("DROP TABLE IF EXISTS users;")
        self.connection.commit()

        # Проверяем, что вызывается исключение при отсутствии таблицы
        with self.assertRaises(RuntimeError) as context:
            check_database_connection(self.connection)
        self.assertEqual(str(context.exception), "Таблица 'users' отсутствует в базе данных.")
    
    def test_failed_connection(self):
        """Тест ошибки при невозможности подключения к базе данных"""
        # Закрываем соединение
        self.connection.close()

        # Проверяем, что вызывается исключение при использовании закрытого подключения
        with self.assertRaises(sqlite3.ProgrammingError):
            check_database_connection(self.connection)

if __name__ == '__main__':
    unittest.main()
