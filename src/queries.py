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
from .dialogue import ai_dialogue
        

class Query(object):
    def __init__(self, jarvis, api_key):
        self.jarvis_core = jarvis
        self.api_key = api_key

    def close_browser(self, browser: str):
        """
        Closes the given browser by process name.
        browser: name like 'chrome', 'firefox', etc.
        """
        sys_os = platform.system()
        name = browser.lower()
        if name == "chrome":
            if sys_os == "Windows":
                os.system("taskkill /F /IM chrome.exe")
            else:
                os.system("pkill chrome")
        elif name in ("firefox", "mozilla"):
            if sys_os == "Windows":
                os.system("taskkill /F /IM firefox.exe")
            else:
                os.system("pkill firefox")

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

            elif 'close chrome' in query:
                self.jarvis_core.speak("closing chrome")
                sys_os = platform.system()
                if sys_os == "Windows":
                    self.jarvis_core.kill_process("chrome.exe")
                    return
                elif sys_os == "Darwin":
                    self.jarvis_core.kill_process("Google Chrome", "Google Chrome")
                    return
                else:
                    self.jarvis_core.kill_process("chrome")
                    return
                
            elif 'close mozilla' in query or 'close firefox' in query:
                self.close_browser('firefox')
                return

            elif 'open google' in query or 'open chrome' in query or 'open browser' in query:
                sys_os = platform.system()
                self.jarvis_core.speak("what should i search?")
                search_query = self.jarvis_core.recognize_speech().lower()
                if sys_os == "Windows":
                    os.startfile(r"C:\Program Files\Mozilla Firefox\firefox.exe")
                elif sys_os == "Darwin":
                    self.jarvis_core.speak("I haven't found google but I found something instead")
                    subprocess.call(["open", "-a", "Firefox"])
                else:
                    self.jarvis_core.speak("I haven't found google but I found something instead")
                    subprocess.call(["firefox"])
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
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
                    self.jarvis_core.kill_process("notepad.exe")
                elif sys_os == "Darwin":
                    self.jarvis_core.kill_process("TextEdit", "TextEdit")
                else:
                    self.jarvis_core.kill_process("gedit")

            elif "open" in query and ("command prompt" in query or "cmd" in query):
                self.jarvis_core.speak("opening terminal")
                self.jarvis_core.open_terminal()
                return

            elif "close command prompt" in query:
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

            elif "open camera" in query:
                # open the webcam and display the video feed
                cap = cv2.VideoCapture(0)
                while True:
                    ret, frame = cap.read()
                    cv2.imshow('webcam', frame)
                    # exit loop when esc key is pressed
                    if cv2.waitKey(50) == 27:
                        break
                cap.release()
                cv2.destroyAllWindows()
                return

            elif "go to sleep" in query:
                self.jarvis_core.speak("alright then, i am switching off")
                sys.exit()

            elif "take screenshot" in query:
                self.jarvis_core.speak("tell me a name for the file")
                file_name = self.jarvis_core.recognize_speech().lower()
                time.sleep(3)
                img = pyautogui.screenshot()
                img.save(f"{file_name}.png")
                self.jarvis_core.speak("screenshot saved")
                return

            elif "calculate" in query:
                # listen for a calculation command and compute the result
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

            elif "what is my ip address" in query:
                self.jarvis_core.speak("checking")
                try:
                    ip_address = requests.get('https://api.ipify.org').text
                    print(ip_address)
                    self.jarvis_core.speak("your ip address is")
                    self.jarvis_core.speak(ip_address)
                    return
                except Exception as e:
                    self.jarvis_core.speak("network is weak, please try again later")

            elif "volume up" in query:
                # increase system volume; note that key names may vary by os
                for _ in range(16):
                    pyautogui.press("volumeup")
                return

            elif "volume down" in query:
                # decrease system volume
                for _ in range(16):
                    pyautogui.press("volumedown")
                return

            elif "mute" in query:
                pyautogui.press("volumemute")
                return

            elif "refresh" in query:
                # simulate refresh by clicking on specific screen coordinates; these may need adjustment per system
                pyautogui.moveTo(1551, 551, 2)
                pyautogui.click(x=1551, y=551, clicks=1, interval=0, button='right')
                pyautogui.moveTo(1620, 667, 1)
                pyautogui.click(x=1620, y=667, clicks=1, interval=0, button='left')
                return

            elif "scroll down" in query:
                pyautogui.scroll(1000)
                return

            elif "drag visual studio to the right" in query:
                # this command is specific to visual studio on windows; may require adjustment on other systems
                pyautogui.moveTo(46, 31, 2)
                pyautogui.dragRel(1857, 31, 2)
                return

            elif "rectangular spiral" in query:
                # draw a rectangular spiral in paint (windows) or equivalent drawing app on other systems
                sys_os = platform.system()
                if sys_os == "Windows":
                    pyautogui.hotkey('win')
                    time.sleep(1)
                    pyautogui.write('paint')
                    time.sleep(1)
                    pyautogui.press('enter')
                    time.sleep(1)
                    pyautogui.moveTo(100, 193, 1)
                    pyautogui.click(button='right')
                    distance = 300
                    while distance > 0:
                        pyautogui.dragRel(distance, 0, 0.1, button="left")
                        distance -= 10
                        pyautogui.dragRel(0, distance, 0.1, button="left")
                        pyautogui.dragRel(-distance, 0, 0.1, button="left")
                        distance -= 10
                        pyautogui.dragRel(0, -distance, 0.1, button="left")
                    return
                else:
                    self.jarvis_core.speak("rectangular spiral command is not supported on this system")
                    return

            elif "close paint" in query:
                sys_os = platform.system()
                if sys_os == "Windows":
                    self.jarvis_core.kill_process("mspaint.exe")
                    return
                elif sys_os == "Darwin":
                    self.jarvis_core.kill_process("Preview", "Preview")
                    return
                else:
                    self.jarvis_core.kill_process("gimp")
                    return

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

            elif "I want to talk with you" in query:
                ai_dialogue(api_key=self.api_key)
                return

            elif 'type' in query:
                # type the following text
                query = query.replace("type", "")
                pyautogui.write(query)

            # fallback to AI dialogue engine
            response = ai_dialogue(self.jarvis_core, self.api_key, query)
            self.jarvis_core.speak(response)
