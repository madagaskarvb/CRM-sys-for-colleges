import sqlite3
import hashlib
import json
from datetime import datetime, timedelta
import os
import sys
import re
import bd

# Подключение к базе данных
connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()

# Функция очистки deleted_users.json (удаляем записи из БД, которым больше 14 дней, а также чистим JSON)
def cleanup_deleted_users():
    """
    Удаляем из БД записи, статус которых "Удалён" больше 14 дней назад.
    Затем чистим deleted_users.json, убирая из него те же записи.
    """
    if not os.path.exists('deleted_users.json'):
        return  # если файла нет, просто выходим

    # Загружаем данные
    try:
        with open('deleted_users.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        data = []

    if not isinstance(data, list):
        data = []

    now = datetime.now()
    new_data = []

    for user_dict in data:
        try:
            deleted_at = datetime.fromisoformat(user_dict.get('deleted_at', '1970-01-01T00:00:00'))
        except ValueError:
            # Если формат неправильный, пропустим запись
            continue

        # Если прошло >= 14 дней
        if (now - deleted_at) >= timedelta(days=14):
            # Удаляем пользователя из БД окончательно
            try:
                cursor.execute("DELETE FROM users WHERE login = ? AND status = 'Удалён'", (user_dict['login'],))
                connection.commit()
            except sqlite3.Error:
                pass
        else:
            # Если не прошло, оставляем в списке
            new_data.append(user_dict)

    # Перезаписываем файл "очищенными" данными
    with open('deleted_users.json', 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)

def changes_in_table():
    name = input("Table name: ")
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'")
    table_exists = cursor.fetchone()
    if not table_exists:
        # If the table does not exist, print a message
        print(f"Table '{name}' does not exist.")
        return
    
    set = input("SET: ")
    where = input("WHERE: ")
    try:
        cursor.execute(f"UPDATE {name} SET {set} WHERE {where}")
        connection.commit()
        print("Data added!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def delete_records_table():
    name = input("Table name: ")
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'")
    table_exists = cursor.fetchone()
    if not table_exists:
        # If the table does not exist, print a message
        print(f"Table '{name}' does not exist.")
        return

    where = input("DELETE WHERE: ")
    cursor.execute(f"DELETE FROM {name} WHERE {where}")

def write_in_table():
    name = input("Table name: ")
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'")
    table_exists = cursor.fetchone()
    if not table_exists:
        # If the table does not exist, print a message
        print(f"Table '{name}' does not exist.")
        return

    data = input("Input data: ")
    try:
        cursor.execute(f"""INSERT INTO {name} VALUES {data}""")
        connection.commit()
        print("Data added!")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def create_table():
    table_name = input("Enter the name of the table: ").strip()

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    table_exists = cursor.fetchone()

    if not table_exists:
        # If the table does not exist, print a message
        print(f"Table '{table_name}' does not exist.")
        return

    table_name = input("Enter the name of the table: ").strip()
    table_attributes = input(f"Enter the attributes for the table '{table_name}': ").strip()
    create_table_query = f"CREATE TABLE {table_name} ({table_attributes});"

    try:
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{table_name}' created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def delete_table():
    table_delete = input("Name of table to delete: ")
    cursor.execute(f"DROP TABLE IF EXISTS {table_delete}")
    connection.commit()
    print("Table deleted!")


# Запись удалённого (точнее, помеченного на удаление) пользователя в deleted_users.json
def store_deleted_user(user_data):
    """Сохраняет данные "удалённого" пользователя в deleted_users.json с датой удаления."""
    if not os.path.exists('deleted_users.json'):
        with open('deleted_users.json', 'w', encoding='utf-8') as f:
            json.dump([], f)

    with open('deleted_users.json', 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
        if not isinstance(existing_data, list):
            existing_data = []

    # Добавляем поле "deleted_at" (прямо сейчас)
    user_data['deleted_at'] = datetime.now().isoformat()
    existing_data.append(user_data)

    with open('deleted_users.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)


def is_valid_email(email):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None:
            return True
        else:
            return False

# Добавление нового пользователя
def add_user():
    print("\n=== Добавление нового пользователя ===")
    name = input("Введите имя: ")
    login = input("Введите логин: ")
    email = input("Введите email: ")
    if not is_valid_email(email):
        email = input("Почта неправильная, введите правильный адрес: ")
    password = input("Введите пароль: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    role = input("Введите роль (admin/user/menager). По умолчанию user: ")
    role_lower = role.strip().lower()
    if role_lower == 'admin':
        user_role = 'admin'
    elif role_lower == 'menager':
        user_role = 'menager'
    else:
        user_role = 'user'

    try:
        cursor.execute(
            "INSERT INTO users(name, login, email, password, level) VALUES (?,?,?,?,?)",
            (name, login, email, hashed_password, user_role)
        )
        connection.commit()
        print("Новый пользователь добавлен!\n")
    except sqlite3.Error as e:
        print("Ошибка при добавлении пользователя:")
        print(f"   {e}\n")


# "Удаление" пользователя (смена статуса на "Удалён")
def delete_user():
    show_users()
    print("\n=== Удаление пользователя (пометка) ===")
    login = input("Введите логин пользователя, которого хотите удалить: ")

    # Сначала ищем пользователя
    cursor.execute("SELECT user_id, name, login, email, status, level, password FROM users WHERE login = ?", (login,))
    user = cursor.fetchone()
    if not user:
        print("Такого пользователя не существует.\n")
        return

    user_dict = {
        "user_id": user[0],
        "name": user[1],
        "login": user[2],
        "email": user[3],
        "status": user[4],
        "level": user[5],
        "password": user[6]
    }

    if user_dict['status'] == 'Удалён':
        print("Этот пользователь уже помечен на удаление.\n")
        return

    # Обновляем статус в БД
    try:
        cursor.execute("UPDATE users SET status = 'Удалён' WHERE login = ?", (login,))
        connection.commit()
    except sqlite3.Error as e:
        print("Ошибка при изменении статуса:")
        print(f"   {e}\n")
        return

    # Сохраняем в JSON
    store_deleted_user(user_dict)
    print("Пользователь помечен как 'Удалён' и записан в deleted_users.json!\n")


# Функция восстановления пользователей
def reincornation_user():
    if not os.path.exists('deleted_users.json'):
        print("Файл с удалёнными пользователями отсутствует, восстанавливать некого.\n")
        return

    with open('deleted_users.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print("Нет ни одного сохранённого удалённого пользователя.\n")
        return

    print("\n=== Список 'удалённых' пользователей ===")
    for idx, user_dict in enumerate(data, start=1):
        print(f"{idx}. Логин: {user_dict.get('login','')}, Имя: {user_dict.get('name','')}, Удалён: {user_dict.get('deleted_at','')}")

    user_to_restore = input("\nВведите логин пользователя, которого хотите восстановить: ")
    target_user_dict = None
    for item in data:
        if item.get('login') == user_to_restore:
            target_user_dict = item
            break

    if not target_user_dict:
        print("Пользователь с таким логином не найден в списке удалённых.\n")
        return

    cursor.execute("SELECT login, status FROM users WHERE login = ?", (target_user_dict['login'],))
    existing = cursor.fetchone()
    if not existing:
        print("ВНИМАНИЕ: в БД отсутствует запись о данном пользователе. Вероятно, уже очищен.")
        return

    # Если статус не "Удалён", бессмысленно «восстанавливать»
    if existing[1] != 'Удалён':
        print(f"У пользователя статус {existing[1]}, восстанавливать не требуется.\n")
        return

    # Меняем статус на "Активный"
    try:
        cursor.execute("UPDATE users SET status = 'Активный' WHERE login = ?", (target_user_dict['login'],))
        connection.commit()
        print(f"Пользователь {target_user_dict['login']} успешно восстановлен (статус 'Активный')!\n")
    except sqlite3.Error as e:
        print("Ошибка при восстановлении пользователя:")
        print(f"   {e}\n")
        return

    # Удаляем запись из JSON
    updated_data = [u for u in data if u.get('login') != user_to_restore]
    with open('deleted_users.json', 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)


# Изменение имени
def change_name(current_login):
    print("\n=== Изменение имени (для себя) ===")
    new_name = input("Введите новое имя: ")
    try:
        cursor.execute("UPDATE users SET name = ? WHERE login = ?", (new_name, current_login))
        connection.commit()
        print("Новое имя успешно сохранено!\n")
    except sqlite3.Error as e:
        print("Ошибка при изменении имени:")
        print(f"   {e}\n")

def change_other_user_name():

    show_users()
    print("\n=== Изменение имени другого пользователя ===")
    login = input("Введите логин пользователя, чьё имя хотите изменить: ")
    # Проверяем, существует ли пользователь
    cursor.execute("SELECT user_id, name FROM users WHERE login = ?", (login,))
    user = cursor.fetchone()
    if not user:
        print("Пользователь с таким логином не найден.\n")
        return

    print(f"Текущее имя пользователя: {user[1]}")
    new_name = input("Введите новое имя: ")
    try:
        cursor.execute("UPDATE users SET name = ? WHERE login = ?", (new_name, login))
        connection.commit()
        print("Имя пользователя успешно изменено!\n")
    except sqlite3.Error as e:
        print("Ошибка при изменении имени другого пользователя:")
        print(f"   {e}\n")

def show_table(db_path: str, table_name: str):
    """
    Prints the contents of the specified SQLite table.
    
    :param db_path: Path to the SQLite database file.
    :param table_name: Name of the table to print.
    """
    try:
        # Connect to the SQLite database
        
        # Fetch column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Fetch table contents
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Print column headers
        print(" | ".join(columns))
        print("-" * (len(" | ".join(columns)) + 5))
        
        # Print rows
        for row in rows:
            print(" | ".join(str(value) for value in row))

    except sqlite3.Error as e:
        print(f"Error: {e}")

def show_users():
    print("\n=== Список пользователей ===")
    print("Имя || Логин || Почта || Статус || Роль")
    for row in cursor.execute("SELECT name, login, email, status, level FROM users"):
        print(row)
    print()

# Функция изменения статуса пользователя (только для admin)
def change_user_status(current_login):

    show_users()
    print("\n=== Изменение статуса пользователя ===")
    login = input("Введите логин пользователя: ")
    cursor.execute("SELECT user_id, status FROM users WHERE login = ?", (login,))
    user = cursor.fetchone()

    if not user:
        print("Такого пользователя не существует.\n")
        return

    # Проверяем, что не пытаемся изменить статус самого себя
    if login == current_login:  # тот же login, что у админа
        print("Нельзя менять свой собственный статус.\n")
        return

    current_status = user[1]

    # Проверяем, что статус не "Удалён"
    if current_status == "Удалён":
        print("Статус 'Удалён': изменять статус такого пользователя нельзя. Воспользуйтесь восстановлением.\n")
        return

# Функция авторизации
def auth():
    print("\n=== Авторизация ===")
    login = input("Логин: ")
    password = input("Пароль: ")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute("SELECT login, level, status FROM users WHERE login = ? AND password = ?", (login, hashed_password))
    user_data = cursor.fetchone()

    if user_data is None:
        print("Неверный логин или пароль.\n")
        return None
    else:
        # user_data = (login, level, status)
        if user_data[2] == "Удалён":
            print("Ваш аккаунт удалён. Обратитесь к администратору.\n")
            return None
        elif user_data[2] == "Не активен":
            print(f"Добро пожаловать, {login}. Ваш аккаунт «Не активен» (забанен).")
            print("Никакие действия, кроме выхода, недоступны.\n")
            return (user_data[0], user_data[1], user_data[2])
        else:
            print(f"Успешный вход! Добро пожаловать, {login} (роль: {user_data[1]}), статус: {user_data[2]}\n")
            return (user_data[0], user_data[1], user_data[2])
            
# Основная «точка входа»
def init():
    create_baza()
    cleanup_deleted_users()  # перед стартом убираем записи старше 14 дней

    # Проверка наличия админов
    cursor.execute("SELECT user_id FROM users WHERE level = 'admin'")
    admin_exists = cursor.fetchone()
    if not admin_exists:
        print("В базе нет администраторов. Создаём первого администратора.\n")
        name = input("Введите имя администратора: ")
        login = input("Введите логин: ")
        email = input("Введите email: ")
        password = input("Введите пароль: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute(
            "INSERT INTO users(name, login, email, password, level) VALUES (?,?,?,?,?)",
            (name, login, email, hashed_password, 'admin')
        )
        connection.commit()
        print("Администратор создан! Можете авторизоваться.\n")

    current_user = None
    while current_user is None:
        current_user = auth()
        if current_user is None:
            again = input("Повторить попытку входа? (y/n): ")
            if again.lower() != 'y':
                print("Выход из программы.")
                sys.exit(0)

    current_login, current_role, current_status = current_user
    return current_login

def menu(current_login):
    while True:
        # print("Выберите действие:")
        # print(" 1 - Удалить пользователя (пометка на удаление)")
        # print(" 2 - Добавить пользователя")
        # print(" 3 - Поменять своё имя")
        # print(" 4 - Отобразить всех пользователей")
        # print(" 5 - Восстановить «Удалённого» пользователя")
        # print(" 6 - Изменить статус пользователя (Активный/Не активен)")
        # print(" 7 - Изменить имя другого пользователя")
        # print(" 0 - Выйти")
        var = input("ACTION: ")

        if var == "CHANGE TABLE":
            changes_in_table()
        elif var == "DELETE":
            delete_records_table()
        elif var == "WRITE":
            write_in_table()
        elif var == "CREATE TABLE":
            create_table()
        elif var == "DELETE TABLE":
            delete_table()
        elif var == "ADD USER":
            add_user()
        elif var == "DELETE USER":
            delete_user()
        elif var == "REINCARNATE USER":
            reincornarion_user()
        elif var == "CHANGE NAME":
            change_name(current_login)
        elif var == "CHANGE OTHER NAME":
            change_other_name()
        elif var == "SHOW TABLE":
            show_table("db.sqlite3", )
        elif var == "CHANGE OTHER NAME":
            change_other_name()
        elif var  ==  "CHANGE USER STATUS":
            change_user_status()
        elif var == "QUIT":
            break
        else:
            print("No such command\n")

if __name__ == "__main__":
    current_login = init()
    menu(current_login)
