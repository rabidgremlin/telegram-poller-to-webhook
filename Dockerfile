FROM python:3.12-slim-bullseye

WORKDIR /app

# Copy requirements file if you have one
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main script
COPY main.py ./

ENV DATA_FOLDER=/tptw_data

# Set the command to run when the container starts
CMD ["python", "main.py"]