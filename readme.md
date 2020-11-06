## Store Project


### ToDo List 

- [ ] WEBSITE
    - [x] Display Products - desktop & mobile view
    - [ ] Search - product name / brand / category 
    - [x] Browse products via category
    - [x] User Signup & Login
    - [x] Forgot passowrd
    - [ ] Session / Cookie guest checkout 
    - [ ] Contact & FAQ page 
- [ ] ADMIN  
    - [ ] Edit Projuct from main page
    - [x] View all orders
    - [x] Manage orders status
    - [x] Views & routes for crud o/p
    - [ ] Ajax search / sugesstion automcomplete
    - [x] Add projucts / brands / category via ajax 
    - [ ] Email shoot 
- [x] USER
    - [x] Add item's to cart & store
    - [x] Project stocks constraint to cart
    - [x] Checkout - COD
    - [x] View all previous orders  
    - [ ]  Edit profile 
- [x] API 
    - [x] Api routes display
    - [x] Get products list - nested json

&nbsp;

----
### Demo Not hosted yet :-

| Website       | URL                  |
| ------------- | ------------------------------ |
| Heroku           |  |
| Pythonanywhere   |  |

<br/>

### Run this Django app on local server?

Create an empty folder :
```sh
git clone https://github.com/NishantGhanate/store.git.
```

In Cli : 1.Create virtual env , 2. Activate it,  3. Install requirements 
```sh
 > virtualenv venv

 > venv\Scripts\activate

 > pip install -r requirements.txt
```

### Generate Django secret key :
```sh
from django.core.management.utils import get_random_secret_key

get_random_secret_key()

'[GENERATED KEY]'
```

&nbsp;

### Env file
Simply create a .env text file on your repository’s root directory where manage.py exists , then paste secertkey :

```sh
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
SECRET_KEY=SECRETKEY
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=
DATABASE_URL=
```

### Inside settings.py of project
```sh
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# django.core.mail.backends.smtp.EmailBackend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = True
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
```

### Run :
> python manage.py migrate

> python manage.py createsuperuser

> python manage.py runserver


&nbsp;

### Easy guide to host on python anywhere
> https://tutorial.djangogirls.org/en/deploy/

&nbsp;

### Somethings about this project 

```sh
This Django project two Django apps 
1. api
2. guptastore

The goal of this project is to create small ecommerce like web-site for my friends kirana store .
This project is still underdevelopment , adding & improvising on certain things like ajax & api 

```