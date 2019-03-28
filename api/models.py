from django.db import models
from django.contrib.postgres.fields import JSONField

STATUS_CHOICES = [
    ('draft', 'draft'),
    ('live', 'live'),
    ('started', 'started'),
    ('ended', 'ended'),
    ('completed', 'completed'),
    ('canceled', 'canceled'),
]


class Event(models.Model):
    uuid = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=1023)
    url = models.URLField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    currency = models.CharField(max_length=255)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, related_name='events')
    organizer = models.ForeignKey('Organizer', on_delete=models.CASCADE, related_name='events')
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='events')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='events')
    start = models.DateTimeField()
    end = models.DateTimeField()
    json_data = JSONField(null=False)
    created = models.DateTimeField()
    changed = models.DateTimeField()

    def __str__(self):
        return self.name


class Venue(models.Model):
    uuid = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=1023, null=True, blank=True)
    json_data = JSONField()

    def __str__(self):
        return self.name


class Category(models.Model):
    uuid = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=1023, null=True, blank=True)
    json_data = JSONField()

    def __str__(self):
        return self.name


class Organizer(models.Model):
    uuid = models.BigIntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=1023, null=True, blank=True)
    json_data = JSONField()

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=1023)
    slug = models.SlugField(max_length=127)
    longitude = models.DecimalField(max_digits=9, decimal_places=7)
    latitude = models.DecimalField(max_digits=9, decimal_places=7)

    def __str__(self):
        return self.name
