import speech_recognition as sr
import pyttsx3

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Configure pyttsx3 properties
voices = engine.getProperty('voices')  # Get available voices
engine.setProperty('voice', voices[0].id)  # Select the first available voice
engine.setProperty('rate', 150)  # Adjust speaking speed


def speak(text):
    """Convert text to speech."""
    print(f"Jarvis: {text}")  # Debugging print statement
    engine.say(text)
    engine.runAndWait()


def listen():
    """Capture and recognize speech from the microphone."""
    with sr.Microphone() as source:
        print("Listening for 'Hey Jarvis'...")
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Reduce background noise

        try:
            audio = recognizer.listen(source, phrase_time_limit=7)  # Extended listening time
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")

            return command

        except sr.UnknownValueError:
            print("Could not understand the audio. Try again.")
        except sr.RequestError:
            print("Could not connect to speech recognition service. Check internet connection.")
        except sr.WaitTimeoutError:
            print("Listening timed out. Try again.")

        return None  # Return None on failure



if __name__ == "__main__":
    speak("Hello Sir, I am Jarvis. Say 'Hey Jarvis' to initialize me.")
    
    attempts = 3  # Limit retries
    while attempts > 0:
        command = listen()
        if command and "hey jarvis" in command:
            speak("Yes Sir, how can I assist you?")
            break
        attempts -= 1

    if attempts == 0:
        speak("I could not detect the wake word. Please try again later.")
