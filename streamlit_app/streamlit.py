import streamlit as st
import requests
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
import os
import psycopg2
import io
import pytz

def create_connection():
    conn = psycopg2.connect(
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=os.getenv("DATABASE_PORT", "5432"),
        user=os.getenv("DATABASE_USER", "postgres"),
        password=os.getenv("DATABASE_PASSWORD", "mysecretpassword"),
        dbname=os.getenv("DATABASE_NAME", "prediction_log")
    )
    return conn

# Insert a new prediction log only when the user provides a true label
def log_prediction(predicted_digit, true_label):
    # Get current timestamp in UTC
    utc_tz = pytz.utc  # UTC timezone
    timestamp = datetime.now(utc_tz)  # This will give the current time in UTC

    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO predictions (timestamp, predicted_digit, true_label) VALUES (%s, %s, %s);",
        (timestamp, predicted_digit, true_label)
    )
    conn.commit()
    cur.close()
    conn.close()

# Fetch logged predictions (only 3 columns)
def get_predictions():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT timestamp, predicted_digit, true_label FROM predictions ORDER BY timestamp DESC LIMIT 10;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

# Preprocessing function
def preprocess_and_send(img):
    pil_img = Image.fromarray(img).convert("L").resize((28, 28))
    
    # Convert the image to a file-like object
    img_byte_arr = io.BytesIO()
    pil_img.save(img_byte_arr, format='PNG')  # Save image in a byte array as PNG
    img_byte_arr.seek(0)  # Go to the start of the byte array

    # Send image to the model API
    response = requests.post(
        os.getenv("MODEL_SERVICE_URL", "http://model_service:8000/predict/"),
        files={"file": ("image.png", img_byte_arr, "image/png")}
    )

    if response.status_code == 200:
        return response.json()["prediction"], response.json().get("confidence", 1.0)
    else:
        return None, None

# Streamlit app UI
st.title("🖌️ The Digit Recognizer Tool")
st.subheader("Draw a Digit and let the Model Predict the Number!")

# Canvas for drawing
canvas_result = st_canvas(
    fill_color="black",
    stroke_width=10,
    stroke_color="white",
    background_color="black",
    width=280,
    height=280,
    drawing_mode="freedraw",
    key="canvas",
)

# Prediction logic
if canvas_result.image_data is not None:
    img_data = canvas_result.image_data
    img = np.array(img_data, dtype=np.uint8)

    if np.sum(img) > 0:  # If something is drawn
        predicted_label, confidence = preprocess_and_send(img)

        if predicted_label is not None:
            st.write(f"**Predicted Digit: {predicted_label}**")
            st.write(f"**Confidence: {confidence * 100:.2f}%**")

            # User feedback
            true_label = st.text_input("Enter the correct digit:", "")

            if st.button("Log Correct Label"):
                if true_label.isdigit():
                    true_label = int(true_label)
                    st.write("✅ Thank you for your feedback! Logging the data now.")
                    log_prediction(predicted_label, true_label)

# Display logged predictions
st.subheader("📜 Prediction History")

# Fetch and display predictions from the database
data = get_predictions()

if data:
    # Convert data into a DataFrame for a cleaner table
    df = pd.DataFrame(data, columns=["Timestamp", "Predicted Digit", "True Label"])

    # Convert the timestamp to UK timezone (UTC +1 during daylight saving time)
    uk_tz = pytz.timezone('Europe/London')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], utc=True).dt.tz_convert(uk_tz)

    # Format the timestamp to show day and hour only, without the timezone offset
    df['Timestamp'] = df['Timestamp'].dt.strftime('%d-%m-%Y %H:%M')

    st.table(df)
else:
    st.write("No predictions logged yet.")
