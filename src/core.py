import pyttsx3
import speech_recognition as sr
import datetime
import os
import platform
import subprocess
import time
from .queries import Query

class Jarvis:
    """
    Core Jarvis assistant.
    """

    def __init__(self, api_key: str, rate: int = 95, voice: int = 3, volume: float = 1.0):
        self.api_key = api_key
        self.rate = rate
        self.voice = voice
        self.volume = volume
        self.engine = self.init_tts_engine()

    def init_tts_engine(self) -> pyttsx3.Engine:
        engine = pyttsx3.init()
        engine.setProperty("rate", self.rate)
        engine.setProperty("volume", self.volume)
        voices = engine.getProperty("voices")
        if 0 <= self.voice < len(voices):
            engine.setProperty("voice", voices[self.voice].id)
        else:
            for v in voices:
                if any(lang.startswith("en") for lang in getattr(v, "languages", [])) \
                   or "English" in v.name:
                    engine.setProperty("voice", v.id)
                    break
        return engine

    def speak(self, text: str):
            self.engine.say(text)
            self.engine.runAndWait()
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
            time.sleep(0.3)

    def wish_me(self):
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good morning!"
        elif hour < 18:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        self.speak(greeting)

    def recognize_speech(self) -> str:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Calibrating for ambient noise…")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening…")
            audio = recognizer.listen(source)
        try:
            print("Recognizing…")
            query = recognizer.recognize_google(audio, language="en-in")
            print(f"You said: {query}")
            return query
        except Exception:
            print("Sorry, I did not catch that.")
            return ""

    def open_file(self, filepath: str):
        sys_os = platform.system()
        if sys_os == "Windows":
            os.startfile(filepath)
        elif sys_os == "Darwin":
            subprocess.call(["open", filepath])
        else:
            subprocess.call(["xdg-open", filepath])

    def kill_process(self, process_name: str, mac_name: str = None):
        sys_os = platform.system()
        if sys_os == "Windows":
            os.system(f"taskkill /F /IM {process_name}")
        elif sys_os == "Darwin":
            name = mac_name or process_name
            os.system(f"killall {name}")
        else:
            os.system(f"pkill -f {process_name}")

    def shutdown_system(self):
        sys_os = platform.system()
        if sys_os == "Windows":
            os.system("shutdown /s /t 5")
        elif sys_os == "Darwin":
            os.system("sudo shutdown -h now")
        else:
            os.system("shutdown -h now")

    def restart_system(self):
        sys_os = platform.system()
        if sys_os == "Windows":
            os.system("shutdown /r /t 5")
        elif sys_os == "Darwin":
            os.system("sudo shutdown -r now")
        else:
            os.system("shutdown -r now")

    def open_terminal(self):
        sys_os = platform.system()
        if sys_os == "Windows":
            os.system("start cmd")
        elif sys_os == "Darwin":
            subprocess.call(["open", "-a", "Terminal"])
        else:
            for term in ["gnome-terminal", "konsole", "x-terminal-emulator"]:
                if os.system(f"which {term} > /dev/null 2>&1") == 0:
                    subprocess.Popen([term])
                    break

    def talk(self):
        self.wish_me()
        while True:
            query = self.recognize_speech().lower()
            if not query:
                continue
            if any(exit_word in query for exit_word in ("exit", "quit", "stop")):
                self.speak("Goodbye!")
                break
            Query(self, self.api_key).query(query)
