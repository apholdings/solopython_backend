FROM python:3.9

# Install SSH client
RUN apt-get update && apt-get install -y openssh-client

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# RUN echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

# Start the SSH tunnel to Serveo
CMD python manage.py runserver 0.0.0.0:8000
# CMD ssh -R 80:localhost:8000 serveo.net && python manage.py runserver 0.0.0.0:8000