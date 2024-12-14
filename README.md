# Little Lemon Project

This project is a RESTful API developed using Django, Django Rest Framework (DRF), and Djoser for Little Lemon, a restaurant management system. It supports user authentication, role-based permissions, and features for managing menu items, categories, carts, and orders. The project is designed to handle interactions between administrators, managers, delivery crew, and customers.

---

## Table of Contents

1. [Repository](#repository)
2. [Features](#features)
   - [Authentication](#authentication)
   - [Admin Features](#admin-features)
   - [Manager Features](#manager-features)
   - [Delivery Crew Features](#delivery-crew-features)
   - [Customer Features](#customer-features)
3. [Installation and Setup](#installation-and-setup)
4. [Users and Credentials](#users-and-credentials)
5. [API Endpoints](#api-endpoints)
   - [Authentication](#authentication)
   - [Categories](#categories)
   - [Menu Items](#menu-items)
   - [Cart](#cart)
   - [Orders](#orders)
   - [User Group Management](#user-group-management)
6. [Testing](#testing)
7. [Deployment Notes](#deployment-notes)
8. [Submission Guidelines](#submission-guidelines)
9. [License](#license)
10. [Contact](#contact)

---

## Repository
[Little Lemon Project on GitHub](https://github.com/Cod-e-Codes/littlelemon)

---

## Features

### Authentication
- Token-based authentication with Djoser.
- Role-based permissions for Admin, Manager, Delivery Crew, and Customer.

### Admin Features
1. Assign users to the `Manager` or `Delivery Crew` groups.
2. Add menu items and categories.

### Manager Features
1. Update menu items of the day.
2. Assign users to the `Delivery Crew` group.
3. Assign orders to the delivery crew.

### Delivery Crew Features
1. View orders assigned to them.
2. Mark orders as delivered.

### Customer Features
1. Register and log in to the system.
2. Browse menu items and categories.
3. Add items to their cart.
4. Place orders.
5. View their own orders.

---

## Installation and Setup

### Prerequisites
- Python 3.10+
- Pipenv (for virtual environment and dependency management)
- SQLite (default database)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Cod-e-Codes/littlelemon.git
   cd littlelemon
   ```

2. **Set Up the Virtual Environment**
   ```bash
   pipenv install --dev
   pipenv shell
   ```

3. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Access the API**
   - Base URL: `http://localhost:8000/api/`

---

## Users and Credentials

### Superuser
- **Username**: admin
- **Password**: littlelemon2024

### Test Users
1. **Manager**
   - Username: manager
   - Password: managerpass
2. **Delivery Crew**
   - Username: delivery
   - Password: deliverypass
3. **Customer**
   - Username: customer
   - Password: customerpass

---

## API Endpoints

### Authentication
| Method | Endpoint                 | Description                      |
|--------|--------------------------|----------------------------------|
| POST   | `/api/token/login/`      | Obtain authentication token.    |
| POST   | `/api/token/logout/`     | Revoke authentication token.    |

### Categories
| Method | Endpoint                 | Description                             |
|--------|--------------------------|-----------------------------------------|
| GET    | `/api/categories/`       | List all categories.                   |
| POST   | `/api/categories/`       | Create a new category (Admin/Manager). |

### Menu Items
| Method | Endpoint                 | Description                             |
|--------|--------------------------|-----------------------------------------|
| GET    | `/api/menu-items/`       | List all menu items.                   |
| POST   | `/api/menu-items/`       | Add a new menu item (Admin/Manager).   |

### Cart
| Method | Endpoint                 | Description                      |
|--------|--------------------------|----------------------------------|
| GET    | `/api/cart/`             | View cart items.                |
| POST   | `/api/cart/`             | Add an item to the cart.        |
| DELETE | `/api/cart/`             | Clear the cart.                 |

### Orders
| Method | Endpoint                         | Description                              |
|--------|----------------------------------|------------------------------------------|
| GET    | `/api/orders/`                   | View orders (filtered by role).          |
| POST   | `/api/orders/`                   | Place a new order (Customer only).       |
| PATCH  | `/api/orders/<id>/deliver/`      | Mark an order as delivered (Delivery).   |

### User Group Management
| Method | Endpoint                                | Description                             |
|--------|----------------------------------------|-----------------------------------------|
| GET    | `/api/groups/manager/users/`           | List all managers.                     |
| POST   | `/api/groups/manager/users/`           | Add a user to the `Manager` group.     |
| GET    | `/api/groups/delivery-crew/users/`     | List all delivery crew members.        |
| POST   | `/api/groups/delivery-crew/users/`     | Add a user to the `Delivery Crew`.     |

---

## Testing

### Run Unit Tests
```bash
python manage.py test
```

---

## Deployment Notes
1. Set `DEBUG = False` in `settings.py` before deployment.
2. Add appropriate `ALLOWED_HOSTS` for production.
3. Use environment variables to secure sensitive data like `SECRET_KEY`.

---

## Submission Guidelines
1. Include the `db.sqlite3` file.
2. Provide the `notes.txt` file with all user credentials.
3. Zip the project directory and submit it.

---

## License
This project is for educational purposes and does not have a specific license. Contact the author for permissions and inquiries.

---

## Contact
For any questions or support, contact:
- **Cody Marsengill**
- Email: contact@cod-e-codes.com
- GitHub: [Cod-e-Codes](https://github.com/Cod-e-Codes)
