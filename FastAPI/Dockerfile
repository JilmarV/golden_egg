FROM python:3.9-slim
# Uses a lightweight Python 3.9 base image (slim = fewer dependencies).

WORKDIR /app
# Sets the working directory inside the container to "/app".
# All subsequent instructions will run from this location.

ENV PYTHONPATH=/app

COPY requirements.txt .
# Copies the dependency file from your local machine to the container.
# This allows Docker to cache dependencies and speed up rebuilds.

RUN pip install --no-cache-dir -r requirements.txt
# Installs the dependencies listed in requirements.txt.
# The --no-cache-dir flag avoids caching to reduce image size.

COPY . .
# Copies the entire project from the build context to the container's /app directory.

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
# Default command when the container starts.
# Runs the FastAPI application with Gunicorn using:
# - 4 worker processes
# - Uvicorn as the ASGI worker class
# - Binds the server to all interfaces on port 8000.
