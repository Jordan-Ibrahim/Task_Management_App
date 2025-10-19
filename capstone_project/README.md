** DOCUMENTATION FOR THE TASK MANAGEMENT APP **

# Task Management API

A Django REST Framework–based API that allows users to efficiently manage their daily tasks.  
Each user can create, view, update, and delete their own tasks — with features like authentication, due-date validation, task filtering, and completion tracking.


# Description

The Task Management API is designed to help users organize their to-dos and priorities seamlessly.  
It provides secure user management and ensures each user can only access their own tasks.

Key highlights:
User authentication and ownership isolation
Full CRUD operations for tasks
Marking tasks as complete or incomplete
Filtering and sorting by priority, due date, or status

---

# Features

User registration, login, and authentication  
CRUD for tasks (Create, Read, Update, Delete)  
Priority levels (Low, Medium, High)  
Task status management (Pending, Completed)  
Validation for due dates (must be in the future)  
Filtering and sorting by due date or priority  
Timestamp when a task is completed  
Secure API endpoints using Django REST Framework  

---
# Project Structure

Task_management_project/
│
├── Task_management_app/
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── urls.py
│ ├── admin.py
│ └── tests.py
│
├── Task_management_project/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
│
├── manage.py
└── README.md

# GitHub Repository
https://github.com/yourusername/Task_Management_App.git

#API Endpoints

| Method | Endpoint                        | Description                   |

| POST   | `/api/users/register/`          | Register a new user           |
| POST   | `/api/users/login/`             | Authenticate and obtain token |
| GET    | `/api/tasks/`                   | List all user tasks           |
| POST   | `/api/tasks/`                   | Create a new task             |
| GET    | `/api/tasks/<id>/`              | Retrieve a specific task      |
| PUT    | `/api/tasks/<id>/`              | Update an existing task       |
| DELETE | `/api/tasks/<id>/`              | Delete a task                 |
| POST   | `/api/tasks/<id>/complete/`     | Mark task as complete         |
| POST   | `/api/tasks/<id>/incomplete/`   | Revert task to incomplete     |
| GET    | `/api/tasks/?status=completed`  | Filter tasks by status        |
| GET    | `/api/tasks/?priority=high`     | Filter by priority            |
| GET    | `/api/tasks/?ordering=due_date` | Sort by due date              |
