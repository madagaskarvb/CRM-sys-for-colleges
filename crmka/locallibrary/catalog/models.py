from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name or "Неизвестный факультет"

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'


class Teachers(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, null=True, blank=False)
    date_of_birth = models.DateField(default=timezone.now, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(
        max_length=18,
        blank=True,
        null=True
    )
    password = models.CharField(max_length=255, null=True, blank=False)
    hire_date = models.DateField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.full_name or "Неизвестный преподаватель"

    def clean(self):
        super().clean()
        try:
            validate_password(self.password, user=self)
        except ValidationError as e:
            raise ValidationError({'password': e.messages})

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Subjects(models.Model):
    subject_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(
        Teachers,
        on_delete=models.CASCADE,
        db_column='teacher_id',
        blank=True,
        null=True
    )
    subject_name = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return self.subject_name or "Неизвестный предмет"

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=255, null=True, blank=False)
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        db_column='faculty',
        blank=True,
        null=True
    )
    study_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.group_name or "Неизвестная группа"

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, null=True, blank=False)
    date_of_birth = models.DateField(default=timezone.now, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(
        max_length=18,
        blank=True,
        null=True
    )
    password = models.CharField(max_length=255, null=True, blank=False)
    group = models.ForeignKey(
        Groups,
        on_delete=models.CASCADE,
        db_column='group_id',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name or "Неизвестный студент"

    def clean(self):
        super().clean()
        try:
            validate_password(self.password, user=self)
        except ValidationError as e:
            raise ValidationError({'password': e.messages})

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class EducationalMaterials(models.Model):
    material_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        db_column='subject_id',
        blank=True,
        null=True
    )
    unit = models.IntegerField(blank=True, null=True)
    topic_name = models.CharField(max_length=255, null=True, blank=False)
    material_type = models.CharField(max_length=255, null=True, blank=False)
    material_source = models.CharField(max_length=255, null=True, blank=False)

    def __str__(self):
        return f"{self.topic_name or 'Без названия'} ({self.material_id})"

    class Meta:
        verbose_name = 'Учебный материал'
        verbose_name_plural = 'Учебные материалы'


class Grades(models.Model):
    grade_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
        db_column='student_id',
        blank=True,
        null=True
    )
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        db_column='subject_id',
        blank=True,
        null=True
    )
    grade = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Оценка {self.grade if self.grade is not None else 'N/A'} для {self.student}"

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'


class GroupSubject(models.Model):
    """
    Промежуточная таблица (Many-to-many) для связи
    между группами (Groups) и предметами (Subjects).
    """
    group = models.ForeignKey(
        Groups,
        on_delete=models.CASCADE,
        db_column='group_id',
        blank=True,
        null=True
    )
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        db_column='subject_id',
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('group', 'subject')
        verbose_name = 'Группа и предмет'
        verbose_name_plural = 'Группы и предметы'

    def __str__(self):
        return f"{self.group or 'Неизвестная группа'} - {self.subject or 'Неизвестный предмет'}"


@receiver(post_save, sender=Students)
def create_student_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(
            username=instance.email,
            email=instance.email,
            password=instance.password,
            first_name=instance.full_name.split()[0],
            last_name=' '.join(instance.full_name.split()[1:])
        )
        student_group = Group.objects.get(name='Студенты')
        user.groups.add(student_group)

@receiver(post_save, sender=Teachers)
def create_teacher_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(
            username=instance.email,
            email=instance.email,
            password=instance.password,
            first_name=instance.full_name.split()[0],
            last_name=' '.join(instance.full_name.split()[1:])
        )
        teacher_group = Group.objects.get(name='Преподаватели')
        user.groups.add(teacher_group)
