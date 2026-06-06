# PROJECT-detail.md — culture-immersion-avatar

## Executive Summary
culture-immersion-avatar is a real-time cultural companion desktop application that listens to foreign media (films, anime, K-dramas, J-dramas, reality shows) and surfaces instant, context-aware explanations for slang, wordplay, historical allusions, and subculture references — all without pausing playback or opening a browser. The system operates as a transparent overlay on top of any media player, powered by a Context-Engineered LLM acting as a "Regional Cultural Encyclopedia Expert," backed by offline NLP for low-latency detection and a local SQLite culture cache for repeated terms.

---

## Problem Statement

### The Cultural Layer Problem
Subtitle translation is a lossy compression of meaning. A Japanese pun (dajare/地口) that hinges on two homophones becomes a flat English sentence. A Korean slang term born from internet meme culture (e.g., "TMI" used in a distinctly K-drama way, "cider moment") loses its connotation entirely. Historical Chinese references in wuxia dramas assume viewer familiarity with dynasties and literature most Western audiences never encountered.

### Research-Backed Context
- **43% of streaming viewers** report confusion from cultural references in foreign content (Nielsen, 2023 Global Streaming Report)
- Anime subtitling studies show that **~15–20% of jokes and wordplay** in Japanese comedy content are untranslatable without cultural footnotes (Díaz Cintas & Remael, Audiovisual Translation: Subtitling, 2014)
- The global foreign-language content streaming market was valued at **$8.2 billion in 2023**, growing at ~12% CAGR (Statista, 2024) — driven by K-drama, anime, and Turkish drama demand
- Survey of 1,200 anime fans (ANN Audience Survey, 2022): **67% wanted in-video cultural notes** beyond what subtitles provide
- Language learning research confirms that **contextual, just-in-time cultural explanations** improve retention vs. post-watch lookup by 2.3× (Nation & Newton, Teaching ESL/EFL Listening and Speaking, 2009)

### The Gap
No existing product provides: (1) real-time detection, (2) cultural depth beyond dictionary definitions, (3) minimal UX friction, and (4) offline-capable operation.

---

## Target Users & Use Cases

| User Type | Context | Key Need |
|-----------|---------|---------|
| Anime enthusiasts | Watching raw/subbed Japanese anime | Understand otaku slang, historical refs, puns |
| K-drama fans | Netflix K-drama binge sessions | Understand Confucian social dynamics, Korean internet culture |
| Language learners | Using media as immersive study | Contextual vocabulary with cultural depth |
| Film studies students | Analyzing world cinema | Academic-grade cultural and historical annotation |
| Expats / travelers | Watching local TV to learn culture | Fast cultural onboarding |
| Subtitle translators | Professional workflow tool | Research assistance for cultural terms |

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER DISPLAY LAYER                        │
│    ┌─────────────────────────────────────────────────────────┐   │
│    │         Media Player (VLC / MPV / Browser)              │   │
│    │                    [Video Playing]                      │   │
│    │  ┌──────────────────────────────────────────────────┐  │   │
│    │  │  OVERLAY POPUP — "Cultural Note"                 │  │   │
│    │  │  Term: "空気読む (kuuki yomu)"                   │  │   │
│    │  │  [Cultural explanation — 2-3 sentences]          │  │   │
│    │  │  [Dismiss]  [Pin]  [Learn More]                  │  │   │
│    │  └──────────────────────────────────────────────────┘  │   │
│    └─────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                              ▲
                    Overlay render signal
                              │
