from django.urls import path
from . import views


urlpatterns = [
    path('student/', views.student_page, name='student_page'),
    path('teacher/', views.teacher_page, name='teacher_page'),
    path('admin/', views.admin_page, name='admin_page'),
]