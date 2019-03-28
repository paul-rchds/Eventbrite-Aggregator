from dateutil import parser
from api.serializers import VenueSerializer, OrganizerSerializer, CategorySerializer
from fetcher.base import ItemFetcher, ItemsFetcher
import logging

logger = logging.getLogger(__name__)


class OrganizerFetcher(ItemFetcher):
    url = 'https://www.eventbriteapi.com/v3/organizers/{0}/'
    serializer_class = OrganizerSerializer


class VenueFetcher(ItemFetcher):
    url = 'https://www.eventbriteapi.com/v3/venues/{0}/'
    serializer_class = VenueSerializer


class CategoryFetcher(ItemFetcher):
    url = 'https://www.eventbriteapi.com/v3/categories/{0}/'
    serializer_class = CategorySerializer


class EventsFetcher(ItemsFetcher):
    url = 'https://www.eventbriteapi.com/v3/events/search'

    @classmethod
    def get_items(cls, location):
        data = {
            'location.longitude': location.longitude,
            'location.latitude': location.latitude,
            'location.within': '100km',
            'page': 1,
        }

        while True:
            response = cls.make_request(
                'GET',
                cls.url,
                params=data,
            )

            r_json = response.json()
            items = r_json.get('events')

            for item in items:
                item['location_id'] = location.id
                try:
                    parsed_items = cls.parse_item(item)
                except KeyError as e:
                    logger.exception(e)
                    continue

                yield parsed_items

            if r_json['pagination']['has_more_items']:
                data['page'] += 1
            else:
                break

    @classmethod
    def parse_item(cls, item):
        organizer = OrganizerFetcher.get_or_fetch(int(item['organizer_id'])).uuid
        venue = VenueFetcher.get_or_fetch(int(item['venue_id'])).uuid

        category = item.get('category_id', None)
        if category:
            category = CategoryFetcher.get_or_fetch(category).uuid

        data = {
            'uuid': int(item['id']),
            'start': parser.parse(item['start']['utc']),
            'end': parser.parse(item['end']['utc']),
            'created': parser.parse(item['created']),
            'changed': parser.parse(item['changed']),
            'name': item['name']['text'],
            'url': item['url'],
            'status': item['status'],
            'currency': item['currency'],
            'json_data': {},
            'organizer': organizer,
            'venue': venue,
            'category': category,
            'location': int(item['location_id']),
        }
        return data
