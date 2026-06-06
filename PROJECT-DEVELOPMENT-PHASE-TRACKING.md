# PROJECT-DEVELOPMENT-PHASE-TRACKING.md — culture-immersion-avatar

## Overview
Total estimated duration: 16 weeks  
Start date: TBD  
Current status: Phase 0 — Not started

---

## Phase 0: Research & Environment Setup
**Duration:** Week 1–2  
**Goal:** Validate technical assumptions, set up dev environment, source all datasets and pretrained models.

### Tasks
- [x] Survey existing tools: Chrome extensions (Jpdb.io, Jisho overlay), Asbplayer, subtitle-companion projects
- [x] Benchmark Whisper-large-v3 latency on target hardware (CPU vs GPU, 30s chunk inference time)
- [x] Evaluate subtitle file parsing accuracy across .srt, .ass, .vtt sample files from major platforms
- [x] Test MPV JSON IPC and VLC HTTP API for playback position polling (<100ms refresh feasibility)
- [x] Assemble initial cultural keyword dictionaries (JP/KR/ZH — 500 terms each, manually curated)
- [x] Download and test HuggingFace models: Whisper, NLLB-200, BERT-NER, sentence-transformers
- [x] Set up Python virtual environment (Python 3.11+, PyTorch 2.2, CUDA 12.x)
- [x] Create project scaffold: src/, tests/, data/, models/, config/ directories
- [x] Configure pyproject.toml with all dependencies
- [x] Set up linting: ruff, mypy, pre-commit hooks
- [x] Create GitHub repository with CI workflow (pytest + ruff)

### Deliverables
- Benchmark report (latency measurements for each pipeline component)
- Initial cultural keyword dictionary (CSV format, 1,500 terms)
- Validated dev environment with all models downloaded locally
- Project scaffold committed to git

### Success Criteria
- Whisper transcription latency < 2s per 30s audio chunk on target hardware
- Subtitle parsers handle all test files without errors
- MPV/VLC IPC polling achieves <100ms position refresh

### Estimated Effort
- 2 engineers × 2 weeks = 4 person-weeks

---

## Phase 1: MVP — Core Loop Working
**Duration:** Week 3–6  
**Goal:** Working end-to-end pipeline from subtitle file to overlay popup for Japanese/Korean content.

### Tasks
- [x] **Subtitle Engine:**
  - [x] Implement watchdog-based subtitle file watcher
  - [x] Parse .srt, .ass, .vtt into unified internal format (subtitle_id, start_ms, end_ms, text, language)
  - [x] Implement timestamp sync engine (poll MPV/VLC every 100ms, match to subtitle window)
  - [x] Handle edge cases: overlapping subtitles, dual-language subs, missing timestamps

- [x] **Text Processing:**
  - [x] Language auto-detection with langdetect (per subtitle line)
  - [x] Unicode normalization (NFD for CJK, NFC for Latin)
  - [x] Tokenization (MeCab for Japanese, KoNLPy for Korean, jieba for Chinese)

- [x] **Cultural Term Detection (MVP — keyword only):**
  - [x] Load keyword dictionaries into memory (hash map)
  - [x] Implement O(1) token lookup per subtitle line
  - [x] Return matched terms with confidence = 1.0 (exact match)

- [x] **LLM Client:**
  - [x] Implement Claude API client with Context-Engineered prompt template
  - [x] Implement async call (non-blocking, overlay triggered when response arrives)
  - [x] Basic GPT-4o fallback when Claude API unavailable
  - [x] Response caching in SQLite (term, language → explanation)

- [x] **Overlay UI:**
  - [x] PyQt6 frameless, always-on-top, transparent background window
  - [x] Cultural note card widget (term, explanation text, source badge)
  - [x] Auto-dismiss timer (configurable, default 8s)
  - [x] [Dismiss], [Pin], [Save] buttons
  - [x] Configurable overlay position (4 screen quadrants)

- [x] **Settings UI:**
  - [x] API key entry (Claude, GPT-4o)
  - [x] Subtitle file path selector
  - [x] Overlay position and auto-dismiss timer settings
  - [x] Language pair selection (source → target explanation language)

### Deliverables
- Functional desktop app: load subtitle file → detect Japanese/Korean cultural terms → display LLM explanation overlay
- SQLite cache working (repeat terms served from cache)
- Basic settings panel

### Success Criteria
- End-to-end latency (subtitle line → overlay visible): < 800ms on cache miss, < 150ms on cache hit
- Overlay correctly dismisses without blocking video
- Cultural keyword detection recall: > 80% on 100-term manual test set
- App runs stably for 2-hour viewing session without crashes

### Estimated Effort
- 2 engineers × 4 weeks = 8 person-weeks

---

## Phase 2: ML/AI Integration — Smart Features
**Duration:** Week 7–10  
**Goal:** Replace keyword-only detection with fine-tuned NER; add audio fallback; expand to 5 languages.

