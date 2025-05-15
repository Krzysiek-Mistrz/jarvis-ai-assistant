# Jarvis Window Assistant

**THIS PACKAGE IS UNDER DEVELOPMENT – ERRORS MAY OCCUR!**

A Python‐based voice assistant framework that listens to your speech, processes commands via Google Gemini (or another AI provider [Open AI API is now paid :(]), and responds using text-to-speech. Designed to be modular, easily extended, and configurable for your own workflows.

## Features

- Voice recognition via `speech_recognition`  
- Text‐to‐speech powered by `pyttsx3` with adjustable rate, volume, and voice  
- AI dialogue integration using Google Gemini (`google-generativeai`)  
- Modular design: separate `core`, `queries` and `dialogue` modules  
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

## Usage

```bash
python3 main.py
```

1. When prompted, paste your `GOOGLE_API_KEY`.  
2. Jarvis will greet you and enter listening mode.  
3. Speak a command (e.g. “what’s the weather?”, “open browser”, etc.).  
4. Jarvis processes via Google Gemini and responds out loud.  

To stop, interrupt with `Ctrl+C`. U may need to interrupt many times...  

## Project Structure

```
jarvis_window_assistant/
├── main.py                   # entry point
├── requirements.txt          # pip dependencies
└── src/
    ├── core.py               # Jarvis class (TTS, ASR, command loop)
    ├── queries.py            # Query dispatcher and action handlers
    └── dialogue.py           # AI chat integration layer
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

GNU GPL V3 @ Krzychu 2025