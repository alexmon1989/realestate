from django.forms import ModelForm
from managers.models import Manager


class ManagerForm(ModelForm):
    """Form for creating Manager objects"""
    class Meta:
        model = Manager
        exclude = ('created_at', 'updated_at', 'user')
