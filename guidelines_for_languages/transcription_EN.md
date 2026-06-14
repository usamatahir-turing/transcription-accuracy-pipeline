# English Transcription Guidelines

Language: English (United States)

## Part 1 - Text normalization

### Superset principle

The transcription rules below define the **minimum required coverage**. Annotation vendors are expected to deliver transcriptions that are a **superset** of these rules — any additional detail, markup, or tagging beyond what is specified here is encouraged and acceptable, as long as it does not contradict the rules. This is not limited to the examples below; vendors may introduce any additional annotation layers that capture more information from the audio.

Examples of acceptable superset additions include (but are not limited to):

- **Pronunciation variants** for acronyms or proper nouns annotated inline:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "SQL" | SQL {PRO: S-Q-L} |
| "SQL" | SQL {PRO: Sequel} |

- **Mispronunciation tags** to flag non-standard renderings:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "The British accent sounds nicer for Vincent Van Goff" | The British accent sounds nicer for Vincent Van Gogh {MIS: Goff} |

- **Hesitation markers and fillers** beyond those listed in the canonical table (Part 2, §2 — Hesitation Markers and Vocal Fillers). Vendors may transcribe additional filler variants (e.g. `umh`, `uhm`, `awe`, etc.) as long as every variant that *is* listed in the canonical table is normalized to its canonical form. Extra variants that fall outside the table should still be transcribed faithfully rather than dropped.

- Any other annotation enrichment (e.g. emotion tags, speaker-effort markers, dialect notes, confidence flags) is welcome as long as it does not alter the base transcription text.

In short: **do not remove detail that is present in the audio**. The rules below set the floor, not the ceiling.

---

### Text Normalization Rules

Transcribe the audio. Convert all numeric, symbolic, and abbreviated tokens to their fully spoken word form using the rules below. Return transcription only.

#### 1. Broad Principles

With the exception of acronyms, initialisms, and clearly intended official spellings, everything should be written out in full spoken words. Abbreviations, symbols, shorthand, and numerals should all be expanded.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "doctor smith" | doctor smith | Dr. Smith |
| "many kilograms" | many kilograms | many kgs / many kg |
| "sunset boulevard" | sunset boulevard | Sunset Blvd. |

#### 2. English Orthography and Script

Use standard English spelling, capitalization, punctuation, and spacing:

- Write English words in the **Latin alphabet** with standard English spelling.
- Use normal capitalization for sentence starts, proper nouns, brands, acronyms, and official names.
- Use apostrophes for contractions and possessives when the spoken form requires them.
- Do not imitate predictable casual pronunciation when the intended standard word is clear.
- Preserve real dialectal vocabulary, contractions, and slang when they are the actual spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "I'm going now" | I'm going now | Im going now |
| "John's car" | John's car | Johns car |
| "new york city" | New York City | new york city |
| "I don't know" | I don't know | I dont know |
| "y'all are coming" | y'all are coming | you all are coming |

#### 3. Numbers

Spell out all digits and numeric expressions as words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "fourteen" | fourteen | 14 |
| "one thousand thirty point five" | one thousand thirty point five | 1,030.5 |
| "twenty twenty four" | twenty twenty four | 2024 |
| "nine three six dash one one" | nine three six dash one one | 936-11 |
| "nine oh two one oh" | nine oh two one oh | 90210 |

#### 4. English Number Readings and Zero Variants

English numbers may be read in several valid ways depending on context. Preserve the speaker's actual reading; do not convert one natural reading into another.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "twenty twenty four" | twenty twenty four | two thousand twenty four / 2024 |
| "two thousand twenty four" | two thousand twenty four | twenty twenty four / 2024 |
| "one oh five" | one oh five | one zero five / 105 |
| "one zero five" | one zero five | one oh five / 105 |
| "nine oh two one oh" | nine oh two one oh | nine zero two one zero / 90210 |
| "zero" | zero | oh, if the speaker said zero |

#### 5. Non-Numeral Usage

Number words should be written out as words when they are part of natural speech and not intended to communicate a specific numeric value. This includes:

