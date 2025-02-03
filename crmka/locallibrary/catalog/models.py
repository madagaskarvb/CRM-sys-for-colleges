from django.db import models

# Модель для факультетов
class Faculty(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название факультета")
    description = models.TextField(verbose_name="Описание факультета", blank=True, null=True)
    
    class Meta:
        db_table = "faculties"
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"
    
    def __str__(self):
        return self.name

# Модель для студентов
class Student(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя студента")
    login = models.CharField(max_length=150, unique=True, verbose_name="Логин")
    email = models.EmailField(verbose_name="Email")
    status = models.CharField(max_length=150, default="Активный", verbose_name="Статус")
    password = models.CharField(max_length=150, verbose_name="Пароль")
    # Связь со факультетом (может быть не указана)
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Факультет"
    )
    
    class Meta:
        db_table = "students"
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
    
    def __str__(self):
        return self.name

# Модель для преподавателей
class Teacher(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя преподавателя")
    login = models.CharField(max_length=150, unique=True, verbose_name="Логин")
    email = models.EmailField(verbose_name="Email")
    status = models.CharField(max_length=150, default="Активный", verbose_name="Статус")
    password = models.CharField(max_length=150, verbose_name="Пароль")
    # Дополнительные поля для преподавателя:
    subject = models.CharField(max_length=150, verbose_name="Предмет", blank=True, null=True)
    bio = models.TextField(verbose_name="Биография", blank=True, null=True)
    # Связь со факультетом (может быть не указана)
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Факультет"
    )
    
    class Meta:
        db_table = "teachers"
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
    
    def __str__(self):
        return self.name

# Модель для учебных материалов
class EducationalMaterial(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    file = models.FileField(upload_to='materials/', verbose_name="Файл", blank=True, null=True)
    # Преподаватель, загрузивший материал
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = "educational_materials"
        verbose_name = "Учебный материал"
        verbose_name_plural = "Учебные материалы"
    
    def __str__(self):
        return self.title

# Модель для оценок студентов
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name="Преподаватель")
    # Опциональная привязка к учебному материалу (например, если оценка за выполнение задания)
    material = models.ForeignKey(
        EducationalMaterial,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Учебный материал"
    )
    grade = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Оценка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выставления оценки")
    
    class Meta:
        db_table = "grades"
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
    
    def __str__(self):
        return f"{self.student.name} - {self.grade}"
