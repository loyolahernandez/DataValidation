# Use the official Python image from the Docker Hub as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define the environment variable to prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Run the application when the container launches
CMD ["python", "run.py"]
