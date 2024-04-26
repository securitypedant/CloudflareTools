# Use the official Python image as a base
FROM python:3.12.2-alpine3.19

# Set environment variables
ENV FLASK_APP=cftools.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create and set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Flask app files to the container
COPY . .

# Create the default files
RUN echo '{ "ddns-sync": { "status": false, "sync_period": 360 } }' > config.json

# Expose the Flask port
EXPOSE 8000

# Command to run the Flask app
CMD ["flask", "run"]