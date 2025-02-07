import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai
from gtts import gTTS
import pygame
import os
import threading
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize required modules
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Load API keys
newsapi = os.getenv("NEWSAPI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize pygame mixer once
pygame.mixer.init()

def speak(text):
    """Convert text to speech using gTTS and play in a separate thread."""
    def play_audio():
        tts = gTTS(text)
        tts.save('temp.mp3')
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.delay(100)
        
        pygame.mixer.music.unload()
        os.remove('temp.mp3')
    
    threading.Thread(target=play_audio, daemon=True).start()

def aiProcess(command):
    """Process command using OpenAI GPT."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful virtual assistant named Jarvis. Keep responses short."},
                {"role": "user", "content": command}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

def processCommand(command):
    """Process user commands efficiently."""
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif command.startswith("play"):
        song = command.split(" ", 1)[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "news" in command:
        topic = command.replace("news", "").strip() or "technology"
        url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=popularity&apiKey={newsapi}"
        
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                articles = r.json().get('articles', [])
                if articles:
                    for article in articles[:3]:  # Read only top 3 headlines
                        speak(article['title'])
                else:
                    speak("No news found.")
            else:
                speak("Error fetching news.")
        except requests.exceptions.RequestException:
            speak("Network error while fetching news.")
    else:
        response = aiProcess(command)
        speak(response)

def listenForWakeWord():
    """Continuously listen for the wake word 'Jarvis' and then process commands."""
    speak("Initializing Jarvis...")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                word = recognizer.recognize_google(audio).lower()
                if word == "jarvis":
                    speak("Yes?")
                    
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                        command = recognizer.recognize_google(audio)
                        
                        processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError:
            print("Speech Recognition service error.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    listenForWakeWord()
