# CLAUDE.md — culture-immersion-avatar

## Project Identity
- **Name:** culture-immersion-avatar
- **Tagline:** Real-time cultural context companion for foreign media — no Googling required.
- **Status:** Pre-development (Phase 0)
- **Current Phase:** Research & Environment Setup

---

## Core Problem
Viewers of foreign films, anime, K-dramas, J-dramas, and international reality shows constantly encounter untranslatable slang, wordplay (puns, homophones), historical allusions, regional idioms, and subculture references that subtitles flatten or omit entirely. Standard subtitle translation captures words but discards cultural layers — leaving the audience disconnected from what actually makes a joke funny or a scene emotionally resonant. This agent bridges that gap in real time, without interrupting the viewing experience.

---

## Architecture Summary
- **Platform:** Cross-platform desktop app (Python + PyQt6 overlay) with optional browser extension mode
- **Input sources:** System audio capture OR subtitle file (.srt/.ass/.vtt) watcher
- **Audio transcription:** Whisper (HuggingFace) for real-time speech-to-text when no subtitles are available
- **Cultural term detection:** Fine-tuned NER + keyword spotting pipeline to flag slang, idioms, allusions
- **Context engine:** LLM API (Claude / GPT-4 / local Ollama) prompted as "Regional Cultural Encyclopedia Expert"
- **Timestamp sync:** Precise millisecond alignment between video playback position and subtitle cursor
- **Output:** Semi-transparent on-screen overlay popup OR text-to-speech whisper via earphones
- **Local storage:** SQLite — user-defined "culture dictionary" that grows with each viewing session

---

## Key Technical Decisions
1. Subtitle-first pipeline: prefer parsing subtitle files (lower latency, no audio noise) over live audio transcription
2. Audio fallback: Whisper-large-v3 activates only when no subtitle file is detected
3. Context Engineering: LLM prompts wrap a multi-layer system — country, era, genre, and detected dialect all fed as context before the query
4. Pluggable LLM backend: Claude API → GPT-4 → Ollama (mistral/llama3) fallback chain
5. Overlay is always non-blocking: auto-dismisses after 8 seconds, user can pin/dismiss manually
6. Local culture dictionary: explanations are cached per (language, term) key to avoid redundant API calls
7. Privacy: no video content or audio ever leaves the device; only detected text snippets sent to LLM API

---

## External LLM API Integrations

| Provider | Purpose | Config Key | Notes |
|----------|---------|------------|-------|
| Anthropic Claude | Primary cultural explanation engine | `ANTHROPIC_API_KEY` | claude-sonnet-4-6 default |
| OpenAI GPT-4o | Fallback explanation engine | `OPENAI_API_KEY` | optional |
| Ollama (local) | Offline fallback | `OLLAMA_HOST` | mistral or llama3 |

---

## HuggingFace Models In Use

| Model ID | Purpose | Link |
|----------|---------|------|
| openai/whisper-large-v3 | Real-time audio transcription | https://huggingface.co/openai/whisper-large-v3 |
| facebook/nllb-200-distilled-600M | Multilingual translation (50+ languages) | https://huggingface.co/facebook/nllb-200-distilled-600M |
| dslim/bert-base-NER | Named entity recognition (persons, places, cultural refs) | https://huggingface.co/dslim/bert-base-NER |
| Helsinki-NLP/opus-mt-ja-en | Japanese → English baseline translation | https://huggingface.co/Helsinki-NLP/opus-mt-ja-en |
| Helsinki-NLP/opus-mt-ko-en | Korean → English baseline translation | https://huggingface.co/Helsinki-NLP/opus-mt-ko-en |
| sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | Semantic similarity for term deduplication | https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |

---

## Current Active Development Tasks
- [ ] Set up Python project scaffold with PyQt6
- [ ] Implement subtitle file watcher (.srt / .ass / .vtt parser)
- [ ] Implement system audio capture pipeline (PyAudio / sounddevice)
- [ ] Integrate Whisper-large-v3 via transformers pipeline
- [ ] Build cultural term detector (keyword dictionary + NER)
- [ ] Design LLM prompt template (Cultural Encyclopedia Expert persona)
- [ ] Build pluggable LLM client (Claude → GPT-4 → Ollama)
- [ ] Implement overlay UI (semi-transparent popup, auto-dismiss)
- [ ] Build SQLite culture cache layer
- [ ] Implement timestamp sync engine
- [ ] Package as single executable (PyInstaller)

---

## Related Files
- `PROJECT-detail.md` — full technical specification and feature list
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap with milestones
- `SECOND-KNOWLEDGE-BRAIN.md` — research papers, models, self-update protocol
