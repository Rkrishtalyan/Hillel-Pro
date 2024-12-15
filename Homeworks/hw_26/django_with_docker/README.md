# Django in Docker

This project demonstrates how to **run a simple Django application** inside a **Docker container** using Docker Compose. It provides a minimal example of setting up Django for development in a containerized environment.

## Table of Contents

- [Description](#description)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Description

This project includes:
- A **Django application** with a simple home page.
- A `Dockerfile` to containerize the Django app.
- A `docker-compose.yml` file to run the application with Docker Compose.

The app listens on port **8001** and renders a basic HTML template to confirm that Django is running in Docker.

## Prerequisites

Ensure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <https://github.com/Rkrishtalyan/Hillel-Pro/tree/main/Homeworks/hw_26/django_with_docker>
   cd django_with_docker
   ```

2. **Prepare the `requirements.txt`:**

   Ensure it contains the following dependency:
   ```
   Django==5.1.0
   ```

3. **Build and Start the Docker Container:**

   Run the following command to build the Docker image and start the container:
   
   ```bash
   docker-compose up --build
   ```

   The `--build` flag ensures the container rebuilds with any new changes.

## Usage

Once the container is running, access the Django application at:

```
http://localhost:8001
```

You should see a page displaying:

```
Django in Docker is working!
```

### Stopping the Application

To stop the containers, press `Ctrl+C` or run:

```bash
docker-compose down
```

### Clean Up

To remove unused Docker images and containers:

```bash
docker system prune
```

## Project Structure

```
django_with_docker/
|
|-- app/
|   |-- migrations/
|   |-- __init__.py       # Package initialization
|   |-- admin.py          # Django admin
|   |-- apps.py           # Application configuration
|   |-- models.py         # Data models
|   |-- tests.py          # Unit tests
|   |-- views.py          # View functions
|
|-- django_with_docker/
|   |-- __init__.py       # Project initialization
|   |-- asgi.py           # ASGI config
|   |-- settings.py       # Project settings
|   |-- urls.py           # URL routing
|   |-- wsgi.py           # WSGI config
|
|-- templates/
|   |-- app/
|       |-- home.html     # HTML template
|
|-- .dockerignore         # Files ignored by Docker
|-- db.sqlite3            # SQLite database
|-- docker-compose.yml    # Docker Compose configuration
|-- Dockerfile            # Docker build file
|-- manage.py             # Django CLI utility
|-- requirements.txt      # Project dependencies
```

## Configuration

### `Dockerfile`

Defines the Docker image for the Django application:

```dockerfile
FROM python:3.10-slim

WORKDIR /django_app

COPY requirements.txt /django_app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /django_app/

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
```

### `docker-compose.yml`

Simplifies service management with Docker Compose:

```yaml
version: "3.8"
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8001:8001"
    volumes:
      - .:/django_app
    command: python manage.py runserver 0.0.0.0:8001
```

### `.dockerignore`

Specifies files to exclude from the Docker image:

```
__pycache__/
*.pyc
.git
.env
Dockerfile
docker-compose.yml
*.log
```

## Troubleshooting

- **Port Conflict:** If port `8001` is in use, change it in `docker-compose.yml`:
  ```yaml
  ports:
    - "<new-port>:8001"
  ```
- **Build Errors:** Ensure the `requirements.txt` file is correct and contains valid dependencies.

## Contributing

Contributions are welcome! Fork this repository and submit a pull request with enhancements or bug fixes.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

Enjoy running Django in Docker! 🚀
