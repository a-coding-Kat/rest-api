# Use python 3.8
FROM python:3.8-slim

# Create directory for project.
WORKDIR /app

# Copy root folder to container /app folder.
COPY . .

# Add our code to the Python path.
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Install the dependencies.
RUN pip install -r requirements.txt

# Create database and import data.
RUN python import_data.py

# Set python as the default program to execute in the container.
ENTRYPOINT [ "python" ]

# Our server is the default module.
CMD [ "wdb_rest/server.py" ]

# Expose port 5000 to other containers.
EXPOSE 5000