- **Idiomatic or determiner-like usage**: "the only one", "two's company"
- **Proper nouns**: "One Direction", "Ocean's Eleven"
- **Stammering or false starts**: "o- o- one hundred and five" (the stammered portion stays as words, only the final intended number is spoken form)

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "you're the only one for me" | you're the only one for me | you're the only 1 for me |
| "One Direction" | One Direction | 1 Direction |
| "o- o- one hundred and five" | o- o- one hundred and five | o- o- 105 |

#### 6. Ordinals, Counters, Decades, and Age Ranges

Read ordinal suffixes, counted items, decades, era references, and age ranges as fully spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "third" | third | 3rd |
| "twenty first" | twenty first | 21st |
| "fiftieth" | fiftieth | 50th |
| "seventies" | seventies | 70s / '70s |
| "twenties" as an age range | twenties | 20s |
| "twenty twenty something" | twenty twenty something | 20 20-something |

#### 7. Dates

Read month, day, and year as fully spoken words. Drop leading zeros.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "january twenty second eighteen forty seven" | january twenty second eighteen forty seven | Jan 22, 1847 |
| "march fifth nineteen ninety" | march fifth nineteen ninety | Mar 5, 1990 |

#### 8. Time of Day

Read hours and minutes as spoken words. Omit :00 when the time is on the hour. Use "o" prefix for minutes 01-09. Write AM/PM as `AM` or `PM` (letters together, not separated).

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "three o five PM" | three o five PM | 3:05 p m / 3:05 p.m. |
| "ten AM" | ten AM | 10 a m / 10 a.m. |
| "one forty five" | one forty five | 1:45 |
| "eight to five" | eight to five | 8:00-5:00 |
| "noon" | noon | 12:00 PM |

Only include AM/PM if the speaker explicitly says it.

#### 9. Money / Currency

Read currency symbol and amount as fully spoken words, including cents if present. Drop trailing .00.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "fifty two dollars" | fifty two dollars | $52 |
| "a thousand dollars" | a thousand dollars | $1,000 |
| "two hundred forty nine dollars and ninety nine cents" | two hundred forty nine dollars and ninety nine cents | $249.99 |
| "thirty, forty dollars" | thirty, forty dollars | $30, $40 |

#### 10. Percentages

Spell out the number and the word "percent".

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "zero point five percent" | zero point five percent | 0.5% |
| "a hundred percent" | a hundred percent | 100% |
| "twenty to thirty percent" | twenty to thirty percent | 20% to 30% |

#### 11. Measures / Units

Read the number as words and expand the unit abbreviation to its full spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "five kilograms" | five kilograms | 5 kg |
| "ninety kilometers per hour" | ninety kilometers per hour | 90 km/h |
| "five foot four" | five foot four | 5'4" |
| "one hundred twenty centimeters" | one hundred twenty centimeters | 120 cm |

#### 12. Fractions, Ratios, and Scores

Spell out fractions, ratios, and scores as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "one and three quarters" | one and three quarters | 1 3/4 |
| "three quarters" | three quarters | 3/4 |
| "one half" | one half | 1/2 |
| "fifty fifty" | fifty fifty | 50:50 |
| "two to one" as a score | two to one | 2-1 / 2:1 |

#### 13. Negative Numbers

Spell out negative numbers as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "negative twelve" | negative twelve | -12 |
| "eighteen below" | eighteen below | -18 |
| "minus five degrees" | minus five degrees | -5 degrees |

#### 14. Phone Numbers, Postal Codes, IDs, and Codes

Read each digit group individually as spoken. Special codes like eight hundred numbers can be read as "eight hundred" when that is what the speaker says. Do not write formatted phone numbers, postal codes, IDs, or codes with digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "one eight hundred five five five zero one nine nine" | one eight hundred five five five zero one nine nine | 1-800-555-0199 |
| "five five five eight six seven five three zero nine" | five five five eight six seven five three zero nine | 555-867-5309 |
| "zip code six two seven zero four" | zip code six two seven zero four | zip code 62704 |
| "A B one two three" | A B one two three | AB123 |

#### 15. Electronic Text (URLs, Emails, IPs)

