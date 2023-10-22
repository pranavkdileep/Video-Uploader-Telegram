# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install gunicorn
RUN apt update && apt install ffmpeg -y
# Expose port 7860 for the Flask app
EXPOSE 7860

# Run app.py when the container launches
CMD ["gunicorn", "-c", "gunicorn_config.py", "main_safe_flask:app"]
