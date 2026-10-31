import ollama
import speech_recognition as sr
import pyttsx3

MODEL = "qwen3:8b"

# Voice engine
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0
recognizer.dynamic_energy_threshold = True


def speak(text):
    print("\n🤖 JARVIS:")
    print(text)

    engine.say(text)
    engine.runAndWait()


def ask_ai(prompt):
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def listen():
    with sr.Microphone() as source:
        print("\n🎤 Listening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=15
            )

            text = recognizer.recognize_google(
                audio,
                language="en-CA"
            )

            print("You:", text)
            return text

        except sr.UnknownValueError:
            print("❌ I couldn't understand you.")
            return None

        except sr.WaitTimeoutError:
            return None

        except sr.RequestError as e:
            print("❌ Speech recognition error:", e)
            return None


speak("JARVIS is now online. How can I help you?")

while True:

    command = listen()

    if command is None:
        continue

    if command.lower() in ["exit", "quit", "shutdown"]:
        speak("Goodbye.")
        break

    try:
        response = ask_ai(command)
        speak(response)

    except Exception as e:
        speak("I encountered an error.")
        print(e)