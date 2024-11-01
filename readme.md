# FastHotelAPI

A small project to learn and experiment with the [FastAPI](https://fastapi.tiangolo.com/) Python library. This API
provides endpoints for managing user reviews for hotels.

## Features

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

   Fill in the `.env` file with your PostgreSQL credentials. An example file `.envexample` is provided. Copy it to
   create your own `.env` file:

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

3. Launch with docker
   ```bash
   cd deploy/
   docker compose --env-file ../.env up -d --build 
   ```

   If you wish to close the docker compose
   ```bash
   docker compose --env-file ../.env down
   ```
