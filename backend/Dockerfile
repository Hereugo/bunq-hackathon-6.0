FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt \
    && pip3 install --no-cache-dir uvicorn

ENV PYTHONUNBUFFERED=1 
ENV PYTHONDONTWRITEBYTECODE=1

COPY . . 

# For development with hot reload, we use uvicorn directly
# The command will be overridden in docker-compose for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
