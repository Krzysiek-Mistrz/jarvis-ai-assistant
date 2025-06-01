# Jarvis Window Assistant

**THIS PACKAGE IS UNDER DEVELOPMENT – ERRORS MAY OCCUR!**

A Python‐based voice assistant framework that listens to your speech, processes commands via Google Gemini (or another AI provider [Open AI API is now paid :(]), and responds using text-to-speech. Designed to be modular, easily extended, and configurable for your own workflows.

## Features

- Voice recognition via `speech_recognition`  
- Text‐to‐speech powered by `pyttsx3` with adjustable rate, volume, and voice  
- AI dialogue integration using Google Gemini (`google-generativeai`)  
- Modular design: separate `core`, `queries` and `llm` modules  
- Easy to configure, extend and replace components

## Requirements

- Python 3.8+  
- See [`requirements.txt`](requirements.txt) for core deps

## Installation

```bash
git clone https://github.com/your-org/jarvis_window_assistant.git
cd jarvis_window_assistant
pip install -r requirements.txt
```

## Configuration

Before running, you must provide your Google Gemini API key -> you just type it to console when it asks u.  
(For devs -> u can just replace input method in main with ur API KEY).  
> **Note**  
> In order to omit some errors you should before using the app do:  
> `export GOOGLE_API_KEY="AIzaSyDvZrWfQlF_SuVgFN9ECw4wmlcvtPw1XZI"`  
> It's not required though...  

## Usage

```bash
python3 main.py
```

1. When prompted, paste your `GOOGLE_API_KEY`.  
2. Jarvis will greet you and enter listening mode.  
3. Speak a command (e.g. “what’s the weather?”, “open browser”, etc.).  
4. Jarvis processes via Google Gemini and tries to make specified action on ur device otherwise responds out loud.  

To stop, interrupt with `Ctrl+C`. U may need to interrupt many times...  

## Available commands

When Jarvis cannot map your speech to an intent fallback happens (I mean jarvis will just treat your query as a question to which it will try to respond), it can still perform local system actions. Below is the full list of commands it supports:

| Command           | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| `wikipedia`       | Searches Wikipedia. Optional `topic`.                         |
| `open_website`    | Searches for a term or website via Google. Prompts for query. |
| `close_browser`   | Closes a browser. Requires `browser`.                         |
| `open_browser`    | Opens a browser. Optional `search_query`.                     |
| `maximize_window` | Maximizes the current window. No parameters.                  |
| `minimize_window` | Minimizes the current window. No parameters.                  |
| `new_window`      | Opens a new browser window/tab. No parameters.                |
| `incognito`       | Opens an incognito/private window. No parameters.             |
| `open_history`    | Opens browser history. No parameters.                         |
| `open_downloads`  | Opens browser downloads. No parameters.                       |
| `prev_tab`        | Switches to previous tab. No parameters.                      |
| `next_tab`        | Switches to next tab. No parameters.                          |
| `close_tab`       | Closes current tab. No parameters.                            |
| `close_window`    | Closes current window. No parameters.                         |
| `clear_history`   | Clears browsing history. No parameters.                       |
| `open_file`       | Opens a file. Requires `filepath`.                            |
| `time`            | Tells the current time. No parameters.                        |
| `shutdown_system` | Shuts down the OS. No parameters.                             |
| `restart_system`  | Restarts the OS. No parameters.                               |
| `sleep`           | Puts assistant to sleep (exit). No parameters.                |
| `open_notepad`    | Opens notepad/TextEdit/gedit. No parameters.                  |
| `close_notepad`   | Closes notepad/TextEdit/gedit. No parameters.                 |
| `open_terminal`   | Opens a terminal. No parameters.                              |
| `close_terminal`  | Closes a terminal. No parameters.                             |
| `open_camera`     | Opens the default webcam stream. No parameters.               |
| `take_screenshot` | Takes a screenshot. Optional `file_name`.                     |
| `calculate`       | Performs a voice-driven calculation. No parameters.           |
| `get_ip`          | Retrieves public IP. No parameters.                           |
| `volume_up`       | Turns volume up. No parameters.                               |
| `volume_down`     | Turns volume down. No parameters.                             |
| `mute`            | Mutes volume. No parameters.                                  |
| `refresh`         | Refreshes the page. No parameters.                            |
| `scroll`          | Scrolls up or down. No parameters (asks user for direction).  |
| `open_paint`      | Opens Paint/GIMP/Pinta. No parameters.                        |
| `close_paint`     | Closes Paint/GIMP/Pinta. No parameters.                       |
| `who_are_you`     | Tells the assistant's name. No parameters.                    |
| `who_created_you` | Tells who created the assistant. No parameters.               |
| `type`            | Types dictated text. Requires `text`.                         |
| `kill_process`    | Kills a process. Requires `proc`, optional `alt`.             |  

## Project Structure

```
jarvis_window_assistant/
├── main.py                   # entry point
├── requirements.txt          # pip dependencies
└── src/
    ├── core.py               # Jarvis class (TTS, ASR, command loop)
    ├── queries.py            # Query dispatcher and action handlers
    └── llm.py           # AI chat integration layer
```

## Customization

- **TTS Settings**  
  In `Jarvis(...)` constructor you can adjust:
  - `rate` (words per minute, default 95 (optimal to type of voice))  
  - `voice` (index into installed voices)  
  - `volume` (0.0–1.0)  

- **AI Model**  
  Swap out the Gemini model (e.g. `chat-bison-001`) or hook in another provider.

- **Commands & Actions**  
  Extend `queries.py` to add new voice commands and automation scripts.

## Contributing

1. Fork the repo  
2. Create a feature branch  
3. Submit a PR for review  

## License

Creative Commons BY-NC-ND 4.0 @ Krzychu 2025