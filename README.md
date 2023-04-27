# Sentigovt24

## Installation

### Database: 
Buat di pgAdmin4 dengan konfigurasi berikut.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sentigovt',
        'USER': 'postgres',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Project Installation:
1. Create virtual environment (python -m venv env)
2. Activate virtual environment (env/Scripts/activate.bat)
3. Upgrade latest pip version (pip install --upgrade pip)
4. Install Requirements (pip install -r requirements.txt)
5. Create database migrations (python manage.py makemigrations)
6. Applying migrations (python manage.py migrate)

### Running Application
`py manage.py runserver`



