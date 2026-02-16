# VentureHub

A Django-based platform connecting **Startups**, **Investors**, and **Manufacturers**.

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/rahulbisht1301/final_project_aaah.git
cd final_project_aaah
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## Application URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |
| Manufacturer Login | http://127.0.0.1:8000/manufacturers/login/ |
| Startup Login | http://127.0.0.1:8000/startups/login/ |
| Investor Login | http://127.0.0.1:8000/investors/login/ |

## Features

### Manufacturers
- Register and login
- Browse approved startups
- Connect with startups via email/phone
- View connection history
- Edit company profile

### Startups
- Register and login
- Manage company profile
- View and respond to connection requests
- Apply for investment from investors

### Investors
- Register and login
- Browse startups by niche/stage
- View startup details and contact info
- Manage investment applications

## Project Structure

```
project-3-/
├── accounts/        # User authentication & profiles
├── startups/        # Startup app
├── investors/       # Investor app
├── manufacturers/   # Manufacturer app
├── templates/       # Base templates
├── venturehub/      # Project settings
├── db.sqlite3       # SQLite database
└── manage.py        # Django management script
```

## Creating Sample Data

To add sample startups for testing:

```bash
python manage.py shell
```

Then paste:

```python
from startups.models import Startup

Startup.objects.create(
    name="TechVision AI",
    niche="Artificial Intelligence",
    stage="Series A",
    valuation=5000000,
    vision="Building next-gen AI solutions",
    status="APPROVED",
    email="contact@techvision.ai",
    phone="+1-555-0101"
)
```

## License

This project is for educational purposes.
