from django import forms
from .models import Student

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'login', 'email', 'status', 'password']  # Поля для ввода


    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['name', 'login', 'email', 'password', 'status']
        for field in required_fields:
            if not cleaned_data.get(field):

                raise forms.ValidationError(f"Поле '{field}' обязательно для заполнения.")
        return cleaned_data
