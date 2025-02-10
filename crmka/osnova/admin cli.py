import django
import os
from django.core.management import execute_from_command_line, call_command
from django.db import models, connection
from crmka.locallibrary.catalog.models import Faculty, Students, Teachers, EducationalMaterials, Grades, GroupSubject, Groups, Subjects

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

def changes_in_table(model_class):
    set_field = input("Field to update: ")
    new_value = input("New value: ")
    filter_field = input("Filter field: ")
    filter_value = input("Filter value: ")
    
    update_count = model_class.objects.filter(**{filter_field: filter_value}).update(**{set_field: new_value})
    if update_count:
        print("Data updated successfully!")
    else:
        print("No matching records found.")


def delete_records_table(model_class):
    filter_field = input("Filter field: ")
    filter_value = input("Filter value: ")
    deleted_count, _ = model_class.objects.filter(**{filter_field: filter_value}).delete()
    print(f"Deleted {deleted_count} records.")


def write_in_table(model_class):
    fields = {field.name: input(f"Enter {field.name}: ") for field in model_class._meta.fields if field.name != 'id'}
    instance = model_class.objects.create(**fields)
    print(f"Record added: {instance}")


def show_table(model_class):
    print(" | ".join([field.name for field in model_class._meta.fields]))
    for obj in model_class.objects.all():
        print(" | ".join(str(getattr(obj, field.name)) for field in model_class._meta.fields))

def menu():
    model_mapping = {"faculty" : Faculty, "student" : Students, 
                    "teacher" : Teachers, "educationalmaterial" : EducationalMaterials, "grade" : Grades,
                    "groupsubject" : GroupSubject, "subjects" : Subjects,  "groups" : Groups
}  # Add your models here
    
    while True:
        action = input("ACTION: ").strip().upper()
        if action == "CHANGES IN":
            model_name = input("Model name: ").lower()
            if model_name in model_mapping:
                changes_in_table(model_mapping[model_name])
        elif action == "DELETE IN":
            model_name = input("Model name: ").lower()
            if model_name in model_mapping:
                delete_records_table(model_mapping[model_name])
        elif action == "WRITE IN":
            model_name = input("Model name: ").lower()
            if model_name in model_mapping:
                write_in_table(model_mapping[model_name])
        elif action == "SHOW TABLE":
            model_name = input("Model name: ").lower()
            if model_name in model_mapping:
                show_table(model_mapping[model_name])
        elif action == "QUIT":
            break
        else:
            print("No such command\n")


if __name__ == "__main__":
    menu()
