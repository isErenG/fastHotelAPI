
# FastHotelAPI

FastHotelAPI is a project built using [FastAPI](https://fastapi.tiangolo.com/) to explore REST API development with Python. It is designed to manage hotels, users, and reviews efficiently while utilizing role-based access control and secure JWT-based authentication.

---

## Key Features

### **Role-Based Access Control**
- Admin-only routes for managing users and sensitive data.
- Regular user routes for managing reviews and accessing hotel data.

### **Secure Authentication**
- Implements JWT for authentication and authorization.
- Supports both admin and user tokens with role distinction.

### **Hotel Management**
- Create, retrieve, and list all hotels.
- Ensures scalability with proper repository and service separation.

### **User Management**
- Admins can manage users, including retrieving, updating, and deleting accounts.
- User registration and login are supported with secure password hashing.

### **Review Management**
- Users can post, retrieve, and delete reviews for hotels.
- Reviews are tied to hotels and users, ensuring a relational structure.

---

## Architecture

### **1. Modular Design**
The application is divided into layers:
- **Routers:** Define API endpoints and handle HTTP requests and responses.
- **Services:** Contain business logic, ensuring separation from data access logic.
- **Repositories:** Handle database interactions, ensuring the persistence layer is isolated from the business logic.

### **2. Dependency Injection**
- Dependencies like repositories are injected using FastAPI's `Depends`, allowing for easier testing and modularity.

### **3. Middleware**
- **LoggingMiddleware:** Logs all incoming requests, response times, and errors.
- **AdminOnlyMiddleware:** Restricts access to admin routes, ensuring enhanced security.

### **4. Database Layer**
- PostgreSQL is used as the database backend.
- Repositories directly interact with the database, abstracting SQL queries and handling schema mappings.

### **5. Security**
- Secure password hashing using `bcrypt`.
- Expirable JWT tokens for session management, with separate keys for access and refresh tokens.

---

## Areas of Improvement

- **Admin Token Issues**: Admin tokens can access user endpoints, which sometimes results in errors. This happens because certain endpoints rely on `user_id` as a foreign key. When using an admin token, the ID belongs to the `admins` table instead of the `users` table, causing mismatches.
- **Logging**: Logging could be improved. I'm not entirely sure if I'm doing it correctly or placing it in the right spots.
- **Admin Dependencies**: The file `util/admin_dependencies.py` feels out of place. I’m not sure where it should go, but I’d prefer to restructure and move it elsewhere.
- **Refresh Tokens**: I still need to implement functioning refresh tokens.
- **Exception Handlers**: The file `middleware/exception_handlers.py` doesn’t feel like typical middleware. Its current location makes some sense, but I’m not entirely satisfied with it.
- **Repository Exceptions**: I might need to move exceptions to the repository classes instead of handling them entirely in the service layer. I like the current cleanliness of the code, but I’m not sure if this is the best approach.

---

## Deployment
- Fully containerized using Docker, ensuring consistent environments across development and production.
- `.env` configuration allows easy setup and deployment flexibility.

---

## Setup

Refer to the instructions below for launching the application.

---

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
