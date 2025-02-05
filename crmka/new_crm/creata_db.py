def create_tables(conn):
    """Создаёт необходимые таблицы, если их нет."""
    try:
        cursor = conn.cursor()

        # Пример таблицы для студентов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name  TEXT NOT NULL,
                email      TEXT NOT NULL UNIQUE,
                phone      TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Пример таблицы для материалов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                material_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                title         TEXT NOT NULL,
                description   TEXT,
                author        TEXT,
                created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Роли
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Roles (
                role_id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_name TEXT NOT NULL UNIQUE
            );
        """)

        # Права (Permissions)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Permissions (
                permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_id INTEGER,
                permission_name TEXT NOT NULL,
                FOREIGN KEY (role_id) REFERENCES Roles(role_id)
            );
        """)

        # Инициализация базовых ролей (пример)
        cursor.execute("INSERT OR IGNORE INTO Roles (role_id, role_name) VALUES (1, 'Администратор'), (2, 'Преподаватель'), (3, 'Студент')")

        # Права - для примера (можно расширять)
        permissions = [
            (1, "Полный доступ"),            # Администратор
            (2, "Добавление материалов"),    # Преподаватель
            (2, "Просмотр всех студентов"),  # Преподаватель
            (3, "Просмотр материалов")       # Студент
        ]
        cursor.executemany("INSERT OR IGNORE INTO Permissions (role_id, permission_name) VALUES (?, ?)", permissions)

        conn.commit()
        print("Таблицы успешно созданы/обновлены.")
    except sqlite3.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
