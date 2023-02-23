# Ecommerce Website
## Setup
### Project Setup
#
- Clone this repository
    > `git clone https://github.com/Hrushikesh74161/ecommerce_store.git`
- In this folder, create virutal environment
    > `python3.11 -m venv venv`
- Run virtual environment
    - In linux/mac
        > `source venv/bin/activate`
    - In windows cmd
        > `venv\bin\acitvate.bat`
    - In widows powershell
        > `venv\bin\activate.ps1`
- Install dependencies, run
    > `pip install -r requirements.txt`
- Get secret key using python shell
    > `python -c 'import secrets; print(secrets.token_urlsafe())` 
- Assign this key to DJANGO_SECRET_KEY in .django_env file.
---
### Database Setup
- Either use postgres or default sqlite3.

#### Postgres database
#
- Create folder named db in project root.

- Set user and password for postgres in .postgres_env file. postgres is default user and password.
- postgres is default database name.
- Install docker
- Run postgres in docker using this command
    > `docker compose up`
#### Default sqlite database
#
- In DATABASES settings

- Change ENGINE option to 'django.db.backends.sqlite3'.

- Change NAME to BASE_DIR/'db.sqlite3'

- Remove USER, PASSWORD, HOST, PORT options.

### Stripe Setup

- Create stripe account
- Get publishable and secret api keys.
- Assign them to STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY in .django_env file.
- Install stripe.
- In windows system, place stripe.exe in project root folder.
- Open shell/cmd and login into stripe

    > `stripe login`

### Running website
- All commands should be run in virtual environment in the project root folder where manage.py file exists.
- If postgres is used, docker should be running.
- To create databaes tables

    > `python manage.py migrate`
- Create superuser
    > `python manage.py createsuperuser`
- For stripe to display events and send those events to our website run
    > `stripe list --forward-to localhost:8000/payment/webhook/`
- Above command creates a webhook secret key assign it to STRIPE_WEBHOOK_ENDPOINT_SECRET in .django_env file.
- To start server
    > `python manage.py runserver`