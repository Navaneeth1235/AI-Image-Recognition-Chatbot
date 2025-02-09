import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #1E1E2F !important;
        color: white !important;
        padding: 20px;
    }

    .title-container {
        text-align: center;
        color: #F8E71C;
        margin-bottom: 20px;
    }

    .upload-container {
        text-align: center;
        background-color: #2C2C3A;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 30px;
    }

    .stButton>button {
        background-color: #F8E71C !important;
        color: #000 !important;
        border-radius: 10px !important;
        font-weight: bold;
    }

    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #F8E71C !important;
        background-color: #2C2C3A;
        color: white;
    }

    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }

    .footer {
        background-color: #F8E71C;
        color: black;
        padding: 10px;
        text-align: center;
        border-radius: 10px;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1 class='title-container'>🤖 AI IMAGE RECOGNITION CHATBOT</h1>", unsafe_allow_html=True)
st.markdown("<p class='title-container'>Upload an image, enter text, or speak to interact with AI.</p>",
            unsafe_allow_html=True)

# Image Upload Section
st.markdown("<div class='upload-container'><h2>📸 Upload an Image</h2></div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "avif"], key="image_uploader")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True, output_format="JPEG")

st.markdown("<br><br>", unsafe_allow_html=True)  # Add some space

# Layout with Two Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📜 Enter Text")
    input_text = st.text_area("Type your input:", placeholder="Enter your prompt here...", height=150)

with col2:
    st.subheader("🎤 Speech-to-Text")
    if st.button("Start Speaking", key="speech_button"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening...")
            try:
                audio = recognizer.listen(source)
                spoken_text = recognizer.recognize_google(audio)
                st.text_area("Recognized Speech:", spoken_text, height=100, disabled=True)
            except sr.UnknownValueError:
                st.warning("Could not understand the audio.")
            except sr.RequestError:
                st.error("Speech recognition service error.")

# Centered "Generate Response" Button
st.markdown("<div class='center-button'>", unsafe_allow_html=True)
if st.button("🚀 Generate Response", key="generate_button"):
    st.success("Response Generated!")
st.markdown("</div>", unsafe_allow_html=True)

# Footer Section
st.markdown(
    """
    <div class='footer'>
        <p><strong>Project Team:</strong> AI & Data Science Department</p>
        <p><strong>Guide:</strong> Prof. XYZ</p>
        <p><strong>Team Members:</strong> Alice, Bob, Charlie, David</p>
        <p>&copy; 2024 AI Image & Speech App. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)
