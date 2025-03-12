import speech_recognition as sr

def get_speech_input():
    """Converts user speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak now...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Speech not recognized."
        except sr.RequestError:
            return "Error connecting to speech service."
