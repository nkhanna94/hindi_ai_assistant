# app.py
import streamlit as st
from pathlib import Path
import tempfile
import time
from record_audio import record_audio

from stt import transcribe_file, transcribe_from_mic
from response import generate_response
from tts import speak_text
from face_detection import check_face_and_show_preview
from utils import save_uploaded_audio

st.set_page_config(page_title="Hindi AI Assistant", layout="wide")

# --- Sidebar: chat history ---
if "chats" not in st.session_state:
    st.session_state.chats = []  # list of dicts: {"user": "...", "assistant": "..."}

st.sidebar.title("Chats")
if st.sidebar.button("Clear chats"):
    st.session_state.chats = []

for i, chat in enumerate(reversed(st.session_state.chats)):
    st.sidebar.markdown(f"**User:** {chat['user']}")
    st.sidebar.markdown(f"**Assistant:** {chat['assistant']}")
    st.sidebar.markdown("---")

# --- Header / Face detection on initial load or when refreshed ---
st.title("Hindi-speaking AI Assistant 🗣️🤖")
st.write("Upload an audio file or record from mic. The assistant transcribes (Hindi), generates a response, and speaks it.")

with st.expander("Face Detection (runs once when app starts or when you click)"):
    if st.button("Run face detection now"):
        detected, frame = check_face_and_show_preview()
        if detected:
            st.success("User detected ✓")
            # st.image(frame[:, :, ::-1], caption="Camera preview (BGR→RGB)", width=400)
        else:
            st.info("No user detected")
    else:
        st.write("Click the button to run face detection (opens a small webcam window).")

st.markdown("---")

# --- Audio input options ---
col1, col2 = st.columns([1, 2])

# --- REPLACE YOUR ENTIRE 'with col1:' BLOCK WITH THIS ---

with col1:
    st.header("Input")
    input_mode = st.radio("Choose input", ("Upload audio file", "Record from microphone"))
    
    # --- 1. Show widgets and save path to session state ---
    if input_mode == "Upload audio file":
        uploaded_file = st.file_uploader("Upload Hindi audio (wav/mp3)", type=["wav", "mp3", "m4a"])
        if uploaded_file is not None:
            # When file is uploaded, save it and update the state
            tmp_path_upload = save_uploaded_audio(uploaded_file)
            st.session_state["audio_path"] = tmp_path_upload
        
    else: # Record from microphone
        st.write("🎤 Record from your mic")
        duration = st.slider("Recording duration (seconds)", 1, 30, 5)

        if st.button("🎙️ Record"):
            st.info("Recording... please speak now!")
            with st.spinner(f"Recording for {duration} seconds..."):
                recorded_path = record_audio(duration=duration)
            st.success(f"Saved recording to {recorded_path}")
            # (Note: No st.audio() here - this fixes the double audio clip)
            st.session_state["audio_path"] = recorded_path

    # --- 2. Read from state to set tmp_path and show audio player ---
    # This logic runs *after* the widgets and *before* the "Transcribe" button
    
    tmp_path = None  # Default to None
    
    if "audio_path" in st.session_state:
        # Check if the file still exists
        current_path = st.session_state["audio_path"]
        if Path(current_path).exists():
            tmp_path = current_path
            # This is the *only* place we show the audio player
            st.audio(tmp_path)
        else:
            # File was deleted or lost, clear the state
            del st.session_state["audio_path"]

    # --- 3. Process button ---
    if st.button("Transcribe & Respond"):

        if tmp_path is None:
            st.error("Please upload or record audio first.")
        else:
            with st.spinner("Transcribing (Whisper)..."):
                transcript = transcribe_file(tmp_path)
            st.success("Transcribed")
            st.markdown("**Transcribed (Hindi)**")
            st.write(transcript)

            # Generate response (Ollama or fallback)
            with st.spinner("Generating response..."):
                assistant_reply = generate_response(transcript)

            st.markdown("**Assistant (Hindi)**")
            st.write(assistant_reply)

            # Save chat
            st.session_state.chats.append({"user": transcript, "assistant": assistant_reply})

            # TTS and play
            with st.spinner("Converting to speech..."):
                speak_text(assistant_reply)
            st.success("Played audio")

# with col1:
#     st.header("Input")
#     input_mode = st.radio("Choose input", ("Upload audio file", "Record from microphone"))
#     uploaded_file = None
#     recorded_path = None

    # if input_mode == "Upload audio file":
    #     uploaded_file = st.file_uploader("Upload Hindi audio (wav/mp3)", type=["wav", "mp3", "m4a"])
    # else:
    #     st.write("🎤 Record from your mic")
    #     duration = st.slider("Recording duration (seconds)", 1, 30, 5)

    #     if st.button("🎙️ Record"):
    #         st.info("Recording... please speak now!")
    #         with st.spinner(f"Recording for {duration} seconds..."):
    #             recorded_path = record_audio(duration=duration)
    #         st.success(f"Saved recording to {recorded_path}")
    #         st.audio(recorded_path)
    #         st.session_state["audio_path"] = recorded_path
    

    # Optionally save uploaded file to temp file for processing
    # if uploaded_file is not None:
    #     tmp_path = save_uploaded_audio(uploaded_file)
    #     st.audio(tmp_path)
    # elif recorded_path:
    #     tmp_path = recorded_path
    #     st.audio(tmp_path)
    # else:
    #     tmp_path = None

    # # Process button
    # if st.button("Transcribe & Respond"):

    #     if tmp_path is None:
    #         st.error("Please upload or record audio first.")
    #     else:
    #         with st.spinner("Transcribing (Whisper)..."):
    #             transcript = transcribe_file(tmp_path)
    #         st.success("Transcribed")
    #         st.markdown("**Transcribed (Hindi)**")
    #         st.write(transcript)

    #         # Generate response (Ollama or fallback)
    #         with st.spinner("Generating response..."):
    #             assistant_reply = generate_response(transcript)

    #         st.markdown("**Assistant (Hindi)**")
    #         st.write(assistant_reply)

    #         # Save chat
    #         st.session_state.chats.append({"user": transcript, "assistant": assistant_reply})

    #         # TTS and play
    #         with st.spinner("Converting to speech..."):
    #             speak_text(assistant_reply)
    #         st.success("Played audio")



with col2:
    st.header("Live Demo / Controls")
    st.markdown(
        """
- The assistant will transcribe Devanagari Hindi and respond in Hindi.
- Uses Whisper (local) for STT.
- LLM: Ollama local (if running at localhost:11434). Falls back to rule-based replies if not available.
- TTS: gTTS (Hindi) + pygame playback.
"""
    )

    st.markdown("## Quick examples (try speaking):")
    st.write("- नमस्ते, आप कैसे हैं?")
    st.write("- मेरा नाम क्या है?")
    st.write("- आज मौसम कैसा है?")

st.markdown("---")