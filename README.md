# DRF Forum #

Remaster project "Forum" on Django REST Framework. A small forum, designed for communication, finding answers to
various problems of the author of the post. Allows you to create questions, answers, take part in voting

# Built on #

* Django REST framework 3.14.0
* Python 3.10


# Getting started #

Clone the repository and enter into it.

``` 
$ git clone https://github.com/Mulyarchik/drf_forum.git
$ cd drf_forum
```

Set your settings in the ‘.env’ file, but defaults is enough just to try the service locally.

Run docker compose to build and run the service and it’s dependencies.

```
$ docker compose up -d --build
```

(Optional) Populate a DB with a dummy data:

```
$ python manage.py loaddata data.json
```

Open in your browser:

```
http://0.0.0.0:8080/
```

