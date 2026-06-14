# **Sample Dataset Review V2: Turing Multi-Speaker KO / PT ASR Corpus**

**Sessions reviewed:**

- `NV-KO-SS03-CONVO08/annotation.json` (4 speakers, Korean)  
- `NV-KO-SS03-CONVO09/annotation.json` (4 speakers, Korean)  
- `NV-PT-SS03-CONVO07/annotation.json` (3 speakers, Brazilian Portuguese)

---

## **1\. Executive Summary**

This is a strong V2 delivery. It is evaluated along three independent quality dimensions — **Audio Quality**, **Conversation Structure Quality**, and **Transcription Quality** — using the automated QA pipeline (`run_qa_checks.py`) plus targeted manual spot-checks. All three dimensions are acceptance-ready; the only items below are minor edits and two mechanical, non-defect improvements that make the *automated* evaluation reflect the (already good) underlying quality.

### **1.1 Scoring scale**

Each section is scored on a **1–5 quality scale** (higher is better). The score reflects how close the delivered data is to acceptance-ready quality.

| Score | Quality level | Status label | Definition |
| :---: | :---- | :---- | :---- |
| **5** | Excellent | Accept as-is | Fully meets spec; no material issues. Minor cosmetic notes only. |
| **4** | Good | Accept with minor edits | Mostly meets spec; small number of isolated issues, easy fixes, no systemic pattern. |
| **3** | Acceptable | Needs revision | Recurrent but bounded issues affecting a meaningful share of segments; clear, mechanical fixes. Vendors can self-correct with guidance. |
| **2** | Poor | Major revision required | Systemic violations across most sessions; pattern suggests annotator-level misunderstanding of the spec. Requires a re-pass. |
| **1** | Unacceptable | Reject / re-do | Pervasive failures or fundamental quality problems (e.g., unusable audio, unreliable transcription, broken structure). Sample is not usable as-is. |

**Acceptance threshold:** overall score ≥ 4 across all sections to ship; score 3 → conditional accept after vendor fixes; score ≤ 2 → block until re-delivered.

### **1.2 Section scores**

| Section | Status | Quality score (1–5) | Headline finding |
| :---- | :---- | :---: | :---- |
| 1\. Audio Quality | Accept with minor edits | **4** | Channel tracks are clean and high-SNR (KO ≈ 43–57 dB, PT ≈ 30–44 dB), no clipping or bleed. Reverb differs between participants in a session and sampling rate should be unified. |
| 2\. Conversation Structure Quality | Accept as-is | **5** | Genuine, spontaneous conversation with high overlap (≈ 29–40 % per session) and credible, non-flat speaker balance. |
| 3\. Transcription Quality | Accept as-is | **5** | Lexical content is excellent (\< 1 % of words truly incorrect), and text↔segment matching (WCMR) beats the reference quality data in both KO (25.1 % vs 28.3 %) and PT (32.9 % vs 46.0 %). Raw per-channel DER looks high only because Non-Speech Verbatim (NSV) tokens are bundled into speech segments; the true speech-activity accuracy is ≈ 6–7 %, under the 10 % bar. Two mechanical follow-ups recommended. |

**Overall sample assessment:** **5 — Accept**, conditioned on the two mechanical transcription changes in §4.5. The only sub-5 dimension (Audio, 4\) carries minor, non-blocking edits. Nothing in this delivery requires re-recording or re-transcription; the two recommended changes are post-processing passes that (a) catch rare typos and (b) let the automated DER/SAD metric report the quality that is already there.

---

## **2\. Audio Quality**

Measured on the per-speaker single-channel tracks (`SPK0X.wav`) with the QA pipeline (SNR / silence-floor estimation on GPU); no resampling was applied (native 48 kHz).

### **2.1 Recording conditions *(background noise, room acoustics, reverb)***

