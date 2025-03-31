# Step 1: Use Python 3.12 slim base image
FROM python:3.12-slim

# Step 2: Install PostgreSQL client and other dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev && apt-get clean

# Step 3: Set working directory
WORKDIR /app

# Step 4: Copy the application files into the container
COPY . /app/

# Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Expose the port Streamlit will run on
EXPOSE 8501

# Step 7: Define the command to run the Streamlit app
CMD ["streamlit", "run", "streamlit.py"]
