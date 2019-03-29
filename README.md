# Eventbrite Aggregator API

This project pulls data from the Eventbrite API and provides API access to a aggregated subset of this data.

Note: 
* When the docker container is built the 'cron_script.py' is run which pulls data from the 
eventbrite API, this can take a few minutes to run.
* Django Rest Framework is used for the API endpoints. It provides an "explorable" WebUI when the 
endpoints are accessed from a browser which is useful for testing.
* For most_popular_venue_per_category a lot of categories the the most popular
venue would tie for first place with just 1 event. I use ROW_NUMBER() to get the first
venue. The other option would be to use Rank() and make venue a list in the output.

## Environmental Variables
* EB_BEARER - This is my api key for Eventbrite. For convenience I have left this in the repo.
* DEBUG - If equal to 'True', the server will be in debug mode. 
* DJANGO_LOG_LEVEL - Set to INFO by default.

Environmental Variables can be changed from the docker-compose.yml file.

## Setup
```
git clone git@github.com:paul-rchds/flexclub_test.git
docker-compose up --build

Browse to http://127.0.0.1:8003/
```

## Endpoints
* http://127.0.0.1:8003/events
    * parameter field name are a bit different from the spec:
        * start_date
        * venue__uuid # Note the double underscore.
        * category__uuid
* http://127.0.0.1:8003/events/<event_id>/
* http://127.0.0.1:8003/organizers/details/<organizer_id>
* http://127.0.0.1:8003/stats/

