import os
import sys
import webbrowser
import re
import json
import random
import psutil # pyright: ignore[reportMissingImports]
import pyttsx3 # pyright: ignore[reportMissingImports]
from openrouter import OpenRouter  # pyright: ignore[reportMissingImports]
from RealtimeSTT import AudioToTextRecorder  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
load_dotenv()
from datetime import datetime
API_KEY = os.getenv("OPENROUTER_API_KEY")
HISTORY_PATH = os.path.join(os.path.dirname(__file__), "chat_history.json")

# Load/save chat history
def load_history_from_json():
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_history_to_json():
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=4, ensure_ascii=False)

chat_history = load_history_from_json()

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
    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    chat_history.append({"role": "user", "content": (
        f"You are a helpful, intelligent personal assistant. Background Info: 1. Device Battery: {psutil.sensors_battery().percent}% .Core Directives:\n 1. Never say your own name.\n 2. Keep responses natural, accurate, and strictly capped at one concise sentence (around 30 words) unless requested otherwise.\n 3. If asked to open an application/website, you must respond EXACTLY with: 'To open an app or a website, say my name then open [app or the website's name] or go to [app or website's name].'\n 4. Internal Context: The current date/time is {time}. Use this for absolute memory/reasoning. Do NOT mention this timestamp in your response unless the user explicitly asks for the current time, current date, or asks when their message was sent and when they ask what time or date a message was sent tell the full date and time using June xx, 20xx format.\n User Message: {txt}"
    )})
    save_history_to_json()
    phrase = ['Working on it', 'Looking into it', 'Just a minute', 'Thinking']
    respond(phrase[random.randint(0, 3)])
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

        def contains_word(words: list[str]) -> bool:
            return any(re.search(rf"\b{re.escape(word)}\b", command) for word in words)

        # Exiting
        if contains_word(["close", "exit", "quit"]):
            respond("Bye bye")
            sys.exit()

        # Greetings
        elif contains_word(["hi", "hello", "hey"]):
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