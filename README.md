# MNIST Digit Recognition Web App

Access the app on: [http://37.27.211.254:8502/](http://37.27.211.254:8502/)

## Project Overview

This project builds an end-to-end MNIST digit recognition app using PyTorch, PostgreSQL, Docker, and Streamlit. The app is deployed on a self-managed server.

### Features:
- **ML Model**: Trains a CNN using the MNIST dataset.
  - Loading and preprocessing the MNIST dataset
  - Designing and building a CNN model architecture
  - Training the model on the training data
  - Evaluating the model's performance on the test data
  - Saving and loading the trained model
- **Frontend**: Built with Streamlit for interactive user input.
- **Logging**: Uses PostgreSQL for storing predictions.
- **Containerization**: Docker is used to containerize the app, the ML model and PostgreSQL.
- **Deployment**: The app is deployed on a server.

### **Project Structure**  

```plaintext
app_ml/
├── docker-compose.yml          # Multi-container setup
├── model_api/                  # Model prediction service
│   ├── Dockerfile              # Dockerfile for model API container
│   ├── model.py                # PyTorch model script
│   ├── app.py                  # FastAPI app serving the model
│   ├──model.pth                   # Pre-trained model weights
│   └── requirements.txt        # Python dependencies for model API
├── streamlit_app/              # Streamlit app directory
│   ├── Dockerfile              # Dockerfile for Streamlit app container
│   ├── streamlit.py            # Main Streamlit app file
│   └── requirements.txt        # Python dependencies for Streamlit app
├── init.sql                    # Initial SQL schema for PostgreSQL
