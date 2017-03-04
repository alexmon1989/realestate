from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from home.models import House


class Mark(models.Model):
    """Marks model."""
    title = models.CharField('Title', null=False, max_length=255)


class MarkedHouse(models.Model):
    """Marked houses by users model."""
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class HouseUserData(models.Model):
    """Liked house user data model."""
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fenced = models.CharField('Fenced', blank=True, null=True, max_length=255)
    title_type = models.CharField('Title type', blank=True, null=True, max_length=255)
    asking_price = models.IntegerField('Asking price',
                                       blank=True,
                                       null=True,
                                       validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    reason_for_selling = models.CharField('Reason for selling', blank=True, null=True, max_length=255)
    first_offer_date = models.DateField('First offer date', blank=True, null=True)
    offer_price = models.IntegerField('Offer price',
                                      blank=True,
                                      null=True,
                                      validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    walk_away_price = models.IntegerField('Walk away price',
                                          blank=True,
                                          null=True,
                                          validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    date_sold = models.DateField('Date sold', blank=True, null=True)
    sale_price = models.IntegerField('Sale price',
                                     blank=True,
                                     null=True,
                                     validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    market_reg_value = models.IntegerField('Market/reg value',
                                           blank=True,
                                           null=True,
                                           validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    owner_rented = models.CharField('Owner/rented', blank=True, null=True, max_length=255)
    rent_per_week = models.FloatField('Rent per week',
                                      blank=True,
                                      null=True,
                                      validators=[MinValueValidator(0)])
    rent_appraisal_done = models.BooleanField('Rent appraisal done', default=False)
    insurance = models.FloatField('Insurance',
                                  blank=True,
                                  null=True,
                                  validators=[MinValueValidator(0)])
    repairs_maintenance = models.FloatField('Repairs & Maintenance',
                                            blank=True,
                                            null=True,
                                            validators=[MinValueValidator(0)])
    body_corporate = models.FloatField('Body Corporate',
                                       blank=True,
                                       null=True,
                                       validators=[MinValueValidator(0)])
    other_expenses = models.FloatField('Other expenses',
                                       blank=True,
                                       null=True,
                                       validators=[MinValueValidator(0)])
    government_value = models.FloatField('Government Value',
                                         blank=True,
                                         null=True,
                                         validators=[MinValueValidator(0)])
    rates = models.FloatField('Rates',
                              blank=True,
                              null=True,
                              validators=[MinValueValidator(0)])
    notes = models.TextField('Notes', blank=True, null=True)

    def __str__(self):
        return '{} for {}'.format(self.user, self.house)
