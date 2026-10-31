"""Explicit, bounded local memory. No automatic collection of conversations."""

import json
import os
from pathlib import Path
import tempfile

MAX_NOTES = 30
MAX_NOTE_LENGTH = 240
DEFAULT_PATH = Path.home() / ".jarvisai" / "memory.json"


class LocalMemory:
    def __init__(self, path=None):
        self.path = Path(path) if path is not None else DEFAULT_PATH

    def _read(self):
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (ValueError, OSError) as error:
            raise RuntimeError("Could not read local memory; no changes made") from error
        if not isinstance(data, list) or not all(isinstance(x, str) for x in data):
            raise RuntimeError("Invalid local memory format; no changes made")
        return data[:MAX_NOTES]

    def _write(self, notes):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_name = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.path.parent,
                prefix=".memory-", suffix=".tmp", delete=False
            ) as handle:
                temp_name = handle.name
                json.dump(notes, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            os.replace(temp_name, self.path)
        finally:
            if temp_name and os.path.exists(temp_name):
                os.unlink(temp_name)

    def remember(self, note):
        note = " ".join(note.split())
        if not note or len(note) > MAX_NOTE_LENGTH:
            return "Please give a note between 1 and 240 characters."
        notes = self._read()
        if note.casefold() in {n.casefold() for n in notes}:
            return "That note is already saved."
        if len(notes) >= MAX_NOTES:
            return "Memory is full (30 notes). Forget a note first."
        notes.append(note)
        self._write(notes)
        return "Saved to local memory."

    def list_notes(self):
        return list(self._read())

    def forget(self, index):
        notes = self._read()
        if not 1 <= index <= len(notes):
            return "That note number doesn't exist."
        del notes[index - 1]
        self._write(notes)
        return "That note was forgotten."

    def clear(self):
        self._write([])
        return "All saved notes were cleared."

    def context(self):
        notes = self._read()
        if not notes:
            return ""
        return "\n".join(f"- {note}" for note in notes)


def handle_memory_command(command, memory):
    """Return response for an explicit memory command, otherwise None."""
    text = command.strip()
    lower = text.casefold()
    if lower.startswith("remember that "):
        return memory.remember(text[len("remember that "):])
    if lower.startswith("remember "):
        return memory.remember(text[len("remember "):])
    if lower in {"what do you remember", "list memories", "show memories"}:
        notes = memory.list_notes()
        if not notes:
            return "No notes saved."
        return "Saved notes: " + "; ".join(
            f"{i}. {note}" for i, note in enumerate(notes, 1)
        )
    if lower.startswith("forget note "):
        number = text[len("forget note "):].strip()
        if number.isdigit():
            return memory.forget(int(number))
        return "Say forget note followed by its number."
    if lower == "clear all memories":
        return "To clear all saved notes, stop Jarvis and delete the file at " + str(memory.path)
    return None
