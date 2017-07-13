from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

from home.models import City


class Manager(models.Model):
    """Managers's model."""
    name = models.CharField('Name', max_length=255)
    agency = models.CharField('Agency', max_length=255)
    phone_numbers = models.CharField('Phone numbers', max_length=255)
    email = models.EmailField('E-mail', max_length=255)
    rate = models.FloatField(
        'Rate',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0)
        ]
    )
    city = models.ForeignKey(City, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'