Read all symbols aloud. Do not write URLs, email addresses, IP addresses, usernames, or file paths in compact written form.

| Symbol | Spoken As |
|--------|-----------|
| @ | at |
| . | dot |
| / | slash |
| : | colon |
| - | dash |

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "example dot com slash pricing" | example dot com slash pricing | example.com/pricing |
| "john at gmail dot com" | john at gmail dot com | john@gmail.com |
| "one nine two dot one six eight dot zero dot one" | one nine two dot one six eight dot zero dot one | 192.168.0.1 |

#### 16. Roman Numerals

Use cardinal form after chapter/title keywords. Use ordinal form after a person's name.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "chapter four" | chapter four | Chapter IV |
| "king henry the eighth" | king henry the eighth | King Henry VIII |
| "elizabeth the second" | elizabeth the second | Elizabeth II |

#### 17. Abbreviations and Initialisms

Expand titles, degrees, and common abbreviations to their full spoken form. Keep spoken acronyms and initialisms in their canonical form when the speaker is saying them as such.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "doctor" | doctor | Dr. |
| "professor" | professor | Prof. |
| "versus" | versus | vs. |
| "department" | department | dept. |
| "without" | without | w/o |
| "phd" | phd | Ph.D. |
| "saint" or "street" (by context) | saint / street | St. |
| "four fifty north main street" | four fifty north main street | 450 N. Main St. |
| "NASA" | NASA | National Aeronautics and Space Administration |
| "FBI" | FBI | Federal Bureau of Investigation |
| "SQL" | SQL | Structured Query Language |
| "Central Intelligence Agency" | Central Intelligence Agency | CIA |

If the speaker says the full expanded form, transcribe the full form, not the acronym.

#### 18. Foreign Words and Loanwords

Loanwords and foreign words do not have a strict boundary, and some cases are gray areas. As a general rule, if a word is commonly used in everyday English, treat it as an English word or borrowed everyday word, not as a foreign-language span.

Do not mark established English loanwords or borrowed everyday words as foreign words. Use the standard English spelling unless the speaker is clearly giving an official foreign spelling, URL, username, code, or other written form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "café" | café | <foreign> café </foreign> |
| "kindergarten" | kindergarten | <foreign> kindergarten </foreign> |
| "karaoke" | karaoke | <foreign> karaoke </foreign> |
| "sushi" | sushi | <foreign> sushi </foreign> |
| "fiancé" | fiancé | <foreign> fiancé </foreign> |

Use the actual foreign spelling only when the speaker is clearly saying a foreign-language word or phrase as foreign speech, rather than using an English loanword. If your pipeline supports foreign-language tags, they may be added as a superset annotation.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "gracias" clearly in Spanish | gracias | <foreign lang="ES"> gracias </foreign> |
| "merci" clearly in French | merci | <foreign lang="FR"> merci </foreign> |
| "Guten Morgen" clearly in German | Guten Morgen | <foreign lang="DE"> Guten Morgen </foreign> |
| "buongiorno" clearly in Italian | buongiorno | <foreign lang="IT"> buongiorno </foreign> |

If a word could be either an English loanword or foreign speech, choose based on how it is used and pronounced in context.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| English loanword pronunciation | we ordered sushi | we ordered <foreign> sushi </foreign> |
| Spanish phrase pronunciation | gracias, amigo | grass yes, amigo |
| Official product or brand spelling is intended | I bought an iPhone | I bought an eye phone, if `iPhone` is clearly intended |
| Ordinary Englishized product reference | I bought an iPhone | I bought a phone, if `iPhone` was spoken |

Proper nouns are not foreign-language spans just because they come from another language.

#### 19. Ambiguity

Rely on audio context to resolve ambiguous tokens.

| Context | Audio | Correct |
|---------|-------|---------|
| Talking about a date | "one four" | one four |
| Talking about a fraction | "one quarter" | one quarter |
| Talking about a year | "twenty twenty" | twenty twenty |