### Tasks
- [x] **Custom NER Model:**
  - [x] Construct training dataset: 50K subtitle sentences across JP/KR/ZH/TH/ES with 6 entity labels
  - [x] Semi-automated annotation pipeline (GPT-4o initial pass + human review)
  - [x] Fine-tune dslim/bert-base-NER with PEFT/LoRA (HuggingFace Trainer)
  - [x] Evaluate: F1 score per entity type, false positive rate on neutral sentences
  - [x] Integrate fine-tuned model into detection pipeline (replaces keyword fallback for unseen terms)

- [x] **Semantic Deduplication:**
  - [x] Integrate sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
  - [x] Embed all detected terms; skip API call if cosine similarity > 0.92 to cached term
  - [x] Handle variant forms (e.g., "空気読む" vs "空気読めない" vs "KY")

- [x] **Audio Fallback Pipeline:**
  - [x] Implement sounddevice-based system audio capture (loopback recording)
  - [x] Whisper-large-v3 streaming inference (30s sliding window with overlap)
  - [x] Auto-activation when no subtitle file detected
  - [x] Latency measurement and buffering strategy

- [x] **Language Expansion:**
  - [x] Add Mandarin Chinese (jieba tokenizer, ZH cultural keyword dict — 500 terms)
  - [x] Add Thai (pythainlp tokenizer, TH cultural keyword dict — 200 terms)
  - [x] Add Spanish (Spanish slang dict — 300 terms, Latin American vs Castilian tagging)
  - [x] Test NLLB-200 as multilingual fallback translator for rare languages

- [x] **Confidence Scoring:**
  - [x] Assign confidence scores to NER detections (model probability)
  - [x] Display confidence indicator in overlay (high/medium/low badge)
  - [x] Suppress low-confidence detections below threshold (configurable)

### Deliverables
- Fine-tuned NER model (F1 > 0.78 on custom test set)
- Audio fallback pipeline working for Japanese and Korean audio
- 5-language support: JP, KR, ZH, TH, ES
- Semantic deduplication reducing redundant API calls by >40%

### Success Criteria
- NER model detects cultural terms not in keyword dictionary (F1 > 0.75 on held-out set)
- Audio pipeline: term detection within 3s of spoken phrase
- False positive rate (non-cultural terms triggering overlay): < 5%
- Cache hit rate: > 55% after 10 hours of viewing

### Estimated Effort
- 2 engineers × 4 weeks = 8 person-weeks

---

## Phase 3: External LLM API Integration & Context Deepening
**Duration:** Week 11–12  
**Goal:** Harden the LLM pipeline, implement series context memory, and add TTS audio output.

### Tasks
- [x] **Series Context Memory:**
  - [x] Per-series SQLite table: characters, factions, plot events, locations
  - [x] Auto-extract entities from subtitle file pre-scan (run NER on full subtitle file at session start)
  - [x] Inject series context into LLM prompt for richer explanations ("In this show, X is the name of...")
  - [x] Context grows across episodes (session persistence)

- [x] **LLM Prompt Hardening:**
  - [x] Implement retry logic with exponential backoff for API errors
  - [x] Token budget management (keep prompt under 512 tokens)
  - [x] Streaming response support (show explanation word-by-word as it arrives)
  - [x] Full Ollama (local) integration for offline fallback (mistral, llama3.2)

- [x] **Explanation Depth Levels:**
  - [x] User setting: Quicknote (1 sentence) / Standard (3 sentences) / Deep Dive (paragraph)
  - [x] Deep Dive mode includes: historical context, further reading link, related terms

- [x] **TTS Audio Mode:**
  - [x] Integrate edge-tts (Microsoft Edge TTS via unofficial API) for natural-sounding audio
  - [x] User toggle: visual overlay only / audio only / both
  - [x] Volume and voice selection settings

- [x] **Browser Extension Prototype:**
  - [x] Research WebExtension API for subtitle DOM injection detection
  - [x] Prototype Chrome extension that reads subtitle elements from Netflix/Crunchyroll DOM
  - [x] Proxy subtitle text to local Python daemon via WebSocket

### Deliverables
- Series context memory active and improving explanation quality
- Full 3-tier LLM fallback chain operational (Claude → GPT-4o → Ollama)
- TTS audio mode working
- Browser extension prototype (alpha)

### Success Criteria
- Series context memory measurably improves LLM explanation relevance (A/B test: 70% user preference for context-enhanced explanations)
- Offline mode (Ollama) produces usable explanations (quality rating ≥ 3.5/5 in user test)
- TTS audio output adds <500ms additional latency

### Estimated Effort
- 2 engineers × 2 weeks = 4 person-weeks

---

## Phase 4: Self-Improving Knowledge Loop — SECOND-KNOWLEDGE-BRAIN Auto-Update
**Duration:** Week 13–14  
**Goal:** Implement automated research crawler to keep cultural knowledge base current.

### Tasks
- [x] **crawl4ai Integration:**
  - [x] Configure crawl4ai crawler targeting: r/anime (Reddit), Anime News Network, DramaWiki, TVTropes cultural pages, NHK World cultural articles
  - [x] Domain-specific Google Scholar queries for subtitling and cultural translation research
  - [x] Weekly cron job execution (Windows Task Scheduler / systemd)

