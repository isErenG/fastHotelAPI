
# FastHotelAPI

FastHotelAPI is a sample project built using [FastAPI](https://fastapi.tiangolo.com/) to explore REST API development with Python. This API provides endpoints for managing hotels, users, and reviews. It features role-based access for admin users and uses JWT for authentication.

## Project Structure

The project is organized as follows:

- **app/**: Contains the main application code.
  - **data/**: Handles database connections and repositories.
    - **repository/**: Contains the repository classes for CRUD operations on `hotels`, `users`, and `reviews`.
  - **di/**: Dependency injection for repositories, enabling easy management of dependencies in FastAPI routes.
  - **middleware/**: Contains middleware classes such as:
    - `AdminOnlyMiddleware` for access control on admin routes.
    - `LoggingMiddleware` for logging incoming requests and response times.
  - **models/**: Defines the data models for `Admin`, `User`, `Hotel`, and `Review`, along with abstract repository interfaces.
  - **routers/**: Contains route definitions for different resources, organized by feature:
    - **admin/**: Routes restricted to admin users.
    - **users/**: Routes accessible by regular users.
  - **schemas/**: Contains request and response schemas for API validation and serialization.
  - **utils/**: Utility functions for tasks like JWT token generation and password hashing.
  - **main.py**: The application entry point, setting up FastAPI and adding middleware and routers.

## Features

- **Role-Based Access**: Admin-only routes for managing users and sensitive data.
- **JWT Authentication**: Securely manages sessions for both users and admins.
- **Hotels Management**: Add, view, and delete hotels.
- **User Management**: Retrieve, create, and delete users.
- **Review Management**: Manage reviews associated with hotels.

## Prerequisites

- **Docker**: Everything is run entirely in a docker container, no further installation required.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/isErenG/FastHotelAPI.git
   ```

2. **Configure Environment Variables**

   Fill in the `.env` file with your PostgreSQL credentials. An example file `.envexample` is provided. Copy it to create your own `.env` file:

   ```bash
   cp .envexample .env
   ```

   Edit `.env` to include the necessary credentials:

   ```env
   POSTGRES_DATABASE=your_database_name
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```

3. **Launch with Docker**

   ```bash
   cd deploy/
   docker compose --env-file ../.env up -d --build 
   ```

   If you wish to close the docker compose

   ```bash
   docker compose --env-file ../.env down
   ```
