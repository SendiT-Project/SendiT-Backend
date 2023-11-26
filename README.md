# SendiT-Backend
# Flask User Authentication and Order Tracking App

This is a Flask application designed for user authentication and order tracking. It provides a secure user registration and login system, allowing users to place orders and track their status.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Database Seeding](#database-seeding)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- User Registration and Authentication
- Secure Password Hashing
- Order Placement and Tracking
- Session Management
- API Endpoints for User and Order Information

## Prerequisites

Before you begin, ensure you have the following prerequisites installed on your machine:

- Python 3.x
- pip (Python package installer)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/flask-auth-order-tracking.git
   cd flask-auth-order-tracking

2. Create and activate a virtual environment (optional but recommended):
venv\Scripts\activate
On macOS and Linux:
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Set up environment variables:
Create a .env file in the root directory and add the following:
SECRET_KEY=your_secret_key
DATABASE_URI=your_database_uri
Replace your_secret_key and your_database_uri with your actual secret key and database URI.

DATABASE MIGRATION:
Run the following commands to apply the database migrations:
flask db init
flask db migrate
flask db upgrade

USAGE
Run the application:
python your_app_filename.py

By default, the application runs in debug mode. Open your web browser and go to http://localhost:5000 to access the app.

CONFIGURATION
Secret Key: The SECRET_KEY is a crucial security measure for Flask applications. Ensure it's kept secret and unique for your application.

Database URI: Configure the DATABASE_URI with the appropriate connection details for your database (e.g., SQLite, PostgreSQL).

ENDPOINTS
/: Home endpoint.
/signup: User registration endpoint (POST request).
/login: User login endpoint (POST request).
/logout: User logout endpoint (DELETE request).
/session: Check user session (GET request).
Database Seeding
To populate the database with sample data, run the seeding script:
python seed.py
This script adds dummy users, orders, and tracking data to the database.

