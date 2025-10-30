import cv2
import time
import streamlit as st

def check_face_and_show_preview(duration_sec: int = 3):
    """
    Works inside Streamlit — uses st.image() instead of cv2.imshow().
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Unable to access webcam.")
        return False, None

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    start = time.time()
    detected = False
    last_frame = None
    frame_placeholder = st.empty()  # for live preview

    while time.time() - start < duration_sec:
        ret, frame = cap.read()
        if not ret:
            break
        last_frame = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if len(faces) > 0:
            detected = True

        # Convert BGR → RGB for Streamlit
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # --- FIX 1: Add 'width' to control size ---
        frame_placeholder.image(frame_rgb, channels="RGB", caption="Face detection preview", width=400)

    cap.release()
    
    # --- FIX 2: Clear the placeholder after the loop ---
    frame_placeholder.empty()
    
    return detected, last_frame