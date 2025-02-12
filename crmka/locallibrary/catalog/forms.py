from django import forms
from .models import Students, Teachers

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = None  # Установим модель в представлении
        fields = ['full_name', 'email', 'contact_phone', 'password']

    def __init__(self, *args, **kwargs):
        user_type = kwargs.pop('user_type', None)
        super().__init__(*args, **kwargs)
        if user_type == 'student':
            self.Meta.model = Students
        elif user_type == 'teacher':
            self.Meta.model = Teachers
