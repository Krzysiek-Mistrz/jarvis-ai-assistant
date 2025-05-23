import wikipedia
import webbrowser
import sys
import pyautogui
import time
import operator
import requests
import random
import cv2
import pywhatkit as kit
import platform
import datetime
import os
import speech_recognition as sr
import subprocess
from pathlib import Path
import re
from .dialogue import ai_dialogue
        

class Query(object):
    def __init__(self, jarvis, api_key):
        self.jarvis_core = jarvis
        self.api_key = api_key

    def close_browser(self, browser: str):
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

    def open_browser(self, browser: str, search_query: str = None):
        """
        Opens given browser from name specified by user
        """
        sys_os = platform.system()
        name = browser.lower()
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

    def kill_process(self, process_name: str, mac_name: str = None):
        sys_os = platform.system()
        if sys_os == "Windows":
            os.system(f"taskkill /F /IM {process_name}")
        elif sys_os == "Darwin":
            name = mac_name or process_name
            os.system(f"killall {name}")
        else:
            os.system(f"pkill -f {process_name}")

    def open_terminal(self):
        sys_os = platform.system()
        if sys_os == "Windows":
            os.system("start cmd")
        elif sys_os == "Darwin":
            subprocess.call(["open", "-a", "Terminal"])
        else:
            for term in ["gnome-terminal", "konsole", "x-terminal-emulator"]:
                if os.system(f"which {term} > /dev/null 2>&1") == 0:
                    subprocess.Popen([term])
                    break

    def query(self, query):
            if 'wikipedia' in query:
                self.jarvis_core.speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "", 1).strip()
                if not query:
                    self.jarvis_core.speak("What should I search on Wikipedia?")
                    query = self.jarvis_core.recognize_speech().lower().strip()
                    if not query:
                        self.jarvis_core.speak("Sorry, I didn't catch a topic. Cancelling Wikipedia search.")
                        return
                try:
                    results = wikipedia.summary(query, sentences=2)
                    self.jarvis_core.speak("According to Wikipedia")
                    print(results)
                    self.jarvis_core.speak(results)
                except wikipedia.exceptions.WikipediaException:
                    self.jarvis_core.speak(f"Sorry, I couldn't find information on Wikipedia for '{query}'.")
                return

            elif "analytics" in query:
                webbrowser.open("https://studio.youtube.com/channel/")
                return

            elif 'search on youtube' in query:
                query = query.replace("search on youtube", "").strip()
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                return

            elif 'open youtube' in query:
                self.jarvis_core.speak("what would you like to watch?")
                search_query = self.jarvis_core.recognize_speech().lower()
                kit.playonyt(search_query)
                return

            elif query.startswith('close '):
                m = re.match(r'close\s+(\w+)', query)
                if m:
                    browser = m.group(1).lower()
                    aliases = {
                        'mozilla': 'firefox',
                        'msedge': 'edge',
                        'chrome': 'google',
                    }
                    browser = aliases.get(browser, browser)
                    self.jarvis_core.speak(f"Closing {browser}")
                    self.close_browser(browser)
                    return
                else:
                    self.jarvis_core.speak("I couldn't understand which browser to close, sorry")
                    return

            elif query.startswith('open '):
                m = re.match(r'open\s+(\w+)', query)
                if m:
                    browser = m.group(1).lower()
                    aliases = {
                        'mozilla': 'firefox',
                        'msedge': 'edge',
                        'google': 'chrome',
                        'browser': 'chrome',
                    }
                    browser = aliases.get(browser, browser)
                    self.jarvis_core.speak(f"What should I search in {browser}?")
                    search_query = self.jarvis_core.recognize_speech().strip()
                    if not search_query:
                        search_query = None
                    self.open_browser(browser, search_query)
                    return
                else:
                    self.jarvis_core.speak("I couldn't understand which browser to open, sorry")
                    return

            elif 'maximize' in query and 'window' in query:
                pyautogui.hotkey('alt', 'space')
                time.sleep(1)
                pyautogui.press('x')
                return

            elif 'minimise' in query and 'window' in query:
                pyautogui.hotkey('alt', 'space')
                time.sleep(1)
                pyautogui.press('n')
                return

            elif 'search' in query and ('browser' in query or 'google' in query or 'firefox' in query or 'edge' in query or 'youtube' in query):
                query = query.replace("search", "").strip()
                pyautogui.hotkey('alt', 'd')
                time.sleep(0.5)
                pyautogui.write(query, interval=0.1)
                pyautogui.press('enter')
                return

            elif 'open' and ('window' in query or 'new' in query):
                pyautogui.hotkey('ctrl', 'n')
                return

            elif 'open' in query and 'incognito' in query:
                pyautogui.hotkey('ctrl', 'shift', 'n')
                pyautogui.hotkey('ctrl', 'shift', 'p')
                return

            elif 'open' in query and 'history' in query:
                pyautogui.hotkey('ctrl', 'h')
                return

            elif 'open' in query and 'download' in query:
                pyautogui.hotkey('ctrl', 'j')
                return

            elif 'previous' in query and 'tab' in query:
                pyautogui.hotkey('ctrl', 'shift', 'tab')
                return

            elif 'next' in query and 'tab' in query:
                pyautogui.hotkey('ctrl', 'tab')
                return

            elif 'close' in query and 'tab' in query:
                self.jarvis_core.speak("closing current tab")
                sys_os = platform.system()
                if sys_os == "Darwin":
                    pyautogui.hotkey('command', 'w')
                else:
                    pyautogui.hotkey('ctrl', 'w')
                return

            elif 'close' in query and 'window' in query:
                pyautogui.hotkey('ctrl', 'shift', 'w')
                return

            elif 'clear' in query and ('browsing' in query or 'history' in query):
                pyautogui.hotkey('ctrl', 'shift', 'delete')
                return

            elif 'open' in query and ('file' in query or 'music' in query):
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

            elif 'time' in query:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                self.jarvis_core.speak(f"the time is {current_time}")
                return

            elif 'shut down' in query and 'system' in query:
                self.jarvis_core.speak("shutting down the system")
                sys_os = platform.system()
                if sys_os == "Windows":
                    os.system("shutdown /s /t 5")
                elif sys_os == "Darwin":
                    os.system("sudo shutdown -h now")
                else:
                    os.system("shutdown -h now")

            elif "restart the system" in query:
                self.jarvis_core.speak("restarting the system")
                sys_os = platform.system()
                if sys_os == "Windows":
                    os.system("shutdown /r /t 5")
                elif sys_os == "Darwin":
                    os.system("sudo shutdown -r now")
                else:
                    os.system("shutdown -r now")
            
            elif "close notepad" in query:
                self.jarvis_core.speak("closing text editor")
                sys_os = platform.system()
                if sys_os == "Windows":
                    self.kill_process("notepad.exe")
                elif sys_os == "Darwin":
                    self.kill_process("TextEdit", "TextEdit")
                else:
                    self.kill_process("gedit")

            elif "open notepad" in query:
                sys_os = platform.system()
                if sys_os == "Windows":
                    pyautogui.hotkey('win')
                    time.sleep(1)
                    pyautogui.write('notepad')
                    time.sleep(1)
                    pyautogui.press('enter')
                    time.sleep(1)
                    return
                elif sys_os == "Darwin":
                    subprocess.call(["open", "-a", "TextEdit"])
                    time.sleep(2)
                    return
                else:
                    subprocess.call(["gedit"])
                    time.sleep(2)
                    return

            elif "open" in query and ("command prompt" in query or "cmd" in query):
                self.jarvis_core.speak("opening terminal")
                self.jarvis_core.open_terminal()
                return

            elif "close" in query and ("command" in query or "cmd" in query):
                self.jarvis_core.speak("closing terminal")
                sys_os = platform.system()
                if sys_os == "Windows":
                    self.jarvis_core.kill_process("cmd.exe")
                elif sys_os == "Darwin":
                    self.jarvis_core.kill_process("Terminal", "Terminal")
                else:
                    for term in ["gnome-terminal", "konsole", "x-terminal-emulator"]:
                        self.jarvis_core.kill_process(term)
                return

            elif "open" in query and "camera" in query:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    self.jarvis_core.speak("Couldn't open default camera")
                    return
                while True:
                    ret, frame = cap.read()
                    cv2.imshow('webcam', frame)
                    if cv2.waitKey(50) == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
                return

            elif "go" in query and "sleep" in query:
                self.jarvis_core.speak("alright then, i am switching off")
                sys.exit()

            elif "take" in query and "screenshot" in query:
                self.jarvis_core.speak("tell me a name for the file")
                file_name = self.jarvis_core.recognize_speech().lower()
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{file_name}.png")
                self.jarvis_core.speak("screenshot saved")
                return

            elif "calculate" in query:
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    self.jarvis_core.speak("ready")
                    print("listening...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                try:
                    calculation = recognizer.recognize_google(audio)
                    print(calculation)
                    return
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
                    return
                except Exception as e:
                    self.jarvis_core.speak("calculation error")

            elif "what" in query and "ip" in query:
                self.jarvis_core.speak("Checking your public IP address…")
                try:
                    response = requests.get('https://api.ipify.org', timeout=5)
                    response.raise_for_status()
                    ip_address = response.text.strip()
                    self.jarvis_core.speak(f"Your IP address is {ip_address}")
                except requests.Timeout:
                    self.jarvis_core.speak("Request timed out. Please check your connection and try again.")
                except requests.RequestException as e:
                    self.jarvis_core.speak("Could not retrieve IP address right now. Please try again later.")
                    print(f"[ERROR] IP lookup failed: {e}")
                return

            elif "volume up" in query:
                self.jarvis_core.speak("Turning volume up")
                for _ in range(16):
                    pyautogui.press("volumeup")
                return

            elif "volume" in query and "down" in query:
                self.jarvis_core.speak("Turning volume down")
                for _ in range(16):
                    pyautogui.press("volumedown")
                return

            elif "mute" in query:
                self.jarvis_core.speak("Muting volume")
                pyautogui.press("volumemute")
                return

            elif "refresh" in query:
                try:
                    if self.sys_os == "Darwin":
                        pyautogui.hotkey('command', 'r')
                    else:
                        pyautogui.press('f5')
                except Exception as e:
                    self.jarvis_core.speak(f"Could not refresh: {e}")
                    return

            elif "scroll down" in query:
                try:
                    pyautogui.scroll(1000)
                    return
                except Exception as e:
                    self.jarvis_core.speak(f"Scrolling failed, error: {e}")
                    return

            elif "open paint" in query:
                try:
                    if self.sys_os == "Windows":
                        os.startfile(r"C:\Windows\System32\mspaint.exe")
                    elif self.sys_os == "Darwin":
                        subprocess.check_call(["open", "-a", "Paintbrush"])
                    else:
                        if subprocess.call(["which", "pinta"], stdout=subprocess.DEVNULL) == 0:
                            subprocess.check_call(["pinta"])
                        else:
                            subprocess.check_call(["gimp"])
                except Exception as e:
                    self.jarvis_core.speak(f"Could not open paint, error: {e}")

            elif "close paint" in query:
                try:
                    if self.sys_os == "Windows":
                        self.jarvis_core.kill_process("mspaint.exe")
                    elif self.sys_os == "Darwin":
                        self.jarvis_core.kill_process("Paintbrush", "Paintbrush")
                    else:
                        if subprocess.call(["pgrep", "pinta"], stdout=subprocess.DEVNULL) == 0:
                            self.jarvis_core.kill_process("pinta")
                        else:
                            self.jarvis_core.kill_process("gimp")
                except Exception as e:
                    self.jarvis_core.speak(f"Could not close paint: {e}")

            elif "who are you" in query:
                print("my name is six")
                self.jarvis_core.speak("my name is six")
                print("i can do everything that my creator programmed me to do")
                self.jarvis_core.speak("i can do everything that my creator programmed me to do")
                return

            elif "who created you" in query:
                print("i was created with python language by krzychu in visual studio code.")
                self.jarvis_core.speak("i was created with python language by krzychu in visual studio code.")
                return

            elif "I" in query and "talk" in query:
                ai_dialogue(api_key=self.api_key)
                return

            elif 'type' in query:
                self.jarvis_core.speak("Please tell me what to write")
                text_to_type = self.jarvis_core.recognize_speech().lower()
                try:
                    pyautogui.write(text_to_type)
                    self.jarvis_core.speak(f"I wrote: {text_to_type}")
                    return
                except Exception as e:
                    self.jarvis_core.speak(f"I couldn't write the text, sorry: {e}")
                    return

            response = ai_dialogue(self.jarvis_core, self.api_key, query)
            self.jarvis_core.speak(response)
