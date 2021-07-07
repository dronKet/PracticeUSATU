from django import forms
from django.forms import ClearableFileInput
from .models import UploadModel


class UploadFile(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True})
        }
