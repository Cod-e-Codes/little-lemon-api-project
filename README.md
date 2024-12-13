# Little Lemon API Project

This repository contains the backend API for the Little Lemon restaurant. The API is built using Django and Django REST Framework (DRF) and provides endpoints for customers, managers, and delivery crew to manage restaurant operations efficiently.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [Authentication Endpoints](#authentication-endpoints)
  - [Menu Endpoints](#menu-endpoints)
  - [Cart Endpoints](#cart-endpoints)
  - [Order Endpoints](#order-endpoints)
- [Throttling](#throttling)
- [Pagination](#pagination)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Authentication**
  - Token-based authentication using Djoser.
  - User roles: customers, managers, and delivery crew.
- **Menu Management**
  - CRUD operations for menu items and categories.
  - Filtering, searching, and ordering by price and title.
- **Cart Management**
  - Add, view, and delete items in the cart.
- **Order Management**
  - Place orders from the cart.
  - Assign delivery crew to orders.
  - Delivery crew can update order status to "delivered."
- **Throttling and Pagination**
  - Throttle API requests based on user roles.
  - Paginate large data sets for better performance.

## Technologies Used
- **Backend**: Django, Django REST Framework
- **Authentication**: Djoser
- **Database**: SQLite (default setup for development)
- **Python Version**: 3.9+

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Cod-e-Codes/little-lemon-api-project.git
   ```
2. Navigate to the project directory:
   ```bash
   cd little-lemon-api-project
   ```
3. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure
```
.
├── LittleLemon           # Main project directory
├── LittleLemonAPI        # API app directory
├── db.sqlite3            # SQLite database file
├── requirements.txt      # Python dependencies
└── manage.py             # Django management script
```

## API Endpoints
### Authentication Endpoints
| Endpoint               | Method | Description                             |
|------------------------|--------|-----------------------------------------|
| `/auth/users/`         | POST   | Register a new user                     |
| `/auth/token/login/`   | POST   | Login and obtain an access token        |
| `/auth/users/me/`      | GET    | Get the details of the logged-in user   |

### Menu Endpoints
| Endpoint                  | Method   | Description                              |
|---------------------------|----------|------------------------------------------|
| `/api/categories/`        | GET, POST | List or create categories                |
| `/api/menu-items/`        | GET, POST | List or create menu items                |
| `/api/menu-items/<id>/`   | GET, PUT, PATCH, DELETE | Manage individual menu items   |

### Cart Endpoints
| Endpoint         | Method   | Description                              |
|------------------|----------|------------------------------------------|
| `/api/cart/`     | GET, POST | View or add items to the cart            |

### Order Endpoints
| Endpoint                 | Method   | Description                              |
|--------------------------|----------|------------------------------------------|
| `/api/orders/`           | GET, POST | View or create orders                    |
| `/api/delivery-orders/`  | GET      | View orders assigned to delivery crew    |

## Throttling
- Authenticated users: **5 requests per minute**.
- Anonymous users: **2 requests per minute**.

## Pagination
- Default page size: **5 items per page**.
- Enabled for menu items and orders.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

