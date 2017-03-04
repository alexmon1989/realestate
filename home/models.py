# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from datetime import datetime
import json
import pytz


class Region(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'region'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.name


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(unique=True, max_length=255)
    capital_growth = models.IntegerField(blank=True, null=True)
    council_link = models.TextField(blank=True, null=True)
    region = models.ForeignKey('Region', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'city'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city_name


class Suburb(models.Model):
    city = models.ForeignKey(City, models.CASCADE)
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'suburb'
        verbose_name = 'Suburb'
        verbose_name_plural = 'Suburbs'

    def __str__(self):
        return self.name


class PricingMethod(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'pricing_method'
        verbose_name = 'Pricing method'
        verbose_name_plural = 'Pricing methods'

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    name = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'property_type'
        verbose_name = 'Property type'
        verbose_name_plural = 'Property types'

    def __str__(self):
        return self.name


class House(models.Model):
    house_id = models.AutoField(primary_key=True)
    street_name = models.CharField(max_length=255)
    street_number = models.CharField(max_length=255)
    suburb = models.ForeignKey('Suburb', models.CASCADE)
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    ensuite = models.BooleanField()
    land = models.FloatField('Land area', blank=True, null=True)
    floor = models.IntegerField('Floor area', blank=True, null=True)
    car_spaces = models.IntegerField(blank=True, null=True)
    property_type = models.ForeignKey('PropertyType', models.CASCADE)
    price = models.IntegerField(blank=True, null=True)
    price_type = models.ForeignKey('PricingMethod', models.CASCADE)
    auction_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=8192, blank=True, null=True)
    government_value = models.IntegerField(blank=True, null=True)
    government_rates = models.IntegerField(blank=True, null=True)
    government_to_price = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)
    photos = models.CharField(max_length=16384, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    additional_data = models.CharField(max_length=2048, blank=True, null=True)
    property_id = models.CharField(max_length=16, blank=True, null=True)
    listing_create_date = models.DateField(blank=True, null=True)
    create_time = models.DateTimeField('Created at')
    agency_link = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'house'
        verbose_name = 'House'
        verbose_name_plural = 'Houses'
        unique_together = (('street_name',
                            'street_number',
                            'suburb',
                            'bedrooms',
                            'bathrooms',
                            'price'),)

    def __str__(self):
        return '{}, {}, {}'.format(self.suburb.city, self.suburb, self.street_name, self.street_number)

    @staticmethod
    def get_new_houses(filters, excluded_pks):
        """Returns queryset with new houses by user's filters."""
        queryset = None

        # getting querysets for each filter and merge them in one queryset
        for f in filters:
            filter_data = json.loads(f.filter_data_json)
            houses = House.objects.extra(
                select={"address": "CONCAT_WS(' ', house.street_number, house.street_name)"}
            ).values(
                'house_id',
                'suburb__name',
                'suburb__city__city_name',
                'suburb__city__region__name',
                'street_name',
                'street_number',
                'land',
                'floor',
                'price',
                'listing_create_date',
                'photos',
                'address'
            ).filter(
                suburb__in=filter_data['suburbs'],
                price__range=(filter_data['price_from'][0], filter_data['price_to'][0]),
                price_type__in=filter_data['pricing_methods'],
                government_value__range=(
                    filter_data['government_value_from'][0], filter_data['government_value_to'][0]
                ),
                government_to_price__range=(
                    filter_data['government_value_to_price_from'][0], filter_data['government_value_to_price_to'][0]
                ),
                bedrooms__range=(filter_data['bedrooms_from'][0], filter_data['bedrooms_to'][0]),
                bathrooms__range=(filter_data['bathrooms_from'][0], filter_data['bathrooms_to'][0]),
                land__range=(filter_data['landarea_from'][0], filter_data['landarea_to'][0]),
                floor__range=(filter_data['floorarea_from'][0], filter_data['floorarea_to'][0]),
                property_type__in=filter_data['property_type'],
                description__contains=filter_data['keywords'][0],
                car_spaces__range=(filter_data['carspace_from'][0], filter_data['carspace_to'][0]),
                listing_create_date__gte=filter_data['listings_date_created'][0],
            ).exclude(
                pk__in=excluded_pks
            )
            if filter_data.get('show_only_properties_with_address'):
                houses = houses.filter(
                    street_name__isnull=False,
                    street_number__isnull=False
                ).exclude(
                    street_name='',
                    street_number=''
                )
            if filter_data.get('ensuite'):
                houses = houses.filter(ensuite=True)
            if filter_data.get('show_only_open_homes'):
                now = datetime.now()
                houses = houses.filter(
                    openhomes__date_from__gte=datetime(now.year, now.month, now.day, tzinfo=pytz.UTC),
                    openhomes__date_to__lte=datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=pytz.UTC),
                )
            if queryset:
                queryset = queryset | houses
            else:
                queryset = houses

        # return houses queryset
        if queryset:
            return queryset.distinct()
        return []


class OpenHomes(models.Model):
    house = models.ForeignKey(House, models.CASCADE)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'open_homes'
        unique_together = (('house', 'date_from', 'date_to'),)


class Agency(models.Model):
    agency_id = models.AutoField(primary_key=True)
    agency_name = models.TextField(unique=True, max_length=512)
    city = models.ForeignKey('City', models.DO_NOTHING)
    email = models.TextField(blank=True, null=True)
    work_phone = models.TextField(blank=True, null=True)
    houses = models.ManyToManyField(House, db_table='agencyhouse')

    def __str__(self):
        return '{} ({})'.format(self.agency_name, self.city)

    class Meta:
        managed = False
        db_table = 'agency'
        verbose_name = 'Agency'
        verbose_name_plural = 'Agencies'


class Agent(models.Model):
    agent_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    mobile_phone = models.TextField(blank=True, null=True)
    ddi_phone = models.TextField(blank=True, null=True)
    work_phone = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    agency = models.ForeignKey(Agency, models.DO_NOTHING)
    houses = models.ManyToManyField(House, db_table='agenthouse')

    def __str__(self):
        return '{} ({})'.format(self.name, self.email)

    class Meta:
        managed = False
        db_table = 'agent'
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'
        unique_together = (('name', 'agency'),)
