"""Chunk-safe filter: never surface text inside <think> blocks.

Delays at most len('<think>') - 1 visible trailing characters to handle
tags split over arbitrary streaming boundaries. Unterminated blocks
are dropped at stream end.
"""

OPEN = "<think>"
CLOSE = "</think>"


class VisibleTextFilter:
    def __init__(self):
        self.buffer = ""
        self.hidden = False

    def feed(self, chunk):
        self.buffer += chunk
        out = []
        while self.buffer:
            tag = CLOSE if self.hidden else OPEN
            index = self.buffer.find(tag)
            if index >= 0:
                if not self.hidden:
                    out.append(self.buffer[:index])
                self.buffer = self.buffer[index + len(tag):]
                self.hidden = not self.hidden
                continue
            # Could be a partial tag crossing the chunk boundary.
            pending = max(
                (n for n in range(1, len(tag))
                 if self.buffer.endswith(tag[:n])),
                default=0
            )
            visible = self.buffer[:-pending] if pending else self.buffer
            if not self.hidden:
                out.append(visible)
            self.buffer = self.buffer[-pending:] if pending else ""
            break
        return "".join(out)

    def finish(self):
        output = "" if self.hidden else self.buffer
        self.buffer = ""
        return output
