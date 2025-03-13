# Base environment with Python + deps

    FROM python:3.9-slim AS base

    WORKDIR /app
    
    # Copy requirements and install them
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copy your Flask app and static folder
    COPY app.py .
    COPY static ./static
    
    
    # FRONTEND (serves static files on port 8080)
   
    FROM base AS frontend
    
    # Change to the 'static' subdirectory so that
    # login.html and signup.html are served at the root
    WORKDIR /app/static
    
    EXPOSE 8080
    CMD ["python", "-m", "http.server", "8080"]
    
   
    # STAGE 3: BACKEND (runs the Flask app on port 5000)
    
    FROM base AS backend
    
    EXPOSE 5000
    CMD ["python", "app.py"]
    