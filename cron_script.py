#!/usr/bin/python
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventbrite_aggr.settings")
django.setup()
from api.models import Location
from api.serializers import EventSerializer
from fetcher.fetchers import EventsFetcher
import logging

logger = logging.getLogger(__name__)


def fetch_events():

    logging.warning('Starting cron script...')

    for location in Location.objects.all():
        events = EventsFetcher.get_items(location)

        for event in events:
            serializer = EventSerializer(data=event)

            if serializer.is_valid():
                serializer.save()
            else:
                logger.error(serializer.errors)

    logging.warning('Finished cron script...')


if __name__ == '__main__':
    fetch_events()


