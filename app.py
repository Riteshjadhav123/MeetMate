import streamlit as st
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Import the functions from your scripts
from transcribe import transcribe
from summarize import summarize_transcript
from send_email import send_summary_email

# Ensure required directories exist
os.makedirs("audio", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# --- Page Configuration ---
st.set_page_config(
    page_title="MeetMate Summarizer",
    page_icon="�",
    layout="centered"
)

# --- Custom CSS for a Futuristic Look ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# You can create a style.css file and call local_css("style.css")
# Or, for simplicity, we can inject the CSS directly:
st.markdown("""
<style>
/* Main App Background */
.stApp {
    background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 74%);
    color: #E0E1DD;
}

/* Title */
h1 {
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700;
    color: #FFFFFF;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    text-align: center;
}

/* Subheaders */
h3 {
    color: #A9B4C2;
    border-bottom: 1px solid #415a77;
    padding-bottom: 10px;
    margin-top: 20px;
}

/* Button Styling */
div.stButton > button:first-child {
    background-color: #415a77;
    color: white;
    border-radius: 10px;
    border: 1px solid #778da9;
    font-size: 16px;
    font-weight: bold;
    padding: 12px 24px;
    width: 100%;
    transition: all 0.3s ease-in-out;
}

div.stButton > button:hover {
    background-color: #778da9;
    border-color: #FFFFFF;
    color: #0d1b2a;
    box-shadow: 0 0 15px rgba(120, 141, 169, 0.7);
}

/* File Uploader */
section[data-testid="stFileUploader"] {
    border: 2px dashed #415a77;
    border-radius: 10px;
    background-color: rgba(13, 27, 42, 0.5);
}
section[data-testid="stFileUploader"] small {
    color: #A9B4C2;
}

/* Text Inputs */
div[data-testid="stTextInput"] input {
    border-radius: 8px;
    border: 1px solid #415a77;
    background-color: #0d1b2a;
    color: #E0E1DD;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)


# --- UI Layout ---
st.title("🤖 MeetMate: AI Meeting Summarizer")
st.markdown("<p style='text-align: center; color: #A9B4C2;'>Upload your meeting audio and get a structured summary delivered to your inbox.</p>", unsafe_allow_html=True)

# Main container for the form
with st.container():
    st.markdown("---")
    
    # 1. Audio File Uploader
    uploaded_file = st.file_uploader(
        "STEP 1: Upload your meeting audio", 
        type=['mp3', 'wav', 'm4a']
    )

    # 2. Email Input Fields
    st.subheader("STEP 2: Configure Delivery")
    col1, col2 = st.columns(2)
    default_sender = os.getenv("SENDER_EMAIL", "")
    default_recipient = os.getenv("RECIPIENT_EMAIL", "")
    with col1:
        sender_email = st.text_input("Your Email (Sender)", value=default_sender, placeholder="your_email@gmail.com")
    with col2:
        recipient_email = st.text_input("Recipient's Email", value=default_recipient, placeholder="recipient@example.com")

    st.markdown("---")

    # 3. "Generate Summary" Button
    if st.button("✨ Generate & Send Summary"):
        if uploaded_file is not None and sender_email and recipient_email:
            with st.spinner("Processing... This may take a few minutes."):
                
                # Save the uploaded file to the 'audio' folder
                os.makedirs("audio", exist_ok=True)
                os.makedirs("outputs", exist_ok=True)
                audio_path = os.path.join("audio", uploaded_file.name)
                with open(audio_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.success(f"✅ File '{uploaded_file.name}' uploaded successfully.")
                time.sleep(1)

                # --- Step 1: Transcription ---
                st.info("Step 1/3: Transcribing audio...")
                transcript_path = 'outputs/meeting_transcript.txt'
                transcribe(audio_path) 
                st.success("Transcription complete!")
                time.sleep(1)
                
                # --- Step 2: Summarization ---
                st.info("Step 2/3: Generating AI summary...")
                summarize_transcript(transcript_path)
                st.success("Summary generated!")
                time.sleep(1)

                # --- Step 3: Emailing ---
                st.info("Step 3/3: Sending the summary email...")
                send_summary_email(sender=sender_email, recipient=recipient_email)
                st.success(f"Email sent to {recipient_email}!")

            st.balloons()
            st.header("🎉 Process Complete!")

        else:
            st.error("Please upload an audio file and fill in both email addresses.")

