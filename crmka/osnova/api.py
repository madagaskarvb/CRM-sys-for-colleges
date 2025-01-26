import os

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

    # Если статус "Не активен", дать только выход
    if current_status == "Не активен":
        while True:
            print("Выберите действие:")
            print(" 0 - Выйти")
            var = input("Ваш выбор: ")
            if var == "0":
                print("Выход.")
                break
            else:
                print("Аккаунт не активен. Никакие действия недоступны.\n")
        return

    # Если "Активный", даём меню в зависимости от роли
    while True: