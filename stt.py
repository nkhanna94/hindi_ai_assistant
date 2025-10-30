# stt.py
import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
from pathlib import Path

MODEL_NAME = "small"  

_model = None


def _load_model():
    global _model
    if _model is None:
        _model = whisper.load_model(MODEL_NAME)
    return _model


def transcribe_file(file_path: str) -> str:
    """
    Transcribe audio file (wav/mp3) using whisper.
    Returns text (Hindi if spoken).
    """
    if not file_path:
        return "No audio file provided."
    model = _load_model()
    result = model.transcribe(file_path, language="hi")
    return result.get("text", "").strip()


def transcribe_from_mic(record_seconds: int = 5, only_record: bool = False) -> str:
    """
    Record from the default microphone for `record_seconds`.
    If only_record True -> returns path to saved wav file without transcribing.
    Otherwise returns transcribed text.
    """
    fs = 16000
    channels = 1
    print("Recording...")
    recording = sd.rec(int(record_seconds * fs), samplerate=fs, channels=channels, dtype="int16")
    sd.wait()
    recording = np.squeeze(recording)

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, recording, fs, subtype="PCM_16")
    tmp.close()

    if only_record:
        return tmp.name

    # else transcribe
    return transcribe_file(tmp.name)
