import pyttsx3
import speech_recognition as sr
import datetime
import os
import time
import tempfile
from gtts import gTTS
from playsound import playsound
from .queries import Query
from .llm import classify_intent

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
        try:
            tts_audio = gTTS(text=text, lang="en", slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts_audio.write_to_fp(tmp)
                tmp_path = tmp.name
            playsound(tmp_path)
            os.remove(tmp_path)
        except Exception as e:
            print(f"gTTS failed, falling back to pyttsx3: {e}")
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

    def talk(self):
        self.wish_me()
        while True:
            user_text = self.recognize_speech().lower()
            if not user_text:
                continue
            if any(word in user_text for word in ("exit", "quit", "stop")):
                self.speak("Goodbye!")
                break
            intent, params = classify_intent(user_text, self.api_key)
            #print(f"[DEBUG] classify_intent returned -> intent: '{intent}', params: {params}")
            query_handler = Query(self, self.api_key)
            if intent and intent != "fallback":
                normalized = intent.replace("-", "_").lower()
                handler_name = f"handle_{normalized}"
                handler = getattr(query_handler, handler_name, None)
                if callable(handler):
                    try:
                        handler(**params)
                        continue
                    except Exception as e:
                        print(f"[ERROR] Intent handler '{handler_name}' raised: {e}")
                else:
                    print(f"[WARN] No handler found for intent '{intent}' (tried '{handler_name}')")
            query_handler.query(user_text)