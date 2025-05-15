import speech_recognition as sr
from google import genai
import pyttsx3
import platform

# TODO
# Implement functuion to open external cli to chat with jarvis
# def chat_with_gpt(prompt: str, api_key: str) -> str:
#     """
#     Simple one-off chat using Google Gemini.
#     """
#     client = genai.Client(api_key=api_key)
#     response = client.models.generate_content(
#         model="gemini-2.0-flash",
#         contents=[prompt]
#     )
#     return response.text

def ai_dialogue(jarvis, api_key: str, prompt: str) -> str:
    """
    Fallback AI dialogue using Google Gemini.
    jarvis: Jarvis instance (for context or future hooks)
    api_key: Google API key
    prompt: user input
    Returns the assistant's response.
    """
    jarvis.speak("Thinking...")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    assistant_text = response.text
    return assistant_text