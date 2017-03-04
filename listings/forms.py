from django.forms import ModelForm
from .models import HouseUserData


class HouseUserDataForm(ModelForm):
    class Meta:
        model = HouseUserData
        exclude = ('user', 'house')
