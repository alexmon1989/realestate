from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import escape
from django.core.urlresolvers import reverse

from home.models import House
from accounts.models import Constants as UserConstants
from managers.models import Manager

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
    reason_for_selling = models.CharField('Reason for selling', blank=True, null=True, max_length=255)
    first_offer_date = models.DateField('First offer date', blank=True, null=True)
    offer_price = models.IntegerField('Offer price *',
                                      blank=True,
                                      null=True,
                                      validators=[MinValueValidator(0)])
    walk_away_price = models.IntegerField('Walk away price',
                                          blank=True,
                                          null=True,
                                          validators=[MinValueValidator(0)])
    date_sold = models.DateField('Date sold', blank=True, null=True)
    sold_for = models.IntegerField('Sold for',
                                   blank=True,
                                   null=True,
                                   validators=[MinValueValidator(0)])
    market_reg_value = models.IntegerField('Market/reg value *',
                                           blank=True,
                                           null=True,
                                           validators=[MinValueValidator(0)])
    owner_occupied = models.BooleanField('Owner occupied', default=False)
    rent_per_week = models.IntegerField('Rent per week *',
                                        blank=True,
                                        null=True,
                                        validators=[MinValueValidator(0)])
    insurance = models.FloatField('Insurance *',
                                  blank=True,
                                  null=True,
                                  validators=[MinValueValidator(0)])
    repairs_maintenance = models.FloatField('Annual Repairs/Maintenance *',
                                            blank=True,
                                            null=True,
                                            validators=[MinValueValidator(0)])
    body_corporate = models.FloatField('Body Corporate Fees',
                                       blank=True,
                                       null=True,
                                       validators=[MinValueValidator(0)])
    government_value = models.FloatField('Government Value',
                                         blank=True,
                                         null=True,
                                         validators=[MinValueValidator(0)])
    rates = models.FloatField('Council Rates *',
                              blank=True,
                              null=True,
                              validators=[MinValueValidator(0)])
    notes = models.TextField('Notes', blank=True, null=True)
    RENT_TYPE_CHOICES = (
        (1, 'Current Rent'),
        (2, 'Agent provided rent appraisal'),
        (3, 'Property Manager appraised'),
    )
    rent_type = models.IntegerField('Appraisal type', choices=RENT_TYPE_CHOICES, null=True, blank=True, default=None)
    TITLE_TYPE_CHOICES = (
        (1, 'Freehold'),
        (2, 'Crosslease'),
        (3, 'Leasehold'),
        (4, 'Unit title'),
    )
    title_type = models.IntegerField('Title type', null=True, blank=True, choices=TITLE_TYPE_CHOICES)
    new_build = models.BooleanField('New Build', default=False)
    FENCED_CHOICES = (
        (1, 'Fully'),
        (2, 'Partially'),
        (3, 'Not fenced'),
    )
    fenced = models.IntegerField('Fenced', blank=True, null=True, choices=FENCED_CHOICES)
    flooding_10 = models.BooleanField('10 year flooding', default=False)
    flooding_100 = models.BooleanField('100 year flooding', default=False)
    renovations = models.FloatField('Renovations', blank=True, null=True)
    revisit_on = models.DateField('Revisit on', blank=True, null=True)
    appraised_on = models.DateField('Appraised on', blank=True, null=True)
    managers = models.ManyToManyField(Manager, verbose_name='Managers')

    def __str__(self):
        return '{} for {}'.format(self.user, self.house)


class OtherExpense(models.Model):
    """Model for other expenses for house user data."""
    house_user_data = models.ForeignKey(HouseUserData, on_delete=models.CASCADE)
    key = models.CharField('Key', max_length=255)
    value = models.FloatField('Value')

    def __str__(self):
        return '{}: {}'.format(self.key, self.value)


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


class UserHouse(models.Model):
    """User's houses model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        """String view of house object"""
        house = House.objects.values(
            'street_number',
            'street_name',
            'suburb__name',
            'suburb__city__city_name',
            'suburb__city__region__name'
        ).get(house_id=self.house.pk)

        return '{} {}, {}, {}, {}'.format(
            house['street_number'],
            house['street_name'],
            house['suburb__name'],
            house['suburb__city__city_name'],
            house['suburb__city__region__name']
        )

    def user_link(self):
        return '<a href="%s">%s</a>' % (reverse("admin:auth_user_change", args=(self.user.id,)), escape(self.user))

    def house_link(self):
        return '<a href="%s">%s</a>' % (reverse("admin:home_house_change", args=(self.house.pk,)), escape(self.house))

    user_link.allow_tags = True
    user_link.short_description = "User"
    house_link.allow_tags = True
    house_link.short_description = "House"
