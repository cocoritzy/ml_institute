# Step 1: Use Python base image
FROM python:3.12-slim

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy the application files into the container
COPY . /app/

# Step 4: Copy model.pth into the container
COPY model.pth /app/model.pth

# Step 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Expose the port FastAPI will run on
EXPOSE 8000

# Step 7: Define the command to run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

