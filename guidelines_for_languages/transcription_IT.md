# Italian Transcription Guidelines

Language: Italian (Italy)

## Part 1 - Text normalization

### Superset principle

The transcription rules below define the **minimum required coverage**. Annotation vendors are expected to deliver transcriptions that are a **superset** of these rules - any additional detail, markup, or tagging beyond what is specified here is encouraged and acceptable, as long as it does not contradict the rules.

Examples of acceptable superset additions include (but are not limited to):

- **Pronunciation variants** for acronyms or proper nouns annotated inline:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "UEFA" said as "wefa" | UEFA {PRO: wefa} |
| "UEFA" said as "u-e-fa" | UEFA {PRO: u-e-fa} |

- **Mispronunciation tags** to flag non-standard renderings:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "caffè" intended but pronounced "cafè" | caffè {MIS: cafè} |

- **Additional hesitation markers, dialect notes, confidence flags, or emotion tags** are acceptable as long as they do not alter the base transcription text.

In short: **do not remove detail that is present in the audio**. The rules below set the floor, not the ceiling.

---

### Text Normalization Rules

Transcribe the audio in standard Italian orthography. Convert numeric, symbolic, and abbreviated tokens to their fully spoken Italian form using the rules below. Return transcription only.

#### 1. Broad Principles

With the exception of acronyms and established proper-name spellings, everything should be written out in full spoken words. Abbreviations, symbols, shorthand, and numerals should all be expanded.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "professor Rossi" | professor Rossi | prof. Rossi, unless that is what was spoken |
| "chilogrammo" | chilogrammo | kg |
| "e" (and) | e | & |
| "iPhone quattordici" | iPhone quattordici | iPhone 14 |
| "Roma capitale" | Roma capitale | Roma cap., unless that is what was spoken |

Use standard spelling and spacing. Do not over-normalize into a form that changes spoken content.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ho mangiato la pasta" | ho mangiato la pasta | homangiato la pasta |
| "non lo so" | non lo so | nonloSo |
| "l'amico mio" | l'amico mio | l' amico mio |
| "è andata bene" | è andata bene | e andata bene |

#### 2. Italian Orthography and Script

Use standard Italian spelling and orthography:

- Write Italian words in the **Latin alphabet** with required diacritical marks. Never substitute accented characters with unaccented equivalents.
- **Grave accent** (`à`, `è`, `ì`, `ò`, `ù`) and **acute accent** (`é`) are mandatory where standard Italian orthography requires them. Missing an accent that changes meaning is an error.
- **Accented monosyllables that form minimal pairs** must carry their accent mark:

| Form | Meaning | Form | Meaning |
|------|---------|------|---------|
| `è` | is (verb) | `e` | and (conjunction) |
| `sì` | yes | `si` | reflexive pronoun |
| `là` / `lì` | there | `la` / `li` | article / pronoun |
| `né` | nor | `ne` | partitive pronoun |
| `dà` | gives | `da` | from / since |

- **Elision and apostrophe:** Contracted articles and prepositions before vowels are standard Italian orthography and must be written with an apostrophe. Do not add a space between the apostrophe and the following word.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "l'amico" | l'amico | l' amico / lamico |
| "dell'acqua" | dell'acqua | dell' acqua |
| "un'amica" | un'amica | un amica / un' amica |
| "all'università" | all'università | all' università |

- **Double consonants (geminate consonants)** are phonemically contrastive in Italian and must be written accurately. Do not single-write a double consonant or double-write a single one.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "palla" | palla | pala |
| "notte" | notte | note |
| "anno" | anno | ano |
| "cassa" | cassa | casa |

- Use the conventional capitalization for proper nouns, titles, and brand names.
- Use standard Italian punctuation where it helps reflect the sentence structure; do not use punctuation to add words, pauses, or emphasis that are not supported by the audio.

#### 3. Numbers

