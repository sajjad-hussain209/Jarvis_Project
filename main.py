import speech_recognition as sr
import webbrowser
import pyttsx3
import music
import requests
from google import genai
from dotenv import load_dotenv
import os

recognizor = sr.Recognizer()
engine = pyttsx3.init()


load_dotenv()
newsapi = os.getenv("newsapi")
api_key = os.getenv("api_key")

def aiprocess(command):
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
    You are a helpful virtual assistant similar to Alexa or Google Assistant.
    You are a text-based virtual assistant. You should not claim that you can perform actions such as controlling smart-home devices, sending messages, making phone calls, opening applications, or accessing the user's files unless those capabilities have actually been connected to the program.

    The user is interacting with you through a Python application, so respond naturally as their personal AI assistant.

    User's request:
    {command}
    """
    )

    return (response.text)

def speak(text):
    engine.say(text)
    engine.runAndWait()


def processCommand(c):
    if 'open google' in c.lower():
        webbrowser.open('https://www.google.com')
    elif 'open facebook' in c.lower():
        webbrowser.open('https://www.facebook.com/')
    elif 'open youtube' in c.lower():
        webbrowser.open('https://www.youtube.com/')
    elif 'open youtube' in c.lower():
            webbrowser.open('https://linkedin.com/')
    elif c.lower().start('play'):
        song = c.lower().split(' ')[1]
        link = music.link[song]
        webbrowser.open(link)
    elif 'news' in c.lower(): 
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=pk&Key={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])

            # print the headlines
            for article in articles:
                speak(article['title'])
    else:
        # let Open AI handle the request
        output = aiprocess(c)
        speak(output)
if __name__ == "__main__":
    speak('initializing Jaarvis...')
    while True:
        # listning for the wake word jarvis

        # obtaining audio from michrophone
        
        print('recognizing')
        # recognize speech using Sphinx
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)            
            word = r.recognize_google(audio)
            if(word.lower()=='jarvis'):
                speak('yes')
                with sr.Microphone() as source:
                    print("Jarvis active....")
                    audio = r.listen(source)            
                    command = r.recognize_google(audio)

                    processCommand(command)

                # listen for command
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
        except Exception as e:
            print("error; {0}".format(e))