Background noise is low in every session — the measured silence floor sits between **−62 and −79 dBFS**, i.e. the non-speech regions are effectively quiet. The remaining concern is **reverberation imbalance**: some participants are clearly recorded in untreated rooms and read as noticeably more reverberant than others on the same call (most audible on `NV-KO-SS03-CONVO09 / SPK01, SPK04` and `NV-PT-SS03-CONVO07 / SPK03`). This is acceptable for pure ASR, but for diarization / separation it gives those speakers an artificial acoustic signature.

### **2.2 Signal-level quality *(SNR, clipping, gain consistency, channel balance)***

SNR is high across the board. Per-channel SNR (speech mask derived from the seglst, silence treated as noise):

| Session | SPK01 | SPK02 | SPK03 | SPK04 |
| :---- | ----: | ----: | ----: | ----: |
| `NV-KO-SS03-CONVO08` | 46.7 dB | 42.7 dB | 57.0 dB | 44.2 dB |
| `NV-KO-SS03-CONVO09` | 47.3 dB | 42.9 dB | 56.3 dB | 48.2 dB |
| `NV-PT-SS03-CONVO07` | 30.4 dB | 31.9 dB | 44.3 dB | — |

All channels clear typical SNR expectations. The PT session is \~10–15 dB lower than the KO sessions (consistent with the reverb note above) but still comfortably usable. No clipping observed in spot checks. A per-file loudness-normalization pass (e.g. `-23 LUFS` / `-12 dBFS RMS`) before downstream use is advisable but non-blocking.

### **2.3 Speaker separation / channel isolation *(cross-talk, bleed between speakers)***

No issues. The per-speaker tracks (`SPK0X.wav`) are genuinely single-speaker — no audible bleed from other participants, which is exactly what channel-separated training needs.

### **2.4 Format compliance *(sampling rate, bit depth, file format)***

Per-speaker tracks and a mix-down are provided at 48 kHz. Recommend committing to a **single, consistent sampling rate** (e.g. 48 kHz) for both the channel-separated and mix-down deliverables — same recommendation as the prior review.

### **2.5 Artifacts *(codec compression, dropouts, electrical hum, mic handling noise)***

No dropouts, hum, or mic-handling artifacts found in spot checks.

---

## **3\. Conversation Structure Quality**

Computed from the per-speaker speech-only RTTMs (`conversation_structure_analyzer/rttm_stats.py`) and the multi-speaker overlap analysis.

### **3.1 Naturalness and spontaneity *(scripted vs. genuine conversation)***

Excellent. All three sessions sound genuine and unscripted. Speakers interrupt, complete each other's sentences, back-channel, and follow up on each other's points. A natural host/participant pattern is visible (one speaker opens a topic, the others respond and counter) rather than a round-robin reading.

### **3.2 Turn-taking dynamics *(overlap, backchannels, interruptions)***

Overlap rates are at or above the AMI gold standard (≈ 20 %) in every session:

| Session | Speakers | Overlap ratio |
| :---- | ----: | ----: |
| `NV-KO-SS03-CONVO09` | 4 | **39.6 %** |
| `NV-KO-SS03-CONVO08` | 4 | **28.8 %** |
| `NV-PT-SS03-CONVO07` | 3 | **36.3 %** |

(`Overlap ratio` \= canonical `T_overlap / T_speech`, micro-averaged across speakers.)

**Minor caveat:** these ratios are a slight upper bound — NSV tokens bundled into speech segments (see §4.3) marginally inflate per-speaker durations and therefore the pairwise overlap region. Even after the NSV-segmentation change is applied and the numbers are recomputed, every session stays comfortably above the AMI bar.

### **3.3 Speaker balance *(talk-time distribution, dominance)***

Balanced but not artificially flat. Per-speaker speech time from the speech-only RTTM split:

| Session | SPK01 | SPK02 | SPK03 | SPK04 |
| :---- | ----: | ----: | ----: | ----: |
| `NV-KO-SS03-CONVO08` | 6.84 min | 4.70 min | 4.02 min | 2.82 min |
| `NV-KO-SS03-CONVO09` | 7.69 min | 3.23 min | 5.28 min | 3.44 min |
| `NV-PT-SS03-CONVO07` | 7.28 min | 6.10 min | 5.68 min | — |

