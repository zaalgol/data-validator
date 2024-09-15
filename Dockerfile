# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY src/ ./src/
COPY documents/ ./documents/

# Create the logs directory
RUN mkdir -p /app/logs


# Expose port if necessary (though not needed for a command-line app)
# EXPOSE 8000

# Set environment variables, if any
# For example, you might set the MongoDB URI via an environment variable
# ENV MONGODB_URI=mongodb://mongo:27017/

# Set the command to run the application
CMD ["python", "src/main.py"]
