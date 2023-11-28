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

   git clone https://github.com/SendiT-Project/SendiT-Backend.git
   cd SendiT-Backend

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

## USAGE
Run the application:
python app.py

By default, the application runs in debug mode. Open your web browser and go to http://localhost:5000 to access the app.

## CONFIGURATION
Secret Key: The SECRET_KEY is a crucial security measure for Flask applications. Ensure it's kept secret and unique for your application.

Database URI: Configure the DATABASE_URI with the appropriate connection details for your database (e.g., SQLite, PostgreSQL).

## ENDPOINTS
* /: Home endpoint.
* /signup: User registration endpoint (POST request).
* /login: User login endpoint (POST request).
* /logout: User logout endpoint (DELETE request).
* /session: Check user session (GET request).
* /orders: User can place orders
* /admin login:Admin login endpoint (POST request).
* /admin logout:Admin logout endpoint (DELETE request).

## TESTING


## Database Seeding
To populate the database with sample data, run the seeding script:
python seed.py
This script adds dummy users, orders, and tracking data to the database.

## Contributors 
* [Medrine Mulindi](https://github.com/Mulindi123)
* [Mucsin Yusuf](https://github.com/muxsinyusuf)
* [Cynthia Oloo](https://github.com/cynthiawuor)
* [Derrick Ochuodho](https://github.com/Dochuodho)


## License
MIT License

Copyright (c) 2023 SendiT Couriers Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.