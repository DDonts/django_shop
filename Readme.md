# Django shop

## Build

The first thing to do is to clone the repository:

```bash
$ git clone https://github.com/DDonts/django_shop.git
$ cd sample-django-app
```

Then create ```settings.ini``` file on base of ```settings.ini.example``` in route directory and set variables

### Docker-compose

```bash
$ docker-compose up
```

### Pure Django
```bash
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```