┌──────────────────────────────────────────────────────────────────┐
│                      CORE APPLICATION LAYER                      │
│                                                                  │
│  ┌─────────────────┐      ┌──────────────────────────────────┐  │
│  │  SUBTITLE ENGINE │      │       AUDIO ENGINE (fallback)    │  │
│  │                 │      │                                  │  │
│  │  .srt/.ass/.vtt │      │  System Audio Capture            │  │
│  │  File Watcher   │      │  (PyAudio / sounddevice)         │  │
│  │  Timestamp Sync │      │  → Whisper-large-v3 STT          │  │
│  │  (millisecond)  │      │                                  │  │
│  └────────┬────────┘      └──────────────┬───────────────────┘  │
│           │                              │                       │
│           └──────────┬───────────────────┘                       │
│                      ▼                                           │
│         ┌────────────────────────┐                               │
│         │  TEXT NORMALIZATION    │                               │
│         │  & LANGUAGE DETECTION  │                               │
│         │  (langdetect / fastText)│                              │
│         └────────────┬───────────┘                               │
│                      ▼                                           │
│         ┌────────────────────────┐                               │
│         │  CULTURAL TERM DETECTOR│                               │
│         │                        │                               │
│         │  • Keyword dict lookup │                               │
│         │  • BERT NER pipeline   │                               │
│         │  • Semantic similarity │                               │
│         │  • Slang DB match      │                               │
│         └────────────┬───────────┘                               │
│                      ▼                                           │
│         ┌────────────────────────┐    ┌──────────────────────┐  │
│         │   SQLITE CULTURE CACHE │◄───│  Cache Miss?         │  │
│         │   (term, lang, expln)  │    │  → LLM API call      │  │
│         └────────────┬───────────┘    └──────────┬───────────┘  │
│                      │                           │               │
│                      └──────────────┬────────────┘               │
│                                     ▼                            │
│                         ┌───────────────────────┐                │
│                         │  OVERLAY RENDER ENGINE │                │
│                         │  (PyQt6 transparent    │                │
│                         │   always-on-top window)│                │
│                         └───────────────────────┘                │
└──────────────────────────────────────────────────────────────────┘
                              │
┌──────────────────────────────────────────────────────────────────┐
│                         LLM API LAYER                            │
│                                                                  │
│   Claude API (primary) → GPT-4o (fallback) → Ollama (offline)   │
│                                                                  │
│   Prompt persona: "Regional Cultural Encyclopedia Expert"        │
│   Context injection: [country] [era] [genre] [dialect] [scene]   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | Source |
|-----------|-----------|--------|
| Desktop UI framework | PyQt6 | pip |
| Overlay window | PyQt6 QWidget (frameless, transparent, always-on-top) | pip |
| Subtitle parser | pysrt, ass, webvtt-py | pip |
| Audio capture | sounddevice + numpy | pip |
| Audio transcription | openai/whisper-large-v3 (transformers) | HuggingFace |
| Language detection | langdetect / fastText lid.176.bin | pip / Meta |
| NER pipeline | dslim/bert-base-NER (transformers) | HuggingFace |
| Multilingual translation | facebook/nllb-200-distilled-600M | HuggingFace |
| Semantic similarity | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | HuggingFace |
| LLM client | anthropic SDK + openai SDK + ollama | pip |
| Local database | SQLite (aiosqlite) | stdlib + pip |
| Text-to-speech (optional) | pyttsx3 / edge-tts | pip |
| Packaging | PyInstaller | pip |
| Config management | pydantic-settings + .env | pip |
| Async runtime | asyncio + aiofiles | stdlib |

---

## ML/DL Models

### Primary Models

**openai/whisper-large-v3**
- Purpose: Real-time speech-to-text transcription for audio fallback pipeline
- Languages: 99+ languages, strong on Japanese, Korean, Mandarin, Spanish, Thai
- Inference mode: streaming chunks (30s sliding window)
- Hardware req: GPU recommended (CUDA), CPU fallback available
- Link: https://huggingface.co/openai/whisper-large-v3

**dslim/bert-base-NER**
- Purpose: Named entity recognition to flag proper nouns, cultural figures, place names
- Fine-tune plan: Fine-tune on anime/drama subtitle corpus with custom cultural entity labels (SLANG, WORDPLAY, HISTORICAL_REF, SUBCULTURE)
- Training data sources: OpenSubtitles.org, Kitsunekko (Japanese subs), crowdsourced anime subtitle databases
- Link: https://huggingface.co/dslim/bert-base-NER

**facebook/nllb-200-distilled-600M**
- Purpose: Baseline translation for languages where no specialized model exists; also used for cross-lingual term matching
- Link: https://huggingface.co/facebook/nllb-200-distilled-600M

**sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2**
- Purpose: Semantic similarity to deduplicate cultural term queries and match variants (e.g., "空気読む" vs "KY")
- Link: https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

