from __future__ import with_statement
import pyttsx3
import speech_recognition as sr
import datetime
import os
import platform
import subprocess
#subpackages
from jarvis_queries import Query


class Jarvis(object):
    """
    jarvis is a class used to create jarvis core to use for various 
    tasks within your local env.

    attributes:
    rate : int [rate of talking of jarvis]
    voice : int [index of voice]

    methods: (most basic functions)
    init_tts_engine
    speak
    wish_me
    recognize_speech
    open_file
    kill_process
    shutdown_system
    restart_system
    open_terminal
    """

    def __init__(self, api_key, rate = 150, voice = 0):
        self.engine = self.init_tts_engine()
        self.rate = rate
        self.voice_nr = voice
        self.api_key = api_key

    def init_tts_engine(self) -> pyttsx3:
        """ 
        initialize text-to-speech engine with cross-platform driver 
        
        returns:
        engine : pyttsx3 [your current tts model object]
        """
        sys_os = platform.system()
        #win
        if sys_os == "Windows":
            engine = pyttsx3.init('sapi5')
        #darwin
        elif sys_os == "Darwin":
            engine = pyttsx3.init('nsss')
        #linux
        else:
            engine = pyttsx3.init('espeak')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[self.voice_nr].id)
        engine.setProperty('rate', self.rate)
        return engine

    def speak(self, text):
        """ speak the provided text """
        self.engine.say(text)
        self.engine.runAndWait()

    def wish_me(self):
        """ greet the user based on current time """
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            self.speak("good morning!")
        elif hour >= 12 and hour < 18:
            self.speak("good afternoon!")
        else:
            self.speak("good evening!")
        self.speak("ready to comply. what can i do for you?")

    def recognize_speech(self) -> str:
        """ 
        listen for a voice command and return the recognized string 
        
        returns:
        query : str [what you said]
        """ 
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            print("recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"user said: {query}\n")
        except Exception as e:
            print("say that again please...")
            return None
        return query

    def open_file(self, filepath):
        """ 
        open a file or application in a cross-platform way, recognizing user os 
        
        parameters:
        filepath : str [filepath to file you want to open]
        """
        sys_os = platform.system()
        if sys_os == "Windows":
            os.startfile(filepath)
        elif sys_os == "Darwin":
            subprocess.call(["open", filepath])
        else:
            subprocess.call(["xdg-open", filepath])

    def kill_process(self, process_name : str, mac_name=None):
        """ 
        kill a process by name in a cross-platform way 
        
        parameters:
        process_name : str [its the name of the process to kill]
        mac_name : str [the same, used for darwin]
        """
        sys_os = platform.system()
        if sys_os == "Windows":
            os.system(f"taskkill /f /im {process_name}")
        elif sys_os == "Darwin":
            name = mac_name if mac_name else process_name
            subprocess.call(["pkill", "-x", name])
        else:
            os.system(f"pkill {process_name}")

    def shutdown_system(self):
        """ shutdown the system in a cross-platform way """
        sys_os = platform.system()
        if sys_os == "Windows":
            os.system("shutdown /s /t 5")
        elif sys_os == "Darwin":
            os.system("sudo shutdown -h now")
        else:
            os.system("shutdown -h now")

    def restart_system(self):
        """ restart the system in a cross-platform way """
        sys_os = platform.system()
        if sys_os == "Windows":
            os.system("shutdown /r /t 5")
        elif sys_os == "Darwin":
            os.system("sudo shutdown -r now")
        else:
            os.system("shutdown -r now")

    def open_terminal(self):
        """ open terminal/command prompt in a cross-platform way """
        sys_os = platform.system()
        if sys_os == "Windows":
            os.system("start cmd")
        elif sys_os == "Darwin":
            subprocess.call(["open", "-a", "Terminal"])
        else:
            # try common terminal emulators on linux
            for term in ["gnome-terminal", "konsole", "x-terminal-emulator"]:
                if os.system(f"which {term} > /dev/null 2>&1") == 0:
                    subprocess.Popen([term])
                    break

    def talk(self):
        """ start to query jarvis for diffrent things """
        self.wish_me()
        query = self.recognize_speech().lower()
        Query(self, self.api_key).query(query)