Spell out all digits and numeric expressions as spoken Italian words. Preserve the speaker's actual reading.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "quattordici" | quattordici | 14 |
| "zero virgola zero cinque" | zero virgola zero cinque | 0,05 |
| "mille e trenta virgola cinque" | mille e trenta virgola cinque | 1.030,5 |
| "duemilaventiquattro" | duemilaventiquattro | 2024 |
| "due zero due quattro" | due zero due quattro | 2024 |
| "meno dodici" | meno dodici | -12 |

In Italian, the decimal separator is the comma (*virgola*) and the thousands separator is the period. Always transcribe the spoken word (`virgola`) rather than its symbol.

#### 4. Italian Number Forms

Italian has compound number forms that involve vowel elision and accent:

- Decades ending in a vowel drop that vowel before `uno` (one) and `otto` (eight):

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ventuno" | ventuno | ventiuno |
| "ventotto" | ventotto | ventiotto |
| "trentuno" | trentuno | trentauno |
| "trentotto" | trentotto | trentaotto |

- Numbers ending in `tre` above twenty carry a written accent (*é*):

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ventitré" | ventitré | ventitre |
| "trentatré" | trentatré | trentatre |
| "quarantatré" | quarantatré | quarantatre |

- Transcribe the form actually spoken; do not convert one valid spoken form into another:

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "due zero zero zero" | due zero zero zero | duemila |
| "duemila" | duemila | due zero zero zero |
| "milleottocento" | milleottocento | mille ottocento |

#### 5. Non-Numeral Usage

Do not convert number words to Arabic numerals when they are part of natural language, idioms, proper nouns, or conventional expressions.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "uno contro uno" | uno contro uno | 1 contro 1 |
| "fare due chiacchiere" | fare due chiacchiere | fare 2 chiacchiere |
| "terzo mondo" | terzo mondo | 3° mondo |
| "Ferrari Cinquecento" as a vehicle name | Ferrari Cinquecento | Ferrari 500 |
| "Trieste" as a city name | Trieste | Tri-este |
| "Tre Cime di Lavaredo" | Tre Cime di Lavaredo | 3 Cime di Lavaredo |

When a disfluency occurs before a non-numeral expression, keep the disfluent portion as spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "u-, uno contro uno" | u- uno contro uno | u- 1 contro 1 |

#### 6. Ordinals, Counters, Decades, and Age Ranges

Spell out ordinal expressions and age/decade ranges as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "primo" | primo | 1° / 1º |
| "secondo" | secondo | 2° |
| "terzo capitolo" | terzo capitolo | 3° capitolo |
| "gli anni settanta" | gli anni settanta | gli anni '70 |
| "sulla trentina" (around thirty) | sulla trentina | sulla 30ina |
| "sulla quarantina" | sulla quarantina | sulla 40ina |

Use the official spoken form for titles, laws, chapters, and product names.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "la seconda guerra mondiale" | la seconda guerra mondiale | la 2ª guerra mondiale |
| "Windows undici" | Windows undici | Windows 11 |
| "iPhone quattordici" | iPhone quattordici | iPhone 14 |

#### 7. Dates

Write dates as spoken Italian words. Do not convert month, day, or year into digits. In Italian, only the first day of the month uses an ordinal (*il primo*); all others use cardinals.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "il ventinove aprile duemilaventiquattro" | il ventinove aprile duemilaventiquattro | 29/04/2024 |
| "il primo gennaio" | il primo gennaio | il 1 gennaio / l'1 gennaio |
| "il due febbraio" | il due febbraio | il 2 febbraio |
| "il dodici dicembre millenovecentonovantasette" | il dodici dicembre millenovecentonovantasette | 12/12/1997 |
| "l'undici settembre" as spoken | l'undici settembre | l'11/9 / l'11 settembre |

If the speaker reads a date digit by digit, preserve that digit-by-digit spoken form.

#### 8. Time of Day

