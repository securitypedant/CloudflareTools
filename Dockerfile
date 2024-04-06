# Use the official Python image as a base
FROM python:3.12.2-alpine3.19

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc

# Create and set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Flask app files to the container
COPY . .

# Expose the Flask port
EXPOSE 5000

# Command to run the Flask app
CMD ["flask", "run"]