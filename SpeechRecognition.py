# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 09:17:12 2021

@author: Sophia
"""

#import the needed librarys: speech recognition, text to speech, and random number generator.
import speech_recognition as sr
import pyttsx3
import random
from random import randint

#initializing the text to speech engine and setting up the voice I wish to use
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


#create recognizer and microphone instances
r = sr.Recognizer()
mic = sr.Microphone()

#uncomment lines bellow and comment out line above if you do not have a default microphone
#print(sr.Microphone.list_microphone_names())
#mic = sr.Microphone((device_index=*insert_desired_mic_index_num_here*))

#list of possible computer responses
response = ["How does that make you feel?",  "Tell me more", "What is wrong with you?",
            "And then what happened?", "Are you ok?", "Why did the chicken cross the road?"]
no_response = "Hey, did you forget about me? Try saying that again."


#recognizes speech from mic and outputs an error if something goes wrong
#user input is stored in transcription
def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    response = {"success": True,
        "error": None,
        "transcription": None}
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    
        
    return response


#generates a random prompt for Biff to ask the user
def random_phrase():
    rando_phrase = randint(0, len(response)-1)
    response_phrase = response[rando_phrase]
    engine.say(response_phrase)
    engine.runAndWait()
    print("Biff: "+response_phrase)

#takes user input and prints it
#or asks the user to try again if something went wrong
def short_interaction():
    transcribed_text = recognize_speech_from_mic(r, mic)["transcription"]
    print(transcribed_text)
    while transcribed_text == None:
        engine.say(no_response)
        engine.runAndWait()
        print("Biff: "+no_response)
        transcribed_text = recognize_speech_from_mic(r, mic)["transcription"]
        print(transcribed_text)

#starts by introducing Biff and asking for user to talk
engine.say("Hello! I am your irreverant friend and my name is Biff. Talk to me, just don't expect me to deduce your meaning.")
engine.runAndWait()
print("Biff: Hello! I am your irreverant friend and my name is Biff. Talk to me, just don't expect me to deduce your meaning.")

#holds a converstation with the user
#gets their input and then asks them something
short_interaction()
random_phrase()
short_interaction()
random_phrase()
short_interaction()
random_phrase()
short_interaction()

#dismisses user 
engine.say("You are dismissed! Thank you for your time.")
engine.runAndWait()