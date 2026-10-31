# JarvisAI

Personal voice-assistant experiments written in Python for Windows.

- `assistant.py` combines local Ollama chat, Faster-Whisper transcription,
  speech output, and PC information tools.
- `main.py` is a simpler Ollama voice assistant using SpeechRecognition.
- `mic_test.py` tests microphone input and wake-word detection.

The assistant scripts require a working microphone and audio output. The
Ollama-based scripts also require Ollama to be installed and running with the
models configured in the source files.
