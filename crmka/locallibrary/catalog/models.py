from django.db import models

class User(models.Model):
    ACCESS_LEVELS = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    ]

    name = models.CharField(max_length=150, verbose_name="Имя пользователя")
    login = models.CharField(max_length=150, unique=True, verbose_name="Логин")
    email = models.EmailField(verbose_name="Email")
    status = models.CharField(max_length=150, default="Активный", verbose_name="Статус")
    level = models.CharField(
        max_length=150,
        choices=ACCESS_LEVELS,  # Указываем варианты выбора
        default='user',         # Значение по умолчанию
        verbose_name="Уровень доступа"
    )
    password = models.CharField(max_length=150, verbose_name="Пароль")

    class Meta:
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name