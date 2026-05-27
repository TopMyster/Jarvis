import os
import sys
import webbrowser
from RealtimeSTT import AudioToTextRecorder  # pyright: ignore[reportMissingImports]
import re

def respond(response):
    print(f"\n{response}\n")
def launch_app(name: str):
    name = name.strip().strip('.,;:!?')
    url_pattern = re.compile(r'^[\w.-]+\.[a-z]{2,}$', re.IGNORECASE)
    if name.startswith(("http://", "https://", "www.")) or url_pattern.match(name):
        url = name if name.startswith("http") else f"https://{name}"
        webbrowser.open(url)
        return

    if sys.platform == "darwin":
        os.system(f'open -a "{name}"')
    elif sys.platform == "win32":
        os.system(f'start "" "{name}"')
    else:
        os.system(f'xdg-open "{name}"')

    
def process_text(text):
    if "jarvis" in text.lower():
        text = text.lower().replace("jarvis", "").strip()
        respond(f"You said: {text}")
        if "close" in text.lower() or "exit" in text.lower() or "quit" in text.lower():
            respond("Bye bye")
            return 

        # Saying hello
        elif "hi" in text.lower() or "hey" in text.lower() or "hello" in text.lower():
            respond("Hello")
        
        # Opening apps/links
        elif "open" in text.lower():
            app = text.lower().replace("open", "").strip()
            launch_app(app.strip(',').strip())

def jarvis():
    recorder = AudioToTextRecorder()

    while True:
        recorder.text(process_text)


if __name__ == "__main__":
    jarvis()