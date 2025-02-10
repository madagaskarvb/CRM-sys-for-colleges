from django.contrib import admin
from .models import Students, Teachers, Grades, Faculty, EducationalMaterials, GroupSubject, Subjects, Groups
from .forms import UserAdminForm

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm

    # Отображение в списке
    list_display = ['full_name', 'group', 'email']
    search_fields = ['full_name', 'group', 'email']

    # Поля для редактирования и добавления
    fieldsets = (
        (None, {
            'fields': ('full_name', 'date_of_birth', 'email', 'contact_phone', 'password', 'group')
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
