GoCardless sample application
Setup

The first thing to do is to clone the repository:
```
$ https://github.com/Scource/TW_flow_site
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

While in `TW_flow_site/fullsite` directory install the dependencies:
```
(env)$ pip install -r requirements.txt
```

Once pip has finished downloading the dependencies:
```
(env)$ cd TW_flow_site/fullsite
(env)$ python manage.py runserver
```

Application should be up and running at `http://127.0.0.1:8000/`.
