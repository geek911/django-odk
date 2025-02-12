# django-odk
Django data collection tool using [ODK-collect](https://play.google.com/store/apps/details?id=org.odk.collect.android&hl=en_US&gl=US) mobile app.


## Prerequisite
- Django web site up and running
- Smartphone or tablet with [ODK-Collect installed](https://play.google.com/store/apps/details?id=org.odk.collect.android&hl=en_US&gl=US)
- Set of forms in [Xforms](https://xlsform.org/en/) format available in xml. Use https://getodk.org/xlsform/ to validate and export your forms in xml format.


## Installation
Run

```bash
$ pip install django-odk
$ python manage.py migrate
$ python manage.py createsuperuser
```

Add django_odk to your INSTALLED_APPS setting:

```py
INSTALLED_APPS = (
    ...
    'odk',
)
```

Add the following variables with appropriate language to settings.py
```py
# django-odk app
AVAILABLE_TXT = 'Available form'
SUBMITTED_TXT = 'Submitted form'
```

Add also appropriate AUTH_USER_MODEL in settings.py
```py
AUTH_USER_MODEL = 'auth.user'
```

Add odk.urls to the main urls.py file:
```py
urlpatterns = [
    ...
    path('odk/', include('odk.urls'), name='odk'),
]
```

Add menu or buttons to access **Available form**
```py
# bootstrap5 menu item example
<li><a class="dropdown-item" href="{% url 'odk:xform_list' %}">{% trans "ODK available forms" %}</a></li>
```

Add menu or buttons to access **Submitted form**
```py
# bootstrap5 menu item example
<li><a class="dropdown-item" href="{% url 'odk:xformsubmit_list' %}">{% trans "ODK submitted forms" %}</a></li>
```

## Upload Xforms
Connect to django-odk => **Available form** => Add and follow instructions to upload xml forms

Once it is done, you are ready to go with form encoding on your smartphone!

> Follow [ODK instructions](https://docs.getodk.org/collect-connect/#configure-server-manually) to configure the connexion to the server

> Get, fill-in and submit data [using ODK Collect](https://docs.getodk.org/collect-using/)

## Get submitted data on server
Go to **Submitted form** menu of your server to see submitted data



