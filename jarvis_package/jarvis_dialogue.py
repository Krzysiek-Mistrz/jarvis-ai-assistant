import speech_recognition as sr
import openai
import pyttsx3
import platform
from jarvis_core.Jarvis import init_tts_engine, recognize_speech

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def ai_dialogue(api_key):
    openai.api_key = api_key
    tts_engine = init_tts_engine()
    while True:
        text = recognize_speech()
        if "exit" not in text:
            print(f"You: {text}")
            response = chat_with_gpt(text)
            print(f"GPT: {response}")
            tts_engine.say(response)
            tts_engine.runAndWait()
        else:
            break