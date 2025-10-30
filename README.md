# Hindi-Speaking AI Assistant

A simple, end-to-end web application that accepts Hindi audio, transcribes it, generates an intelligent response using a local LLM, and speaks the Hindi response back to the user.

## Features

  * **🎙️ Speech-to-Text:** Transcribes spoken Hindi from microphone input or an uploaded audio file (wav/mp3).
  * **🧠 Response Generation:** Uses a local LLM (Llama 3) to generate intelligent, conversational replies in Hindi.
  * **🔊 Text-to-Speech:** Converts the AI's Hindi text response back into audible speech automatically.
  * **😀 Face Detection (Bonus):** Uses OpenCV to detect a user's face via webcam and displays a "User detected" status.
  * **💬 Chat History:** Displays a running log of the conversation in the sidebar.

## Technologies Used

  * **Application Framework:** **Streamlit** (for the interactive web UI).
  * **Speech-to-Text (STT):** **OpenAI Whisper** (using the `small` model for high-accuracy Hindi transcription).
  * **Response Generation (LLM):** **Ollama** running **Llama 3 (8B)** locally for chat responses.
  * **Text-to-Speech (TTS):** **gTTS (Google Text-to-Speech)** for generating the Hindi audio output.
  * **Face Detection:** **OpenCV** (using a pre-trained Haar Cascade model).
  * **Audio Handling:** **PyAudio** (for mic recording) and **Pygame** (for audio playback).

## Setup and Run

### 1\. Prerequisites

  * Python 3.10+
  * [Ollama](https://ollama.com/) (must be installed and running)

### 2\. Clone Repository

```bash
git clone <https://github.com/nkhanna94/hindi-ai-assistant.git>
cd hindi-ai-assistant
```

### 3\. Set Up Environment & Install Models

```bash
# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Download the Llama 3 model for Ollama
ollama pull llama3

# (The Whisper 'small' model will download automatically on first run)
```

### 4\. Run the Application

```bash
# Make sure your Ollama server is running in a separate terminal
ollama serve

# Run the Streamlit app
streamlit run app.py
```

## Challenges & Solutions

You're right, my apologies. The prompt complexity is a valid trade-off.

Here are two other *excellent* challenges you definitely solved:

### Challenge 1: Ollama Connection Failing Silently

* **Challenge:** The application always used its fallback "माफ़ कीजिये..." reply, even though the Ollama server was running. The `_ollama_available()` function was returning `False` without any error message, making it impossible to debug.
* **Solution:** We modified the `_ollama_available` function to include detailed `try...except` blocks with `print` statements. This immediately revealed the true error: a `404 Not Found`. The code was checking for a `/ping` endpoint that didn't exist. The fix was to change the health check URL to the base `/` address, which immediately established a connection.

### Challenge 2: Audio File Lost on Rerun

* **Challenge:** After recording an audio, clicking the "Transcribe & Respond" button would fail with a "Please upload or record audio first" error. This was happening because Streamlit reruns the script on every interaction, and the variable holding the `recorded_path` was reset to `None`.
* **Solution:** We re-architected the audio handling logic to use `st.session_state`. After recording or uploading, the file path is now stored in `st.session_state["audio_path"]`. This state persists across reruns, allowing the "Transcribe" button to reliably find and process the audio file.


## Ideas for Improvement

  * **Better TTS:** Replace gTTS with a more natural-sounding "neural" voice service, such as **Google Cloud TTS** or **ElevenLabs**, to make the assistant sound less robotic.
  * **Wake Word:** Implement a "wake word" (e.g., "नमस्ते असिस्टेंट") using a library like `pvporcupine` to start recording automatically.
  * **Streaming:** Implement streaming for all components (STT, LLM, TTS) so the assistant can listen, think, and speak in real-time without waiting for each step to complete.