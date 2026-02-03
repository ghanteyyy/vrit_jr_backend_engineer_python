# vrit_jr_backend_engineer_python

## Tech Stack

- Python
- Django
- Django REST Framework
- HTML / CSS / JavaScript
- Postgresql

---

## Local Setup

### Clone the repository
```
git clone https://github.com/ghanteyyy/vrit_jr_backend_engineer_python.git
cd vrit_jr_backend_engineer_python
```

### Create and activate virtual environment

Windows:
```
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Run migrations
```
python manage.py makemigrations
python manage.py migrate
```

### Create superuser (optional)
```
python manage.py createsuperuser
```

## How It Works

### URL Shortening
- User submits a long URL
- System generates a unique short key
- Short URL is saved in the database

Example:
```
Original URL: https://example.com/some/very/long/url
Short URL:    http://127.0.0.1:8000/r/abc123/
```

### Redirection
- Visiting `/r/<short_key>/`
- Automatically redirects to the original URL

---

## API Authentication

For protected endpoints, include the access token in headers:

```
Authorization: Bearer <access_token>
```
