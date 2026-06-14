# NeMo Speech AI Multilingual Transcription Guidelines

This folder contains NeMo-style multilingual transcription guidelines. New language documents must follow the format and policy below so the guideline set stays consistent across languages.

This README is the source-of-truth for the required format and policy. Existing completed language files, especially `transcription_EN.md`, `transcription_JA.md`, `transcription_KO.md`, `transcription_DE.md`, and `transcription_RU.md`, show the current multilingual style.

## Required Policy

All generated language guidelines must follow these rules:

- Use only **Part 1 - Text normalization**, **Part 2 - Disfluency**, and **Part 3 - Rich Transcription: Paralinguistic Tokens**.
- Do **not** include timestamp annotation, diarization, WER/DER/SNR QA, channel bleed checks, or any old Part 4 / Part 5 sections.
- Transcriptions must use the **spoken form**. Do not use digits, compact URLs, currency symbols, percent signs, or numeric shorthand in `Correct` transcription examples.
- Digit and symbol forms may appear in `Incorrect` examples to show what not to do.
- Keep acronyms, initialisms, and clearly intended official spellings in canonical form when the speaker is saying them as such.
- Use standard orthography for the target language when the intended word is clear. Do not imitate predictable casual pronunciation or surface phonetics unless the language-specific section says to preserve a real colloquial/dialectal form.
- Keep NeMo bracket tokens in English for every language: `[laugh]`, `[cough]`, `[unintelligible]`, `[other-noise]`, etc.
- Use `{PRO: ...}` and `{MIS: ...}` only as optional superset annotations. Do not introduce alternate tag taxonomies.

## Required Document Shape

Each file must be named:

```text
guidelines_for_languages/transcription_[ISO_LANG_CODE].md
```

Use this top-level shape:

```markdown
# [Language] Transcription Guidelines

Language: [Language] ([Region])

## Part 1 - Text normalization

### Superset principle

### Text Normalization Rules

#### 1. Broad Principles
...

## Part 2 - Disfluency
...

## Part 3 - Rich Transcription: Paralinguistic Tokens
...
```

Use Markdown tables heavily. Prefer short rules plus `Audio`, `Correct`, and `Incorrect` examples.

## Part 1 Required Sections

Part 1 must include these topics, in this general order. Renumber sections as needed if the language requires additional orthography or number-system sections, but do not omit any required topic.

1. **Broad Principles**: State that abbreviations, symbols, shorthand, and numerals are expanded to spoken form, except acronyms/initialisms and clearly intended official spellings.
2. **Orthography and Script Choice**: Explain the target language's writing system, capitalization, spacing, diacritics, punctuation, and official spelling conventions.
3. **Numbers**: Spell out all digits and numeric expressions as spoken words. `Correct` must not use Arabic numerals.
4. **Language-specific Number Readings**, if relevant: Native/Sino number systems, digit-by-digit readings, counters, gender/case agreement, special readings, or zero variants.
5. **Non-Numeral Usage**: Idioms, proper nouns, compounds, and conventional expressions stay as words, never digits.
6. **Ordinals, Counters, Decades, and Age Ranges**: Spell out as spoken, preserving language-specific grammar.
7. **Dates**: Write dates as spoken words. Do not convert month/day/year into digit notation.
8. **Time of Day**: Write time as spoken words. Do not use clock notation such as `2:30`, `14:30`, or `8 PM` in `Correct`.
9. **Money / Currency**: Spell out amounts and currency words as spoken. Do not use `$`, `€`, `¥`, `%`, or digit amounts in `Correct`.
10. **Percentages**: Spell out the number and percent word in the target language.
11. **Measures / Units**: Spell out numbers and units as spoken. If the speaker reads letters or a technical shorthand, transcribe that spoken form.
12. **Fractions, Ratios, and Scores**: Spell out as spoken words.
13. **Negative Numbers**: Preserve the spoken negative marker and spell the number as words.
14. **Phone Numbers, Postal Codes, IDs, and Codes**: Write each digit group as spoken. Do not format as compact digit strings.
15. **Electronic Text (URLs, Emails, IPs)**: Write symbols aloud as spoken. Do not use compact URL/email/IP forms in `Correct`.
16. **Roman Numerals**: Use the spoken title/regnal/cardinal/ordinal form. Do not convert to Roman numerals in `Correct`.
17. **Abbreviations and Initialisms**: Expand spoken full forms; keep acronyms/initialisms only when spoken as such.
18. **Foreign Words and Loanwords**: Distinguish established target-language loanwords from actual foreign-language speech.
19. **Ambiguity**: Include context-based examples for exact homophones when the language has them. Do not include merely similar-sounding words.
20. **Guidelines for Language-specific Issues**: Add the highest-risk language-specific ASR transcription issues not already covered, with short examples.

The final numbering may differ when a language needs extra required sections, but **Ambiguity** and **Guidelines for Language-specific Issues** should appear at the end of Part 1.

## Spoken-Form Standard

This is the most important normalization rule.

`Correct` examples should look like this:

| Type | Correct style | Incorrect style |
|------|---------------|-----------------|
| Number | fourteen / vierzehn / 십사 / 十四 / четырнадцать | 14 |
| Date | twenty ninth April / 이천이십사 년 사 월 이십구 일 | 2024-04-29 |
| Time | two thirty / 두 시 삼십 분 / acht Uhr dreißig | 2:30 |
| Percent | zero point five percent / 영 점 오 퍼센트 | 0.5% |
| URL | example dot com slash pricing | example.com/pricing |

