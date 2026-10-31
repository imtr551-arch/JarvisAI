import speech_recognition as sr

recognizer = sr.Recognizer()

# Microphone settings
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 1.0
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5

WAKE_WORD = "jarvis"

with sr.Microphone() as source:
    print("Calibrating microphone...")
    recognizer.adjust_for_ambient_noise(source, duration=2)

    print("\n================================")
    print("      JARVIS IS STANDBY")
    print("      Say 'Jarvis' to wake me")
    print("================================\n")

    while True:
        try:
            # Listen for wake word
            audio = recognizer.listen(
                source,
                timeout=None,
                phrase_time_limit=5
            )

            text = recognizer.recognize_google(
                audio,
                language="en-CA"
            ).lower().strip()

            print("Heard:", text)

            # Check for wake word
            if WAKE_WORD in text:
                print("\n>>> JARVIS ACTIVATED <<<")
                print("Listening for command...")

                # Listen for actual command
                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=15
                )

                command = recognizer.recognize_google(
                    audio,
                    language="en-CA"
                )

                print("You said:", command)

                # Go back to standby
                print("\nWaiting for 'Jarvis'...")

        except sr.UnknownValueError:
            # Couldn't understand audio, keep listening
            pass

        except sr.WaitTimeoutError:
            print("You didn't say anything.")

        except sr.RequestError as e:
            print("Google speech recognition error:", e)