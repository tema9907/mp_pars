# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Make the start.sh script executable
RUN chmod +x start.sh

# Run start.sh when the container launches
CMD ["./start.sh"]