Before finishing a language file, scan tables for digits in the `Correct` column. Digits in `Correct` usually indicate a mistake unless they are part of a canonical acronym, brand, or official spelling that is intentionally preserved.

## Part 2 Required Sections

Part 2 must include:

1. **Filler Words**: Common lexical fillers and backchannels for the target language.
2. **Hesitation Markers and Vocal Fillers**: Canonical forms for filled pauses and reactive backchannels.
3. **Repetitions**: Unintentional repeated words or short phrases are kept as spoken, with no added punctuation.
4. **False Starts / Cut-Off Words**: Use a single dash (`-`) for abandoned word fragments.
5. **Casual Forms, Slang, and Dialect**: Preserve real colloquial or dialectal forms; normalize only predictable phonetic reductions when standard spelling is clearly intended.
6. **Spelled-Out Words**: Explain how to transcribe spelled-out Latin letters and language-specific letters/characters.
7. **Mispronunciations**: Transcribe intelligible substitutions as spoken; `{MIS: ...}` is optional superset metadata only.
8. **Wrong Grammar**: Preserve grammatical errors and non-standard morphology.

Do not use double dashes for repetitions or cutoffs. The current standard is no punctuation for repetitions and single dash for false starts.

## Part 3 Required Sections

Part 3 must keep the NeMo canonical English token spellings exactly. Do not translate bracket tokens into the target language.

Required subsections:

- `#### Rules for this section`
- `#### Token list and descriptions`
- `#### Examples`
- `#### Quick reference (canonical spellings)`

The token intro must make this explicit:

```markdown
Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into [LANGUAGE] or replace them with local-language labels.
```

## Source Material

An agent should be able to create a new language guideline by reading this README and the completed language examples in this folder. Use the existing examples to copy the document structure, table style, spoken-form normalization policy, disfluency style, and canonical token list.

When constructing a new language file, gather or infer language-specific knowledge for:

- orthography and script conventions
- number/date/time/currency/unit readings
- abbreviations, acronyms, names, and brands
- fillers, disfluencies, slang, dialect, and common reductions
- homophones, ambiguity, punctuation, and spacing
- foreign words, loanwords, and transliteration conventions

Do not add unrelated material such as alternate tag systems, links, task instructions, QA metrics, timestamps, diarization, or non-transcription sections.

## Validation Checklist

Before considering a generated guideline complete:

- [ ] File has only Part 1, Part 2, and Part 3.
- [ ] No Part 4, Part 5, timestamp, diarization, WER, DER, SNR, or channel-bleed sections.
- [ ] `Correct` transcription examples use spoken form, not digits or compact symbols.
- [ ] Ambiguity section includes exact target-language homophones (not just similar-sounding words) or context-sensitive spelling issues where relevant.
- [ ] Language-specific issues section covers the major ASR transcription risks for that language.
- [ ] Repetitions are kept as spoken with no added punctuation.
- [ ] False starts use a single dash, not double dashes.
- [ ] NeMo bracket tokens remain in English.
- [ ] Linter reports no obvious Markdown issues.

## Progress

- [x] `en-US` - US English: `transcription_EN.md`
- [x] `es` - Spanish (Spain, US, Latin America, Central America): `transcription_ES.md`
- [x] `fr-FR` - French (France): `transcription_FR.md`
- [x] `de-DE` - German (Germany): `transcription_DE.md`
- [x] `it-IT` - Italian (Italy): `transcription_IT.md`
- [x] `pt-BR` - Portuguese (Brazil): `transcription_PT.md`
- [x] `ar` - Arabic (Modern Standard Arabic, Saudi Arabia, United Arab Emirates): `transcription_AR.md`
- [x] `ja-JP` - Japanese (Japan): `transcription_JA.md`
- [x] `ko-KR` - Korean (Korea): `transcription_KO.md`
- [x] `ru-RU` - Russian (Russia): `transcription_RU.md`

## Agent Prompt Template

```text
@guidelines_for_languages/README.md

Read the README.
The README defines the required multilingual document format, NeMo policy, and canonical tags.
Use the completed language examples in this folder to match the current multilingual style.

Now create the same type of guideline for [LANGUAGE_NAME] ([LOCALE]).

Important:
- Keep the result in NeMo style and follow the README section requirements.
- Use language-specific knowledge for orthography, number systems, ambiguity, disfluencies, spelling, punctuation, loanwords, and common ASR transcription risks.
- Do not include timestamp annotation or non-transcription QA sections.
- The output must contain only Part 1, Part 2, and Part 3.
- Use spoken form for all numeric, symbolic, date/time, URL, code, and measurement transcriptions.
- Do not use digits in `Correct` transcription examples unless they are part of a canonical acronym, brand, or official spelling that is intentionally preserved.
- Keep NeMo canonical non-speech tokens in English.
- Use `{PRO: ...}` and `{MIS: ...}` as optional superset annotations.

Create this file:
~/projects/ChSepAudioQA/guidelines_for_languages/transcription_[ISO_LANG_CODE].md

After writing:
- Check the new file for linter issues.
- Check for accidental formatting artifacts.
- Check that no digit-form normalization remains in `Correct` examples.
- Summarize the main language-specific adaptations.
```
