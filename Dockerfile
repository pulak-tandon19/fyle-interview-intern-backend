FROM python:3.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project files
COPY . /code/

# Ensure the bash script has executable permissions
RUN chmod +x /code/run.sh

# Expose the port the app runs on
EXPOSE 5000

# Run the bash script
CMD ["/code/run.sh"]
