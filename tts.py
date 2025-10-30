# tts.py
from gtts import gTTS
import tempfile
import pygame
import time
import os

def speak_text(text: str, lang="hi"):
    """
    Convert text (Hindi) to speech using gTTS, play it with pygame.
    Blocks until playback finishes.
    """
    if not text:
        return

    # Save to temp mp3
    tf = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tf.close()
    mp3_path = tf.name

    tts = gTTS(text=text, lang=lang)
    tts.save(mp3_path)

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_path)
        pygame.mixer.music.play()
        # wait until finished
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    finally:
        try:
            pygame.mixer.quit()
        except Exception:
            pass
        # remove tmp file
        try:
            os.remove(mp3_path)
        except Exception:
            pass
