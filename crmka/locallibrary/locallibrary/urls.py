"""
URL configuration for locallibrary project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from catalog import views
from django.shortcuts import render
# Используйте include() чтобы добавлять URL из каталога приложения
from django.urls import include
from django.urls import path
# Добавьте URL соотношения, чтобы перенаправить запросы с корневого URL, на URL приложения
from django.views.generic import RedirectView
# Используйте static() чтобы добавить соотношения для статических файлов
# Только на период разработки
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', views.studentPage, name='student_page'),
    path('teacher/', views.teacherPage, name='teacher_page'),
    path('admin_page/', views.adminPage, name='admin_page'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', views.mainPage, name='main_page'),
    path('logged_out/', views.loggedOutPage, name='logged_out'),
    path('password_reset_complete/', views.passwordResetCompletePage, name='password_reset_complete'),
    path('password_reset_confirm/', views.passwordResetConfirmPage, name='password_reset_confirm'),
    path('password_reset_done/', views.passwordResetDonePage, name='password_reset_done'),
    path('password_reset_email/', views.passwordResetEmailPage, name='password_reset_email'),
    path('password_reset_form/', views.passwordResetFormPage, name='password_reset_form'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('list_of_students/', views.listOfStudentsPage, name='list_of_students'),
    path('list_of_teachers/', views.listOfTeachersPage, name='list_of_teachers'),
    path('education_materials/', views.EducationMaterialsPage, name='education_materials'),
    path('page_for_change_name/', views.PageForChangeNamePage, name='page_for_change_name'),
    path('add_material/', views.add_material_view, name='add_material'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


