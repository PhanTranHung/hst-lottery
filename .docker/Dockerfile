FROM python:3.9-slim

# Set working directory
WORKDIR /app

ENV APP_DIR=../backend/crawl_lottery

# Copy requirements file and install dependencies
COPY $APP_DIR/requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY $APP_DIR .

# Expose the port the app will run on
EXPOSE 8801

# Command to run the application
CMD ["python", "app.py"]
