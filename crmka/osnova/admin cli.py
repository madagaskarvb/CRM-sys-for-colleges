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

def is_valid_email(email):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None:
            return True
        else:
            return False

def show_table(db_path: str):
    """
    Prints the contents of the specified SQLite table.
    
    :param db_path: Path to the SQLite database file.
    :param table_name: Name of the table to print.
    """
    try:
        # Connect to the SQLite database
        
        # Fetch column names
        table_name = input("Table name: ")
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

def menu():
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

        if var == "CHANGES IN":
            changes_in_table()
        elif var == "DELETE IN":
            delete_records_table()
        elif var == "WRITE IN":
            write_in_table()
        elif var == "CREATE TABLE":
            create_table()
        elif var == "DELETE TABLE":
            delete_table()
        elif var == "SHOW TABLE":
            show_table("db.sqlite3")
        elif var == "QUIT":
            connection.close()
            break
        else:
            print("No such command\n")

if __name__ == "__main__":
    menu()
