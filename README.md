### Usage

This is a project for food recipes. 
The frontend part was kindly provided by yandex-praktikum.

Start backend project like this:

Create and activate virtual environment: \
`python -m venv venv && source venv/bin/activate`

Now make sure you have everything installed in your virtualenv: \
`cd backend`
`pip install -r requirements.txt`

Migrate the database:\
`cd backend`\
`python manage.py makemigrations && python manage.py migrate`

Now you are all set and can run the project!\
`python manage.py runserver`

### Technologies:
* Python
* Django
* Django REST Framework
* Djoser

### API:
API documentation locally: \
`cd /infra`\
`docker-compose up`\
and go to http://localhost/api/docs/
