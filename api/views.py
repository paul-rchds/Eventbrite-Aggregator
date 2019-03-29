import logging
from itertools import groupby
from django.db.models import Count
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Event, Organizer, Venue
from api.serializers import EventSerializer
from utils.sql import execute_sql

logger_sql = logging.getLogger('sql')


class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('start', 'venue__uuid', 'category__uuid')


class EventDetail(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'uuid'


class OrganizerDetail(APIView):

    def get_object(self, uuid):
        try:
            return Organizer.objects.get(uuid=uuid)
        except Organizer.DoesNotExist:
            raise Http404

    def get(self, request, uuid):
        organizer = self.get_object(uuid)
        events = organizer.events.order_by('created')
        first_event = EventSerializer(events.first())
        last_event = EventSerializer(events.last())

        venue_count = Venue.objects.filter(events__organizer__uuid=uuid).\
            annotate(event_count=Count('events')).\
            values('event_count', 'name', 'uuid')

        data = {
            'first_event': first_event.data,
            'last_event': last_event.data,
            'total_events': events.count(),
            'venue_count': list(venue_count)
        }
        return Response(data)


class StatsDetail(APIView):

    @staticmethod
    def avg_weekly_events_per_month_location():
        sub_query = """
                SELECT location.name, 
                        location.id,
                        DATE_TRUNC('week', event.start) AS week, 
                        DATE_TRUNC('month', event.start) AS month, 
                        COUNT(event.uuid) AS week_count 
                FROM api_event event
                INNER JOIN api_location location ON (event.location_id = location.id) 
                GROUP BY location.name, week, month, location.id
                """
        main_query = """
                SELECT month, name, ROUND(AVG("week_count"), 2) as weekly_avg
                FROM (%s) AS sub_table
                GROUP BY month, name
                ORDER BY name
                """ % (sub_query,)
        return execute_sql(main_query)

    @staticmethod
    def most_popular_venue_per_category():
        sub_query = """
            SELECT category.uuid AS category_uuid, 
                    category.name AS category_name, 
                    venue.name AS venue_name, 
                    venue.uuid AS venue_uuid, 
                    COUNT(event.uuid) AS event_count,
            ROW_NUMBER () OVER (
            PARTITION BY category.uuid
            ORDER BY
            COUNT(event.uuid) DESC
            ) AS rank_filter
            FROM api_venue venue 
            INNER JOIN api_event event ON (venue.uuid = event.venue_id) 
            INNER JOIN api_category category ON (category.uuid = event.category_id) 
            GROUP BY category_uuid, category_name, venue_name, venue_uuid
            """
        main_query = """
                    SELECT * 
                    FROM (%s) AS sub_table
                    WHERE "rank_filter" = 1
                    """ % (sub_query,)
        return execute_sql(main_query)

    @classmethod
    def get_location_data(cls):
        location_data = []
        rows = cls.avg_weekly_events_per_month_location()

        for key, group in groupby(rows, key=lambda x: x['name']):
            dict_ = {
                "location": key,
                "months": {},
            }
            for item in group:
                dict_['months'][item['month'].strftime("%B")] = float(item['weekly_avg'])

            location_data.append(dict_)

        return location_data

    @classmethod
    def get_popular_category_data(cls):
        category_data = []
        rows = cls.most_popular_venue_per_category()

        for row in rows:
            dict_ = {
                'category': {
                    'uuid': row['category_uuid'], # Field name changed from the spec.
                    'name': row['category_name'],
                },
                'venue': {
                    'uuid': row['venue_uuid'],
                    'name': row['venue_name'],
                    'event_count': row['event_count'], # Just adding event count here even though its not in the spec.
                }

            }
            category_data.append(dict_)

        return category_data

    def get(self, request):
        data = {
            'avg_weekly_events_per_month_location': self.get_location_data(),
            'most_popular_venue_per_category': self.get_popular_category_data(),
        }
        return Response(data)
