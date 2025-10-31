# stt.py
import whisper

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