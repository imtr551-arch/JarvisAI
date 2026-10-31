import tempfile
import unittest
from pathlib import Path
from jarvis_memory import LocalMemory, handle_memory_command
from jarvis_stream import VisibleTextFilter


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "memory.json"
        self.memory = LocalMemory(self.path)

    def test_explicit_storage_and_persistence(self):
        self.assertFalse(self.path.exists())
        self.assertEqual(handle_memory_command("Remember that my dog is Max", self.memory),
                         "Saved to local memory.")
        self.assertEqual(LocalMemory(self.path).list_notes(), ["my dog is Max"])

    def test_duplicates_and_bounds(self):
        self.memory.remember("my dog is Max")
        self.assertIn("already saved", self.memory.remember("MY DOG IS MAX"))
        self.assertIn("240 characters", self.memory.remember("x" * 241))

    def test_forget(self):
        self.memory.remember("one")
        self.memory.remember("two")
        self.assertEqual(handle_memory_command("forget note 1", self.memory),
                         "That note was forgotten.")
        self.assertEqual(self.memory.list_notes(), ["two"])

    def test_clear_and_no_implicit_command(self):
        self.memory.remember("one")
        self.assertIsNone(handle_memory_command("Do you remember yesterday?", self.memory))
        self.assertEqual(self.memory.clear(), "All saved notes were cleared.")
        self.assertEqual(self.memory.list_notes(), [])

    def test_corruption_is_not_overwritten(self):
        self.path.write_text("broken!", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            self.memory.remember("new")
        self.assertEqual(self.path.read_text(encoding="utf-8"), "broken!")


class StreamFilterTests(unittest.TestCase):
    def test_normal_chunks(self):
        filt = VisibleTextFilter()
        result = "".join(map(filt.feed, ["Hello ", "world!"])) + filt.finish()
        self.assertEqual(result, "Hello world!")

    def test_split_hidden_block(self):
        filt = VisibleTextFilter()
        result = "".join(map(filt.feed,
            ["Hello <th", "ink>secret", " detail</th", "ink> world!"])) + filt.finish()
        self.assertEqual(result, "Hello  world!")

    def test_unterminated_hidden(self):
        filt = VisibleTextFilter()
        result = filt.feed("Ready <think>ignore this") + filt.finish()
        self.assertEqual(result, "Ready ")

    def test_multiple_hidden(self):
        filt = VisibleTextFilter()
        result = filt.feed("<think>x</think>Answer<think>y</think>.") + filt.finish()
        self.assertEqual(result, "Answer.")


if __name__ == "__main__":
    unittest.main()
