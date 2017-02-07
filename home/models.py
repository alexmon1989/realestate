# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(unique=True, max_length=255)
    capital_growth = models.IntegerField(blank=True, null=True)
    council_link = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.city_name


class House(models.Model):
    house_id = models.AutoField(primary_key=True)
    street_name = models.CharField(max_length=255)
    street_number = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    city = models.ForeignKey(City, models.DO_NOTHING)
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    ensuite = models.IntegerField(blank=True, null=True)
    land = models.FloatField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    car_spaces = models.IntegerField(blank=True, null=True)
    property_type = models.IntegerField()
    price = models.IntegerField(blank=True, null=True)
    price_type = models.IntegerField()
    open_homes = models.CharField(max_length=1024, blank=True, null=True)
    auction_time = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=8192, blank=True, null=True)
    government_value = models.IntegerField(blank=True, null=True)
    government_rates = models.IntegerField(blank=True, null=True)
    photos = models.CharField(max_length=16384, blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    additional_data = models.CharField(max_length=2048, blank=True, null=True)
    property_id = models.CharField(max_length=16, blank=True, null=True)
    listing_create_date = models.DateField(blank=True, null=True)
    create_time = models.DateTimeField()
    agency_link = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'house'
        verbose_name = 'House'
        verbose_name_plural = 'Houses'
        unique_together = (('street_name',
                            'street_number',
                            'suburb',
                            'region',
                            'city',
                            'bedrooms',
                            'bathrooms',
                            'price'),)

    def __str__(self):
        return '{}, {}, {}'.format(self.city, self.street_name, self.street_number)


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
