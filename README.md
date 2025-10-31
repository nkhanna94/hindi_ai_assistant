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

### Challenge 1: Gender bias

* **Challenge:** The model was using incorrect gender forms in Hindi responses. 
* **Solution:** I fixed this by updating the prompt to explicitly enforce feminine grammar (e.g., “कर सकती हूँ”) and adding example responses to guide consistency.
* 
### Challenge 2: Audio File Lost on Rerun

* **Challenge:** After recording an audio, clicking the "Transcribe & Respond" button would fail with a "Please upload or record audio first" error. This was happening because Streamlit reruns the script on every interaction, and the variable holding the `recorded_path` was reset to `None`.
* **Solution:** I re-architected the audio handling logic to use `st.session_state`. After recording or uploading, the file path is now stored in `st.session_state["audio_path"]`. This state persists across reruns, allowing the "Transcribe" button to reliably find and process the audio file.


## Ideas for Improvement

  * **Better TTS:** Replace gTTS with a more natural-sounding "neural" voice service, such as **Google Cloud TTS** or **ElevenLabs**, to make the assistant sound less robotic.
  * **Better UI/UX:** The current Streamlit app works fine, but it’s quite basic. I could redesign it into a more interactive, chat-style interface with mic controls, message history, and a cleaner layout.
  * **Persistent Sessions:** At the moment, the chat resets every time the app reloads. I could store the conversation history in a database so the assistant remembers past interactions and feels more continuous.
