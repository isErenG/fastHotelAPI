# FastHotelAPI

A small project to learn and experiment with the [FastAPI](https://fastapi.tiangolo.com/) Python library. This API provides endpoints for managing user reviews for hotels.

## Features

- **Hotels Management**: Add, view, and delete hotels.
- **User Management**: Retrieve, create, and delete users.
- **Review Management**: Manage reviews associated with hotels.

## Prerequisites

- **Python 3.8+**
- **PostgreSQL**: Ensure PostgreSQL is installed and accessible on your machine.
- **Docker (optional)**: You can run PostgreSQL in a Docker container if preferred.

## Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/FastHotelAPI.git
   cd FastHotelAPI
   ```

2. **Create and Activate a Virtual Environment**

   It’s recommended to create a virtual environment to keep dependencies isolated.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   Install the required dependencies from `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL**

   If you have PostgreSQL installed locally, create a new database for this project. You can also use Docker to launch PostgreSQL with a simple command.

   ```bash
   docker run --name container_name -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
   ```
5. **Run startup script**

    Run the startup script located at `/deploy`. If you are using docker, you can run the following commands below.
    
    ```bash
    docker cp deploy/database_scripts.sql container_name:/setup.sql
    docker exec -it container_name psql -U postgres -d your_database_name -f /setup.sql
   ```


6. **Configure Environment Variables**

   Fill in the `.env` file with your PostgreSQL credentials. An example file `.envexample` is provided. Copy it to create your own `.env` file:

   ```bash
   cp .envexample .env
   ```

   Edit `.env` to include the necessary credentials:

   ```env
   POSTGRES_DATABASE=your_database_name
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_HOST=localhost  # Or use the container name if using Docker, e.g., "hotelreviews"
   POSTGRES_PORT=5432
   ```