Write clock times as spoken Italian words. Include `di mattina`, `di pomeriggio`, `di sera`, `di notte` only if spoken. Use `mezzogiorno` and `mezzanotte` when spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "le due e trenta di pomeriggio" | le due e trenta di pomeriggio | 2:30 PM |
| "le due e trenta" | le due e trenta | 2:30 |
| "l'una e quarantacinque" | l'una e quarantacinque | 1:45 |
| "le quattordici e trenta" | le quattordici e trenta | 14:30 |
| "mezzogiorno" | mezzogiorno | 12:00 |
| "mezzanotte" | mezzanotte | 0:00 / 24:00 |
| "dalle otto alle cinque" | dalle otto alle cinque | dalle 8 alle 5 |
| "le due e trenta" while reading "2:30" | le due e trenta | 2:30 |
| "le zero e quindici" | le zero e quindici | 0:15 |

#### 9. Money / Currency

Spell out money and currency amounts as spoken Italian words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cinquantadue euro" | cinquantadue euro | 52€ / 52 euro |
| "mille euro" | mille euro | 1.000€ / 1000 euro |
| "due dollari e cinquanta centesimi" | due dollari e cinquanta centesimi | $2,50 |
| "trenta, quaranta euro" | trenta, quaranta euro | 30, 40 euro |
| "dai trenta ai quaranta euro" | dai trenta ai quaranta euro | 30-40 euro |

Do not normalize informal or approximate money expressions.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "due soldi" (idiomatic) | due soldi | due euro |
| "non ho una lira" | non ho una lira | non ho un euro |

#### 10. Percentages

Spell out the number and the word `percento`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "zero virgola cinque percento" | zero virgola cinque percento | 0,5% |
| "cento percento" | cento percento | 100% |
| "dal venti al trenta percento" | dal venti al trenta percento | dal 20% al 30% |

#### 11. Measures / Units

Read the number as words and expand the unit abbreviation to its full spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cinque chilogrammi" | cinque chilogrammi | 5 kg / 5kg |
| "novanta chilometri all'ora" | novanta chilometri all'ora | 90 km/h |
| "un metro e settanta centimetri" | un metro e settanta centimetri | 1 m 70 cm / 1,70 m |
| "otto bit" | otto bit | 8 bit |
| "quattro K" | quattro K | 4K |
| "cento watt" | cento watt | 100 W |

#### 12. Fractions, Ratios, and Scores

Spell out fractions, ratios, and scores as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "tre quarti" | tre quarti | 3/4 |
| "uno e tre quarti" | uno e tre quarti | 1 3/4 |
| "la metà" | la metà | 1/2 |
| "un mezzo" | un mezzo | 1/2 |
| "mezzo" | mezzo | 1/2 |
| "cinquanta a cinquanta" | cinquanta a cinquanta | 50:50 |
| "due a uno" as a score | due a uno | 2:1 / 2-1 |

#### 13. Negative Numbers

Spell out negative numbers as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "meno dodici" | meno dodici | -12 |
| "meno diciotto gradi" | meno diciotto gradi | -18° / -18 gradi |
| "sotto zero cinque gradi" | sotto zero cinque gradi | -5° gradi |

Use `meno` when the speaker says `meno`. Use `sotto zero` when the speaker says `sotto zero`.

#### 14. Phone Numbers, Postal Codes, IDs, and Codes

Read each digit group individually as spoken. Do not write formatted phone numbers, postal codes, or IDs with digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "tre tre tre uno due tre quattro cinque sei sette" | tre tre tre uno due tre quattro cinque sei sette | 333-1234567 |
| "zero due uno due tre quattro cinque sei sette otto" | zero due uno due tre quattro cinque sei sette otto | 02-12345678 |
| "codice postale zero uno due tre quattro" | codice postale zero uno due tre quattro | CAP 01234 |
| "a bi uno due tre" | a bi uno due tre | AB123 |

#### 15. Electronic Text (URLs, Emails, IPs)

Read all symbols aloud. Do not write URLs, email addresses, IP addresses, usernames, or file paths in their compact written form.

