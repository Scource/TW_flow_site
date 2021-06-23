# TW_flow_site
Application for tracking team progress during pandemic

## Setup

The first thing to do is to clone the repository:
```
$ git clone https://github.com/Scource/TW_flow_site
```

Create a virtual environment to install dependencies in and activate it:
```
$ python virtualenv.py ENV
$ source env/bin/activate
```
for WINDOWS
```
\path\to\env\Scripts\activate
```

Installing dependencies while in `TW_flow_site/fullsite`:
```
(env)$ pip install -r requirements.txt
```

Once pip has finished downloading the dependencies:
```
(env)$ cd TW_flow_site/fullsite
(env)$ python manage.py runserver
```

Application should be up and running at `http://127.0.0.1:8000/`.
