from django import forms
from .models import ModelFile
from django.contrib.auth.forms import AuthenticationForm

class ImageForm(forms.ModelForm):
    class Meta:
        model = ModelFile
        fields = ('image',)
        exclude =['id','result','registered_date']

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label