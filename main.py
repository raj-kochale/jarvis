import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize Pygame mixer for gTTS playback
pygame.mixer.init()

# API Keys (Replace these with your actual API keys)
newsapi_key = "YOUR_NEWSAPI_KEY"
openai_key = "YOUR_OPENAI_KEY"

# Function to speak using Google Text-to-Speech
def speak(text):
    print(f"Jarvis: {text}")  # Debugging print
    tts = gTTS(text)
    tts.save('temp.mp3')
    
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

# Function to process AI-based responses
def ai_process(command):
    client = OpenAI(api_key=openai_key)
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa."},
            {"role": "user", "content": command}
        ]
    )
    
    return completion.choices[0].message.content

# Function to handle voice commands
def process_command(command):
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")

    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")

    elif "news" in command:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi_key}")
        
        if r.status_code == 200:
            articles = r.json().get('articles', [])
            for article in articles[:5]:  # Read first 5 headlines
                speak(article['title'])
        else:
            speak("Sorry, I couldn't fetch the news.")

    else:
        response = ai_process(command)
        speak(response)

# Function to listen for voice input
def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Listening for 'Hey Jarvis'...")
        
        try:
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError:
            print("Could not connect to the speech recognition service.")
        except sr.WaitTimeoutError:
            print("Listening timed out.")

    return None

# Main function
if __name__ == "__main__":
    speak("Hello Sir, I am Jarvis. Say 'Hey Jarvis' to initialize me.")

    attempts = 3  # Limit retries
    while attempts > 0:
        command = listen()
        if command and "hey jarvis" in command:
            speak("Yes Sir, how can I assist you?")
            while True:  # Infinite loop for commands
                command = listen()
                if command:
                    if "exit" in command or "bye" in command:
                        speak("Goodbye, Sir!")
                        exit()
                    process_command(command)
        attempts -= 1

    speak("I could not detect the wake word. Please try again later.")