| Symbol | Spoken As |
|--------|-----------|
| @ | chiocciola / at, as spoken |
| . | punto |
| / | slash / barra, as spoken |
| : | due punti |
| - | trattino / lineetta, as spoken |
| _ | underscore / trattino basso, as spoken |

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "example punto com slash pricing" | example punto com slash pricing | example.com/pricing |
| "google punto it" | google punto it | google.it |
| "mario chiocciola gmail punto com" | mario chiocciola gmail punto com | mario@gmail.com |
| "uno nove due punto uno sei otto punto zero punto uno" | uno nove due punto uno sei otto punto zero punto uno | 192.168.0.1 |

#### 16. Roman Numerals

Use the spoken cardinal, ordinal, or regnal form. Do not convert to Roman numeral notation in `Correct`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Star Wars episodio quattro" | Star Wars episodio quattro | Star Wars Episode IV |
| "GTA cinque" | GTA cinque | GTA V |
| "Carlo quinto" | Carlo quinto | Carlo V |
| "il ventesimo secolo" | il ventesimo secolo | il XX secolo |
| "Enrico ottavo" | Enrico ottavo | Enrico VIII |

#### 17. Abbreviations and Initialisms

Keep spoken acronyms and initialisms in their canonical form. Do not expand them unless the speaker says the expanded form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "rai" as RAI | RAI | Radiotelevisione Italiana |
| "o-en-u" | ONU | Organizzazione delle Nazioni Unite |
| "nato" as NATO | NATO | Organizzazione del Trattato del Nord Atlantico |
| "i-va" | IVA | Imposta sul Valore Aggiunto |
| "imposta sul valore aggiunto" | imposta sul valore aggiunto | IVA |
| "pi-i-elle" | PIL | Prodotto Interno Lordo |

When pronunciation is ambiguous or important, `{PRO: ...}` is an acceptable superset annotation.

#### 18. Foreign Words and Loanwords

Established Italian loanwords that are listed in standard Italian dictionaries or are in common everyday use should be written as Italian words in the Latin alphabet, not tagged as foreign speech.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "computer" | computer | <foreign> computer </foreign> |
| "internet" | internet | <foreign> internet </foreign> |
| "weekend" | weekend | <foreign> weekend </foreign> |
| "ok" / "okay" | ok / okay | <foreign> okay </foreign> |
| "sport" | sport | <foreign> sport </foreign> |
| "film" | film | <foreign> film </foreign> |
| "caffè" | caffè | <foreign> café </foreign> |
| "manager" | manager | <foreign> manager </foreign> |

Use the actual foreign spelling only when the speaker is clearly producing a foreign-language phrase as foreign speech.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "thank you" clearly in English | thank you | <foreign lang="EN"> thank you </foreign> |
| "merci" clearly in French | merci | <foreign lang="FR"> merci </foreign> |
| "gracias" clearly in Spanish | gracias | <foreign lang="ES"> gracias </foreign> |
| "danke" clearly in German | danke | <foreign lang="DE"> danke </foreign> |

If a word could be either an Italian loanword or foreign speech, choose based on how it is pronounced and used in context.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Italian loanword pronunciation | fare il jogging | fare il <foreign> jogging </foreign> |
| English phrase pronounced in English | let's go, please | andiamo, per favore |
| Official brand or product spelling intended | ho comprato un iPhone | ho comprato un aifon |
| Ordinary Italian reference to product | comprato un iPhone | comprato un aifon |

Proper nouns are not foreign-language spans just because they come from another language.

#### 19. Ambiguity

Rely on audio context to resolve ambiguous tokens.

| Context | Audio | Correct |
|---------|-------|---------|
| Time | "le due" | le due |
| Quantity | "due libri" | due libri |
| Natural expression | "fare due chiacchiere" | fare due chiacchiere |
| Proper noun | "Cinquecento" as vehicle model | Cinquecento |
| Acronym | "rai" | RAI |