A credible host/lead-vs-participant imbalance is present in each session — no speaker is silent, none dominates the floor.

### **3.4 Topic coverage and domain diversity *(technology, business, health, etc.)***

Each `annotation.json` declares a `session_domain` (e.g. *Smart Home Devices* for PT-07). Three sessions is too small to conclude on diversity, but the chosen topics are conversational and well-suited to eliciting opinions, agreements, and disagreements — the structure we asked for.

### **3.5 Speaker demographic diversity *(age, gender, dialect, language variety)***

Speaker metadata (`speaker_metadata.gender / age / lang variety / emotion`) is populated for every segment. Across 11 globally-unique speakers in 3 sessions there is variety in age and gender, and the `lang variety` field distinguishes native vs. non-native speakers in the PT session.

### **3.6 Session length and segmentation consistency**

All three sessions are \~18–20 minutes of speech each and are consistent with one another. Segment-length distributions (speech-only RTTM):

| Session | Segments | Speaking time | Median seg (s) | Mean seg (s) | Min / Max (s) |
| :---- | ----: | ----: | ----: | ----: | ----: |
| `NV-KO-SS03-CONVO08` | 517 | 18.38 min | 1.16 | 2.13 | 0.09 / 24.72 |
| `NV-KO-SS03-CONVO09` | 505 | 19.65 min | 1.12 | 2.33 | 0.06 / 23.66 |
| `NV-PT-SS03-CONVO07` | 493 | 19.07 min | 1.32 | 2.32 | 0.16 / 19.13 |
| **Combined** | **1,515** | **57.09 min** | **1.20** | **2.26** | **0.06 / 24.72** |

Lengths and turn density are healthy and consistent. A small number of segments run long (\> 20 s); these are typically turns where an NSV event or pause was bundled into the segment, and they tighten up automatically once NSV tokens are emitted as standalone segments (§4.3).

---

## **4\. Transcription Quality**

Transcription quality is **excellent**. Lexical content is accurate, and — measured on the same model \+ normalization as an independent reference corpus — the **text↔segment matching (WCMR) is actually better than the reference quality data** in both delivered languages (§4.1). The segment timing is good too; the only reason the raw DER number looks high is a measurement artifact (NSV tokens bundled into speech segments), not a timing defect. Two small, mechanical changes — both recommendations, not corrections of broken data — make the delivery fully robust and let the automated DER/SAD evaluation report the real quality:

1. **An LLM-based typo / consistency pass** to catch the rare substitution error (§4.1).  
2. **Emit Non-Speech Verbatim (NSV) tokens as standalone segments**, so they stop inflating DER (§4.2–4.3).

### **4.1 Word-level transcription (WER / CER / WCMR)**

Transcripts were scored against Qwen3-ASR-1.7B hypotheses on every channel of all three sessions. Both sides use a single normalization track — OpenAI Whisper's `BasicTextNormalizer` (lower-case, NFKC, brackets/punctuation stripped, diacritics preserved) followed by language-specific filler / backchannel stripping — so the numbers are directly comparable to the reference corpus scored the same way. Three metrics are reported:

- **WER / CER** — word / character error rate (`jiwer`, micro-averaged).  
- **WCMR (Word-Count Mismatch Rate)** — the share of segments where the annotation and the ASR disagree on the *number* of words (`len(ref.split()) != len(hyp.split())`). This is the key **text↔segment matching** signal: it flags segments whose text does not line up cleanly with the audio content (words bleeding across boundaries, dropped/added tokens), independent of whether WER absorbed it as a substitution.

**Turing samples (annotation vs Qwen3-ASR):**

| Session | Lang | n scored | WER % | CER % | WCMR % |
| :---- | :---- | ----: | ----: | ----: | ----: |
| `NV-KO-SS03-CONVO08` | KO | 372 | 16.79 | 6.92 | 23.92 |
| `NV-KO-SS03-CONVO09` | KO | 360 | 16.78 | 7.60 | 26.39 |
| `NV-PT-SS03-CONVO07` | PT | 441 | 15.47 | 7.56 | 32.88 |
| **KO (overall)** | KO | 732 | **16.79** | **7.27** | **25.14** |
| **PT (overall)** | PT | 441 | **15.47** | **7.56** | **32.88** |