English has homophones where the same pronunciation maps to different spellings and meanings. When pronunciation alone is ambiguous, use the surrounding meaning and context to choose the standard written form.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Direction or destination | "go to the store" | go to the store | go too the store / go two the store |
| Excess or also | "too much" | too much | to much / two much |
| Number word | "two people" | two people | to people / too people |
| Possessive | "their house" | their house | there house / they're house |
| Location | "over there" | over there | over their / over they're |
| Contraction | "they're coming" | they're coming | their coming / there coming |
| Existence | "there is a problem" | there is a problem | their is a problem |
| Possessive | "your name" | your name | you're name |
| Contraction | "you're right" | you're right | your right |
| Time | "it's late" | it's late | its late |
| Possessive | "its color" | its color | it's color |

If multiple written forms are acceptable after context is considered, choose the form that best preserves the speaker's intended meaning and is most natural in English.

#### 20. Guidelines for Language-specific Issues

The following English-specific issues should follow the same principles above: preserve what was spoken, use standard English spelling when the intended word is clear, and do not invent unsupported written forms.

**Homophones and contractions:** Use context to choose the correct spelling for same-sounding words and contractions.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Contraction | "you're right" | you're right | your right |
| Possessive | "your name" | your name | you're name |
| Contraction | "they're here" | they're here | their here / there here |
| Location | "over there" | over there | over their |
| Possessive | "its color" | its color | it's color |

**Proper names and spelling variants:** English names can have multiple valid spellings. If the official spelling is not known from context, do not guess a special spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Katherine" with unknown spelling | Katherine / Catherine, only if known | Guessing one spelling without evidence |
| "Steven" with unknown spelling | Steven / Stephen, only if known | Guessing one spelling without evidence |
| "Sara" with unknown spelling | Sara / Sarah, only if known | Guessing one spelling without evidence |

**Apostrophes and possessives:** Use standard apostrophes for contractions and possessives. Do not add apostrophes to ordinary plurals.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "John's car" | John's car | Johns car |
| "the dogs are outside" | the dogs are outside | the dog's are outside |
| "the dog's collar" | the dog's collar | the dogs collar |
| "I can't go" | I can't go | I cant go |

**Hyphenated compounds:** Use standard spelling for common compounds and prefixes. Do not split or hyphenate inconsistently.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "email address" | email address | e mail address |
| "twenty first century" | twenty first century | 21st century |
| "part time job" | part time job | part-time job, unless the project requires dictionary hyphenation |

**Dialect and regional vocabulary:** Preserve real dialect or regional vocabulary when spoken. Do not rewrite it into another variety of English.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "y'all are coming" | y'all are coming | you all are coming |
| "I reckon so" | I reckon so | I think so |
| "the lift is broken" | the lift is broken | the elevator is broken |

**Letter-number patterns:** When a letter is followed by a number, preserve the letter and spell the number. Spell out years that follow.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "q two" | q two | Q2 |
| "b twelve" | b twelve | B12 |
| "q two nineteen sixty five" | q two nineteen sixty five | Q2 1965 |

**Spoken sound words:** English sound-symbolic words are lexical words when spoken. Transcribe them as words, not as non-speech tags.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "it went boom" | it went boom | it went [other-noise] |
| "the bell went ding dong" | the bell went ding dong | the bell went [other-noise] |
| "she said shh" | she said shh | she said [shush] |

---

## Part 2 - Disfluency

### Disfluency Rules

You are given an audio clip and its existing transcription. Your task is to output the transcription as provided, adding all speech disfluencies that you hear based on the rules below. Return only the transcription text.

#### 1. Filler Words

Words like "yeah", "yes", "like", "you know" should always be added to the transcription. Keep them exactly as spoken.

| Audio | Correct |
|-------|---------|
| "and yeah we moved on" | and yeah we moved on |
| "it was like really good" | it was like really good |
| "you know what I mean" | you know what I mean |

#### 2. Hesitation Markers and Vocal Fillers

Listen for **non-lexical vocalizations** during pauses, planning, and reactive listening. Standardize spellings to the **canonical form** for each group. Use **sentence-initial capitalization** (`Hm`, `Um`, …) where your style guide requires it for sentence starts.

