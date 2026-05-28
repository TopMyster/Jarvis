# Jarvis

A cross‑platform voice‑controlled assistant built on **RealtimeSTT** that understands simple commands, and can launch applications or open URLs.


## Features

- Wake word detection (`jarvis`)
- Opens Apps and websites
- Get Answers from AI
- Cross platform support (macOS, Windows, Linux)

## Requirements

- Python **3.11** or newer
- PortAudio development libraries

### macOS

```bash
brew install portaudio
```

### Linux

```bash
sudo apt-get install python3-dev portaudio19-dev
```


## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Jarvis.git
cd Jarvis

# Install Jarvis
pip install -e .
```

---

## Running Jarvis

```bash
jarvis
```

When prompted, say commands like:
- "Jarvis open Spotify" – Jarvis will launch the Spotify app.
- "Jarvis open google.com" – Jarvis will open the website in your default browser.
- "Jarvis search python tutorials" - Jarvis will search Google for your query.
- "Jarvis what is the capital of France?" - Jarvis will ask the AI and speak the answer.
- "Jarvis hey" – Jarvis will greet you.
- "Jarvis quit" – Jarvis will exit the assistant.

---

## License

[MIT License](LICENSE)