Italian has homophones where the same pronunciation maps to different spellings depending on meaning. Use surrounding context to choose the correct orthographic form.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Affirmative | "sì, certo" | sì, certo | si, certo |
| Reflexive | "si alza" | si alza | sì alza |
| There (place) | "è là" | è là | è la |
| Direct object | "la vedo" | la vedo | là vedo |
| Verb "give" | "mi dà fastidio" | mi dà fastidio | mi da fastidio |
| Preposition | "vengo da Roma" | vengo da Roma | vengo dà Roma |
| Conjunction "nor" | "né lui né lei" | né lui né lei | ne lui ne lei |
| Partitive pronoun | "ne voglio ancora" | ne voglio ancora | né voglio ancora |
| Face | "ha un bel viso" | ha un bel viso | a un bel viso |
| Verb "have" | "a me piace" | a me piace | ha me piace |

**H-initial forms:** Italian words beginning with *h* are grammatically distinct from visually similar words without *h*. Confusing these is a common ASR error.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Verb "have" (1st sg.) | "ho freddo" | ho freddo | o freddo |
| Conjunction "or" | "o questo o quello" | o questo o quello | ho questo ho quello |
| Verb "have" (2nd sg.) | "hai capito" | hai capito | ai capito |
| Preposition | "vai ai mercati" | vai ai mercati | vai hai mercati |
| Year | "l'anno scorso" | l'anno scorso | l'hanno scorso |
| Verb "have" (3rd pl.) | "lo hanno detto" | lo hanno detto | lo anno detto |

#### 20. Guidelines for Language-specific Issues

The following Italian-specific issues should follow the same principles above: preserve what was spoken, use standard Italian spelling when the intended word is clear, and do not invent unsupported written forms.

**Mandatory accent marks:** Standard Italian orthography requires accent marks on certain words. Missing or misplacing an accent that changes meaning is an error. The most critical distinctions are covered in section 19 above.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "la città" | la città | la citta |
| "il caffè" | il caffè | il caffe |
| "l'università" | l'università | l'universita |
| "perché" | perché | perche |
| "venerdì" | venerdì | venerdi |

**Compound number elision:** The vowel drop in compound numbers (section 4) is part of standard Italian orthography, not a casual reduction.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ventuno anni" | ventuno anni | ventiuno anni |
| "ventotto persone" | ventotto persone | ventiotto persone |

**Double consonants:** Geminate consonants in Italian are phonemically meaningful. Transcribe them accurately based on the intended word.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "la palla" | la palla | la pala |
| "la notte" | la notte | la note |
| "sono nonno" | sono nonno | sono nono |

**Regional phonetic reductions vs standard spelling:** Speakers in different regions may reduce certain sounds. Write the standard spelling when the intended word is clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cosa" pronounced as "csa" (rapid Northern speech) | cosa | csa |
| "adesso" said as "adè" (Southern reduction) | adesso | adè |
| "molto" said as "motto" (Southern hypercorrection) | molto | motto |

Preserve genuine dialectal or colloquial vocabulary when it is a real spoken form, not merely a reduction of a standard word.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "vabbè" | vabbè | va bene |
| "'sto" as colloquial "questo" | 'sto | questo, if the colloquial clitic form is clearly intended |
| "mannaggia" | mannaggia | maledizione |

**Verb forms and clitic clusters:** Standard Italian clusters clitics with verbs. Do not split or modify them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "dimmelo" | dimmelo | dimmi lo |
| "lasciamoci" | lasciamoci | lasciamo ci |
| "farcela" | farcela | fare ce la |

**Interrogative vs. orthographic accent on "sé" and compounds:** The conjunction `che` never carries an accent. For this guideline, use `sé` with an accent for the reflexive pronoun, including before `stesso` and related forms. This is a project consistency convention; some Italian style guides also accept `se stesso`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "perché sei qui" | perché sei qui | perche sei qui |
| "se vuoi venire" | se vuoi venire | sé vuoi venire |
| "pensa solo a sé stesso" | pensa solo a sé stesso | pensa solo a se stesso, under this guideline |

---

## Part 2 - Disfluency

### Disfluency Rules

