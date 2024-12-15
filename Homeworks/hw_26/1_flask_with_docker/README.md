# Flask in Docker

This project demonstrates how to **run a simple Flask application** inside a **Docker container** using Docker Compose.
This guide is intended for developers and users who want to quickly set up and run the application in a containerized environment.

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

This project is a **Flask-based web application** that runs inside a Docker container. It includes:
- A Flask server that returns a simple message.
- A `Dockerfile` to define the application environment.
- A `docker-compose.yml` file to simplify container orchestration.

The Flask application listens on port `5001` and can be accessed via `http://localhost:5001`.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Rkrishtalyan/Hillel-Pro/tree/main/Homeworks/hw_26
   cd 1_flask_with_docker
   ```

2. **Install Flask Dependencies:**
   Ensure `requirements.txt` has the necessary Flask dependency:
   ```
   Flask==3.0.0
   ```

3. **Build and Start the Docker Container:**

   Use Docker Compose to build the image and start the service:

   ```bash
   docker-compose up --build
   ```

   The `--build` flag ensures Docker builds the image with the latest changes.

## Usage

Once the container is running, you can access the Flask application at:

```
http://localhost:5001
```

You should see the message:

```
Flask in Docker is working!
```

### Stopping the Application

To stop the running containers, use:

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
1_flask_with_docker/
|
|-- app/
|   |-- flask_app.py      # Main Flask application
|
|-- .dockerignore         # Files ignored by Docker
|-- docker-compose.yml    # Docker Compose configuration
|-- Dockerfile            # Docker build file
|-- README.md             # Project documentation
|-- requirements.txt      # Python dependencies
```

## Configuration

### `docker-compose.yml`

Defines the service configuration for Docker Compose:

```yaml
version: "3.8"
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5001:5001"
    volumes:
      - ./app:/flask_app
    command: python flask_app.py
```

### `Dockerfile`

Specifies how to build the Flask app image:

```dockerfile
FROM python:3.10-slim

WORKDIR /flask_app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app/ .

CMD ["python", "flask_app.py"]
```

## Troubleshooting

- **Port Conflict:** If port `5001` is already in use, change it in `docker-compose.yml`:
  ```yaml
  ports:
    - "<new-port>:5001"
  ```
- **Build Errors:** Ensure `requirements.txt` and `Dockerfile` are correctly formatted.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request with improvements or fixes.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

Enjoy running Flask in Docker! 🚀
