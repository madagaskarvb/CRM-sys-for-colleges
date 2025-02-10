from django.contrib import admin
from .models import Students, Teachers, Grades, Faculty, EducationalMaterials, GroupSubject, Subjects, Groups
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
admin.site.register(Students, UserAdmin)
admin.site.register(Teachers)
admin.site.register(Grades)
admin.site.register(Faculty)
admin.site.register(EducationalMaterials)
admin.site.register(GroupSubject)
admin.site.register(Subjects)
admin.site.register(Groups)
