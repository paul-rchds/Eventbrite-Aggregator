from django.db import models
from django.contrib.postgres.fields import JSONField


class Event(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=1023)
    url = models.URLField()
    status = models.CharField(max_length=255, choices=[])
    currency = models.CharField(max_length=255, choices=[])
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    organizer = models.ForeignKey('Organizer', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    started_ad = models.DateTimeField()
    ended_at = models.DateTimeField()
    json_data = JSONField()

    def __str__(self):
        return self.name



class Venue(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=1023)
    json_data = JSONField()

    def __str__(self):
        return self.name


class Category(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=1023)
    json_data = JSONField()

    def __str__(self):
        return self.name


class Organizer(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=1023)
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
