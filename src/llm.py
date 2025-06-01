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
    {"name": "wikipedia",        "description": "Searches Wikipedia. Optional 'topic'."},
    {"name": "open_website",     "description": "Searches for a term or website via Google. No params (asks user)."},
    {"name": "close_browser",    "description": "Closes a browser. Requires 'browser'."},
    {"name": "open_browser",     "description": "Opens a browser. Optional 'search_query'."},
    {"name": "maximize_window",  "description": "Maximizes the current window. No parameters."},
    {"name": "minimize_window",  "description": "Minimizes the current window. No parameters."},
    {"name": "new_window",       "description": "Opens a new browser window/tab. No parameters."},
    {"name": "incognito",        "description": "Opens an incognito/private window. No parameters."},
    {"name": "open_history",     "description": "Opens browser history. No parameters."},
    {"name": "open_downloads",   "description": "Opens browser downloads. No parameters."},
    {"name": "prev_tab",         "description": "Switches to previous tab. No parameters."},
    {"name": "next_tab",         "description": "Switches to next tab. No parameters."},
    {"name": "close_tab",        "description": "Closes current tab. No parameters."},
    {"name": "close_window",     "description": "Closes current window. No parameters."},
    {"name": "clear_history",    "description": "Clears browsing history. No parameters."},
    {"name": "open_file",        "description": "Opens a file. Requires 'filepath'."},
    {"name": "time",             "description": "Tells the current time. No parameters."},
    {"name": "shutdown_system",  "description": "Shuts down the OS. No parameters."},
    {"name": "restart_system",   "description": "Restarts the OS. No parameters."},
    {"name": "sleep",            "description": "Puts assistant to sleep (exit). No parameters."},
    {"name": "open_notepad",     "description": "Opens notepad/TextEdit/gedit. No parameters."},
    {"name": "close_notepad",    "description": "Closes notepad/TextEdit/gedit. No parameters."},
    {"name": "open_terminal",    "description": "Opens a terminal. No parameters."},
    {"name": "close_terminal",   "description": "Closes a terminal. No parameters."},
    {"name": "open_camera",      "description": "Opens the default webcam stream. No parameters."},
    {"name": "take_screenshot",  "description": "Takes a screenshot. Optional 'file_name'."},
    {"name": "calculate",        "description": "Performs a voice-driven calculation. No parameters."},
    {"name": "get_ip",           "description": "Retrieves public IP. No parameters."},
    {"name": "volume_up",        "description": "Turns volume up. No parameters."},
    {"name": "volume_down",      "description": "Turns volume down. No parameters."},
    {"name": "mute",             "description": "Mutes volume. No parameters."},
    {"name": "refresh",          "description": "Refreshes the page. No parameters."},
    {"name": "scroll",           "description": "Scrolls up or down. No parameters (asks user)."},
    {"name": "open_paint",       "description": "Opens Paint/GIMP/Pinta. No parameters."},
    {"name": "close_paint",      "description": "Closes Paint/GIMP/Pinta. No parameters."},
    {"name": "who_are_you",      "description": "Tells the assistant's name. No parameters."},
    {"name": "who_created_you",  "description": "Tells who created the assistant. No parameters."},
    {"name": "type",             "description": "Types dictated text. Requires 'text'."},
    {"name": "kill_process",     "description": "Kills a process. Requires 'proc', optional 'alt'."},
    {"name": "write_code",       "description": "Generates code for a specified goal in the user-specified programming language."}
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
        "  intent: one of the handler method names above (example: 'kill_process' or 'volume_down'), or 'fallback'\n"
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
    print('\n',response,'\n')
    raw = response.text.strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    try:
        data = json.loads(raw)
        print('\n',data,'\n')
        intent = data.get("intent", "fallback")
        params = data.get("params", {}) or {}
    except Exception:
        intent, params = "fallback", {}
    return intent, params