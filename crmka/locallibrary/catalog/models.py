from django.db import models
from django.utils import timezone


class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name or "Неизвестный факультет"


class Teachers(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    full_name = models.TextField(blank=True, null=True)
    date_of_birth = models.DateTimeField(default=timezone.now, blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    hire_date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.full_name or "Неизвестный преподаватель"


class Subjects(models.Model):
    subject_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(
        Teachers,
        on_delete=models.CASCADE,
        db_column='teacher_id',
        blank=True,
        null=True
    )
    subject_name = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.subject_name or "Неизвестный предмет"


class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.TextField(unique=True, blank=True, null=True)
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


class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    full_name = models.TextField(blank=True, null=True)
    date_of_birth = models.DateTimeField(default=timezone.now, blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    contact_phone = models.IntegerField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    group = models.ForeignKey(
        Groups,
        on_delete=models.CASCADE,
        db_column='group_id',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name or "Неизвестный студент"


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
    topic_name = models.TextField(blank=True, null=True)
    material_type = models.TextField(blank=True, null=True)
    material_source = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.topic_name or 'Без названия'} ({self.material_id})"


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
        return f"Grade {self.grade if self.grade is not None else 'N/A'} for {self.student}"


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

    def __str__(self):
        return f"{self.group or 'Неизвестная группа'} - {self.subject or 'Неизвестный предмет'}"
