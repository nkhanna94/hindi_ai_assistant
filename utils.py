# utils.py
import tempfile
from pathlib import Path

def save_uploaded_audio(uploaded_file) -> str:
    """
    Save Streamlit uploaded file to a temporary path and return path.
    """
    suffix = Path(uploaded_file.name).suffix
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    tmp.write(uploaded_file.getbuffer())
    tmp.flush()
    tmp.close()
    return tmp.name