**Filled pauses / hesitation** (speaker holds the floor, searching for words):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|------------------------------|
| **hm** | `hm` | `mm`, `hmm`, `mmm`, `mmh`, `hmmm`, long nasal hums like `hmhmm` / `hmmhmm` (thinking / mulling, not backchannel assent) |
| **um** | `um` | `umm`, `uhm`, `umh`, `ummh` |
| **uh** | `uh` | bare prolongations `uhh`, `uuh`; do **not** fold **uh-huh**, **uh-uh**, or **uh-oh** into plain `uh` |
| **ah** | `ah` | `ahh`, `aah`, `ahhh` |
| **er** | `er` | `err`, `erm` |
| **oh** | `oh` | `ohh` (mild surprise / filler; distinct from drawn-out **ooh**) |
| **eh** | `eh` | `ehh` |
| **ooh** | `ooh` | `oooh`, `aw`, `awe` when spoken as an exclamation (not the word *awe* in context) |
| **mn** | `mn` | `mmn`, `mnn`, closed-mouth nasal; if your pipeline marks mouth noise, `([mn])`-style tags align with this bucket |

**Backchannel / response** (listener signals agreement, negation, or doubt — reactive, not turn-taking):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|------------------------------|
| **mm-hmm** | `mm-hmm` | `mhm`, `m-hm`, `mmhm`, `mhmm`, `mm-hm`, hyphen/space variants; **affirmative** acknowledgment |
| **uh-huh** | `uh-huh` | `uhhuh`, `uh-hum`, `uhhum`, `unh-hun`; **affirmative** |
| **uh-uh** | `uh-uh` | `uhuh` when meaning **no**; `unh-uh` |
| **nuh-uh** | `nuh-uh` | `nuhuh`, `nuh uh`; **emphatic negative** |
| **mm-mm** | `mm-mm` | `mm mm`, `mhm-mm`, **negative** / head-shake sense (not prolonged `mmmm` nasal hum → use **hm**) |
| **hm-mm** | `hm-mm` | `hmm-mm`, **doubtful** or negative |

When the same phones could be **hesitation** vs **backchannel**, use **audio and dialogue role**: mid-utterance planning → **hm** / **uh** / **um**; short reactive assent while the other speaker talks → **mm-hmm** / **uh-huh**.

| Situation | Correct (canonical) | Incorrect (raw / inconsistent) |
|-----------|---------------------|----------------------------------|
| Filled pause before content | `um I think so` | `uhm I think so`, `umm I think so` |
| Thinking / nasal mulling (not assent) | `hm that's interesting` | `hmmm that's interesting`, `mmhm` used as plain hesitation here |
| Listener **yes** (backchannel) | `mm-hmm` | `mhm`, `hmm` as assent |
| Listener **yes** (backchannel) | `uh-huh` | `uh huh`, `uhhuh`, `uh-hum` |
| Listener **no** | `uh-uh` or `nuh-uh` | `uh uh`, `nuhuh` (unless you intentionally keep two-word form) |
| Negative / doubtful nasal | `mm-mm` or `hm-mm` | ad hoc spellings for the head-shake contour |
| Sentence-initial exclamation filler | `Ah okay` | `Ahhh okay` |
| Surprise / alarm filler | `uh-oh` | `uhoh` split across rules inconsistently |

#### 3. Repetitions

Consecutive instances of the same word or short phrase spoken unintentionally. Keep all repetitions as-is with no added punctuation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "I I think" | I I think | I- I think |
| "the the problem" | the the problem | the- the problem |
| "we we we need to go" | we we we need to go | we- we- we need to go |

#### 4. False Starts / Cut-Off Words

Incomplete words or phrases that the speaker abandons. Mark with a single dash followed by a space.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "I was go- going to the store" | I was go- going to the store | I was go-- going / I was going |
| "the ice cre- froyo" | the ice cre- froyo | the ice cream froyo |
| "I thi- I think so" | I thi- I think so | I think so |

If the speaker cuts off and stops entirely, still use a single dash:

| Audio | Correct |
|-------|---------|
| "I was getting the ice cre-" | I was getting the ice cre- |

