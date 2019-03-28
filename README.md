# Eventbrite Aggregator API

This project pulls data from the Eventbrite API and provides API access to a aggregated subset of this data.

Note: 
* When the docker container is built the 'cron_script.py' is run which pulls data from the 
eventbrite API, this can take a few minutes to run.
* Django Rest Framework is used for the API endpoints. It provides an "explorable" WebUI when the 
endpoints are accessed from a browser which is useful for testing.

## Environmental Variables
* EB_BEARER - This is my api key for Eventbrite. For convenience I have left this in the repo.
* DEBUG - If equal to 'True', the server will be in debug mode. 

Environmental Variables can be changed from the docker-compose.yml file.

## Setup
```
git clone <repo>
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

