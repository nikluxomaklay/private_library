# Private Library

## Project Description

**Private Library** is a Django web application for managing a personal book collection. It provides a comprehensive system for cataloging books, authors, editions, series, publishers, and tracking your reading history with detailed logging capabilities.

### Main Features:
- **Book Management**: Store books with original and extended titles in multiple languages
- **Author Management**: Comprehensive author profiles with first, middle, and last names
- **Edition Tracking**: Multiple editions of the same book with publisher and series information
- **Reading Log**: Track when you start and finish reading books with month/year precision
- **Series & Publishers**: Organize books by series and track publishing information
- **Advanced Search**: Autocomplete functionality and filtering by various parameters


---

## Installation and Launch

### 1. Clone the repository
```bash
git clone <repository-url>
cd private_library
```

### 2. Run with Docker (Recommended)

#### 2.1. Set up environment variables
Copy the environment variables file:
```bash
cp docker_debug/default.env .env
```

Edit the values in `.env` file:
```bash
# Required settings
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost 127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:51101

# Database settings
DATABASE_USER=your_db_user
DATABASE_PASS=your_db_password
DATABASE_DB=your_db_name
DATABASE_MOUNTED_DUMPS_DIR=/path/to/dumps  # Optional

# Frontend settings
ENABLE_DJANGO_FRONTEND=1  # 1 - enable front, 0 - disable
STATIC_ROOT=/app/static    # Absolute path for static files (optional)
```

#### 2.2. Start the containers
```bash
docker compose -f docker_debug/compose.yaml up --build
```

- The application will be available at: http://localhost:51101/
- The Django app runs on port 8011
- To stop the containers:
```bash
docker compose -f docker_debug/compose.yaml down
```

---

### 3. Run with Python Debugger Support (debugpy)

This mode allows you to connect a Python debugger (e.g., from VSCode or PyCharm) to the running Django app inside the container.

#### 3.1. Start the containers with debug support
```bash
docker compose -f docker_debug/compose.yaml up --build
```

- The Django app will be available at: http://localhost:8011/
- The debugpy server will listen on port 5678

#### 3.2. Connect your IDE debugger
- **Host**: `localhost`
- **Port**: `5678`
- **Mode**: Attach to the running Python process (do not launch a new one)

---

### 4. Local Development Setup

#### 4.1. Install dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Linux/macOS
venv\Scripts\activate     # for Windows
pip install -r requirements.txt
```

#### 4.2. Database setup
Install and configure PostgreSQL, then create a database for the project.

#### 4.3. Configuration
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
ENABLE_DJANGO_FRONTEND: 1
STATIC_ROOT: "/app/static"
```

#### 4.4. Apply migrations and run
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

---

## Project Structure

```
private_library/
├── core/                    # Core models and business logic
│   ├── models.py           # Database models (Book, Author, Edition, etc.)
│   ├── enums.py            # Enumeration classes
│   └── migrations/         # Database migrations
├── front/                   # Web interface components
│   ├── views/              # Django views and forms
│   ├── forms/              # Form definitions
│   ├── urls.py             # URL routing
│   └── apps.py             # App configuration
├── templates/               # HTML templates
│   ├── base_layout.html    # Base template
│   ├── book/               # Book-related templates
│   ├── author/             # Author templates
│   ├── reading_log/        # Reading log templates
│   └── ...                 # Other entity templates
├── static/                  # Static files (CSS, JS, images)
├── docker/                  # Production Docker configuration
├── docker_debug/            # Development Docker configuration with debugpy
└── private_library/         # Django project settings
```

---

## Data Models

### Core Entities:
- **Book**: Base book information with titles in multiple languages
- **Author**: Author profiles with full name support
- **BookEdition**: Specific editions with publisher, series, and publication details
- **Publisher**: Publishing house information
- **BookSeries**: Book series organization
- **ReadingLog**: Detailed reading history with start/finish dates
- **Year**: Year reference for reading logs

### Key Features:
- **Multi-language Support**: Original and translated titles
- **Flexible Author Names**: First, middle, and last name support
- **Edition Management**: Track different versions of the same book
- **Reading Progress**: Month and year precision for reading logs
- **Relationship Management**: Complex relationships between books, authors, and editions

---

## Dependencies

- **Django**: 5.1.1 - Web framework
- **django-autocomplete-light**: 3.12.1 - Enhanced autocomplete functionality
- **django-bootstrap5**: 24.3 - Bootstrap 5 integration
- **PyYAML**: 6.0.2 - Configuration file support
- **psycopg[binary]**: 3.2.9 - PostgreSQL database adapter

---

## Development

### Adding New Features
1. Create models in `core/models.py`
2. Generate and apply migrations: `python manage.py makemigrations && python manage.py migrate`
3. Create views in `front/views/`
4. Add URL patterns in `front/urls.py`
5. Create templates in `templates/`

### Code Style
- Follow Django best practices
- Use meaningful model and field names
- Include proper docstrings for complex methods
- Maintain consistent formatting
- Adhere to the project's core principles:
  - **Minimalism in the frontend**: Simple web page design, without special effects and complex logic
  - **Model-First**: Every feature starts as a well-defined Django model
  - **Admin Interface**: Expose all model functionality via Django admin
  - **Test-First**: Write tests before implementation (TDD)
  - **Integration Testing**: Focus on testing model relationships and inter-model communication
  - **Observability**: Implement structured logging and follow MAJOR.MINOR.BUILD versioning

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Support

For questions or issues, please create an issue in the repository or contact the maintainers.