# Eventbrite Aggregator API

This project pulls data from the Eventbrite API and provides API access to a aggregated subset of this data.

Notes: 
* When the docker container is built the 'cron_script.py' is run automatically
which pulls data from the eventbrite API, this can take a few minutes to run.
* Django Rest Framework is used for the API endpoints. It provides an "explorable" WebUI when the 
endpoints are accessed from a browser which is useful for testing. This UI is 
switched off when debug mode is turned off.
* For most_popular_venue_per_category a lot of categories the the most popular
venue would tie for first place with just 1 event. I use ROW_NUMBER() to get the first
venue. The other option would be to use Rank() and make venue a list in the output.
* first_event and last_event are based on created date.

## Environmental Variables
* EB_BEARER - This is my api key for Eventbrite. For convenience I have left this in the repo.
* DEBUG - If equal to 'True', the server will be in debug mode. 
* DJANGO_LOG_LEVEL - Set to INFO by default.

Environmental Variables can be changed from the docker-compose.yml file.

## Setup
```
git clone git@github.com:paul-rchds/flexclub_test.git
docker-compose up --build

Browse to http://127.0.0.1:8001/events/
```

## Endpoints
* http://127.0.0.1:8001/events/
    * parameter field name are a bit different from the spec:
        * start
        * venue__uuid # Note the double underscore.
        * category__uuid
* http://127.0.0.1:8001/events/<event_id>/
* http://127.0.0.1:8001/organizers/details/<organizer_id>
* http://127.0.0.1:8001/stats/

