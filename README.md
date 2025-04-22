# Task Management System

This is a FastAPI-based application for managing tasks, designed to meet the requirements of creating, retrieving, updating, and deleting tasks with PostgreSQL as the backend database. It includes a health-check endpoint and is ready for architectural scaling as outlined in the `architecture_design.md`.

## Prerequisites

- **Python 3.12+**
- **PostgreSQL** (installed locally or via Docker)
- **Virtual Environment** (optional but recommended)
- **Git** (for version control)
- **VS Code** (or any code editor)
- **Postman** (for API testing)

## Installation

Here i run every commands on bash

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/spandey6395/fastapi-task-app.git
   cd task-management

   ```

2. **Set Up Virtual Environment (optional)**:

```bash
python -m venv venv

source venv/Scripts/activate # On Windows

```

3. **Install Dependencies**:

```bash
pip install -r requirements.txt

```

4. Configure Environment:
   Create a .env file in the root directory with the following content:

```bash
DATABASE_URL=postgresql://postgres:yourpass@localhost:5432/your_db_name

```

5. **Apply Databse migrations**:

   ```bash
   alembic upgrade head

   ```

Running the Application

1. Start the Server:

```bash
   uvicorn app.main:app --reload
```

The app will be available at http://127.0.0.1:8000.

2. Test the APIs (using Postman):

Health Check: GET http://localhost:8000/health (expect {"status": "Database connection OK"})

Create Task: POST http://localhost:8000/tasks with body {"title": "Test Task", "description": "A sample task", "status": "pending"}

Get Tasks: GET http://localhost:8000/tasks?skip=0&limit=10

Update Task: PUT http://localhost:8000/tasks/{task_id} with body {"title": "Updated Test Task", "status": "in-progress"}

Delete Task: DELETE http://localhost:8000/tasks/{task_id}

Project Structure

app/: Contains FastAPI routes, models, schemas, and CRUD logic.

alembic/: Migration scripts for database schema changes.

.env: Environment variables for database connection.

requirements.txt: Python dependencies.

architecture_design.md: Architecture design document for Part 2.

README.md: This file.

Architecture Design

For detailed architecture design (Part 2), refer to architecture_design.md, which covers database design, API scalability, authentication setup, caching, message queuing, and a text-based diagram.