#### 5. Casual Forms, Slang, and Dialect

Use contractions if that's how it was spoken and the contraction is clearly audible. If unsure, default to the formal full spelling. Do not adjust for dropped-G pronunciations.

##### Approved contractions list:

| Spoken | Transcribe As |
|--------|--------------|
| "'cause" | 'cause |
| "wanna" | wanna |
| "gonna" | gonna |
| "kinda" | kinda |
| "lemme" | lemme |
| "lotta" | lotta |
| "outta" | outta |
| "Imma" (contraction of "I'm gonna") | Imma |
| "sorta" | sorta |
| "ya" | ya |
| "m'kay" | m'kay |
| "finna" | finna |
| "tryna" | tryna |
| "ole" | ole |

##### Dropped-G rule:

Always write the full word form. Do not transcribe the dropped-G pronunciation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "somethin" | something | somethin |
| "nuthin" | nothing | nuthin |
| "runnin" | running | runnin |

Preserve real slang, colloquial forms, and dialectal vocabulary when they are spoken. Do not rewrite them into another variety of English.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "y'all are coming" | y'all are coming | you all are coming |
| "I'm finna leave" | I'm finna leave | I'm going to leave |
| "I reckon so" | I reckon so | I think so |
| "the lift is broken" | the lift is broken | the elevator is broken |

#### 6. Spelled-Out Words

If a speaker spells out a word one letter at a time that is not an acronym or initialism, use capital letters separated with dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "My name is Masego, M A S E G O" | My name is Masego, M-A-S-E-G-O | My name is Masego, M A S E G O |

#### 7. Mispronunciations

Transcribe intelligible substitutions as spoken. Do not correct mispronunciations in the base transcript and do not add a tag unless your project uses superset `{MIS: ...}` annotations.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "I went to the peach to swim" | I went to the peach to swim | I went to the beach to swim |
| "shashimi" | shashimi | sashimi |
| "dorpclosh" (unintelligible) | dorpclosh | (omitted) |

#### 8. Wrong Grammar

Grammatical errors should be faithfully captured in the transcript. Do NOT correct them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "he don't know nothing" | he don't know nothing | he doesn't know anything |
| "me and him went there" | me and him went there | he and I went there |


## Part 3 - Rich Transcription: Paralinguistic Tokens

### Non-Speech Sound Tokens

Bracket tokens mark **audible non-lexical or non-linguistic events** that are **not** regular words. Write each tag **exactly** as listed (square brackets included). Prefer **one tag per distinct event**; if several happen in sequence, repeat tags in **time order**, separated by spaces.

Use the NeMo canonical English tag names below, even in English transcripts.

#### Rules for this section

1. **Tag vs words** — If the speaker says a word (e.g. *sigh*, *laugh*, *cough*) as intentional speech, transcribe the **word**. Use a **bracket tag** only for the **sound event** itself (audible exhalation, laugh sound, cough sound) when it is **not** delivered as normal lexical speech.
2. **No invented words** — Do not replace a tag with a phonetic guess (e.g. “ahhh”) unless your style guide treats that as a **filled pause** elsewhere; for isolated events, use the tag.
3. **Placement** — Put the tag **where the sound occurs** in the word stream, usually as its own token between words (same rules as punctuation spacing for your pipeline).
4. **Overlap** — If a sound overlaps speech, place the tag at the **start** of the overlap window unless your time-aligned format specifies otherwise; do not merge unrelated words into the tag.
5. **Sequences** — Use `[laugh] [laugh]` for two separate laugh bursts, not a single stretched token unless your schema forbids repetition.
6. **Unknown / generic background** — Use `[other-noise]` for audible non-speech you cannot classify; use `[unintelligible]` only when **linguistic content** was likely present but cannot be recovered (see below).
7. **Minor mouth sounds** — Do not tag faint natural mouth clicks, lip noise, or routine breathing unless they are prominent or communicative.

#### Token list and descriptions

Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into English or replace them with local-language labels.

