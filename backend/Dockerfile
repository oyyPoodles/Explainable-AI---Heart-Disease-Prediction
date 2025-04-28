FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better cache usage
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY backend/ .

# Copy data and trained model
COPY data/ ./data/
COPY backend/model/ ./model/

# Expose the port for the API
EXPOSE 8000

# Command to run the API server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]