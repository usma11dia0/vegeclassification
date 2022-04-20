from django import forms
from .models import ModelFile

class ImageForm(forms.ModelForm):
    class Meta:
        model = ModelFile
        fields = ('image',)
        exclude =['id','result','registered_date']