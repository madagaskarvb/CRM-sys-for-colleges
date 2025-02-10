from django.shortcuts import render
from django.contrib.auth.views import LoginView
# Create your views here.
from .models import Student


def adminPage(request):
    return render(request, 'basikPages/adminPage.html', {'css_file': 'basikPages/adminPage.css'})

def studentPage(request):
    return render(request, 'basikPages/studentPage.html', {'css_file': 'basikPages/studentPage.css'})

def mainPage(request):
    return render(request, 'basikPages/main.html', {'css_file': 'basikPages/mainPage.css'})

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

def listOfStudentsPage(request):
    return render(request, 'basikPages/listOfStudents.html', {'css_file': 'basikPages/listOfStudents.css'})

def listOfTeachersPage(request):
    return render(request, 'basikPages/listOfTeachers.html', {'css_file': 'basikPages/listOfTeachers.css'})

def EducationMaterialsPage(request):
    return render(request, 'basikPages/EducationMaterials.html', {'css_file': 'basikPages/EducationMaterials.css'})

def PageForChangeNamePage(request):
    return render(request, 'basikPages/PageForChangeName.html', {'css_file': 'basikPages/PageForChangeName.css'})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['css_file'] = 'registration/login.css'
        return context