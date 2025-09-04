# Cafe Billing and Management System

This is a web-based Cafe Billing and Management System built with Django and MySQL. It allows cafe staff to manage orders, items, categories, payments, and generate reports efficiently through a user-friendly interface.

## Features
- User authentication (login/logout)
- Manage menu items and categories
- Place and manage customer orders
- Payment type selection and order tracking
- Maintenance mode for system updates
- Generate sales and order reports

## Folder Structure
```
CafeBillingAndManagementSystem-main/
├── manage.py
├── Cafe/                # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── ROBO/                # Main app with models, views, templates, static files
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   └── static/
└── README.md
```

## Prerequisites
- Python 3.x
- Django 3.x or above
- MySQL

## Setup Instructions
1. **Clone the repository:**
	```bash
	git clone https://github.com/yashdeep94/CafeBillingAndManagementSystem
	cd CafeBillingAndManagementSystem-main
	```
2. **Create and activate a virtual environment (optional but recommended):**
	```bash
	python -m venv venv
	venv\Scripts\activate  # On Windows
	# source venv/bin/activate  # On Linux/Mac
	```
3. **Install dependencies:**
	```bash
	pip install django mysqlclient
	```
4. **Configure MySQL database:**
	- Create a MySQL database and user.
	- Update `Cafe/settings.py` with your database credentials.
5. **Apply migrations:**
	```bash
	python manage.py makemigrations
	python manage.py migrate
	```
6. **Create a superuser (admin):**
	```bash
	python manage.py createsuperuser
	```
7. **Run the development server:**
	```bash
	python manage.py runserver
	```
8. **Access the app:**
	- Open your browser and go to `http://127.0.0.1:8000/`

## Usage
- Log in with your credentials.
- Add or edit menu items and categories.
- Place new orders and manage existing ones.
- View reports from the reports section.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
