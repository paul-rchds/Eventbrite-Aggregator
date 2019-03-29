import logging
import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from utils.errors import APIError

logger = logging.getLogger(__name__)


class Fetcher:
    headers = {'Authorization': f'Bearer {settings.EB_BEARER}'}
    url = None

    @classmethod
    def make_request(cls, method, url, **kwargs):
        r = requests.request(method=method, url=url, headers=cls.headers, **kwargs) # TODO Catch some IO exceptions.

        logger.warning(r.url)

        if r.status_code < 200 or r.status_code > 299:
            logger.error(r.text)
            raise APIError(r)

        return r

    @classmethod
    def parse_item(cls, item):
        raise NotImplementedError()


class ItemFetcher(Fetcher):
    serializer_class = None

    @classmethod
    def get_item(cls, pk):
        url = cls.url.format(pk)
        response = cls.make_request('GET', url)
        r_json = response.json()
        return cls.parse_item(r_json)

    @classmethod
    def parse_item(cls, item):
        data = {
            'uuid': int(item.pop('id', None)),
            'name': item.pop('name', None),
            'json_data': {},
        }
        return data

    @classmethod
    def get_or_fetch(cls, pk):
        try:
            return cls.serializer_class.Meta.model.objects.get(uuid=pk)
        except ObjectDoesNotExist as e:
            logger.info(f'{pk} does not exist. Creating...')

        item = cls.get_item(pk)
        serializer = cls.serializer_class(data=item)

        if serializer.is_valid():
            return serializer.save()

        logger.error(serializer.errors)


class ItemsFetcher(Fetcher):

    @classmethod
    def get_items(cls, location):
        raise NotImplementedError()
