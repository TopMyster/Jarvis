import os
import sys
import webbrowser
import re
import warnings
import subprocess
import pygame
from importlib.resources import files, as_file
warnings.filterwarnings("ignore", category=UserWarning)
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pyttsx3 # pyright: ignore[reportMissingImports]
from openrouter import OpenRouter  # pyright: ignore[reportMissingImports]
from RealtimeSTT import AudioToTextRecorder  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
chat_history = []

def respond(response):
    print(f"\n{response}\n")
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()


def launch_app(name: str):
    name = name.strip().strip('.,;:!?')

    # Detect URLs/domains
    url_pattern = re.compile(r'^[\w.-]+\.[a-z]{2,}$', re.IGNORECASE)

    if (
        name.startswith(("http://", "https://", "www."))
        or url_pattern.match(name)
    ):
        url = name if name.startswith(("http://", "https://")) else f"https://{name}"
        webbrowser.open(url)
        respond(f"Opening {name}")
        return

    # Open local apps
    if sys.platform == "darwin":  # macOS
        os.system(f'open -a "{name}"')

    elif sys.platform == "win32":  # Windows
        os.system(f'start "" "{name}"')

    else:  # Linux
        os.system(f'xdg-open "{name}"')

    respond(f"Opening {name}")

def ask_ai(txt):
    chat_history.append({"role": "user", "content": f"You are Jarvis, an intelligent personal assistant. Do not ever say your name. Provide accurate, clear, and natural responses in a single, concise sentence (around 30 words), unless the user explicitly requests more detail. If asked to open an application, simply reply: 'To open an app, say my name then open [app name] or go to [app name]. This is the users question/statement: {txt}'"})
    respond("Working on it")
    with OpenRouter(
        api_key=API_KEY
    ) as client:
        response = client.chat.send(
            model="openai/gpt-oss-20b",
            messages=chat_history,
            temperature=0.6
        )

        ai_msg = response.choices[0].message
        chat_history.append({"role": "assistant", "content": ai_msg.content})
        return ai_msg.content


def process_text(text):

    if "jarvis" in text.lower():
        print(f"You said: {text}")
        command = text.lower().replace("jarvis", "", 1).strip(" ,.!?;:")
        # Exiting
        if any(word in command for word in ["close", "exit", "quit"]):
            respond("Bye bye")
            sys.exit()

        # Greetings
        elif any(word in command for word in ["hi", "hello", "hey"]):
            respond("Hello")

        # Help
        elif command.startswith("help"):
            webbrowser.open("https://github.com/TopMyster/Jarvis/blob/main/README.md")
            respond("I opened some instructions to assist you")

        # Opening apps/websites
        elif command.startswith(("go to", "open")):
            if command.startswith("go to"):
                app = command.replace("go to", "", 1).strip()
            elif command.startswith("open"):
                app = command.replace("open", "", 1).strip()
            if app:
                launch_app(app)
            else:
                respond("What should I open?")

        #Searching in Google
        elif command.startswith("search"):
            query = command.replace("search", "", 1).strip()
            if query.startswith("for "):
                query = query.replace("for ", "", 1).strip()
            elif query.startswith("up "):
                query = query.replace("up ", "", 1).strip()
                
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                respond(f"Searching the web for {query}")
        #Asking AI
        else:
            pygame.mixer.init()
            pygame.mixer.music.load("")
            pygame.mixer.music.play()
            answer = ask_ai(command.replace("jarvis", "", 1).strip(" ,.!?;:"))
            respond(answer)

def main():
    print(
        r"""
     _                  _
    | | __ _ _ ____   _(_)___
 _  | |/ _` | '__\ \ / / / __|
| |_| | (_| | |   \ V /| \__ \
 \___/ \__,_|_|    \_/ |_|___/
        """
    )
    global API_KEY
    if not API_KEY:
        API_KEY = input("Enter your Openrouter API KEY here: \n> ")
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        with open(env_path, "w") as f:
            f.write(f'OPENROUTER_API_KEY="{API_KEY}"\n')
        print("API Key saved.")

    recorder = AudioToTextRecorder()

    while True:
        text = recorder.text()

        if text:
            process_text(text)


if __name__ == "__main__":
    main()