You are given an audio clip and its existing transcription. Your task is to output the transcription as provided, adding all speech disfluencies that you hear based on the rules below. Return only the transcription text.

#### 1. Filler Words

Words like `eh`, `uhm`, `mm`, `ah`, `beh`, `mah`, `boh`, `allora`, `dunque`, `cioè`, `insomma`, `praticamente`, `tipo`, `ecco`, `diciamo`, and `comunque` should be added to the transcription when spoken. Keep lexical fillers as spoken, but standardize excessive elongation according to the canonical table below.

| Audio | Correct |
|-------|---------|
| "eh, non lo so esattamente" | eh, non lo so esattamente |
| "uhm, questo è complicato" | uhm, questo è complicato |
| "allora, ricominciamo da capo" | allora, ricominciamo da capo |
| "tipo, non ci avevo pensato" | tipo, non ci avevo pensato |

#### 2. Hesitation Markers and Vocal Fillers

Listen for **non-lexical vocalizations** during pauses, planning, and reactive listening. Standardize spellings to the canonical form for each group. Use normal Italian sentence spacing and punctuation.

**Filled pauses / hesitation** (speaker holds the floor, searching for words):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **eh** | `eh` | `ehh`, `eh...`, `ehhh` when used as hesitation |
| **uhm** | `uhm` | `uhm...`, `mhm` when used as a thinking sound |
| **mm** | `mm` | `mmm`, `mm...` |
| **ah** | `ah` | `ahh`, `ah...` when used as realization or hesitation |
| **beh** | `beh` | `bè`, `beh...` when used as hesitation |
| **mah** | `mah` | `ma...`, `mah...` when used as hesitation |
| **boh** | `boh` | `bo`, `boh...` expressing uncertainty |
| **allora** | `allora` | `alora`, if the project normalizes to standard form |

**Backchannel / response** (listener signals agreement, negation, or reaction):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **sì** | `sì` | `sì sì`, affirmative response when not repeated intentionally |
| **no** | `no` | `no no` when a single negation is intended |
| **mhm** | `mhm` | `mhmm`, `m-hm` |
| **già** | `già` | `già già`, acknowledgment of known information |
| **certo** | `certo` | `certo certo` when a single acknowledgment is intended |
| **capito** | `capito` | understanding acknowledgment |
| **appunto** | `appunto` | agreement with what was just said |

When the same sounds could be **hesitation** vs **backchannel**, use audio and dialogue role: mid-utterance planning → hesitation; short reactive assent while the other speaker talks → backchannel.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Filled pause before content | eh, domani vengo | ehh, domani vengo |
| Thinking sound | uhm, è difficile | uhm uhm, è difficile |
| Listener yes | sì, capito | sì sì, capito if only one acknowledgment |
| Polite acknowledgment | certo, capisco | certo certo, capisco |
| Surprise/realization | ah, davvero? | ahh, davvero? |

#### 3. Repetitions

Consecutive instances of the same word or short phrase spoken unintentionally should be kept as-is with no added punctuation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "io io io non lo so" | io io io non lo so | io- io- io non lo so / non lo so |
| "e e questo" | e e questo | e- e questo / e questo |
| "ma ma alla fine ci siamo andati" | ma ma alla fine ci siamo andati | ma- ma alla fine ci siamo andati / alla fine ci siamo andati |
| "era una cosa era una cosa strana" | era una cosa era una cosa strana | era una cosa- era una cosa strana |

If a repetition is intentional, rhythmic, or emphatic, use normal Italian punctuation instead of disfluency dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "sì, sì, andiamo" | sì, sì, andiamo | sì- sì- andiamo |
| "certo, certo" | certo, certo | certo- certo |

#### 4. False Starts / Cut-Off Words

Incomplete words or phrases that the speaker abandons should be marked with a single dash followed by a space. If the speaker cuts off and stops entirely, still use a single dash.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "gelat- un semifreddo, per favore" | gelat- un semifreddo, per favore | gelato un semifreddo, per favore |
| "ho cercato di- dove stavo andando?" | ho cercato di- dove stavo andando? | ho cercato di, dove stavo andando? |
| "ho preso un ca-" | ho preso un ca- | ho preso un caffè |

