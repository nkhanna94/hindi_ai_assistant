from gtts import gTTS
import tempfile

def speak_text(text: str, lang="hi"):
    """
    Convert text (Hindi) to speech using gTTS and save to a temp file.
    Returns the path to the temporary MP3 file.
    
    DOES NOT play the audio.
    """
    if not text:
        return None

    try:
        # Create a temp file to save the audio
        tf = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tf.close()
        mp3_path = tf.name

        # Generate the speech and save it
        tts = gTTS(text=text, lang=lang)
        tts.save(mp3_path)
        
        return mp3_path # Return the path to the file
        
    except Exception as e:
        print(f"Error creating TTS file: {e}")
        return None