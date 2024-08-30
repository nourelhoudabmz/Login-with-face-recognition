# Overview
This project is a Face Recognition Security System built with Django  It provides a robust API for user registration and authentication.

## In This Project:
- User registration and authentication
- Login with face

# Installation
1. Clone the repository:
    git clone [https://github.com/nourelhoudabmz/Login-with-face-recognition.git]
    cd src
2. Create and activate a virtual environment:
    python -m venv venv
    source venv/bin/activate
3. Install the required packages:
    pip-compile src/requirements/requirements.in -o src/requirements.txt
    pip install -r src/requirements.txt
4. Apply migrations:
    python manage.py migrate
5. Run the development server:
   python manage.py runserver
