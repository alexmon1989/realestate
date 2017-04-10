from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Global(models.Model):
    bond_link = models.CharField('Bond link', max_length=255)
    gst = models.FloatField(
        'GST, %',
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5)
        ]
    )
    qv_link = models.FloatField(
        'QV link, %',
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5)
        ]
    )
    loan_deposit = models.FloatField(
        'Loan deposit, %',
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5)
        ]
    )
    new_built_loan_deposit = models.FloatField(
        'New-build loan deposit, %',
        validators=[
            MaxValueValidator(95),
            MinValueValidator(5)
        ]
    )
    property_management_commission = models.FloatField(
        'Property Management commission, %',
        validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ]
    )
    vacancy_rate = models.IntegerField(
        'Vacancy rate, weeks',
        validators=[
            MinValueValidator(0)
        ]
    )
    gross_yield = models.FloatField(
        'Gross yield, %',
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1),
        ]
    )
    net_yield = models.FloatField(
        'Net yield, %',
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1),
        ]
    )
    min_cashflow = models.IntegerField(
        'Min cashflow',
        validators=[
            MinValueValidator(0)
        ]
    )
    inflation = models.FloatField(
        'Inflation, %',
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
