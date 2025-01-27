from django.contrib import admin
from .models import User
from .forms import UserAdminForm

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm

    # Отображение в списке
    list_display = ['name', 'login', 'email', 'level']
    search_fields = ['name', 'login', 'email']
    list_filter = ['level']

    # Поля для редактирования и добавления
    fieldsets = (
        (None, {
            'fields': ('name', 'login', 'email', 'level', 'password')
        }),
    )

admin.site.register(User, UserAdmin)