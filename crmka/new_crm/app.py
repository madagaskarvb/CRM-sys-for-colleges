from flask import Flask, render_template, request, redirect, url_for
import os

# Импортируем наши функции из db_utils
from db_utils import (
    create_connection, 
    create_tables,
    get_all_clients, 
    add_client, 
    get_all_materials, 
    add_material
)

app = Flask(__name__)

# Указываем путь к файлу БД
DATABASE = os.path.join(os.path.dirname(__file__), 'crm_database.db')

# При запуске приложения: подключимся к БД и создадим таблицы (если нет)
with create_connection(DATABASE) as conn:
    if conn:
        create_tables(conn)
    else:
        print("Ошибка: Не удалось установить соединение с БД.")

@app.route('/')
def index():
    """
    Главная страница (например, страница входа).
    Шаблон: templates/index.html
    """
    return render_template('index.html')

@app.route('/students')
def students():
    """
    Страница со списком студентов.
    Данные берутся из таблицы clients (через get_all_clients).
    Шаблон: templates/students.html
    """
    with create_connection(DATABASE) as conn:
        all_students = get_all_clients(conn)
    return render_template('students.html', students=all_students)

@app.route('/students/add', methods=['GET', 'POST'])
def add_new_student():
    """
    Страница с формой добавления нового студента.
    При GET-запросе: отобразить форму (templates/add_student.html).
    При POST-запросе: добавить в БД и перекинуть на список студентов.
    """
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        with create_connection(DATABASE) as conn:
            add_client(conn, first_name, last_name, email, phone)

        return redirect(url_for('students'))

    return render_template('add_student.html')

@app.route('/materials')
def materials():
    """
    Страница со списком учебных материалов.
    Данные берём из таблицы materials (через get_all_materials).
    Шаблон: templates/materials.html
    """
    with create_connection(DATABASE) as conn:
        all_mats = get_all_materials(conn)
    return render_template('materials.html', materials=all_mats)

@app.route('/materials/add', methods=['GET', 'POST'])
def add_new_material():
    """
    Страница с формой добавления нового материала.
    При GET: показать форму (templates/add_material.html).
    При POST: сохранить материал и перенаправить на список материалов.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('description')
        author = request.form.get('author')

        with create_connection(DATABASE) as conn:
            add_material(conn, title, desc, author)

        return redirect(url_for('materials'))

    return render_template('add_material.html')

# Пример отдельных страниц для "преподавателя" и "студента"
@app.route('/user/student')
def student_user():
    """
    Личный кабинет ученика (пример).
    Шаблон: templates/student_user.html
    """
    return render_template('student_user.html')

@app.route('/user/teacher')
def teacher_user():
    """
    Личный кабинет преподавателя (пример).
    Шаблон: templates/teacher_user.html
    """
    return render_template('teacher_user.html')


# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)
