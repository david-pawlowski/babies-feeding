# Baby feeding plan
It is a feeding planner app for babies. User can add different type of milk, and track how much and when newborns ate.
For now email notifications and push notifications are hardcoded to happen 2 hours after every feeding.

To set it working run:
1. Use *.env.example* file as a template to create *.env* file
    - You need to specify PUSHOVER_API_TOKEN generate it on:
    https://pushover.net/apps/build
    - EMAIL_HOST_USER and EMAIL_HOST_PASSWORD credentials for smtp
    - SECRETKEY, django secret key use for example https://djecrety.ir/ to generate it
    - Changing other variables may cause need of adjustment some parts in code so it is not recommended
2.
```bash
docker compose up -d
```
3.
```bash
docker exec -it baby_db psql -d postgres -U myuser
```
4.
```bash
CREATE DATABASE babydb WITH ENCODING 'UTF8'
```

Steps 3 and 4 can be skipped if you change DBNAME, DBUSER to *postgres* in .env and docker-compose.yml
5. Apply migrations to newly created database
```bash
docker exec -it baby_backend python manage.py migrate
```

6. You need user to login into admin, let's create super user
```bash
docker exec -it baby_backend python manage.py createsuperuser
```