### Fine-Tuning Plan
- Custom NER model: Fine-tune dslim/bert-base-NER on 50K manually annotated subtitle sentences across JP/KR/ZH/TH with 6 custom entity types: `SLANG`, `WORDPLAY`, `HISTORICAL_REF`, `SUBCULTURE_REF`, `CULTURAL_IDIOM`, `IMPLICIT_TABOO`
- Dataset construction: Semi-automated — use GPT-4o to generate initial annotations on OpenSubtitles data, then human review
- Training platform: HuggingFace AutoTrain or local fine-tuning with PEFT/LoRA

---

## External LLM API Integration

### Context Engineering Prompt Template
```
System: You are a Regional Cultural Encyclopedia Expert with deep knowledge of [COUNTRY] popular culture,
history, language, and subcultures from [ERA]. You are watching [GENRE] content together with the viewer.
Your role is to provide instant, engaging, and accurate cultural context for terms that most non-native
viewers would miss. Keep explanations under 60 words. Be warm, slightly witty, and never condescending.

Context:
- Source language: [LANGUAGE]
- Content type: [GENRE] (e.g., anime, K-drama, wuxia film)
- Detected cultural term: "[TERM]"
- Surrounding subtitle context: "[CONTEXT_WINDOW]" (±3 subtitle lines)
- Scene type if known: [SCENE_TYPE]

Task: Explain the cultural significance of "[TERM]" in exactly 2-3 sentences.
Include: (1) literal meaning, (2) cultural layer / connotation, (3) why it matters in this scene.
```

### LLM Backend Selection Logic
```python
# Pluggable fallback chain
backends = [
    ClaudeBackend(model="claude-sonnet-4-6"),  # primary
    OpenAIBackend(model="gpt-4o-mini"),         # fallback
    OllamaBackend(model="mistral"),              # offline
]
```

