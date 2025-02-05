import sqlite3

def create_connection(db_file: str):
    """Создаёт или открывает подключение к SQLite БД."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # Включим режим возврата строк в виде словарей (для удобства)
        conn.row_factory = sqlite3.Row
        print("Соединение с базой установлено.")
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    return conn

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

# ----- Операции со студентами (clients) -----

def add_client(conn, first_name, last_name, email, phone=None):
    """Добавляет нового клиента (студента)."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clients (first_name, last_name, email, phone)
            VALUES (?, ?, ?, ?)
        """, (first_name, last_name, email, phone))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении клиента: {e}")
        return None

def get_all_clients(conn):
    """Возвращает список всех студентов (clients)."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT client_id, first_name, last_name, email, phone, created_at
            FROM clients
            ORDER BY client_id
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ошибка при получении списка клиентов: {e}")
        return []

# ... (прочие функции: get_client, update_client, delete_client и т.д.)

# ----- Операции с материалами -----

def add_material(conn, title, description=None, author=None):
    """Добавляет новый учебный материал."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO materials (title, description, author)
            VALUES (?, ?, ?)
        """, (title, description, author))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении материала: {e}")
        return None

def get_all_materials(conn):
    """Возвращает список всех материалов."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT material_id, title, description, author, created_at
            FROM materials
            ORDER BY material_id
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Ошибка при получении списка материалов: {e}")
        return []


