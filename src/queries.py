import wikipedia
import webbrowser
import sys
import pyautogui
import time
import operator
import requests
import cv2
import pywhatkit as kit
import platform
import datetime
import os
import speech_recognition as sr
import subprocess
from pathlib import Path
from .llm import ai_dialogue
from google import genai
from google.genai import types
import re


class Query(object):
    def __init__(self, jarvis, api_key):
        self.jarvis_core = jarvis
        self.api_key = api_key

    def handle_write_code(self):
        self.jarvis_core.speak("What should the code do?")
        goal = self.jarvis_core.recognize_speech()
        if not goal:
            self.jarvis_core.speak("Sorry, I did not catch the goal.")
            return
        self.jarvis_core.speak("Which programming language should I use?")
        language = self.jarvis_core.recognize_speech().lower()
        if not language:
            self.jarvis_core.speak("Sorry, I did not catch the language.")
            return
        client = genai.Client(api_key=self.api_key)
        ext_map = {
            "python": "py", "javascript": "js", "typescript": "ts",
            "java": "java", "c++": "cpp", "c": "c", "c#": "cs",
            "go": "go", "ruby": "rb", "php": "php", "rust": "rs",
            "swift": "swift", "kotlin": "kt"
        }
        system_prompt = "You are an intent programming language classifier. Map the user's specified language to one of these programming languages:\n"
        for lang in ext_map.keys():
            system_prompt += f"- {lang}\n"
        system_prompt += (
            "\nRespond ONLY with a valid string object in qotes selected from the languages above, for example proper response should be like this: \"python\" \n"
            "Do not include any additional text."
        )
        gen_config = types.GenerateContentConfig(
            max_output_tokens=20,
            temperature=0.2,
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=system_prompt,
            config=gen_config
        )
        raw = response.text.strip()
        print('\n',raw[1:-1],'\n')
        ext = ext_map.get(raw[1:-1], language)
        ts = datetime.datetime.now().strftime("%d%H%M")
        filename = f"code_{ts}.{ext}"
        filepath = os.path.join(os.getcwd(), filename)
        system_prompt = "You are a helpful coding assistant. Provide only the code."
        user_prompt = f"Write {language} code that achieves this goal: {goal}."
        gen_config = types.GenerateContentConfig(max_output_tokens=1500, temperature=0.2)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[system_prompt, user_prompt],
            config=gen_config
        )
        code_text = response.text.strip()
        code_text = re.sub(r"\A```[^\n]*\n", "", code_text)
        code_text = re.sub(r"\n```+\s*\Z", "", code_text)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code_text)
        try:
            subprocess.Popen(["code", filepath])
            self.jarvis_core.speak(f"I've created {filename} and opened it in VSCode.")
        except Exception as e:
            self.jarvis_core.speak(f"Created {filename}, but could not open in VSCode: {e}")

    def handle_wikipedia(self, topic: str = None):
        """
        Search Wikipedia for a topic and speak summary.
        """
        self.jarvis_core.speak("Searching Wikipedia...")
        if not topic:
            self.jarvis_core.speak("What should I search on Wikipedia?")
            topic = self.jarvis_core.recognize_speech().lower().strip()
            if not topic:
                self.jarvis_core.speak("Cancelling Wikipedia search.")
                return
        try:
            results = wikipedia.summary(topic, sentences=2)
            self.jarvis_core.speak("According to Wikipedia")
            print(results)
            self.jarvis_core.speak(results)
        except wikipedia.exceptions.WikipediaException:
            self.jarvis_core.speak(f"No info found for '{topic}' on Wikipedia.")

    def handle_open_website(self):
        """look for certain website on browser"""
        try:
            self.jarvis_core.speak("What would you like to search?")
            query = self.jarvis_core.recognize_speech().lower()
            search = query.replace(' ', '+')
            url = f"https://www.google.com/search?q={search}"
            webbrowser.open(url)
        except Exception:
            return

    def handle_close_browser(self, browser: str):
        """
        Closes the given browser by process name.
        browser: name like 'chrome', 'firefox', 'edge', etc.
        """
        sys_os = platform.system()
        name = browser.lower()
        def kill_windows(proc_name):
            os.system(f"taskkill /F /IM {proc_name}")
        def kill_unix(proc_pattern):
            os.system(f"pkill -f {proc_pattern}")
        if name in ("chrome", "google"):
            if sys_os == "Windows":
                kill_windows("chrome.exe")
            else:
                kill_unix("chrome")
        elif name in ("firefox", "mozilla"):
            if sys_os == "Windows":
                kill_windows("firefox.exe")
            else:
                kill_unix("firefox")
        elif name in ("edge", "microsoft edge", "msedge"):
            if sys_os == "Windows":
                kill_windows("msedge.exe")
            elif sys_os == "Darwin":
                kill_unix("Microsoft Edge")
            else:
                kill_unix("msedge")
        else:
            self.jarvis_core.speak(f"I couldn't recognize the browser, sorry")

    def handle_open_browser(self, browser: str, search_query: str = None):
        """
        Opens given browser from name specified by user
        """
        self.jarvis_core.speak("What browser would you like to open?")
        browser = self.jarvis_core.recognize_speech().lower()
        sys_os = platform.system()
        name = browser.lower()
        self.jarvis_core.speak("What would you like to watch?")
        search_query = self.jarvis_core.recognize_speech().lower()
        try:
            if name == "chrome":
                if sys_os == "Windows":
                    os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
                elif sys_os == "Darwin":
                    subprocess.check_call(["open", "-a", "Google Chrome"])
                else:
                    subprocess.check_call(["google-chrome"])
            elif name in ("firefox", "mozilla"):
                if sys_os == "Windows":
                    os.startfile(r"C:\Program Files\Mozilla Firefox\firefox.exe")
                elif sys_os == "Darwin":
                    subprocess.check_call(["open", "-a", "Firefox"])
                else:
                    subprocess.check_call(["firefox"])
            elif name in ("edge", "msedge", "microsoft edge"):
                if sys_os == "Windows":
                    os.startfile(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
                elif sys_os == "Darwin":
                    subprocess.check_call(["open", "-a", "Microsoft Edge"])
                else:
                    subprocess.check_call(["msedge"])
            elif name == "safari":
                if sys_os == "Darwin":
                    subprocess.check_call(["open", "-a", "Safari"])
                else:
                    raise RuntimeError("Safari jest dostępne tylko na macOS")
            else:
                raise ValueError(f"Selected browser is yet unsupported, sorry: {browser}")
            if search_query:
                url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                webbrowser.open(url)
        except Exception as e:
            self.jarvis_core.speak(f"I couldn't open the browser, sorry, error message is: {e}")

    def handle_maximize_window(self):
        pyautogui.hotkey('alt','space'); time.sleep(0.5); pyautogui.press('x')

    def handle_minimize_window(self):
        pyautogui.hotkey('alt','space'); time.sleep(0.5); pyautogui.press('n')

    def handle_new_window(self):
        pyautogui.hotkey('ctrl','n')

    def handle_incognito(self):
        pyautogui.hotkey('ctrl','shift','n'); pyautogui.hotkey('ctrl', 'shift', 'p')

    def handle_open_history(self):
        pyautogui.hotkey('ctrl','h')

    def handle_open_downloads(self):
        pyautogui.hotkey('ctrl','j')

    def handle_prev_tab(self):
        pyautogui.hotkey('ctrl','shift','tab')

    def handle_next_tab(self):
        pyautogui.hotkey('ctrl','tab')

    def handle_close_tab(self):
        key = 'command' if platform.system()=='Darwin' else 'ctrl'
        self.jarvis_core.speak('Closing current tab')
        pyautogui.hotkey(key,'w')

    def handle_close_window(self):
        pyautogui.hotkey('ctrl','shift','w')

    def handle_clear_history(self):
        pyautogui.hotkey('ctrl','shift','delete')

    def handle_open_file(self):
        self.jarvis_core.speak('give me your filepath')
        filepath = self.jarvis_core.recognize_speech().lower()
        path = Path(filepath).expanduser()
        if not path.exists():
            self.jarvis_core.speak("I couldn't locate the file, sorry")
            return
        if not os.access(path, os.R_OK):
            self.jarvis_core.speak("I don't have sufficient permissions to open this file, sorry")
            return
        sys_os = platform.system()
        if sys_os == "Windows":
            os.startfile(filepath)
        elif sys_os == "Darwin":
            subprocess.call(["open", filepath])
        else:
            subprocess.call(["xdg-open", filepath])

    def handle_time(self):
        now = datetime.datetime.now().strftime('%H:%M:%S')
        self.jarvis_core.speak(f"The time is {now}")

    def handle_shutdown_system(self):
        self.jarvis_core.speak("Shutting down")
        cmd = {'Windows':'shutdown /s /t 5','Darwin':'sudo shutdown -h now'}.get(platform.system(),'shutdown -h now')
        os.system(cmd)

    def handle_restart_system(self):
        self.jarvis_core.speak("Restarting")
        cmd = {'Windows':'shutdown /r /t 5','Darwin':'sudo shutdown -r now'}.get(platform.system(),'shutdown -r now')
        os.system(cmd)

    def handle_sleep(self):
        self.jarvis_core.speak("Switching off"); sys.exit()

    def handle_open_notepad(self):
        os_cmd = platform.system()
        if os_cmd=='Windows': pyautogui.hotkey('win'); time.sleep(1); pyautogui.write('notepad'); pyautogui.press('enter')
        elif os_cmd=='Darwin': subprocess.call(["open","-a","TextEdit"]);
        else: subprocess.call(["gedit"])

    def handle_close_notepad(self):
        if platform.system()=='Windows': self.handle_kill_process('notepad.exe')
        elif platform.system()=='Darwin': self.handle_kill_process('TextEdit','TextEdit')
        else: self.handle_kill_process('gedit')

    def handle_open_terminal(self):
        if platform.system()=='Windows': os.system('start cmd')
        elif platform.system()=='Darwin': subprocess.call(["open","-a","Terminal"])
        else:
            for t in ('gnome-terminal','konsole','x-terminal-emulator'):
                if os.system(f"which {t} > /dev/null")==0:
                    subprocess.Popen([t]); break

    def handle_close_terminal(self):
        if platform.system()=='Windows': self.handle_kill_process('cmd.exe')
        elif platform.system()=='Darwin': self.handle_kill_process('Terminal','Terminal')
        else: self.handle_kill_process('gnome-terminal')

    def handle_open_camera(self):
        cap=cv2.VideoCapture(0)
        if not cap.isOpened(): self.jarvis_core.speak("Cannot open camera"); return
        while True:
            ret,frame=cap.read(); cv2.imshow('cam',frame)
            if cv2.waitKey(50)==27: break
        cap.release(); cv2.destroyAllWindows()

    def handle_take_screenshot(self):
        self.jarvis_core.speak("tell me a name for the file")
        file_name = self.jarvis_core.recognize_speech().lower()
        self.jarvis_core.speak("Taking screenshot")
        time.sleep(1)
        img=pyautogui.screenshot(); img.save(f"{file_name}.png")
        self.jarvis_core.speak(f"Saved as {file_name}.png")

    def handle_calculate(self, expression: str):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.jarvis_core.speak("ready")
            print("listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            calculation = recognizer.recognize_google(audio)
            print(calculation)
        except Exception as e:
            self.jarvis_core.speak("could not understand calculation")
        def get_operator_fn(op):
            return {
                '+' : operator.add,
                '-' : operator.sub,
                'x' : operator.mul,
                'divided' : operator.__truediv__,
            }[op]
        def eval_binary_expr(op1, oper, op2):
            op1, op2 = int(op1), int(op2)
            return get_operator_fn(oper)(op1, op2)
        try:
            result = eval_binary_expr(*(calculation.split()))
            self.jarvis_core.speak("your result is")
            self.jarvis_core.speak(result)
        except Exception as e:
            self.jarvis_core.speak("calculation error")

    def handle_get_ip(self):
        self.jarvis_core.speak("Checking IP...")
        try:
            ip=requests.get('https://api.ipify.org',timeout=5).text
            self.jarvis_core.speak(f"Your IP is {ip}")
        except Exception:
            self.jarvis_core.speak("Cannot retrieve IP")

    def handle_volume_up(self):
        self.jarvis_core.speak("Volume up")
        for _ in range(10): pyautogui.press('volumeup')

    def handle_volume_down(self):
        self.jarvis_core.speak("Volume down")
        for _ in range(10): pyautogui.press('volumedown')

    def handle_mute(self):
        self.jarvis_core.speak("Muting")
        pyautogui.press('volumemute')

    def handle_refresh(self):
        key='command' if platform.system()=='Darwin' else 'f5'
        pyautogui.press(key)

    def handle_scroll(self):
        try:
            self.jarvis_core.speak("Do you want me to scroll down or up?")
            decision = self.jarvis_core.recognize_speech().lower()
            if decision == "up": pyautogui.scroll(500) 
            elif decision == "down": pyautogui.scroll(-500)
            else: self.jarvis_core.speak("Couldn't recognize whether to scroll up or down, please try again")
        except Exception:
            return

    def handle_open_paint(self):
        try:
            os_cmd=platform.system()
            if os_cmd=='Windows': os.startfile(r"C:\Windows\System32\mspaint.exe")
            elif os_cmd=='Darwin': subprocess.call(["open","-a","Paintbrush"])
            else:
                if subprocess.call(["which","pinta"],stdout=subprocess.DEVNULL)==0: subprocess.call(["pinta"])
                else: subprocess.call(["gimp"])
        except Exception:
            return

    def handle_close_paint(self):
        if platform.system()=='Windows': self.handle_kill_process('mspaint.exe')
        elif platform.system()=='Darwin': self.handle_kill_process('Paintbrush','Paintbrush')
        else:
            if subprocess.call(["pgrep","pinta"],stdout=subprocess.DEVNULL)==0: self.handle_kill_process('pinta')
            else: self.handle_kill_process('gimp')

    def handle_who_are_you(self):
        self.jarvis_core.speak("My name is Six. I do what I'm programmed to.")

    def handle_who_created_you(self):
        self.jarvis_core.speak("I was created by Krzychu in Python.")

    def handle_ai_dialogue(self):
        ai_dialogue(api_key=self.api_key)

    def handle_type(self, text: str):
        self.jarvis_core.speak("Please tell me what to write")
        text_to_type = self.jarvis_core.recognize_speech().lower()
        try:
            pyautogui.write(text_to_type)
            self.jarvis_core.speak(f"I wrote: {text_to_type}")
        except Exception as e:
            self.jarvis_core.speak(f"I couldn't write the text, sorry: {e}")

    def handle_kill_process(self, proc: str, alt: str=None):
        if platform.system()=='Windows': os.system(f"taskkill /F /IM {proc}")
        else: os.system(f"killall {alt or proc}")

    def query(self, text: str):
        """Fallback handler when no intent matches."""
        response = ai_dialogue(self.jarvis_core, self.api_key, text)
        self.jarvis_core.speak(response)
