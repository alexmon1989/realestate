from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from annoying.fields import AutoOneToOneField

from home.models import City, House
from settings.models import Global as GlobalSettings


class HousesFilter(models.Model):
    """House filter model."""
    name = models.CharField('Filter Name', max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filter_data_json = models.TextField('Filter Data', blank=True, null=True)
    disabled = models.BooleanField('Disabled', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    """Profile model for extending User model fields."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    show_photos_filters = models.BooleanField('Show title photo', default=False)
    font_ratio = models.FloatField('Font size', default=1)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.get_or_create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = Profile.objects.get(user=self.user)
                self.pk = p.pk
            except Profile.DoesNotExist:
                pass

        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Constants(models.Model):
    """Constants user model (extends User model fields)."""
    user = AutoOneToOneField(User, on_delete=models.CASCADE)
    loan_interest_rate = models.FloatField(
        'Loan interest rate, %',
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5)
        ],
        default=5
    )
    loan_deposit = models.FloatField(
        'Loan deposit, %',
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5)
        ],
        default=GlobalSettings.objects.values('loan_deposit').first()['loan_deposit']
    )
    new_built_loan_deposit = models.FloatField(
        'New-build loan deposit, %',
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5)
        ],
        default=GlobalSettings.objects.values('new_built_loan_deposit').first()['new_built_loan_deposit']
    )
    property_management_commission = models.FloatField(
        'Property Management commission, %',
        validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ],
        default=GlobalSettings.objects.values('property_management_commission').first()['property_management_commission']
    )
    vacancy_rate = models.IntegerField(
        'Vacancy rate, weeks',
        validators=[
            MinValueValidator(0)
        ],
        default=GlobalSettings.objects.values('vacancy_rate').first()['vacancy_rate']
    )
    gross_yield = models.FloatField(
        'Gross yield, %',
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1),
        ],
        default=GlobalSettings.objects.values('gross_yield').first()['gross_yield']
    )
    net_yield = models.FloatField(
        'Net yield, %',
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1),
        ],
        default=GlobalSettings.objects.values('net_yield').first()['net_yield']
    )
    min_cashflow = models.IntegerField(
        'Min cashflow',
        validators=[
            MinValueValidator(0)
        ],
        default=GlobalSettings.objects.values('min_cashflow').first()['min_cashflow']
    )
    inflation = models.FloatField(
        'Inflation, %',
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1),
        ],
        default=GlobalSettings.objects.values('inflation').first()['inflation']
    )

    def __str__(self):
        return "User's constants"


class CitiesConstants(models.Model):
    """Cities constants model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    capital_growth = models.FloatField(blank=True, null=True)
