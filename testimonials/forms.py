from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['designation', 'batch', 'branch', 'profile_picture']
        widgets = {
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CEO at Google or UG Student'}),
            'batch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2024'}),
            'branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