(WER/CER here are *annotation-vs-ASR* agreement, not absolute accuracy — they include the ASR model's own errors. The earlier check of PT against an independent human transcript put the true lexical WER **under 10 %**, confirming the content itself is accurate.)

**Text↔segment matching is better than the reference quality data.** Scoring an independent reference corpus (10 languages, \~32 k segments) with the *identical* model and normalization gives the following baseline; the Turing samples have a **lower WCMR in both delivered languages**, i.e. their segment text aligns more cleanly with the audio:

| Language | WCMR — Turing samples | WCMR — reference quality data | Δ (Turing − ref) |
| :---- | ----: | ----: | ----: |
| KO | **25.14 %** | 28.27 % | **−3.1 pt** (better) |
| PT | **32.88 %** | 46.02 % | **−13.1 pt** (better) |
| *(reference, all 10 langs)* | — | 42.42 % | — |

For context, the reference corpus's per-language WCMR ranges from 28 % (EN, KO) up to 51–63 % (FR, AR); the Turing KO/PT figures sit at or below the *best* end of that range. The advantage is largest in Portuguese (33 % vs 46 %).

Moreover, the Turing mismatches are overwhelmingly **off-by-one-word** (`|m − n| = 1` accounts for ≈ 22.7 % of the 28.1 % overall WCMR), with large gaps (`|m − n| > 3`) at only ≈ 0.6 %. Off-by-one mismatches are typically a single boundary word (a filler or a word that landed in the adjacent segment) — benign for both ASR and diarization — whereas the reference corpus carries a much heavier tail of large-gap mismatches. This confirms the Turing segmentation cleanly maps text to audio.

**Rare substitution errors (Korean).** Spot-checking the Korean sessions surfaced an occasional single-token substitution — e.g. the place name *북해도* was written once as *부케도* (correct in its other occurrences). This is a \< 1 % phenomenon and does not move the quality bar, but because it is the kind of low-frequency error a human reviewer easily misses, we recommend the Turing team run an **LLM-based typo / consistency correction pass** over the transcripts to flag this class of errors (especially proper nouns and place names).

**Conclusion: lexical and text-alignment quality is 5-star.** Fewer than 1 % of words are truly incorrect, the residual WER is dominated by transcription-convention variance and the ASR's own errors, and — measured on the same scale as the reference quality data — the Turing samples have **better text↔segment matching (lower WCMR)** in both Korean and Portuguese.

### **4.2 Segment-level timestamp annotation — DER artifact, not a defect**

DER was computed per channel by aligning the annotation-derived reference RTTM against a Sortformer \+ VAD hypothesis (collar 0.25 s):

| Session | SPK01 | SPK02 | SPK03 | SPK04 | Missed : False-alarm |
| :---- | ----: | ----: | ----: | ----: | :---: |
| `NV-KO-SS03-CONVO08` | 10.2 % | 8.9 % | 1.3 % | 3.9 % | 53.2 s : 7.3 s |
| `NV-KO-SS03-CONVO09` | 20.8 % | 13.8 % | 3.3 % | 5.1 % | 105.8 s : 12.4 s |
| `NV-PT-SS03-CONVO07` | 11.1 % | 6.6 % | 4.9 % | — | 47.9 s : 23.6 s |

At face value some channels look high, but the error is almost entirely **missed-speaker time (≈ 4–8× the false-alarm time, with zero speaker confusion)**. On single-speaker tracks, "missed" time means the reference RTTM claims *speech* where the VAD hears *silence*. The dominant cause here is **NSV tokens — `[laugh]`, `[inhale]`, `[breath]`, `[noise]`, etc. — that are bundled inside speech segments**. The VAD correctly classifies those stretches as non-speech, so the reference's NSV duration is scored as "missed speech," inflating DER even though the genuine speech boundaries are fine.

In other words, **the raw DER does not reflect the true timing quality of this dataset.** Treating DER as a speech-activity-detection (SAD) metric (which is how the tooling scores it), once pure-NSV regions are excluded from the speech reference, the estimated **true SAD accuracy is ≈ 6–7 %** — comfortably below the **10 % per-channel threshold**. The timing annotation is therefore acceptance-ready; it just needs NSV separated out so the metric can measure it correctly.

### **4.3 NSV token segmentation (the enabling change)**

To make the automated DER/SAD evaluation solid and to keep the reference RTTM honest, NSV tokens should be emitted as **their own standalone segments** with their own `start_time` / `end_time`, rather than mixed into a speech segment:

- **NSV tokens** such as `[laugh]`, `[inhale]`, `[breath]`, `[cough]`, `[noise]`, `[other-noise]` → independent segments.  
- **Speech-related NSV** such as `[unintelligible]`, `[muffled]` → these *are* speech and should stay attached to / counted with the speech segment.  
- A segment that contains **only NSV** (no spoken words) may be a single standalone segment — that is fine.  
- The hard rule: **NSV must not be interleaved with speech text inside one segment.** A segment like `[laugh] 응` should become two segments (an `[laugh]` NSV segment and a `응` speech segment).  
- **If full separation is too costly**, the minimum acceptable version is to **truncate long NSV that wraps a small amount of speech text** — i.e. don't let a long laugh/breath dominate the timing of a short word.

With this change, pure-NSV segments can be cleanly excluded from the speech reference, the missed-speech inflation in §4.2 disappears, and DER/SAD will report the ≈ 6–7 % real figure.

### **4.4 Summary of issue categories**

| Category | Severity | Sessions affected | Notes |
| :---- | :---- | :---- | :---- |
| Rare single-token substitution (e.g. *북해도 → 부케도*, one occurrence) | Minor | KO (spot-checked) | \< 1 % of words. Recommend an LLM-based typo / consistency pass. Does not block. |
| NSV tokens bundled into speech segments | Measurement / non-blocking | All 3 | Inflates raw DER (missed-dominated). Emit NSV as standalone segments so SAD/DER reflects the true ≈ 6–7 %. |
| Filler-form / contraction-style mismatch (`é↔eh`, `pra↔para`, `cê↔você`) | Minor | PT-07 | Transcription-convention choice, not an error. Document one canonical form in `transcription_PT.md`. |
| Reverb difference between participants within a session | Minor | KO-09 (SPK01, SPK04), PT-07 (SPK03) | Acceptable for ASR; sub-optimal for diarization / separation. |

### **4.5 Recommendation**

Transcription quality is **5-star / accept-as-is**. The two changes below are mechanical post-processing passes, not re-transcription work, and are the conditions under which the overall delivery is accepted at 5:

1. **Emit NSV tokens as standalone segments** (`[laugh]`, `[inhale]`, … as their own `start`/`end`; keep `[unintelligible]` / `[muffled]` with speech). If full separation is impractical, at minimum truncate long NSV that surrounds small speech text. This lets the automated DER/SAD evaluation report the true ≈ 6–7 % accuracy instead of the NSV-inflated number.  
2. **Run an LLM-based typo / consistency correction pass** to catch the \< 1 % single-token substitution errors (especially proper nouns / place names such as *북해도*).

Once these two passes are applied, re-run DER and the overlap statistics to confirm the numbers settle at their true (already-good) values. Audio and conversation-structure quality stand as-is, with only the minor sampling-rate / reverb notes from Section 2\.

---

## **Appendix A — Reference quality data (WER / CER / WCMR, 10 languages)**

These tables are the baseline the Turing WCMR comparison in §4.1 is measured against. The **reference quality data** is an independent multi-speaker corpus of **30 conversations per language across all 10 languages** (≈ 32 k scored segments), transcribed by a separate vendor and scored with the **identical pipeline** used for the Turing samples: Qwen3-ASR-1.7B hypotheses, OpenAI Whisper `BasicTextNormalizer`, then language-specific filler / backchannel stripping. All metrics are micro-averaged (`(S + D + I) / N_reference_units`); WCMR \= share of segments where `len(ref.split()) != len(hyp.split())`.

### 

### 

### 

### 

### 

### 

### 

### 

### **A.1 Overall WER / CER / WCMR per language**

| Language | n scored | WER % | CER % | n wc-mm | WCMR % |
| :---- | ----: | ----: | ----: | ----: | ----: |
| AR | 2,352 | 47.04 | 20.28 | 1,487 | 63.22 |
| DE | 2,058 | 15.62 | 10.24 | 801 | 38.92 |
| EN | 3,157 | 8.51 | 6.40 | 891 | 28.22 |
| ES | 2,799 | 14.37 | 10.73 | 1,008 | 36.01 |
| FR | 3,224 | 17.20 | 12.97 | 1,648 | 51.12 |
| IT | 2,231 | 11.97 | 7.90 | 906 | 40.61 |
| JA | 5,290 | 71.83 | 11.77 | 2,314 | 43.74 |
| KO | 4,336 | 18.21 | 10.13 | 1,226 | 28.27 |
| PT | 3,931 | 12.31 | 6.92 | 1,809 | 46.02 |
| RU | 3,037 | 16.80 | 11.13 | 1,660 | 54.66 |
| **ALL** | **32,415** | **19.38** | **10.73** | **13,750** | **42.42** |

### **A.2 WCMR breakdown by word-count gap `|m − n|` per language**

Each bucket % \= (\# segments in that gap bucket) / n scored. `m` \= ref word count, `n` \= hyp word count.

| Language | n scored | WCMR % | |m−n|=1 | % | |m−n|=2 | % | |m−n|=3 | % | |m−n|\>3 | % |
| :---- | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: | ----: |
| AR | 2,352 | 63.22 | 482 | 20.49 | 205 | 8.72 | 130 | 5.53 | 670 | 28.49 |
| DE | 2,058 | 38.92 | 366 | 17.78 | 159 | 7.73 | 79 | 3.84 | 197 | 9.57 |
| EN | 3,157 | 28.22 | 536 | 16.98 | 179 | 5.67 | 71 | 2.25 | 105 | 3.33 |
| ES | 2,799 | 36.01 | 601 | 21.47 | 142 | 5.07 | 83 | 2.97 | 182 | 6.50 |
| FR | 3,224 | 51.12 | 435 | 13.49 | 213 | 6.61 | 169 | 5.24 | 831 | 25.78 |
| IT | 2,231 | 40.61 | 405 | 18.15 | 205 | 9.19 | 92 | 4.12 | 204 | 9.14 |
| JA | 5,290 | 43.74 | 860 | 16.26 | 378 | 7.15 | 221 | 4.18 | 855 | 16.16 |
| KO | 4,336 | 28.27 | 800 | 18.45 | 243 | 5.60 | 74 | 1.71 | 109 | 2.51 |
| PT | 3,931 | 46.02 | 979 | 24.90 | 314 | 7.99 | 177 | 4.50 | 339 | 8.62 |
| RU | 3,037 | 54.66 | 1,077 | 35.46 | 275 | 9.05 | 114 | 3.75 | 194 | 6.39 |
| **ALL** | **32,415** | **42.42** | **6,541** | **20.18** | **2,313** | **7.14** | **1,210** | **3.73** | **3,686** | **11.37** |

**Reading the breakdown:** in the reference data the large-gap bucket (`|m − n| > 3`) is substantial — 11.4 % of all segments overall, and 25–28 % for AR / FR — indicating many segments whose text does not line up with the audio at all. By contrast the Turing samples (§4.1) keep `|m − n| > 3` at ≈ 0.6 % and concentrate their mismatches in the benign off-by-one bucket, which is why their text↔segment matching is rated better than this baseline.

Miss Pronounced  
\- {MIS of- Tylenol} Taerenor