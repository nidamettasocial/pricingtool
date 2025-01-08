# FastAPI Application
## Features

- **FastAPI Framework** for creating API endpoints.
- **Automatic Interactive API Docs** powered by Swagger UI and ReDoc.
- **CRUD Operations** for a simple resource (e.g., user, item).
- **JWT Authentication** to secure endpoints.
- **Request Validation** using Pydantic models.
- **Database Integration** with  PostgreSQL .
- **Background Tasks** to handle long-running tasks asynchronously.

## Installation

### Prerequisites

- Python 3.12.3
- pip package manager

##  Set up a virtual environment  ( Development done using mac)

python3 -m venv env
source env/bin/activate  

# On Windows, use `venv\Scripts\activate`

# Install Depenedencies

pip install -r requirements.txt

# Set up environment variables


# Have used SQL Achemy for model migration 
Run database migrations to set up your schema with alembic :

 alembic  stamp head 
 alembic revision --autogenerate 
 alembic upgrade head


# Running the application

1. Set up python path 
 Mac - export PYTHONPATH=$PWD

2. Navigate to app folder
  cd app

3. Run the server 

  uvicorn main:app --reload

# Accessing the API Docs
 
Swagger UI: Go to http://127.0.0.1:8000/docs to interact with the API through Swagger UI.
ReDoc: Go to http://127.0.0.1:8000/redoc for an alternative view of the API documentation.


# Testing the Endpoints:

You can test the API using the interactive docs

# Project Structure

# Authentication
 using JWT

 
