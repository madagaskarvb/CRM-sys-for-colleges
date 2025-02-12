from django import forms
from .models import Students, Teachers, EducationalMaterials

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
        model = Students
        fields = ['full_name', 'email', 'contact_phone']
        labels = {
            'full_name': 'Введите имя',
            'email': 'Введите email',
            'contact_phone': 'Введите номер телефона',
        }

class EducationalMaterialForm(forms.ModelForm):
    class Meta:
        model = EducationalMaterials
        fields = ['subject', 'topic_name', 'material_type', 'material_source']
        labels = {
            'subject': 'Выберите предмет',
            'topic_name': 'Введите название темы',
            'material_type': 'Введите тип материала',
            'material_source': 'Введите ссылку на материал',
        }
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'topic_name': forms.TextInput(attrs={'class': 'form-control'}),
            'material_type': forms.TextInput(attrs={'class': 'form-control'}),
            'material_source': forms.TextInput(attrs={'class': 'form-control'}),
        }
