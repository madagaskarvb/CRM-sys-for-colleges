from django.shortcuts import render

# Create your views here.
from .models import Student

# def index(request):
#     """
#     Функция отображения для домашней страницы сайта.
#     """
#     # Генерация "количеств" некоторых главных объектов
#     num_users = Student.objects.all().count()

#     # Отрисовка HTML-шаблона index.html с данными внутри
#     # переменной контекста context
#     return render(
#         request,
#         'index.html',
#         context={'num_users':num_users},
#     )

def student_page(request):
    return render(request, 'basikPages/studentPage.html')

def teacher_page(request):
    return render(request, 'basikPages/teacherPage.html')

def admin_page(request):
    return render(request, 'basikPages/adminPage.html')

def main(request):
    return render(request, 'basikPages/main.html')