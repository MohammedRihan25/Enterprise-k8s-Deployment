# 1. Base Image: Lightweight official Python 3.12 on Debian Linux
FROM python:3.12-slim

# 2. Set environment variables so Python prints logs immediately and doesn't write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# 3. Create and set the working directory inside the container
WORKDIR /app

# 4. Copy ONLY requirements.txt first to leverage Docker layer caching
COPY app/requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application source code
COPY app/ .

# 7. Document that the container listens on port 5000
EXPOSE 5000

# 8. Start the production server using Gunicorn (2 worker processes)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "main:app"]
