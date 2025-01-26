import json
import os
from datetime import datetime, timedelta

class UserManager:
    def init(self, storage_file='deleted_users.json'):
        self.storage_file = storage_file
        self.load_deleted_users()

    def load_deleted_users(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                self.deleted_users = json.load(file)
        else:
            self.deleted_users = []

    def save_deleted_users(self):
        with open(self.storage_file, 'w') as file:
            json.dump(self.deleted_users, file, indent=4)

    def delete_user(self, username):
        # добавить логику для удаления пользователя из вашей системы
        deletion_time = datetime.now().isoformat()
        self.deleted_users.append({'username': username, 'deleted_at': deletion_time})
        self.save_deleted_users()
        print(f'Пользователь {username} удалён.')

    def clean_up_old_users(self):
        two_weeks_ago = datetime.now() - timedelta(weeks=2)
        self.deleted_users = [
            user for user in self.deleted_users
            if datetime.fromisoformat(user['deleted_at']) > two_weeks_ago
        ]
        self.save_deleted_users()

    def show_deleted_users(self):
        self.clean_up_old_users()  # Удаляем старые записи перед показом
        if not self.deleted_users:
            print("Нет удалённых пользователей.")
        else:
            print("Удалённые пользователи:")
            for user in self.deleted_users:
                print(f"Пользователь: {user['username']}, Дата удаления: {user['deleted_at']}")

if name == "main":
    user_manager = UserManager()

    # Пример как можно посмотреть
    while True:
        print("\n1. Удалить пользователя")
        print("2. Показать удалённых пользователей")
        print("3. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            username = input("Введите имя пользователя для удаления: ")
            user_manager.delete_user(username)
        elif choice == '2':
            user_manager.show_deleted_users()
        elif choice == '3':
            break
        else:
            print("Неверный выбор, попробуйте снова.")


    # # Проверка прав администратора
    # is_admin = True  # Замените на вашу логику проверки администратора

    # if is_admin:
    #     # Добавление удалённого пользователя
    #     add_deleted_user('user123')
        
    #     # Удаление устаревших пользователей
    #     remove_expired_users()
    # else:
    #     print("У вас нет прав для выполнения этой операции.")
