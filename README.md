# JarvisAI

Experimental local-first Windows voice assistant built in Python.

## Features

- Ollama for chat, with separate configurable fast and smart model choices
- Faster-Whisper speech-to-text in `assistant.py`
- Text-to-speech via a background Windows voice worker
- Wake phrases: "Jarvis", "Hey Jarvis", "OK Jarvis", "Okay Jarvis"
- CPU, RAM, disk, GPU, and system-information commands
- Commands to open Chrome, Discord, YouTube, and Google
- Short in-session conversation history

## Requirements

- Windows, Python 3.10 or newer, a working microphone, and audio output
- [Ollama](https://ollama.com/) running locally
- An Ollama model installed (the default is `qwen3:8b`)
- Internet access for first-time model downloads

## Installation (PowerShell)

1. Clone the repository and change into its directory.
2. Create a virtual environment and install dependencies:

       py -m venv .venv
       .\.venv\Scripts\Activate.ps1
       python -m pip install -r requirements.txt

3. Download the default Ollama model:

       ollama pull qwen3:8b

4. Keep Ollama running, then start Jarvis:

       python assistant.py

If `PyAudio` fails to install, use a supported Windows/Python combination
and check that your microphone is available. The first run may download
the Faster-Whisper `base` model.

## Using Jarvis

Try: **"Hey Jarvis, what is my CPU usage?"**

Or say **"Jarvis"**, wait for "Yes?", and then give one command.

Normal background speech is ignored until a wake phrase. To exit,
say **"Jarvis, goodbye"**. Speech playback finishes before the
microphone starts listening again.

## Model choices

By default both routes use `qwen3:8b`, so a single installed model works.
To make the fast route use a smaller model, first run
`ollama pull qwen3:4b`, then set:

    $env:JARVIS_MODEL_FAST = "qwen3:4b"
    $env:JARVIS_MODEL_SMART = "qwen3:8b"
    python assistant.py

The keyword-based router is a heuristic; it is not an automatic model
performance benchmark.

## Other scripts

- `main.py` is a smaller alternative using SpeechRecognition's Google
  recognizer (requires an internet connection). It does not implement
  the same wake-word controls as `assistant.py`.
- `mic_test.py` tests microphone input and wake detection using the
  Google recognizer (requires an internet connection).
- `jarvis_core.py` contains pure wake-word and model-routing helpers.

## Tests

    python -m unittest discover -s tests -v

The automated tests cover command parsing and model selection; actual
microphone, voice engine, and Ollama behavior must be tested on Windows.

## Notes

Jarvis currently performs a limited allowlist of local PC actions.
It does not execute arbitrary AI-generated shell commands. Temporary
audio recordings made during transcription are deleted after each
transcription attempt, including failures.