#### 5. Casual Forms, Slang, and Dialect

Use casual forms if that is how they were spoken and the form is clearly audible. If unsure, default to the standard dictionary spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "roba" | roba | cosa |
| "vabbè" | vabbè | va bene |
| "un sacco di" | un sacco di | molto |
| "figurati" | figurati | non c'è di che |
| "in bocca al lupo" | in bocca al lupo | buona fortuna |

Preserve recognized written elisions and colloquial forms when they are clearly spoken. Normalize only pure phonetic reductions when the intended word is clear and the reduced form is not a standard or accepted written form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "s'è" clearly spoken as the elided form of "si è" | s'è | si è |
| "si è" fully articulated | si è | s'è |
| "c'ho" in colloquial use | c'ho | ci ho (when clearly the colloquial elided form) |
| "t'ho detto" | t'ho detto | ti ho detto (when elision is clearly intended) |

Do not rewrite dialectal or colloquial grammar into formal standard Italian if the form is a real spoken form and not merely a dropped sound.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ammazza" (Roman exclamation) | ammazza | incredibile |
| "uagliò" (Neapolitan) | uagliò | ragazzo |
| "ndo vai?" (Roman "dove vai") | ndo vai? | dove vai? if the dialectal form is clearly intended |

#### 6. Spelled-Out Words

If a speaker spells out a non-acronym word one letter at a time using Italian letter names or Latin letters, use capital letters separated with dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "si scrive M-A-R-I-O" | si scrive M-A-R-I-O | si scrive M A R I O |
| "il codice è A-B-uno-due-tre" | il codice è A-B-uno-due-tre | il codice è AB123 |

If a speaker uses Italian alphabet letter names (e.g., *emme*, *acca*, *erre*), transcribe the letter names as spoken. Do not infer a full word unless the speaker clearly provides it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "emme, acca, erre" | emme, acca, erre | mhr |
| "ci, acca, e" | ci, acca, e | che |

If the speaker is saying an acronym or initialism, use the canonical acronym form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "rai" | RAI | R-A-I |
| "o-en-u" | ONU | O-N-U |

#### 7. Mispronunciations

Transcribe intelligible real-word substitutions as spoken. Do not correct the word in the base transcript and do not add a tag unless your project uses superset `{MIS: ...}` annotations.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "bello" where "quello" was intended | bello | quello |
| "fatto" where "detto" was intended by context | fatto | detto |
| "capetto" | capetto | cappotto, unless using superset `cappotto {MIS: capetto}` |

If the sound is intelligible but not a real word and the intended word is unclear, transcribe the sound phonetically using Italian spelling conventions.

| Audio | Correct |
|-------|---------|
| "brifolampo" (non-word) | brifolampo |

#### 8. Wrong Grammar

Grammatical errors, dialectal grammar, and non-standard morphology should be faithfully captured. Do not correct them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "io gli ho detto a lui" | io gli ho detto a lui | gli ho detto |
| "me ne sono andato via" | me ne sono andato via | me ne sono andato |
| "lui ha detto che veniva ieri" | lui ha detto che veniva ieri | lui ha detto che è venuto ieri |
| "ho comprato una libro" | ho comprato una libro | ho comprato un libro |

---

## Part 3 - Rich Transcription: Paralinguistic Tokens

### Non-Speech Sound Tokens

Bracket tokens mark **audible non-lexical or non-linguistic events** that are **not** regular words. Write each tag **exactly** as listed (square brackets included). Prefer **one tag per distinct event**; if several happen in sequence, repeat tags in **time order**, separated by spaces.

Use the NeMo canonical English tag names below, even in Italian transcripts.

#### Rules for this section

