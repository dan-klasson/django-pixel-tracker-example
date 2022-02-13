# Django Pixel Tracker Example

Run `docker-compose` to build the app.

    docker-compose up --build -d

Which should give you access to the following tracked web pages:

    http://localhost:8005/about.html
    http://localhost:8005/contact.html

To run the commands:

    docker-compose run pixeltracker python manage.py tracker
    docker-compose run pixeltracker python manage.py tracker --date_from '2022-01-01 10:00:00'
    docker-compose run pixeltracker python manage.py tracker --date_to '2022-01-01 10:00:00'

To run the tests:

    docker-compose run pixeltracker python manage.py test
