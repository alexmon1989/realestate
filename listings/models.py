from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from home.models import House
from accounts.models import Constants as UserConstants


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
    repairs_maintenance = models.FloatField('Annual Repairs/Maintenance',
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


class Calculator(models.Model):
    """Calculator values model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    managed = models.BooleanField('Managed', default=True)
    property_managers_commission = models.FloatField(
        'Property Manager’s commission, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(1),
        ],
    )
    int_rate = models.FloatField(
        'Int Rate, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5),
        ],
    )
    deposit = models.FloatField(
        'Deposit, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5),
        ],
    )
    vacancy = models.IntegerField(
        'Vacancy, weeks',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
        ],
    )
    capital_growth = models.FloatField(
        'Capital Growth rate, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0),
        ],
    )
    gross_yield = models.FloatField(
        'Gross Yield, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1),
        ],
    )
    net_yield = models.FloatField(
        'Net Yield, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1),
        ],
    )
    min_cashflow = models.FloatField(
        'Min Cashflow, $',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
        ],
    )

    @staticmethod
    def get_or_create(user, house):
        """Returns existed calculator model or creates new and return it."""
        try:
            calculator = Calculator.objects.get(user=user, house=house)
        except Calculator.DoesNotExist:
            calculator = Calculator(user=user, house=house)

            # Initial values
            users_constants, created = UserConstants.objects.get_or_create(user=user)
            calculator.property_managers_commission = users_constants.property_management_commission
            calculator.int_rate = users_constants.loan_interest_rate
            calculator.deposit = users_constants.loan_deposit
            calculator.vacancy = users_constants.vacancy_rate
            calculator.capital_growth = house.suburb.city.capital_growth
            calculator.gross_yield = users_constants.gross_yield
            calculator.net_yield = users_constants.net_yield
            calculator.min_cashflow = users_constants.min_cashflow

            # saving
            calculator.save()
        return calculator
