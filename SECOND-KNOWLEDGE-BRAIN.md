# SECOND-KNOWLEDGE-BRAIN.md — culture-immersion-avatar

> Self-improving knowledge base. Updated weekly by automated crawler (crawl4ai).
> Last manual seed: 2026-06-03

---

## Core Concepts & Theoretical Foundations

### Cultural Linguistics & Translation Theory
- **Cultural equivalence** (Nida, 1964): Translating meaning and cultural effect, not just words. Dynamic equivalence vs. formal equivalence — foreign media subtitles typically sacrifice dynamic equivalence.
- **Culture-specific items (CSIs)** (Díaz Cintas & Remael, 2014): Terms that carry cultural meaning untranslatable without footnotes — realia, allusions, humor, wordplay, taboo references.
- **Polysystem Theory** (Even-Zohar, 1990): Translation occupies a secondary position in target culture's literary system; subtitles further compress meaning due to temporal and spatial constraints.
- **Domestication vs. Foreignization** (Venuti, 1995): Subtitles tend toward domestication (replacing foreign concepts with local equivalents), erasing cultural specificity that platforms like culture-immersion-avatar should restore.

### Subtitling Constraints
- **Reading speed constraint:** Viewers read subtitles at 140–180 WPM; expansion for cultural notes is impossible inline. This justifies an overlay system external to the subtitle track.
- **Temporal compression:** Subtitles follow speech pace — there is no room for cultural footnotes in standard subtitle formats (.srt, .ass). Cultural annotation must be asynchronous.
- **Subtitle translation loss studies:** Research shows 15–25% of humor, wordplay, and cultural allusions are lost or altered in subtitle translation (Yau, 2004; Chiaro, 2008).

### Real-Time NLP Concepts
- **Sliding window transcription:** Whisper processes fixed-length audio chunks (30s). Overlapping windows (stride 15s) reduce boundary errors on phrase detection.
- **Named Entity Recognition (NER):** Sequence labeling task — BIO tagging scheme (Begin, Inside, Outside) used to tag custom cultural entity types.
- **Semantic similarity:** Cosine distance in embedding space used to match variant forms of the same cultural concept (e.g., "츤데레" and "tsundere" share high semantic similarity across languages).

### Context Engineering for LLM
- **Role prompting:** Assigning a domain expert persona (e.g., "Cultural Encyclopedia Expert") significantly improves LLM factual accuracy for specialized domains (Wei et al., 2022 — Chain-of-Thought Prompting).
- **Context injection:** Providing surrounding dialogue (±3 subtitle lines) dramatically improves LLM disambiguation — the same word has different cultural meanings in comedy vs. drama vs. historical settings.
- **Few-shot cultural examples:** Including 2–3 example explanations in the prompt (one-shot or few-shot) constrains output format and register, reducing verbosity and off-topic responses.

---

## Key Research Papers

| Title | Authors | Year | Venue | Link | Relevance |
|-------|---------|------|-------|------|-----------|
| Audiovisual Translation: Subtitling | Díaz Cintas, J. & Remael, A. | 2014 | Routledge (2nd ed.) | ISBN: 9781909309265 | Foundational reference on subtitle translation constraints and cultural loss |
| Humour and Translation | Chiaro, D. | 2008 | John Benjamins | DOI: 10.1075/btl.75 | Quantifies humor loss in subtitle translation; relevant to wordplay detection |
| Towards a Science of Translating | Nida, E. | 1964 | Brill | ISBN: 9789004015296 | Dynamic equivalence theory — theoretical basis for cultural annotation over literal translation |
| The Position of Translated Literature within the Literary Polysystem | Even-Zohar, I. | 1990 | Poetics Today | https://www.jstor.org/stable/1772668 | Polysystem theory explaining why subtitles flatten cultural layers |
| The Translator's Invisibility | Venuti, L. | 1995 | Routledge | ISBN: 9780415115929 | Domestication vs. foreignization — why cultural specificity is erased in subtitles |
| Robust Speech Recognition via Large-Scale Weak Supervision (Whisper) | Radford et al. | 2023 | ICML | https://arxiv.org/abs/2212.04356 | Whisper model paper — STT backbone for audio fallback pipeline |
| No Language Left Behind: NLLB | NLLB Team, Meta | 2022 | arXiv | https://arxiv.org/abs/2207.04672 | 200-language translation model used for multilingual support |
| BERT: Pre-training of Deep Bidirectional Transformers | Devlin et al. | 2019 | NAACL | https://arxiv.org/abs/1810.04805 | Foundational model for NER fine-tuning pipeline |
| Chain-of-Thought Prompting Elicits Reasoning in LLMs | Wei et al. | 2022 | NeurIPS | https://arxiv.org/abs/2201.11903 | Context engineering principles for LLM cultural explanation quality |
| Sentence-BERT: Sentence Embeddings using Siamese BERT | Reimers & Gurevych | 2019 | EMNLP | https://arxiv.org/abs/1908.10084 | Semantic similarity model for cultural term deduplication |
| LoRA: Low-Rank Adaptation of Large Language Models | Hu et al. | 2022 | ICLR | https://arxiv.org/abs/2106.09685 | PEFT fine-tuning method for custom NER model training |
| Cultural Scripts: What They Are and How to Use Them | Wierzbicka, A. | 2004 | Intercultural Pragmatics | DOI: 10.1515/iprg.1.2.169 | Cultural script theory — underpins how cultural explanations should be structured |
| Machine Translation of Culturally Specific Items | Vinay & Darbelnet | 1958 (tr. 1995) | John Benjamins | ISBN: 9789027216007 | Classic taxonomy of translation procedures for culture-specific items |

