from django import forms
from .models import ModelFile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

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
            if field.label == 'ユーザー名':
                field.widget.attrs['id'] = 'username'
            elif field.label == 'パスワード':
                field.widget.attrs['id'] = 'password'


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            if field.label == 'ユーザー名':
                field.widget.attrs['id'] = 'username'
            elif field.label == 'パスワード':
                field.widget.attrs['id'] = 'password1'
            elif field.label == 'パスワード(確認用)':
                field.widget.attrs['id'] = 'password2'

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')