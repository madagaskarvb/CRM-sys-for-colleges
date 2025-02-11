from django.urls import path
from . import views


urlpatterns = [
    path('student/', views.studentPage, name='student_page'),
    path('teacher/', views.teacherPage, name='teacher_page'),
]

