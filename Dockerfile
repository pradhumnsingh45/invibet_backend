# Use an official Python runtime as the base image
FROM python:3.9


RUN ls -l /usr/local/bin/python

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the project files into the container
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /usr/src/app/requirements.txt

# Copy the rest of the project files into the container
COPY . /usr/src/app

# Expose port if needed
EXPOSE 8004

# Define the command to run your application
CMD ["python", "app.py"]