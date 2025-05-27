from google import genai
from google.genai import types
import json

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

INTENTS = [
    {"name": "close_browser",   "description": "Closes a browser. Requires 'browser'."},
    {"name": "open_browser",    "description": "Opens a browser. Optional 'search_query'."},
    {"name": "kill_process",    "description": "Kills a process. Requires 'process_name', optional 'mac_name'."},
    {"name": "open_terminal",   "description": "Opens a terminal window. No parameters."},
    {"name": "search_wikipedia","description": "Searches Wikipedia. Requires 'query'."},
    {"name": "analytics",       "description": "Opens YouTube analytics. No parameters."},
    {"name": "search_youtube",  "description": "Searches YouTube. Requires 'query'."},
]

def ai_dialogue(jarvis, api_key: str, prompt: str, max_output_tokens: int = 150, temperature: float = 0.7) -> str:
    """
    Fallback AI dialogue using Google Gemini.
    jarvis: Jarvis instance (for context or future hooks)
    api_key: Google API key
    prompt: user input
    max_output_tokens: maximum number of tokens in the assistant's response
    temperature: sampling temperature to control randomness (lower = more focused)
    Returns the assistant's response.
    """
    jarvis.speak("Thinking...")
    client = genai.Client(api_key=api_key)
    system_prompt = "Please be concise and to the point."
    full_contents = [system_prompt, prompt]
    gen_config = types.GenerateContentConfig(
        max_output_tokens=max_output_tokens,
        temperature=temperature,
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_contents,
        config=gen_config
    )
    return response.text.strip()

def classify_intent(text: str, api_key: str, max_output_tokens: int = 100, temperature: float = 0.0):
    """
    Calls Gemini to map free text into a supported intent or 'fallback'.
    Returns a tuple (intent_name, params_dict).
    """
    client = genai.Client(api_key=api_key)
    system_prompt = "You are an intent classifier. Map the user's command to one of these intents:\n"
    for intent in INTENTS:
        system_prompt += f"- {intent['name']}: {intent['description']}\n"
    system_prompt += (
        "\nRespond ONLY with a valid JSON object with two keys:\n"
        "  intent: one of the names above, or 'fallback'\n"
        "  params: an object with argument names and values (empty {} if none)\n"
        "Do not include any additional text."
    )

    gen_config = types.GenerateContentConfig(
        max_output_tokens=max_output_tokens,
        temperature=temperature,
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[system_prompt, text],
        config=gen_config
    )
    raw = response.text.strip()
    try:
        data = json.loads(raw)
        intent = data.get("intent", "fallback")
        params = data.get("params", {}) or {}
    except Exception:
        intent, params = "fallback", {}
    return intent, params