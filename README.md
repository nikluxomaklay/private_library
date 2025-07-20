# private_library

## Project Description

**private_library** is a Django web application for managing a personal library. It allows you to store information about books, authors, editions, series, publishers, and track your reading history.

### Main Features:
- Cataloging books, authors, editions, series, and publishers
- Keeping a reading log
- Search and filtering by various parameters
- User-friendly web interface with autocomplete

---

## Installation and Launch

### 1. Clone the repository
```bash
git clone <repository-url>
cd private_library
```

### 2. Run with Docker (recommended)

#### 2.1. Set up environment variables

Copy the environment variables file:
```bash
cp docker/default.env .env
```

Edit the values in `.env` (e.g., SECRET_KEY, DATABASE_USER, DATABASE_PASS, DATABASE_DB).

#### 2.2. Start the containers
```bash
docker compose -f docker/compose.yaml up --build
```

- The application will be available at: http://localhost:51100/
- To stop the containers, use:
```bash
docker compose -f docker/compose.yaml down
```

---

### 3. Local launch without Docker

#### 3.1. Install dependencies

It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Linux/macOS
venv\Scripts\activate   # for Windows
pip install -r requirements.txt
```

#### 3.2. Configuration

Create a `config.yml` file or use environment variables (see example in `docker/default.env`).

Example `config.yml`:
```yaml
SECRET_KEY: "your_secret_key"
ALLOWED_HOSTS: "localhost 127.0.0.1"
DATABASE_ENGINE: "django.db.backends.postgresql"
DATABASE_HOST: "localhost"
DATABASE_USER: "your_db_user"
DATABASE_PASS: "your_db_password"
DATABASE_DB: "your_db_name"
```

#### 3.3. Apply migrations and run
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

---

## Project Structure
- `core/` — main models and business logic
- `front/` — views and forms for the web interface
- `private_library/` — Django settings and configuration
- `templates/` — HTML templates
- `static/` — static files (CSS, JS, images)
- `docker/` — files for containerization and environment setup

---

## Dependencies
- Django 5.1.1
- django-autocomplete-light
- django-bootstrap5
- PyYAML
- psycopg[binary]

---

## License

MIT (or specify your license)