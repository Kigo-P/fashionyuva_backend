# Fashionyuva Backend

Welcome to the **Fashionyuva Backend**, the core engine powering our fashionable clothing e-commerce platform. This repository contains the backend code built using Flask, designed to support a seamless and engaging user experience for our fashion-conscious customers.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

---

## About

Fashionyuva aims to stand out in the competitive online fashion retail market by offering a unique, visually engaging platform with a curated collection of trendy clothing. The backend is responsible for:

- Managing product catalogs with detailed information (sizing, fit, fabric, etc.).
- Processing user authentication and account management.
- Facilitating secure and seamless payment processing.
- Handling order management, including shipping and returns.
- Supporting scalability and reliability for smooth user experiences across devices.

---

## Features

- **Product Management**: Manage the catalog of fashionable clothing items with detailed information.
- **User Authentication**: Secure login, registration, and session management.
- **Order Processing**: Handle orders, shipping, and returns reliably.
- **Payment Integration**: Seamless and secure payment gateway support.
- **API-Driven Architecture**: RESTful APIs for communication with the frontend.
- **Scalable Design**: Optimized to handle high traffic and diverse user devices.

---

## Technologies Used

- **Framework**: Flask - Lightweight Python web framework.
- **Database**: POSTGRES and SQLAlchemy for ORM and database interactions.
- **Authentication**: JWT
- **Payment**: Integration with payment gateways (e.g. Mpesa).
- **API Documentation**:Swagger UI for endpoint documentation.

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- pip (Python package manager)
- Virtual environment tool (`venv` or `virtualenv`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Kigo-P/fashionyuva_backend.git
   cd FASHIONYUVA_BACKEND

    Create and activate a virtual environment:
   ```

python3 -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`

Install the dependencies:

    pip install -r requirements.txt

Running the Server

    Set up environment variables (see Environment Variables).

    Run the development server:

    flask run

    The server will be available at http://127.0.0.1:5555.

API Endpoints

Here is a brief overview of key API endpoints:
Authentication

    POST /api/register: Register a new user.
    POST /api/login: User login.

Products

    GET /api/products: Fetch all products.
    GET /api/products/<id>: Fetch details of a specific product.

Orders

    POST /api/orders: Create a new order.
    GET /api/orders/<id>: Fetch details of a specific order.

Payments

    POST /api/payments: Process a payment.

Detailed API documentation is available here (link to Swagger UI documentation).
Environment Variables

The backend uses environment variables to configure sensitive settings. Create a .env file in the project root and add the following:

ENV='production'
SECRET_KEY='dfghxcbnjdfkscndbjkfnh'

POSTGRES_USERNAME='dennis'
POSTGRES_PASSWORD='dennis'
POSTGRES_URL = 'postgresql://dennis:TTOszQYBlz7ljFPdZhQtlFvd3PucGvwi@dpg-cso8dj8gph6c73bo21vg-a.oregon-postgres.render.com/fashionyuva'

Replace placeholders with actual values.
Contributing

We welcome contributions to improve the backend! To contribute:

    Fork the repository.
    Create a feature branch (git checkout -b feature-name).
    Commit your changes (git commit -m "Add feature").
    Push to the branch (git push origin feature-name).
    Open a Pull Request.

License

This project is licensed under the MIT License. See the LICENSE file for details.
Contact

For any questions or feedback, please contact us at support@fashionyuva.com.

Thank you for contributing to Fashionyuva!

You can adjust the placeholders (e.g., repository URL, email, and payment gateway)

HAPPY CODING!!
