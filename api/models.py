from django.db import models


class Event(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=1023)
    url = models.URLField()
    status = models.CharField(max_length=255, choices=[])
    currency = models.CharField(max_length=255, choices=[])
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE)
    organizer = models.ForeignKey('Venue', on_delete=models.CASCADE)
    location = models.ForeignKey('Venue', on_delete=models.CASCADE)
    category = models.ForeignKey('Venue', on_delete=models.SET_NULL, null=True)
    started_ad = models.DateTimeField()
    ended_at = models.DateTimeField()
    json_data = models.JSONField()


class Venue(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=1023)
    json_data = models.JSONField()


class Category(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=1023)
    json_data = models.JSONField()


class Organizer(models.Model):
    uuid = models.UUIDField(unique=True)
    name = models.CharField(max_length=1023)
    json_data = models.JSONField()


class Location(models.Model):
    name = models.CharField(max_length=1023)
    slug = models.SlugField(max_length=127)
    longitude = models.DecimalField(max_digits=9, decimal_places=7)
    latitude = models.DecimalField(max_digits=9, decimal_places=7)

