# app.py
import streamlit as st
from pathlib import Path
from record_audio import record_audio

from stt import transcribe_file
from response import generate_response
from tts import speak_text
from face_detection import check_face_and_show_preview
from utils import save_uploaded_audio

st.set_page_config(page_title="सहायिकाAI", layout="centered")

# --- Sidebar: chat history ---
if "chats" not in st.session_state:
    st.session_state.chats = []  # list of dicts: {"user": "...", "assistant": "..."}

st.sidebar.title("Chat History 📜")
if st.sidebar.button("Clear chats 🗑️"):
    st.session_state.chats = []

for i, chat in enumerate(reversed(st.session_state.chats)):
    st.sidebar.markdown(f"**User:** {chat['user']}")
    st.sidebar.markdown(f"**Assistant:** {chat['assistant']}")
    st.sidebar.markdown("---")

st.markdown(
    """
    <h1 style='text-align: center; font-family: "Noto Serif Devanagari", serif;'>
        सहायिकाAI 🇮🇳
    </h1>
    """,
    unsafe_allow_html=True
)
# st.write("I am your Hindi AI assistant. Please provide an audio file or record your voice.")
st.markdown(
    """
    <p style='text-align: center;
              font-size: 20px;
              color: #6C584C;
              font-style: italic;'>
        I am your Hindi AI assistant. Please provide an audio file or record your voice.
    </p>
    """,
    unsafe_allow_html=True
)


# --- Header / Face detection on initial load or when refreshed ---
with st.expander("Face Detection (runs once when app starts or when you click)"):
    if st.button("Run face detection now"):
        detected, frame = check_face_and_show_preview()
        if detected:
            st.success("User detected! 👋")
        else:
            st.info("No user detected 😶")
    else:
        st.write("Click the button to run face detection (opens a small webcam window).")

# st.markdown("---")

with st.container(border=True):
    st.markdown("## Input")
    
    # Tabs for better organization
    tab1, tab2 = st.tabs(["📤 Upload Audio", "🎙️ Record Audio"])
    
    with tab1:
        st.markdown("##### Upload your Hindi audio file →")
        uploaded_file = st.file_uploader(
            "Supported formats: WAV, MP3, M4A",
            type=["wav", "mp3", "m4a"],
            help="Upload a clear audio file in Hindi"
        )
        if uploaded_file is not None:
            tmp_path_upload = save_uploaded_audio(uploaded_file)
            st.session_state["audio_path"] = tmp_path_upload
            st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    with tab2:
        st.markdown("### Record your voice")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            duration = st.slider(
                "Recording duration (seconds)",
                min_value=1,
                max_value=30,
                value=5,
                help="Choose how long to record"
            )
        
        if st.button("🎙️ Start Recording", use_container_width=True):
            st.info("🔴 Recording in progress... Please speak now!")
            with st.spinner(f"Recording for {duration} seconds..."):
                recorded_path = record_audio(duration=duration)
            st.success(f"✅ Recording saved successfully!")
            st.session_state["audio_path"] = recorded_path

    # Display audio player
    tmp_path = None
    if "audio_path" in st.session_state:
        current_path = st.session_state["audio_path"]
        if Path(current_path).exists():
            tmp_path = current_path
            st.markdown("### 🔊 Preview Your Audio")
            st.audio(tmp_path)
        else:
            del st.session_state["audio_path"]

# ===== PROCESSING SECTION =====
with st.container():
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # --- Custom styling for Transcribe button ---
        st.markdown("""
            <style>
            div.stButton > button:first-child {
                background-color: #6C584C;      /* your primary color */
                color: #F0EAD2;                 /* text color to match theme */
                font-size: 17px;
                font-weight: 600;
                border-radius: 40px;            /* makes it oval */
                border: none;
                padding: 0.6em 1.5em;
                box-shadow: 0px 3px 6px rgba(0,0,0,0.2);
                transition: all 0.25s ease-in-out;
            }
            div.stButton > button:first-child:hover {
                background-color: #7B6F5E;      /* slightly lighter hover tone */
                transform: scale(1.03);
                box-shadow: 0px 5px 10px rgba(0,0,0,0.25);
            }
            </style>
        """, unsafe_allow_html=True)

        if st.button("🚀 Transcribe & Generate Response", use_container_width=True):
            if tmp_path is None:
                st.error("❌ Please upload or record audio first!")
            else:
                # Transcription
                with st.spinner("🎯 Transcribing your audio..."):
                    transcript = transcribe_file(tmp_path)
                st.success("✅ Transcription complete!")
                
                # Display transcript in a nice box
                st.markdown("### 📝 Your Message (Transcribed)")
                st.info(transcript)

                # Generate response
                with st.spinner("🤔 Generating intelligent response..."):
                    assistant_reply = generate_response(transcript)

                # Display response in a nice box
                st.markdown("### 🤖 Assistant's Response")
                st.success(assistant_reply)

                # Save to chat history
                st.session_state.chats.append({
                    "user": transcript,
                    "assistant": assistant_reply
                })

                # Text-to-speech
                with st.spinner("🔊 Converting to speech..."):
                    speak_text(assistant_reply)
                st.toast("✅ Audio playback complete!", icon="🔊")

st.markdown("\n")

with st.expander("ℹ️ About this Assistant", expanded=False):
    with st.container(border=True):
        col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ##### Features 🎯
        🎤 Whisper-powered Hindi transcription\n
        🧠 Ollama LLM for natural responses\n
        🔊 gTTS Hindi voice output\n
        👁️ Optional user verification
        """)
    
    with col2:
        st.markdown("""
        ##### Try These Examples 💡
        ‣ *नमस्ते, आप कैसे हैं?*\n
        ‣ *मेरा नाम क्या है?*\n
        ‣ *आज मौसम कैसा है?*\n
        ‣ *मुझे एक कहानी सुनाओ*
        """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #6C584C;'>Crafted with ❤️ | Powered by Llama 3</p>", unsafe_allow_html=True)