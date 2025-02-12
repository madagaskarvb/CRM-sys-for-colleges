from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.models import Group
from collections import defaultdict
# Create your views here.
from .models import Students, Teachers, EducationalMaterials


def adminPage(request):
    return render(request, 'basikPages/adminPage.html', {'css_file': 'basikPages/adminPage.css'})

def studentPage(request):
    # user = request.user
    # if user.groups.filter(name='Студенты').exists():
        return render(request, 'basikPages/studentPage.html', {'css_file': 'basikPages/studentPage.css'})

def mainPage(request):
    return render(request, 'basikPages/main.html', {'css_file': 'basikPages/mainPage.css'})

def teacherPage(request):
    # user = request.user
    # if user.groups.filter(name='Преподаватели').exists():
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

def listOfStudentsPage(request):
    return render(request, 'basikPages/listOfStudents.html', {'css_file': 'basikPages/listOfStudents.css'})

def listOfTeachersPage(request):
    return render(request, 'basikPages/listOfTeachers.html', {'css_file': 'basikPages/listOfTeachers.css'})

def EducationMaterialsPage(request):
    materials = EducationalMaterials.objects.all()
    grouped_materials = defaultdict(list)

    for material in materials:
        grouped_materials[material.subject.subject_name].append(material)

    print(grouped_materials)  # Добавьте это для отладки

    return render(request, 'basikPages/EducationMaterials.html', {
        'grouped_materials': grouped_materials,
        'css_file': 'basikPages/EducationMaterials.css'
    })

def PageForChangeNamePage(request):
    return render(request, 'basikPages/PageForChangeName.html', {'css_file': 'basikPages/PageForChangeName.css'})

def AddMaterialPage(request):
    return render(request, 'basikPages/AddMaterial.html', {'css_file': 'basikPages/AddMaterial.css'})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['css_file'] = 'registration/login.css'
        return context

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Студенты').exists():  # Проверяем, есть ли у пользователя группа "Студенты"
            return '/student/'  # URL для студента
        elif user.groups.filter(name='Преподаватели').exists():  # Проверяем, есть ли у пользователя группа "Преподаватели"
            return '/teacher/'  # URL для преподавателя
        else:
            return '/'