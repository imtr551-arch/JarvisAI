"""Pure command parsing helpers; safe to import without microphone or AI models."""

WAKE_PHRASES = ("hey jarvis", "okay jarvis", "ok jarvis", "jarvis")
WAKE_BOUNDARY = " ,.!?:;"


def remove_wake_word(command: str) -> str | None:
    """Return the command after a leading wake phrase, or None if absent.

    A bare wake phrase returns an empty string, so the caller may ask
    for the next command. A word like "jarvisian" does not wake JARVIS.
    """
    text = command.strip()
    lowered = text.casefold()

    for phrase in WAKE_PHRASES:
        if lowered.startswith(phrase):
            boundary = len(phrase)
            if len(text) == boundary or text[boundary] in WAKE_BOUNDARY:
                return text[boundary:].lstrip(WAKE_BOUNDARY)

    return None


def choose_model_for_prompt(
    prompt: str, fast_model: str, smart_model: str, smart_keywords
) -> str:
    """Select a model using the existing length and keyword heuristics."""
    text = prompt.casefold()
    if len(text.split()) > 40:
        return smart_model
    if any(keyword in text for keyword in smart_keywords):
        return smart_model
    return fast_model
