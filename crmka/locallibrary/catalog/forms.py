from django import forms
from .models import Students

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['full_name', 'date_of_birth', 'email', 'contact_phone', 'password', 'group']  # Поля для ввода


    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['full_name', 'date_of_birth', 'email', 'contact_phone', 'password', 'group']
        for field in required_fields:
            if not cleaned_data.get(field):

                raise forms.ValidationError(f"Поле '{field}' обязательно для заполнения.")
        return cleaned_data
