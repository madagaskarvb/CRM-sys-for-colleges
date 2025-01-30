import sqlite3
import hashlib
import json
from datetime import datetime, timedelta
import os
import sys
import re
import bd

# Подключение к базе данных
connection = sqlite3.connect('nn.db')
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

# Отобразить всех пользователей (не зависит от статуса)
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

print(f"Текущий статус пользователя: {current_status}")
print("Выберите новый статус:")
print(" 1 - Активный")
print(" 2 - Не активен")
choice = input("Ваш выбор: ")
if choice == "1":
    new_status = "Активный"
elif choice == "2":
    new_status = "Не активен"
else:
    print("Некорректный выбор.\n")
try:
    cursor.execute("UPDATE users SET status = ? WHERE login = ?", (new_status, login))
    connection.commit()
    print(f"Статус пользователя обновлён на '{new_status}'.\n")
except sqlite3.Error as e:
    print("Ошибка при обновлении статуса:")
    print(f"   {e}\n")

print("Выберите действие:")

print(" 1 - Удалить пользователя (пометка на удаление)")
print(" 2 - Добавить пользователя")
print(" 3 - Поменять своё имя")
print(" 4 - Отобразить всех пользователей")
print(" 5 - Восстановить «Удалённого» пользователя")
print(" 6 - Изменить статус пользователя (Активный/Не активен)")
print(" 7 - Изменить имя другого пользователя")
print(" 0 - Выйти")
var = input("Ваш выбор: ")

if var == "1":
    delete_user()
elif var == "2":
    add_user()
elif var == "3":
    change_name(current_login)
elif var == "4":
    show_users()
elif var == "5":
    reincornation_user()
elif var == "6":
    change_user_status(current_login)
elif var == "7":
    change_other_user_name()
elif var == "0":
    print("Выход.")
    break
else:
    print("Нет такой команды.\n")

if __name__ == "__main__":
    init()
