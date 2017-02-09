from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User


class UserForm(ModelForm):
    """Форма создания/редактирования документа."""
    email = forms.CharField(max_length=75, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
