# Pull base image
FROM python:3.10.1

# Set environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /uzamazon

# Install dependencies
COPY requirements.txt /uzamazon/
RUN pip install -r requirements.txt

# Copy project
COPY . /uzamazon/
