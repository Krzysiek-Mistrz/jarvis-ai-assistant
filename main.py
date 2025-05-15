from google import genai
from src.core import Jarvis

def main():
    api_key = input("Please set your GOOGLE_API_KEY: ")
    while not api_key:
        print("Error: Please set your GOOGLE_API_KEY environment variable.")
        api_key = input("Please set your GOOGLE_API_KEY: ")

    # Konfiguracja nowego klienta
    client = genai.Client(api_key=api_key)

    jarvis = Jarvis(api_key=api_key)
    jarvis.talk()

if __name__ == "__main__":
    main()
