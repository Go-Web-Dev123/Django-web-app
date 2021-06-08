from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('fullname','mobile','Password')
        labels = {
            'fullname':'UserName',
            'Password':'Password',
        }
        widgets = {
            'fullname': forms.TextInput(attrs={'placeholder': 'UserName'}),
            'Password':forms.TextInput(attrs={'placeholder':'Password','type':'password'}),
            'mobile':forms.TextInput(attrs={'placeholder':'Mobile Number','type':'number','pattern':'"[1-9]{1}[0-9]{9}"'})
         }


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Employee
        fields = ( 'image',)