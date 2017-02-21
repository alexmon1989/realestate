from django.db import models
from django.contrib.auth.models import User


class HousesFilter(models.Model):
    """House filter model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filter_data_json = models.TextField('Filter Data', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
