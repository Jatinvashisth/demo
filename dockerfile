# 1. Python base image
FROM python:3.12-slim

# 2. Container ke andar working directory
WORKDIR /app

# 3. Dependencies install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Application code copy
COPY . .

# 5. Expose port
EXPOSE 8000

# 6. Start FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]