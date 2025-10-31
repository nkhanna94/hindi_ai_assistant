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
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        frame_placeholder = st.empty() 

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
        
        frame_placeholder.image(frame_rgb, channels="RGB", caption="Face detection preview", width=400)

    cap.release()

    frame_placeholder.empty()
    
    return detected, last_frame