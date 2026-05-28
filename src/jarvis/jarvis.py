import os
import sys
import webbrowser
import re
import pyttsx3
from openrouter import OpenRouter 
from RealtimeSTT import AudioToTextRecorder  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv
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
    chat_history.append({"role": "user", "content": txt})
    with OpenRouter(
        api_key=API_KEY
    ) as client:
        response = client.chat.send(
            model="openai/gpt-oss-20b",
            messages=chat_history,
            temperature=0.7
        )

        ai_msg = response.choices[0].message
        chat_history.append({"role": "assistant", "content": ai_msg.content})
        return ai_msg.content


def process_text(text):

    if "jarvis" in text.lower():
        print(f"You said: {text}")
        command = text.lower().replace("jarvis", "", 1).strip()
        # Exiting
        if any(word in command for word in ["close", "exit", "quit"]):
            respond("Bye bye")
            sys.exit()

        # Greetings
        elif any(word in command for word in ["hi", "hello", "hey"]):
            respond("Hello")

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
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                respond(f"Searching the web for {query}")
        #Asking AI
        else:
            answer = ask_ai(command.replace("jarvis", "", 1).strip())
            respond(answer)


def jarvis():
    print(
        r"""
     _                  _
    | | __ _ _ ____   _(_)___
 _  | |/ _` | '__\ \ / / / __|
| |_| | (_| | |   \ V /| \__ \
 \___/ \__,_|_|    \_/ |_|___/
        """
    )

    recorder = AudioToTextRecorder()

    while True:
        text = recorder.text()

        if text:
            process_text(text)


if __name__ == "__main__":
    jarvis()