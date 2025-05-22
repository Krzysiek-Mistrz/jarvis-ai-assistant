from google import genai
from google.genai import types

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