| Token | Description |
|-------|-------------|
| `[breath]` | Audible breath sound without a clear inhale vs exhale distinction (light breathing picked up by the mic). |
| `[inhale]` | Clear **inward** breath before or between phrases (audible intake). |
| `[exhale]` | Clear **outward** breath, often after a phrase or under stress (not a full sigh). |
| `[sigh]` | Prolonged or marked **sigh** (typically falling pitch, expressive release). |
| `[sniff]` | Nasal **sniff** (inhale through the nose), including wet or dry sniffles. |
| `[gasp]` | Sharp **gasp** or sudden air intake (surprise, shock, pain). |
| `[blow]` | Audible **blow** through the mouth (e.g. cooling, blowing dust), not speech. |
| `[laugh]` | **Laughter** vocalization (any voiced laugh). Use finer tags below if clearly one type. |
| `[chuckle]` | **Chuckle**: softer, shorter, suppressed laugh. |
| `[giggle]` | **Giggle**: higher-pitched or repeated light laugh. |
| `[snort]` | **Snort** through nose or mouth while laughing or reacting. |
| `[scoff]` | **Scoff** / dismissive exhalation or laugh-like puff (attitude, not a word). |
| `[grunt]` | Short **grunt** or effort vocalization (lifting, strain, annoyance). |
| `[groan]` | Longer **groan** or moan (pain, complaint, theater). |
| `[cry]` | **Crying** sounds (sobbing, wailing) without relying on orthographic “whining” words. |
| `[hum-tune]` | **Humming** a melody or tune (closed-mouth or mm-based), not lexical humming words. |
| `[whoop]` | **Whoop** or cheer-like shout (excitement), not normal spoken “whoop.” |
| `[whistle]` | **Whistling** (lips or hands), not the word *whistle* spoken. |
| `[tongue-click]` | **Tongue click** / alveolar click (tsk-like but discrete click). |
| `[tsk]` | **Tsk-tsk** / reproach click or similar dental/alveolar scrape (often written *tsk*). |
| `[lip-smack]` | **Lip smack** (parting lips with audible smack), including moist smacks before speech. |
| `[teeth-suck]` | **Suck** through teeth or sharp dental inhale (distaste, thinking). |
| `[lip-trill]` | **Bilabial trill** / lip buzz (not rolled R in speech). |
| `[shush]` | **Shushing** sound ([ʃ]) used to quiet someone, not the word *shush* as dialogue. |
| `[swallow]` | Audible **swallow** (gulp) of saliva. |
| `[clear-throat]` | **Throat clear** / hack / harrumph to clear cords. |
| `[cough]` | **Cough** sound (any cough). |
| `[sneeze]` | **Sneeze** sound. |
| `[yawn]` | **Yawn** sound (open-mouth yawn vocalization). |
| `[hiccup]` | **Hiccup** sound. |
| `[unintelligible]` | A stretch where **speech was likely** but words cannot be resolved (masking, overlap, clip); use sparingly and **not** for pure noise. |
| `[other-noise]` | Any **non-speech** sound that does not fit a label above (handling object, bump, generic background burst). Prefer a specific tag when clearly identifiable. |

#### Examples

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| Speaker laughs before speaking | [laugh] that was funny. | [laughter] that was funny. |
| Speaker coughs mid-sentence | that is [cough] not a problem. | that is cough not a problem. |
| Speech is masked and unrecoverable | I think [unintelligible] tomorrow. | I think tomorrow. |
| Background object noise | [other-noise] can you repeat that? | [noise] can you repeat that? |

#### Quick reference (canonical spellings)

- `[breath]` · `[inhale]` · `[exhale]` · `[sigh]` · `[sniff]` · `[gasp]` · `[blow]`
- `[laugh]` · `[chuckle]` · `[giggle]` · `[snort]` · `[scoff]` · `[grunt]` · `[groan]` · `[cry]`
- `[hum-tune]` · `[whoop]` · `[whistle]` · `[tongue-click]` · `[tsk]` · `[lip-smack]` · `[teeth-suck]` · `[lip-trill]` · `[shush]` · `[swallow]` · `[clear-throat]`
- `[cough]` · `[sneeze]` · `[yawn]` · `[hiccup]` · `[unintelligible]` · `[other-noise]`
