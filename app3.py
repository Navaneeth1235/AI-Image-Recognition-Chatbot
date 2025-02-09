import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize TTS Engine
engine = pyttsx3.init()

# Initialize session state for text and speech input
if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ""

if 'speech_text' not in st.session_state:
    st.session_state['speech_text'] = ""

# Function to get Gemini AI response
def get_gemini_response(final_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if final_text.strip():
        response = model.generate_content([final_text, image] if image else [final_text])
        return response.text
    return "Please provide some input."

# Function to recognize speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError:
            return "Error with the speech recognition service."

# Function to handle text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Streamlit App UI
st.set_page_config(page_title="Multi-Input AI App", layout="wide")

st.title("AI Image Recognition & Speech App")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📜 Manual Text Input")
    st.session_state['input_text'] = st.text_area(
        "Enter your prompt:",
        placeholder="Type your prompt here...",
        value=st.session_state['input_text']
    )

    st.subheader("🎤 Speech-to-Text")
    if st.button("Start Speaking"):
        spoken_text = recognize_speech()
        if spoken_text and "Could not understand" not in spoken_text:
            st.write(f"Recognized: {spoken_text}")
            st.session_state['speech_text'] += " " + spoken_text  # Append to stored text
            st.rerun()  # Refresh UI

    st.text_area(
        "Recognized Speech:",
        value=st.session_state['speech_text'],
        height=100,
        disabled=True
    )

with col2:
    st.subheader("📸 Upload an Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = Image.open(uploaded_file) if uploaded_file else None
    if image:
        st.image(image, caption="Uploaded Image", use_column_width=True)

# Combine both inputs before generating output
final_text = st.session_state['input_text'].strip() + "\n" + st.session_state['speech_text'].strip()

if st.button("🚀 Generate Response"):
    if not final_text.strip():
        st.warning("Please enter text or speak before generating a response.")
    else:
        with st.spinner("Generating response..."):
            response = get_gemini_response(final_text, image)
        st.success("Response generated!")
        st.write(response)

        if st.button("🔊 Read Aloud"):
            speak(response)