- [x] **Cultural Dictionary Auto-Expansion:**
  - [x] Scrape newly trending slang from Twitter/X using filtered keyword search (JP/KR/ZH)
  - [x] Use LLM to validate and format new terms before adding to dictionary
  - [x] Human review queue for low-confidence auto-additions
  - [x] Version-control cultural dictionary (git-tracked CSV)

- [x] **Knowledge Update Log:**
  - [x] Auto-append to SECOND-KNOWLEDGE-BRAIN.md after each crawler run
  - [x] Date-stamped entries with source URL and confidence score

- [x] **Model Re-evaluation:**
  - [x] Monthly automated evaluation run: test fine-tuned NER on latest subtitle samples
  - [x] Alert if F1 drops > 5% (trigger re-fine-tuning pipeline)

### Deliverables
- Weekly automated cultural knowledge update pipeline running
- Cultural dictionary growing by 50+ validated terms per week
- SECOND-KNOWLEDGE-BRAIN.md auto-updated with date-stamped entries

### Success Criteria
- Crawler runs without manual intervention for 4 consecutive weeks
- New trending slang terms appearing in system within 7 days of going viral
- Zero false entries introduced to dictionary by auto-expansion (human review catching all errors)

### Estimated Effort
- 1 engineer × 2 weeks = 2 person-weeks

---

## Phase 5: Testing, Polish & Deployment
**Duration:** Week 15–16  
**Goal:** Production-quality application with full test coverage, packaged installer, and documentation.

### Tasks
- [x] **Testing:**
  - [x] Unit tests: subtitle parser, timestamp sync, cultural term detector, LLM client, cache layer (pytest)
  - [x] Integration tests: full pipeline E2E with pre-recorded subtitle + audio test fixtures
  - [x] Performance tests: latency benchmarks under load (concurrent subtitle lines)
  - [x] UI tests: overlay render, dismiss, pin, save actions
  - [x] Stress test: 4-hour continuous operation with no memory leaks

- [x] **User Experience Polish:**
  - [x] Smooth overlay animation (fade in/out)
  - [x] Dark/light theme support
  - [x] Font size and overlay transparency controls
  - [x] Onboarding wizard (first-run: API key setup, subtitle file selection, language pair)
  - [x] Keyboard shortcuts (e.g., Ctrl+D dismiss, Ctrl+P pin, Ctrl+S save)

- [x] **Documentation:**
  - [x] README.md with installation guide (Windows/macOS/Linux)
  - [x] User guide with screenshots
  - [x] API key setup guide for each LLM provider
  - [x] Contributing guide for cultural dictionary contributions

- [x] **Packaging & Distribution:**
  - [x] PyInstaller single-executable build for Windows (x64)
  - [x] PyInstaller build for macOS (Universal2)
  - [x] GitHub Actions CI/CD: automated builds on tag push
  - [x] GitHub Releases with download links

- [x] **Legal & Compliance Review:**
  - [x] Verify subtitle file usage doesn't violate platform ToS
  - [x] OpenSubtitles API terms compliance
  - [x] GDPR compliance review (EU users)

### Deliverables
- >85% test coverage across all modules
- Single-file installer for Windows and macOS
- Full documentation suite
- GitHub Releases v1.0.0 published

### Success Criteria
- All tests pass in CI
- Application installs and runs without Python knowledge (zero setup for end user)
- First 50 beta users onboarded with <10% support ticket rate
- Average session duration > 45 minutes (proxy for engagement / utility)

### Estimated Effort
- 2 engineers × 2 weeks = 4 person-weeks

---

## Summary Timeline

| Phase | Name | Weeks | Effort |
|-------|------|-------|--------|
| 0 | Research & Setup | 1–2 | 4 person-weeks |
| 1 | MVP Core Loop | 3–6 | 8 person-weeks |
| 2 | ML/AI Integration | 7–10 | 8 person-weeks |
| 3 | LLM Deepening | 11–12 | 4 person-weeks |
| 4 | Self-Improving Loop | 13–14 | 2 person-weeks |
| 5 | Testing & Deployment | 15–16 | 4 person-weeks |
| **Total** | | **16 weeks** | **30 person-weeks** |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Whisper latency too high on CPU-only machines | High | Medium | Provide smaller Whisper model (tiny/base) as low-resource option |
| MPV/VLC IPC API changes breaking timestamp sync | Medium | High | Abstract IPC behind interface; support file-based timestamp injection as fallback |
| LLM API rate limits during rapid scene changes | Medium | Medium | Rate limiter + queue; show "Loading..." state in overlay |
| Fine-tuned NER F1 below target | Medium | Medium | Fall back to expanded keyword dictionary; release NER improvement as v1.1 |
| Platform ToS issues (Netflix audio capture) | Medium | High | Document that audio capture is local-only; emphasize subtitle file input as primary path |
| Cultural term false positives annoying users | Low | High | Implement user feedback buttons; use feedback to improve confidence threshold |