---

## State-of-the-Art ML/DL Models

### Speech-to-Text (STT)
| Model | HuggingFace ID | Benchmark | Notes |
|-------|---------------|-----------|-------|
| Whisper Large v3 | openai/whisper-large-v3 | WER 2.7% (LibriSpeech test-clean) | Primary audio transcription; 99 languages |
| Whisper Medium | openai/whisper-medium | WER 3.4% (LibriSpeech) | Lower-resource alternative |
| MMS-300M | facebook/mms-300m | Strong on low-resource languages | Meta Massively Multilingual Speech |

### Named Entity Recognition (NER)
| Model | HuggingFace ID | Benchmark | Notes |
|-------|---------------|-----------|-------|
| BERT-base NER | dslim/bert-base-NER | F1 92.4% (CoNLL-2003) | Base model for fine-tuning |
| XLM-RoBERTa NER | xlm-roberta-large-finetuned-conll03-english | F1 93.4% | Multilingual; better for cross-lingual cultural entities |
| mBERT NER | bert-base-multilingual-cased | F1 85.3% (WikiANN) | Baseline multilingual NER |

### Translation
| Model | HuggingFace ID | Benchmark | Notes |
|-------|---------------|-----------|-------|
| NLLB-200-Distilled-600M | facebook/nllb-200-distilled-600M | BLEU ~35–45 (varies by pair) | 200 languages; primary multilingual translation |
| NLLB-200-1.3B | facebook/nllb-200-1.3B | Higher quality | Use when compute allows |
| Opus-MT JP→EN | Helsinki-NLP/opus-mt-ja-en | BLEU 22.4 (WMT) | Fast JP→EN for keyword translation |
| Opus-MT KO→EN | Helsinki-NLP/opus-mt-ko-en | BLEU 20.1 | Fast KO→EN |

### Semantic Similarity / Embeddings
| Model | HuggingFace ID | Benchmark | Notes |
|-------|---------------|-----------|-------|
| Multilingual MiniLM | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 | STS-B 84.9 | Fast, multilingual; deduplication |
| LaBSE | sentence-transformers/LaBSE | Best multilingual STS | Higher quality, heavier |
| E5-multilingual-large | intfloat/multilingual-e5-large | MTEB SOTA | State-of-art cross-lingual retrieval |

### Language Detection
| Model | Source | Notes |
|-------|--------|-------|
| fastText lid.176.bin | Meta (fastText) | 176 languages, <1ms per detection |
| langdetect | Python (ported from Google) | Slower but no binary model needed |

---

## Tools, Libraries & Frameworks

| Tool | GitHub / Link | Use Case |
|------|-------------|---------|
| crawl4ai | https://github.com/unclecode/crawl4ai | Web crawler for automated knowledge updates |
| PyQt6 | https://www.riverbankcomputing.com/software/pyqt/ | Desktop UI and transparent overlay |
| pysrt | https://github.com/byroot/pysrt | .srt subtitle parsing |
| python-ass | https://github.com/chireiden/python-ass | .ass subtitle parsing (Advanced SubStation Alpha) |
| webvtt-py | https://github.com/glut23/webvtt-py | .vtt WebVTT subtitle parsing |
| watchdog | https://github.com/gorakhargosh/watchdog | Cross-platform file system watcher |
| sounddevice | https://python-sounddevice.readthedocs.io/ | System audio loopback capture |
| edge-tts | https://github.com/rany2/edge-tts | Natural TTS via Microsoft Edge voices |
| keyring | https://github.com/jaraco/keyring | OS-native secure credential storage |
| MeCab | https://taku910.github.io/mecab/ | Japanese morphological tokenizer |
| KoNLPy | https://konlpy.org/ | Korean NLP tokenization |
| jieba | https://github.com/fxsjy/jieba | Chinese text segmentation |
| pythainlp | https://github.com/PyThaiNLP/pythainlp | Thai NLP processing |
| aiosqlite | https://github.com/omnilib/aiosqlite | Async SQLite for Python |
| pydantic-settings | https://github.com/pydantic/pydantic-settings | Type-safe config management |
| Ollama | https://github.com/ollama/ollama | Local LLM inference server |
| AnkiConnect | https://github.com/FooSoft/anki-connect | Anki flashcard integration API |
| PyInstaller | https://github.com/pyinstaller/pyinstaller | Single-executable packaging |
| OpenSubtitles API | https://opensubtitles.stoplight.io/ | Subtitle database for pre-caching |
| Kitsunekko | https://kitsunekko.net/ | Japanese subtitle database for training data |

