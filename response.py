# response.py
import os
import requests
import json

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")  # default Ollama local server
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3:latest")

def _ollama_available() -> bool:
    try:
        
        r = requests.get(OLLAMA_URL, timeout=3.0) 

        # Check the status code explicitly
        if r.status_code == 200:
            print("--- Ollama server is available (ping successful) ---")
            return True
        else:
            print(f"--- Ollama server is running but base URL check failed (Status: {r.status_code}) ---")
            return False
            
    except requests.ConnectionError:
        print(f"--- ERROR: Could not connect to Ollama at {OLLAMA_URL} ---")
        print("--- Is the Ollama server running? ---")
        return False
    except Exception as e:
        print(f"--- ERROR: An unexpected error occurred checking Ollama: {e} ---")
        return False

def query_ollama(prompt: str, model: str = OLLAMA_MODEL, timeout: int = 20) -> str:
    """
    Send prompt to local Ollama (if available). Returns text response.
    """

    payload = {"model": model, "prompt": prompt, "max_tokens": 256, "stream": False}
    
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, dict) and "response" in data:
            return data["response"].strip()
        
        # if response structure different:
        return json.dumps(data)
    except Exception as e:
        # print the error to see what's wrong
        print(f"Error querying Ollama: {e}") 
        raise


def rule_based_response(transcript: str) -> str:
    """
    Simple Hindi rule-based fallback. You can expand rules as needed.
    """
    t = transcript.strip().lower()
    if "मेरा नाम क्या" in t or "मेरा नाम क्या है" in t:
        return "मुझे खेद है, मुझे आपका नाम नहीं पता।"
    if "तुम कैसे" in t or "आप कैसे" in t:
        return "नमस्ते! मैं ठीक हूँ। आपकी क्या मदद कर सकता हूँ?"
    if "मौसम" in t:
        return "मैं मौसम की जानकारी नहीं दे सकता।"
    if "धन्यवाद" in t or "थैंक यू" in t:
        return "आपका स्वागत है!"
    # default polite fallback
    return "माफ़ कीजिये, मैं आपकी बात समझ नहीं पाया। क्या आप दोहरा सकते हैं?"

def generate_response(transcript: str) -> str:
    """
    Main entry: tries Ollama, falls back to rule-based.
    """
    prompt = f"""
    You are a friendly female Hindi AI assistant named सहायिका AI. 
    Respond **only in simple, clear, and concise Hindi** using **feminine grammar** (e.g., 'मैं बता सकती हूँ').
    Keep your tone **polite and conversational**. 

    User: {transcript}
    Assistant:
    """

    if _ollama_available():
        try:
            resp = query_ollama(prompt)
            return resp.strip()
        except Exception:
            return rule_based_response(transcript)
    else:
        return rule_based_response(transcript)