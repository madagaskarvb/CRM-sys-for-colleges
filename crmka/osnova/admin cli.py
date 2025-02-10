import django
import os
from django.core.management import execute_from_command_line, call_command
from django.db import models, connection
from crmka.locallibrary.catalog.models import Faculty, Students, Teachers, EducationalMaterials, Grades, GroupSubject, Groups, Subjects

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

def create_dynamic_table(app_name):
    """
    Dynamically create a model and generate migrations for the specified table.
    
    Parameters:
        app_name (str): The name of the Django app where the model will be defined.
        table_name (str): The name of the table to be created.
        fields (list of tuples): A list of tuples containing field name and field type.
                                Example: [('name', 'CharField', {'max_length': 100}), ('age', 'IntegerField', {})]
    """

    table_name = input("Table name: ")
    fields = input("Fields: ")

    # Define the model as a new class
    class Meta:
        app_label = app_name

    # Dynamically create the model class
    model_class = type(table_name, (models.Model,), {'__module__': app_name, 'Meta': Meta})

    for field in fields:
        field_name, field_type, field_options = field
        field_class = getattr(models, field_type)  # Get the corresponding Django field class
        model_class.add_to_class(field_name, field_class(**field_options))

    # Write the model to the app's models.py file
    app_model_file = os.path.join(app_name, 'models.py')

    # Read the current content of models.py
    with open(app_model_file, 'r') as file:
        model_code = file.read()

    # Add the new model code at the end of models.py
    with open(app_model_file, 'a') as file:
        model_code += f"\n\nclass {table_name}(models.Model):\n"
        for field in fields:
            field_name, field_type, field_options = field
            field_class = getattr(models, field_type)
            file.write(f"    {field_name} = models.{field_type}({', '.join([f'{k}={v}' for k, v in field_options.items()])})\n")

    # Generate migrations
    call_command('makemigrations', app_name)
    call_command('migrate')

    print(f"Table '{table_name}' created successfully with the following fields: {fields}")


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
