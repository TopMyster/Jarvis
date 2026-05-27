import os
import sys
import webbrowser
from RealtimeSTT import AudioToTextRecorder  # pyright: ignore[reportMissingImports]

def launch_app(name: str):
    if name.startswith(("http://", "https://", "www.")) or ("." in name and "/" not in name):
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
        print(f"You said: {text}")
        if "close" in text.lower() or "exit" in text.lower() or "quit" in text.lower():
            print("Bye bye")
            return 

        # Saying hello
        elif "hi" in text.lower() or "hey" in text.lower() or "hello" in text.lower():
            print("Hello")
        
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