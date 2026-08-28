from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['name', 'email', 'phone_no', 'designation', 'batch', 'branch', 'profile_picture']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. name@example.com'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +1 234 567 8900'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CEO at Google or UG Student'}),
            'batch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2024'}),
            'branch': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Computer Science'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }
