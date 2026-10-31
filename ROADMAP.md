# JarvisAI staged roadmap

This is the planned sequence. Features marked "future" are **not implemented**.

## Stage 1 — Reliable voice (PR #1 foundation; ongoing)

- [x] Define default Ollama model configuration
- [x] Gate commands on leading wake phrases
- [x] Avoid hearing playback when listening
- [x] Add basic unit tests and automated CI
- [x] Follow-up: chunk-safe removal of streamed \`<think>\` content (this PR)
- [ ] Windows hardware/Whisper/SAPI5 integration tests
- [ ] Barge-in/interruption support and latency benchmarks

## Stage 2 — AI and user-controlled memory (this PR: foundation)

- [x] Local notes, explicit "remember" and "forget note N" commands
- [x] Opt-in persistence; no automatic saving of conversations
- [x] Bound notes; test persistence, delete, corruption handling
- [ ] Confirmation-based memory clearing and visible settings UI
- [ ] Better relevance selection, injection-resistant context, privacy controls
- [ ] More capable model routing, error recovery, and context-window pruning

## Stage 3 — Safe Windows PC tools (future)

- [ ] Typed, allowlisted tool registry (never arbitrary AI-generated commands)
- [ ] Volume/media controls and explicit application launch
- [ ] Confirmations for consequential changes; audit log; unit tests
- [ ] Permission/settings controls and graceful failure handling

## Stage 4 — Desktop dashboard (future)

- [ ] Lightweight UI framework and architecture decision
- [ ] Transcript, state, visualizer, mute/privacy indicators
- [ ] System metrics and editable settings/memory
- [ ] Packaging, Windows accessibility, and end-to-end testing

## Review and merge order

1. Review, test on Windows, then merge PR #1.
2. Rebase/retarget this stacked PR against main and review CI and memory privacy.
3. Continue subsequent stages in separately reviewable branches.

## Manual smoke tests

- Start \`python assistant.py\` with Ollama running and a microphone.
- Say: "Jarvis, remember that my favorite color is teal".
- Say: "Jarvis, what do you remember".
- Say: "Jarvis, forget note 1".
- Try background speech without "Jarvis"; it should be ignored.
- Verify recordings are deleted after transcription attempts.
- Test model output containing partial or unterminated think tags in unit tests.
