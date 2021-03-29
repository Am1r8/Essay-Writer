# Created by AlPHA or some people call me coach AlPHA
# This is a essay writer for making online schools much easier and it will correct your grammar if there is any
# Please don't share this with your teacher:)
# And remember to only say correct commends or you have to start over
# Enjoy
# 1.3.4
# AlPHA

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import speech_recognition as sr
import pyttsx3
import pyaudio
from time import sleep
import sys
from textblob import TextBlob
from gingerit.gingerit import GingerIt

# starting works #
SCOPES = ['https://www.googleapis.com/auth/drive.file']
creds = None
r = sr.Recognizer()
mic = sr.Microphone()
text = ""
docId = ""
text5 = ""

# Starting The speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', 155)
volume = engine.getProperty('volume')
engine.setProperty('volume', 1.0)
engine.runAndWait()


# starting functions
# speaking function
def speak(text):
    engine.say(text)
    return engine.runAndWait()


# tokenizing google doc
def start():
    global creds
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


# speech to text function
def speech_te():
    global text
    with sr.Microphone() as source:
        print("Listening ...")
        r.adjust_for_ambient_noise(source)
        audio_data = r.listen(source)
        text = r.recognize_google(audio_data)
        print("Recognizing...")
        # text = r.recognize_google(audio_data)
        print(text)


# speech to text function number 2 for defining the document text
def speech_2():
    global text5
    with sr.Microphone() as source:
        print("Listening ...")
        r.adjust_for_ambient_noise(source)
        audio_data = r.listen(source)
        text5 = r.recognize_google(audio_data)
        print("Recognizing...")
        print(text5)


# start of program
if __name__ == '__main__':
    speak("Hey, I'm essay Writer, I can help you with writing essay for you, Let's start")
    sleep(0.1)
    start()
    service = build('docs', 'v1', credentials=creds)

    # Creating the Document of google drive
    speak("do you want to make a doc")
    speech_te()
    if text == "yes" or text == "yeah" or text == "yes please":
        text = ""
        speak("what do you want to call your doc?")
        speech_te()
        title = text
        body = {'title': title}
        doc = service.documents().create(body=body).execute()
        docId = doc.get('documentId')
        print('Created document with title: {0}'.format(doc.get('title')))
        speak('Created document with title: {0}'.format(doc.get('title')))
    elif text == "No" or text == "I have a document":
        text = ""
        speak("Sorry this option is not available right now")
        print("Sorry this option is not available right now")
    else:
        text = ""
        speak("Sorry This command is not available yet")
        print("Sorry This command is not available yet")
        exit()

    # Starting the program to listen to essay
    text = ""
    speak("recording is ready, Please speak!")

    # I did this because some time weird thing weird things happened to speech to text engine so it give gives chance
    # to user to say the essay two times if needed
    try:
        speech_te()
    except:
        speech_te()
        print("Please repeat")
        speak("please repeat")
    sleep(1)
    speak("you can see your document in few seconds")
    # finding the length of essay words
    lent_text = len(text) + 1
    speak(text)

    # correcting the text and checking ofr grammar issue
    result5 = GingerIt().parse(text)
    text2 = TextBlob(text)
    text2 = text2.correct()
    text2 = str(text2)
    speak("We corrected Your speaking and we founded some grammar and spelling issue, do you want us to insert your "
          "speech or our corrected sentence to your document?")

    speech_2()

    # Asking user which speech they want to insert to document, there own or corrected with different engines
    if text5 == "let me see" or text5 == "yes" or text5 == "yes show me":
        print("1)", result5['result'], "\n2)", text2, "\n3) or Original version)", text)
        speak("Please say the number you want")

        sleep(2)
        text5 = ""
        speech_2()
        if text5 == "1" or text5 == "number 1":
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': result5
                    }
                }
            ]

            result = service.documents().batchUpdate(documentId=docId, body={'requests': requests}).execute()
        elif text5 == "2" or text5 == "number 2":
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': text2
                    }
                }
            ]

            result = service.documents().batchUpdate(documentId=docId, body={'requests': requests}).execute()
        elif text5 == "3" or text5 == "number 3":
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': text
                    }
                }
            ]

            result = service.documents().batchUpdate(documentId=docId, body={'requests': requests}).execute()
        else:
            speak("Please enter a valid number")
            print("Please enter a valid number")
            exit()
    else:
        speak("I will write your speech in the document")
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': text
                }
            }
        ]

        result = service.documents().batchUpdate(documentId=docId, body={'requests': requests}).execute()

    # giving the link of google doc to the user so they can visit it
    speak("We entered your speech into text and it's available in below link")
    print("https://docs.google.com/document/d/" + docId + "/edit")
    exit()
