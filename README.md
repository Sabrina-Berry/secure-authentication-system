# Secure Authentication System
A Python-based web application demonstrating secure user authentication & password hashing.

# Features
User registration and login
Secure password hashing using Werkzeug
SQLite database integration
Protected dashboard
Session management
Secure logout
CSRF protection using Flask-WTF
Input validation
Automated testing using Pytest
Technologies
Python
Flask
SQLite
Werkzeug
Flask-WTF
HTML
CSS
Pytest
Git and GitHub

# Project Structure
Secure-Authentication-System/
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/
│   ├── style.css
│   └── tests/
│       └── test_auth.py
├── app.py
├── database.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

# Installation
Clone the repository
Navigate into the project folder
Create and activate a virtual environment
Install dependencies:
requirements.txt
Create a .env file
Start the application

# Security Features
Passwords are hashed before database storage.
Parameterized SQL queries help prevent SQL injection.
CSRF protection helps prevent cross-site request forgery.
Protected routes restrict unauthorized dashboard access.
Environment variables keep application secrets outside source code.