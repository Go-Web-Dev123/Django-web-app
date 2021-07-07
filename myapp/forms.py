from django import forms
from .models import Employee




class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Employee
        fields = ( 'image',)