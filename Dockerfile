# Use a base image that includes Python
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to the container
COPY listener.py .

# Set the command to run the Python script
CMD ["python", "listener.py"]