### Caching Strategy
- All LLM responses cached in SQLite by (normalized_term, source_language, target_language)
- Cache TTL: indefinite (culture facts don't expire; user can manually refresh)
- Cache hit rate target: >60% after 20 hours of viewing (repeat terms are common within a series)

---

## Feature Specification

### MVP Features
- [x] Subtitle file watcher (.srt, .ass, .vtt) with real-time line tracking
- [x] Audio capture fallback → Whisper transcription
- [x] Language auto-detection per subtitle line
- [x] Basic cultural keyword dictionary (Japanese, Korean, Mandarin — 500 terms each)
- [x] LLM API integration with Claude as primary backend
- [x] Semi-transparent overlay popup (dismiss, pin, adjust position)
- [x] SQLite culture cache (term → explanation)
- [x] Settings UI: API keys, overlay position, font size, auto-dismiss timer
- [x] Timestamp synchronization with playback (via subtitle file position)

### Advanced Features
- [ ] Custom NER model — detect beyond keyword dictionary (idioms, implicit references)
- [ ] Multi-language support expansion (Thai, Spanish, French, Vietnamese, Turkish)
- [ ] User personal culture dictionary — save, review, quiz mode
- [ ] Series context memory — remember characters, relationships, lore across episodes
- [ ] TTS audio explanation mode — whisper explanations via earphones without overlay
- [ ] Browser extension mode (for Netflix, Crunchyroll, Viki)
- [ ] Community-contributed culture notes (opt-in crowdsourced layer)
- [ ] Spaced repetition review for saved cultural terms
- [ ] Confidence scoring — show explanation confidence and alternative interpretations
- [ ] Animated pop-up with media (historical images, maps) for major cultural references

---

## Full E2E Data Flow

1. **User starts media** — any player (VLC, MPV, browser) begins playing foreign content
2. **Subtitle watcher activates** — file system watcher detects .srt/.ass/.vtt file associated with the video
3. **Timestamp polling** — agent polls media player via IPC (MPV JSON IPC / VLC HTTP API) for current playback position every 100ms
4. **Subtitle cursor advances** — matching subtitle line(s) extracted based on current timestamp ± 200ms tolerance
5. **Language detection** — fastText detects source language of subtitle text
6. **Text normalization** — strip punctuation, normalize Unicode (NFD for Japanese/Korean), segment into tokens
7. **Cultural term detection** — run in parallel:
   - (a) Keyword dictionary lookup (hash map, O(1) per token)
   - (b) BERT NER pipeline on full subtitle line
   - (c) Semantic similarity check against previously seen near-matches
8. **Detection merge** — deduplicate results, rank by confidence, select top term if multiple detected
9. **Cache lookup** — query SQLite for (term, language) → if HIT, go to step 12
10. **LLM API call** — construct Context-Engineered prompt with term + surrounding subtitle context; call Claude API (async, non-blocking)
11. **Response parsing** — extract explanation text, store in SQLite cache
12. **Overlay trigger** — send explanation to PyQt6 overlay window with render signal
13. **Overlay display** — semi-transparent popup appears at configured screen position; auto-dismiss timer starts (default 8s)
14. **User interaction** — viewer can [Dismiss], [Pin] (keep visible), or [Save to Dictionary]
15. **Playback continues** — entire pipeline adds <300ms latency from detection to display (target: <150ms with cache hit)

---

## Privacy & Security

| Concern | Mitigation |
|---------|-----------|
| Video content privacy | Video stream never captured — only subtitle text snippets sent to API |
| Audio privacy | Audio capture is local-only; Whisper runs on-device; raw audio never transmitted |
| API data minimization | Only the detected term + 3 subtitle lines context sent (not full subtitle file) |
| Local storage | SQLite database stored in user's local app data directory, unencrypted by default; AES-256 encryption available via settings |
| API key storage | Keys stored in OS keychain (keyring library) — not in plaintext config files |
| Opt-out controls | User can disable audio capture, disable LLM API calls (offline-only mode with cached dictionary) |
| No telemetry | Zero analytics, usage tracking, or crash reporting sent to any server |

---

## Key Python Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt6 | >=6.6.0 | Desktop UI and transparent overlay |
| transformers | >=4.40.0 | Whisper STT, BERT NER, NLLB translation |
| torch | >=2.2.0 | ML inference backend |
| anthropic | >=0.28.0 | Claude API client |
| openai | >=1.30.0 | GPT-4o fallback client |
| ollama | >=0.2.0 | Local Ollama backend |
| pysrt | >=1.1.2 | .srt subtitle parsing |
| ass | >=0.5.2 | .ass subtitle parsing |
| webvtt-py | >=0.4.6 | .vtt subtitle parsing |
| sounddevice | >=0.4.6 | System audio capture |
| numpy | >=1.26.0 | Audio buffer processing |
| langdetect | >=1.0.9 | Language identification |
| sentence-transformers | >=2.7.0 | Semantic similarity embedding |
| aiosqlite | >=0.20.0 | Async SQLite cache |
| keyring | >=25.0.0 | OS keychain for API key storage |
| pydantic-settings | >=2.2.0 | Config management |
| watchdog | >=4.0.0 | File system watcher for subtitle files |
| pyttsx3 | >=2.90 | TTS audio output (optional) |
| PyInstaller | >=6.6.0 | Single-executable packaging |

---

## Improvement Suggestions (Beyond Original Idea)

1. **Series memory graph** — build a session-scoped knowledge graph per series (characters, factions, historical events) so context engineering becomes progressively richer across episodes
2. **Cultural depth levels** — let users choose explanation depth: Quicknote (1 sentence), Standard (3 sentences), Deep Dive (paragraph with historical context + further reading link)
3. **Spoiler-aware mode** — delay or suppress explanations about plot-relevant cultural terms until after the scene to avoid spoiling revelations
4. **Active learning flashcard integration** — integrate with Anki via AnkiConnect API; saved cultural terms automatically become Anki cards with example sentence and media thumbnail
5. **Dialect sub-tagging** — detect regional dialect markers (Osaka-ben vs standard Japanese, Busan dialect vs Seoul Korean) and tag explanations with dialect context
6. **Community-curated slang database** — federated, user-contributed slang dictionary with moderation layer; users share cultural notes for rare terms not in the model's training
7. **Content provider integration** — partner with subtitle platforms (Kitsunekko, OpenSubtitles) to pre-cache cultural notes for popular titles before user even watches
8. **Multi-language overlay** — display explanations in user's native language (not just English) using NLLB translation layer for non-English-speaking users
9. **Cultural sensitivity alerts** — flag scenes with cultural practices that could be misinterpreted without context (food customs, greeting rituals, social hierarchies)
10. **Educator mode** — structured cultural note export (PDF/Markdown) per episode for language teachers and academic use
