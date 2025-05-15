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
#from submodules
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
        while True:
            if 'wikipedia' in query:
                self.jarvis_core.speak("searching wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                self.jarvis_core.speak("according to wikipedia")
                print(results)
                self.jarvis_core.speak(results)
                return

            elif "channel analytics" in query:
                webbrowser.open("https://studio.youtube.com/channel/UCxeYbp9rU_HuIwVcuHvK0pw/analytics/tab-overview/period-default")
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

            elif 'close youtube' in query:
                self.jarvis_core.speak("closing browser")
                # assuming youtube runs in edge on windows; adjust if needed
                sys_os = platform.system()
                if sys_os == "Windows":
                    self.jarvis_core.kill_process("msedge.exe")
                    return
                elif sys_os == "Darwin":
                    self.jarvis_core.kill_process("Microsoft Edge", "Microsoft Edge")
                    return
                else:
                    self.jarvis_core.kill_process("msedge")
                    return

            elif 'open google' in query or 'open chrome' in query:
                sys_os = platform.system()
                self.jarvis_core.speak("what should i search?")
                search_query = self.jarvis_core.recognize_speech().lower()
                if sys_os == "Windows":
                    os.startfile(r"C:\Program Files\Mozilla Firefox\firefox.exe")
                elif sys_os == "Darwin":
                    subprocess.call(["open", "-a", "Firefox"])
                else:  # assume Linux
                    subprocess.call(["firefox"])
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                return

            elif 'close google' in query or 'close chrome' in query:
                self.close_browser('chrome')
                return

            elif 'close mozilla' in query or 'close firefox' in query:
                self.close_browser('firefox')
                return

            elif 'maximize this window' in query:
                # TODO
                pyautogui.hotkey('alt', 'space')
                time.sleep(1)
                pyautogui.press('x')
                return

            elif 'minimise this window' in query:
                # TODO
                pyautogui.hotkey('alt', 'space')
                time.sleep(1)
                pyautogui.press('n')
                return

            elif 'google search' in query:
                # perform google search in current browser
                query = query.replace("google search", "").strip()
                pyautogui.hotkey('alt', 'd')
                time.sleep(0.5)
                pyautogui.write(query, interval=0.1)
                pyautogui.press('enter')
                return

            elif 'youtube search' in query:
                # perform youtube search in current browser
                query = query.replace("youtube search", "").strip()
                pyautogui.hotkey('alt', 'd')
                time.sleep(0.5)
                for _ in range(4):
                    pyautogui.press('tab')
                    time.sleep(0.2)
                pyautogui.write(query, interval=0.1)
                pyautogui.press('enter')
                return

            elif 'open new window' in query:
                # TODO
                pyautogui.hotkey('ctrl', 'n')
                return

            elif 'open incognito window' in query:
                pyautogui.hotkey('ctrl', 'shift', 'n')
                pyautogui.hotkey('ctrl', 'shift', 'p')
                return

            elif 'open history' in query:
                # open browser history
                pyautogui.hotkey('ctrl', 'h')
                return

            elif 'open downloads' in query:
                # open browser downloads page
                pyautogui.hotkey('ctrl', 'j')
                return

            elif 'previous tab' in query:
                # switch to previous tab
                pyautogui.hotkey('ctrl', 'shift', 'tab')
                return

            elif 'next tab' in query:
                # switch to next tab
                pyautogui.hotkey('ctrl', 'tab')
                return

            elif 'close tab' in query:
                # close current tab
                pyautogui.hotkey('ctrl', 'w')
                return

            elif 'close window' in query:
                # close current window
                pyautogui.hotkey('ctrl', 'shift', 'w')
                return

            elif 'clear browsing history' in query:
                # open clear browsing data dialog; shortcut may vary by browser
                pyautogui.hotkey('ctrl', 'shift', 'delete')
                return

            # TODO
            elif 'play music' in query:
                # play a random music file from the music directory; adjust path as needed
                music_dir = 'E:\\Musics' if platform.system() == "Windows" else os.path.expanduser("~/Music")
                try:
                    songs = os.listdir(music_dir)
                    self.jarvis_core.open_file(os.path.join(music_dir, random.choice(songs)))
                    return
                except Exception:
                    self.jarvis_core.speak("music directory not found or empty")
            
            elif 'close movie' in query or 'close music' in query:
                self.jarvis_core.speak("closing media player")
                sys_os = platform.system()
                if sys_os == "Windows":
                    self.jarvis_core.kill_process("vlc.exe")
                    return
                elif sys_os == "Darwin":
                    self.jarvis_core.kill_process("VLC", "VLC")
                    return
                else:
                    self.jarvis_core.kill_process("vlc")
                    return

            elif 'the time' in query:
                # announce the current time
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                self.jarvis_core.speak(f"the time is {current_time}")
                return

            elif "shut down the system" in query:
                self.jarvis_core.speak("shutting down the system")
                self.jarvis_core.shutdown_system()

            elif "restart the system" in query:
                self.jarvis_core.speak("restarting the system")
                self.jarvis_core.restart_system()
            
            elif "close notepad" in query:
                self.jarvis_core.speak("closing text editor")
                sys_os = platform.system()
                if sys_os == "Windows":
                    self.jarvis_core.kill_process("notepad.exe")
                elif sys_os == "Darwin":
                    self.jarvis_core.kill_process("TextEdit", "TextEdit")
                else:
                    self.jarvis_core.kill_process("gedit")

            elif "open command prompt" in query:
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
                    # linux terminal closing may vary; pkill common terminals
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
                    continue

                def get_operator_fn(op):
                    # return the operator function based on the operator string
                    return {
                        '+' : operator.add,
                        '-' : operator.sub,
                        'x' : operator.mul,
                        'divided' : operator.__truediv__,
                    }[op]

                def eval_binary_expr(op1, oper, op2):
                    # evaluate a binary expression
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
                return

            # fallback to AI dialogue engine
            response = ai_dialogue(self.jarvis_core, self.api_key, query)
            self.jarvis_core.speak(response)
