from django.shortcuts import render
from django.contrib.auth.views import LoginView

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

def adminPage(request):
    return render(request, 'basikPages/adminPage.html', {'css_file': 'basikPages/adminPage.css'})

def studentPage(request):
    return render(request, 'basikPages/studentPage.html', {'css_file': 'basikPages/studentPage.css'})

def mainPage(request):
    return render(request, 'base_generic.html', {'css_file': 'basikPages/mainPage.css'})

def teacherPage(request):
    return render(request, 'basikPages/teacherPage.html', {'css_file': 'basikPages/teacherPage.css'})

def loginPage(request):
    return render(request, 'registration/login.html', {'css_file': 'registration/login.css'})

def loggedOutPage(request):
    return render(request, 'registration/logged_out.html', {'css_file': 'registration/logged_out.css'})

def passwordResetCompletePage(request):
    return render(request, 'registration/password_reset_complete.html', {'css_file': 'registration/password_reset_complete.css'})

def passwordResetConfirmPage(request):
    return render(request, 'registration/password_reset_confirm.html', {'css_file': 'registration/password_reset_confirm.css'})

def passwordResetDonePage(request):
    return render(request, 'registration/password_reset_done.html', {'css_file': 'registration/password_reset_done.css'})

def passwordResetEmailPage(request):
    return render(request, 'registration/password_reset_email.html', {'css_file': 'registration/password_reset_email.css'})

def passwordResetFormPage(request):
    return render(request, 'registration/password_reset_form.html', {'css_file': 'registration/password_reset_form.css'})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['css_file'] = 'registration/login.css'
        return context