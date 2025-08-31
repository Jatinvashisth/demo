FROM python:3.12-slim as build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Optionally, run tests or build steps here

# Stage 2: Final lightweight image
FROM python:3.12-slim
WORKDIR /app

# Copy only installed packages and app code from build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /app /app

# Expose port
EXPOSE 8000

# Start FastAPI server
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
