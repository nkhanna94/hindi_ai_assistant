# record_audio.py
import sounddevice as sd
import wavio
import os

def record_audio(duration=5, filename="recorded_audio.wav", samplerate=16000):
    """
    Records audio from mic for 'duration' seconds and saves it as a WAV file.
    Returns the full file path.
    """
    os.makedirs("recordings", exist_ok=True)
    filepath = os.path.join("recordings", filename)

    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()  # wait until recording finishes

    # Save as WAV
    wavio.write(filepath, audio_data, samplerate, sampwidth=2)
    print(f"Saved recording to {filepath}")
    return filepath
