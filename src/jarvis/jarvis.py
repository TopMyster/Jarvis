import os
os.environ["CT2_LOG_LEVEL"] = "ERROR"
from RealtimeSTT import AudioToTextRecorder  # pyright: ignore[reportMissingImports]


def jarvis():
    with AudioToTextRecorder() as recorder:
        print("Jarvis")
        text = recorder.text()
        if "open" in text.lower():
            print("Ready sir")


if __name__ == "__main__":
    jarvis()