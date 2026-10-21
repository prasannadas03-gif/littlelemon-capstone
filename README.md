# Little Lemon – Web Application API (Django REST Framework + MySQL)

Project: `littlelemon` · App: `restaurant`

## Setup

```bash
# 1. Create the MySQL database
mysql -u root -p -e "CREATE DATABASE littlelemon;"

# 2. Install dependencies with pipenv
pipenv install
pipenv shell

# 3. Put YOUR MySQL user/password in littlelemon/settings.py (DATABASES)
#    or export MYSQL_USER / MYSQL_PASSWORD

# 4. Migrate and run
python manage.py migrate
python manage.py runserver
```

## Endpoints

| Endpoint | Methods | Auth |
|---|---|---|
| `/` or `/restaurant/` | Static HTML home page | None |
| `/auth/users/` | POST – register a user (Djoser) | None |
| `/api-token-auth/` | POST – get a token (`username`, `password`) | None |
| `/auth/token/login/`, `/auth/token/logout/` | Djoser token login/logout | – |
| `/restaurant/menu/` | GET list, POST create | Token for POST |
| `/restaurant/menu/<id>` | GET, PUT, PATCH, DELETE | Token to change |
| `/restaurant/booking/tables/` | GET, POST | Token |
| `/restaurant/booking/tables/<id>/` | GET, PUT, PATCH, DELETE | Token |

Send the token as a header: `Authorization: Token <your-token>`.

## Testing with Insomnia

1. In Insomnia: **Import** → choose `insomnia_collection.json`.
2. Run **1. Register user**, then **2. Get token**.
3. Paste the token into the environment variable `token` (Manage Environments).
4. Run the Menu and Booking requests.

## Unit tests

```bash
python manage.py test restaurant
```

Tests are in `restaurant/tests/` (`test_models.py`, `test_views.py`).
Django creates a temporary `test_littlelemon` database, so your MySQL
user needs permission to create databases.
