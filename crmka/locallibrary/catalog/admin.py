from django.contrib import admin
from .models import Student, Teacher, Grade, Faculty, EducationalMaterial
from .forms import UserAdminForm

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm

    # Отображение в списке
    list_display = ['name', 'login', 'email']
    search_fields = ['name', 'login', 'email']

    # Поля для редактирования и добавления
    fieldsets = (
        (None, {
            'fields': ('name', 'login', 'email', 'password')
        }),
    )

# Регистрируем каждую модель отдельно
admin.site.register(Student, UserAdmin)
admin.site.register(Teacher)
admin.site.register(Grade)
admin.site.register(Faculty)
admin.site.register(EducationalMaterial)