---

## Self-Update Protocol (crawl4ai Configuration)

### Target Sources

| Source | URL Pattern | Content Type | Priority |
|--------|------------|-------------|---------|
| ArXiv cs.CL | arxiv.org/list/cs.CL/recent | NLP/CL papers | High |
| HuggingFace Papers | huggingface.co/papers | ML model papers | High |
| Anime News Network | animenewsnetwork.com/encyclopedia | Anime cultural reference | Medium |
| DramaWiki | wiki.d-addicts.com | K-drama cultural notes | Medium |
| TVTropes (culture) | tvtropes.org/pmwiki/pmwiki.php/Main/JapanTakesOverTheWorld | Pop culture tropes | Medium |
| NHK World Culture | nhk.or.jp/nhkworld/en/learnjapanese/ | Japanese cultural articles | Medium |
| Reddit r/anime | reddit.com/r/anime/search?q=cultural+reference | Community cultural notes | Low |
| ACL Anthology | aclanthology.org | Translation/NLP papers | High |
| Papers With Code | paperswithcode.com/task/machine-translation | SOTA benchmarks | High |

### Domain-Specific Search Queries

**Academic (Google Scholar / Semantic Scholar):**
- `"cultural untranslatability" subtitle film 2024`
- `"audiovisual translation" "cultural references" machine learning`
- `"subtitle NLP" "named entity" cultural`
- `"anime subtitle" translation loss cultural`
- `"K-drama" linguistic cultural analysis`
- `"real-time subtitle" overlay annotation system`

**HuggingFace Hub Queries:**
- `subtitle NER cultural`
- `multilingual sentiment subtitle`
- `whisper fine-tuned Japanese`
- `Korean named entity recognition`

**Model Benchmarks (Papers With Code):**
- Speech Recognition leaderboard — filter: multilingual
- Named Entity Recognition leaderboard — filter: multilingual
- Machine Translation leaderboard — filter: Asian languages

### crawl4ai Configuration Snippet
```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

config = CrawlerRunConfig(
    target_sources=[
        "https://arxiv.org/list/cs.CL/recent",
        "https://huggingface.co/papers",
        "https://aclanthology.org/search/?q=subtitle+cultural",
    ],
    keywords=[
        "cultural reference", "subtitle translation", "NER cultural",
        "audiovisual translation", "slang detection", "cross-lingual"
    ],
    max_pages_per_source=10,
    output_format="markdown",
    update_log_path="SECOND-KNOWLEDGE-BRAIN.md",
    section_append="## Knowledge Update Log",
)

async def weekly_update():
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(config.target_sources, config=config)
        process_and_append_results(results)
```

### Update Frequency
- **Weekly:** ArXiv cs.CL new papers, HuggingFace trending models, Reddit cultural discussion threads
- **Monthly:** Full sweep of DramaWiki, TVTropes, NHK World cultural articles
- **On-demand:** When user reports unknown cultural term not in dictionary

### Format for New Entries
```markdown
### [DATE] — [SOURCE]
**New Research / Tool / Term:**
- Title/Term: [title or term name]
- Source: [URL]
- Relevance: [1-2 sentence note on why this is relevant to culture-immersion-avatar]
- Action: [Add to dictionary / Update model benchmark / Note for future fine-tuning]
```

---

## Knowledge Update Log

### 2026-06-03 — Initial Seed (Manual)
- Seeded core research papers on audiovisual translation theory (Díaz Cintas, Chiaro, Venuti, Nida)
- Added Whisper, NLLB-200, BERT-NER, sentence-transformers model benchmarks
- Added 15 foundational tools and libraries
- Added crawl4ai self-update protocol with 9 target sources and domain-specific query templates
- Identified 10 improvement vectors beyond original idea (series memory, dialect detection, Anki integration, etc.)
- Status: Initial knowledge base seeded. Automated crawl4ai pipeline to be implemented in Phase 4.
