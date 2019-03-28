from rest_framework import serializers
from api.models import Organizer, Venue, Category, Event


class OrganizerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organizer
        fields = ('uuid', 'name', 'json_data')


class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ('uuid', 'name', 'json_data')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('uuid', 'name', 'json_data')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

