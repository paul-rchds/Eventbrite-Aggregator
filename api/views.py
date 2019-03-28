from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.views import APIView
from api.models import Event, Organizer, Venue, Category
from api.serializers import EventSerializer
from django.http import Http404
from rest_framework.response import Response
from django.db.models import Count, Avg, F, ExpressionWrapper, FloatField, Max
from decimal import Decimal
import logging

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
        events = organizer.events.all()
        first_event = EventSerializer(events.first())
        last_event = EventSerializer(events.last())

        venue_count = Venue.objects.filter(events__organizer__uuid=uuid).\
            annotate(event_count=Count('events')).\
            values('event_count', 'name', 'uuid')

        logger_sql.info(venue_count.query)

        data = {
            'first_event': first_event.data,
            'last_event': last_event.data,
            'total_events': events.count(),
            'venue_count': list(venue_count)
        }

        return Response(data)


class StatsDetail(APIView):

    def get(self, request):

        # FIXME This is far from elegant. Maybe raw sql would be better.
        events = Event.objects.\
            values('location__name', 'start__month').\
            annotate(month_count=ExpressionWrapper(
            Count('uuid')*Decimal('1.0')/4,
            output_field=FloatField()
        ))

        # logger_sql.info(events.query)

        # for event in events:
        #     print(event)

        # categories = Category.objects.annotate(venue_count=Count('events__venue'))
        # venues = Venue.objects.values('events__category').annotate(num_events=Count('events')).annotate(max_events=Max('num_events'))

        venues = Venue.objects.raw('select ')

        print(venues)
        print(venues.query)

        for venue in venues:
            print(venue)

        data = {}
        return Response(data)
