from google import genai
from google.genai import types
import json
import ast
import shutil
from importlib import reload
import os
import textwrap
from . import llm
from . import queries

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
    {"name": "write_code",       "description": "Generates code for a specified goal in the user-specified programming language."},
    {"name": "ai_dialogue",      "description": "talks with user on any topic if user asks to talk or speak about something. Requires 'prompt'"}
]

def classify_intent(text: str, api_key: str, max_output_tokens: int = 100, temperature: float = 0.0):
    """
    Calls Gemini to map free text into a supported intent or 'fallback'.
    Returns a tuple (intent_name, params_dict).
    """
    client = genai.Client(api_key=api_key)
    system_prompt = "You are an intent classifier. Map the user's command to one of these intents (IF THERE IS NO PROPER INTENT JUST PUT 'fallback' IN INTENT):\n"
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
    if intent == "fallback":
            name, desc = generate_new_intent(text, api_key)
            add_intent_to_llm("./src/llm.py", name, desc)
            reload(llm)
            add_handler_to_queries("./src/queries.py", api_key, name, desc)
            reload(queries)
            return name, {}
    return intent, params

def generate_new_intent(command: str, api_key: str, max_output_tokens: int = 150, temperature: float = 0.0) -> tuple[str, str]:
    """
    We simulate using Google Gemini (genai) to generate a name and description for a new intent
    based on a user command
    """
    client = genai.Client(api_key=api_key)
    prompt = f"User said: '{command}'. How would you name an intent in keyword form (snake_case) and provide its description? Please return intent and description in this format: intent:description (for example: 'draw_something:The user has requested the AI to generate an image.')."
    gen_config = types.GenerateContentConfig(
        max_output_tokens=max_output_tokens,
        temperature=temperature,
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt],
        config=gen_config
    )
    print('\n',response,'\n')
    response = response.text.strip()
    try:
        intent_name, intent_description = response.split(":", 1)
    except ValueError:
        intent_name = "new_intent"
        intent_description = "No description provided."
    intent_name = intent_name.strip()
    intent_description = intent_description.strip()
    intent_name = intent_name.replace(" ", "_").lower()
    return intent_name, intent_description

def add_intent_to_llm(llm_path: str, intent_name: str, intent_description: str):
    """
    Adds a new intent (a dictionary of 'name' and 'description') to 
    the INTENTS list in llm.py. If the intent exists, do nothing.
    """
    with open(llm_path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "INTENTS":
                    intents_list = node.value
                    if not isinstance(intents_list, ast.List):
                        raise ValueError("INTENTS is not a list")
                    for elt in intents_list.elts:
                        if isinstance(elt, ast.Dict):
                            keys = [k.value for k in elt.keys if isinstance(k, ast.Constant)]
                            values = [v.value for v in elt.values if isinstance(v, ast.Constant)]
                            if "name" in keys:
                                idx = keys.index("name")
                                existing_name = values[idx] if idx < len(values) else None
                                if existing_name == intent_name:
                                    print(f"Intent '{intent_name}' already exists in llm.py. Cannot add a duplicate.")
                                    return
                    new_intent_dict = ast.Dict(
                        keys=[ast.Constant(value="name"), ast.Constant(value="description")],
                        values=[ast.Constant(value=intent_name), ast.Constant(value=intent_description)]
                    )
                    intents_list.elts.append(new_intent_dict)
                    new_code = ast.unparse(tree)
                    backup_path = llm_path + ".bak"
                    if not os.path.exists(backup_path):
                        shutil.copy(llm_path, backup_path)
                    with open(llm_path, "w", encoding="utf-8") as f:
                        f.write(new_code)
                    print(f"Intent added '{intent_name}' to llm.py.")
                    return
    raise RuntimeError("Cannot find INTENTS in llm.py")

def add_handler_to_queries(queries_path: str, api_key : str, intent_name: str, intent_description: str):
    """
    Adds a new method handle_<intent_name> to the Query class in queries.py. 
    If the method exists, it does nothing.
    """
    with open(queries_path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == "Query":
            method_name = f"handle_{intent_name}"
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    print(f"Handler {method_name} already exists in Query class. Nothing to add.")
                    return
            client = genai.Client(api_key=api_key)
            prompt = (
                f"""Please implement in Python the following method for class Query:
            def handle_{intent_name}(self, **params):
                \"\"\"{intent_description}\"\"\"
                # your code here

            It should perform the action described in the intent. Write only valid Python code for that method."""
            )
            gen_config = types.GenerateContentConfig(
                max_output_tokens=1000,
                temperature=0.2,
            )
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt],
                config=gen_config
            )
            print('\n',response,'\n')
            handler_code = response.text.strip()
            if handler_code.startswith("```"):
                lines = handler_code.splitlines()
                if lines and lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                handler_code = "\n".join(lines)
            handler_code = textwrap.dedent(handler_code)
            try:
                new_handler_ast = ast.parse(handler_code).body[0]
            except SyntaxError as e:
                raise RuntimeError(f"LLM generated incorrect code handler method\n{e}\nCode:\n{handler_code}")
            node.body.append(new_handler_ast)
            new_code = ast.unparse(tree)
            backup_path = queries_path + ".bak"
            if not os.path.exists(backup_path):
                shutil.copy(queries_path, backup_path)
            with open(queries_path, "w", encoding="utf-8") as f:
                f.write(new_code)
            print(f"Added handler '{method_name}' to Query class in queries.py.")
            return
    raise RuntimeError("Cannot find Query class in queries.py")