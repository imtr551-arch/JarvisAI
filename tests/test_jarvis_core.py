"""Tests for command parsing without requiring microphone/Ollama installation."""

import unittest

from jarvis_core import choose_model_for_prompt, remove_wake_word


class WakeWordTests(unittest.TestCase):
    def test_bare_wake_word(self):
        self.assertEqual(remove_wake_word("Jarvis"), "")

    def test_direct_command(self):
        self.assertEqual(remove_wake_word("Jarvis, open Chrome"), "open Chrome")

    def test_hey_jarvis(self):
        self.assertEqual(remove_wake_word("Hey Jarvis, what's my CPU usage?"),
                         "what's my CPU usage?")

    def test_okay_jarvis(self):
        self.assertEqual(remove_wake_word("Okay Jarvis: hello"), "hello")

    def test_non_wake_speech_ignored(self):
        self.assertIsNone(remove_wake_word("please open Chrome"))

    def test_mid_sentence_ignored(self):
        self.assertIsNone(remove_wake_word("Can you ask Jarvis?"))

    def test_partial_word_ignored(self):
        self.assertIsNone(remove_wake_word("jarvisian"))

    def test_empty_ignored(self):
        self.assertIsNone(remove_wake_word(""))


class ModelRoutingTests(unittest.TestCase):
    def test_simple_prompt(self):
        self.assertEqual(choose_model_for_prompt("hello", "fast", "smart",
                                                  ("python", "explain")),
                         "fast")

    def test_keyword(self):
        self.assertEqual(choose_model_for_prompt("write python", "fast", "smart",
                                                  ("python",)),
                         "smart")

    def test_long_prompt(self):
        prompt = "word " * 41
        self.assertEqual(choose_model_for_prompt(prompt, "fast", "smart", ()),
                         "smart")


if __name__ == "__main__":
    unittest.main()