1. **Tag vs words** - If the speaker says a word, transcribe the word. Use a bracket tag only for the sound event itself.
2. **No invented words** - Do not replace a tag with a phonetic guess unless the sound is a lexical filler covered in Part 2.
3. **Placement** - Put the tag where the sound occurs in the word stream, usually as its own token between words.
4. **Overlap** - If a sound overlaps speech, place the tag at the start of the overlap window unless your time-aligned format specifies otherwise.
5. **Sequences** - Use `[laugh] [laugh]` for two separate laugh bursts, not a single stretched token.
6. **Unknown / generic background** - Use `[other-noise]` for audible non-speech you cannot classify; use `[unintelligible]` only when linguistic content was likely present but cannot be recovered.
7. **Minor mouth sounds** - Do not tag faint natural mouth clicks, lip noise, or routine breathing unless they are prominent or communicative.

#### Token list and descriptions

Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into Italian or replace them with local-language labels.

| Token | Description |
|-------|-------------|
| `[breath]` | Audible breath sound without a clear inhale vs exhale distinction. |
| `[inhale]` | Clear inward breath before or between phrases. |
| `[exhale]` | Clear outward breath, often after a phrase or under stress. |
| `[sigh]` | Prolonged or marked sigh. |
| `[sniff]` | Nasal sniff or sniffle. |
| `[gasp]` | Sharp gasp or sudden air intake. |
| `[blow]` | Audible blow through the mouth, not speech. |
| `[laugh]` | Laughter vocalization. |
| `[chuckle]` | Softer, shorter, suppressed laugh. |
| `[giggle]` | Higher-pitched or repeated light laugh. |
| `[snort]` | Snort through nose or mouth while laughing or reacting. |
| `[scoff]` | Dismissive exhalation or laugh-like puff. |
| `[grunt]` | Short grunt or effort vocalization. |
| `[groan]` | Longer groan or moan. |
| `[cry]` | Crying, sobbing, or wailing sounds. |
| `[hum-tune]` | Humming a melody or tune, not lexical humming words. |
| `[whoop]` | Whoop or cheer-like shout, not normal spoken "whoop." |
| `[whistle]` | Whistling. |
| `[tongue-click]` | Tongue click / alveolar click. |
| `[tsk]` | Tsk-tsk / reproach click. |
| `[lip-smack]` | Lip smack. |
| `[teeth-suck]` | Suck through teeth or sharp dental inhale. |
| `[lip-trill]` | Bilabial trill / lip buzz. |
| `[shush]` | Shushing sound, not the spoken word. |
| `[swallow]` | Audible swallow. |
| `[clear-throat]` | Throat clear / hack / harrumph. |
| `[cough]` | Cough sound. |
| `[sneeze]` | Sneeze sound. |
| `[yawn]` | Yawn sound. |
| `[hiccup]` | Hiccup sound. |
| `[unintelligible]` | Speech was likely present but the words cannot be resolved. |
| `[other-noise]` | Non-speech sound that does not fit a label above. |

#### Examples

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| Speaker laughs before speaking | [laugh] è davvero divertente. | [risata] è davvero divertente. |
| Speaker coughs mid-sentence | questo è [cough] assolutamente corretto. | questo è tosse assolutamente corretto. |
| Speech is masked and unrecoverable | era [unintelligible] di sicuro. | era di sicuro. |
| Background object noise | [other-noise] può ripetere, per favore? | [rumore] può ripetere, per favore? |

#### Quick reference (canonical spellings)

- `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`, `[sniff]`, `[gasp]`, `[blow]`
- `[laugh]`, `[chuckle]`, `[giggle]`, `[snort]`, `[scoff]`, `[grunt]`, `[groan]`, `[cry]`
- `[hum-tune]`, `[whoop]`, `[whistle]`, `[tongue-click]`, `[tsk]`, `[lip-smack]`, `[teeth-suck]`, `[lip-trill]`, `[shush]`, `[swallow]`, `[clear-throat]`
- `[cough]`, `[sneeze]`, `[yawn]`, `[hiccup]`, `[unintelligible]`, `[other-noise]`
