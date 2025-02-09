from django.db import models

class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    faculty_name = models.TextField()

    def str(self):
        return self.faculty_name


class Teachers(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    full_name = models.TextField()
    date_of_birth = models.DateTimeField()
    email = models.TextField()
    phone = models.IntegerField()
    password = models.TextField()
    hire_date = models.DateTimeField()

    def str(self):
        return self.full_name


class Subjects(models.Model):
    subject_id = models.AutoField(primary_key=True)
    teacher = models.ForeignKey(
        Teachers,
        on_delete=models.CASCADE,
        db_column='teacher_id'
    )
    name = models.TextField()

    def str(self):
        return self.name


class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.TextField(unique=True)
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        db_column='faculty'
    )
    study_year = models.IntegerField()

    def str(self):
        return self.group_name


class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    full_name = models.TextField()
    date_of_birth = models.DateTimeField()
    email = models.TextField()
    contact_phone = models.IntegerField()
    password = models.TextField()
    group = models.ForeignKey(
        Groups,
        on_delete=models.CASCADE,
        db_column='group_id'
    )

    def str(self):
        return self.full_name


class EducationalMaterials(models.Model):
    material_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        db_column='subject_id'
    )
    unit = models.IntegerField()
    topic_name = models.TextField()
    material_type = models.TextField()
    material_source = models.TextField()

    def str(self):
        return f"{self.topic_name} ({self.material_id})"


class Grades(models.Model):
    grade_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Students,
        on_delete=models.CASCADE,
        db_column='student_id'
    )
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        db_column='subject_id'
    )
    grade = models.IntegerField()

    def str(self):
        return f"Grade {self.grade} for {self.student}"


class GroupSubject(models.Model):
    """
    Промежуточная таблица (Many-to-many) для связи
    между группами (Groups) и предметами (Subjects).
    """
    group = models.ForeignKey(
        Groups,
        on_delete=models.CASCADE,
        db_column='group_id'
    )
    subject = models.ForeignKey(
        Subjects,
        on_delete=models.CASCADE,
        db_column='subject_id'
    )

    class Meta:
        # Если нужно уникальное сочетание (group_id, subject_id), то можно задать:
        unique_together = ('group', 'subject')

    def str(self):
        return f"{self.group} - {self.subject}"
