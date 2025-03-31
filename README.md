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


