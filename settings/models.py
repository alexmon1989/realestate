from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Global(models.Model):
    bond_link = models.CharField('Bond link', max_length=255, null=True, blank=True)
    gst = models.FloatField(
        'GST, %',
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5)
        ]
    )
    qv_growth = models.CharField('QV Growth link', max_length=255, null=True, blank=True)
    qv_rental = models.CharField('QV Rental link', max_length=255, null=True, blank=True)
    qv_sales = models.CharField('QV Sales link', max_length=255, null=True, blank=True)
    loan_deposit = models.FloatField(
        'Loan deposit, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5)
        ]
    )
    new_built_loan_deposit = models.FloatField(
        'New-build loan deposit, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5)
        ]
    )
    property_management_commission = models.FloatField(
        'Property Management commission, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ]
    )
    vacancy_rate = models.IntegerField(
        'Vacancy rate, weeks',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0)
        ]
    )
    gross_yield = models.FloatField(
        'Gross yield, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1),
        ]
    )
    net_yield = models.FloatField(
        'Net yield, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1),
        ]
    )
    min_cashflow = models.IntegerField(
        'Min cashflow',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0)
        ]
    )
    inflation = models.FloatField(
        'Inflation, %',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1),
        ]
    )

    def __str__(self):
        return "Global constants"

    class Meta:
        verbose_name = 'Global constants'
        verbose_name_plural = 'Global constants'


class MotdBanner(models.Model):
    enabled = models.BooleanField('Enabled', default=False)
    message = models.CharField('Message', default='It will be tachnical work on the site soon.', max_length=255)

    class Meta:
        verbose_name = 'MOTD banner'
        verbose_name_plural = 'MOTD banner'
