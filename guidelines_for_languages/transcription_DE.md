# German Transcription Guidelines

Language: German (Germany)

## Part 1 - Text normalization

### Superset principle

The transcription rules below define the **minimum required coverage**. Annotation vendors are expected to deliver transcriptions that are a **superset** of these rules - any additional detail, markup, or tagging beyond what is specified here is encouraged and acceptable, as long as it does not contradict the rules.

Examples of acceptable superset additions include (but are not limited to):

- **Pronunciation variants** for acronyms or proper nouns annotated inline:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "ASAP" said as "A-S-A-P" | ASAP {PRO: A-S-A-P} |
| "ASAP" said as "a-sap" | ASAP {PRO: a-sap} |

- **Mispronunciation tags** to flag non-standard renderings:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "Arbeitsehkick" intended as "Arbeitsethik" | Arbeitsethik {MIS: Arbeitsehkick} |

- **Additional hesitation markers, dialect notes, confidence flags, or emotion tags** are acceptable as long as they do not alter the base transcription text.

In short: **do not remove detail that is present in the audio**. The rules below set the floor, not the ceiling.

---

### Text Normalization Rules

Transcribe the audio in standard German orthography. Convert numeric, symbolic, and abbreviated tokens to their fully spoken German form using the rules below. Return transcription only.

#### 1. Broad Principles

With the exception of acronyms, initialisms, and clearly intended proper-name spellings, everything should be written out in full spoken words. Abbreviations, symbols, shorthand, and numerals should all be expanded.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Doktor Schmidt" | Doktor Schmidt | Dr. Schmidt |
| "viele Kilogramm" | viele Kilogramm | viele kg |
| "und so weiter" | und so weiter | usw. |
| "Sankt Martin" | Sankt Martin | St. Martin |
| "iPhone zehn" | iPhone zehn | iPhone 10 / iPhone X |

German nouns, proper names, and nominalized words are capitalized.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "das gute daran" | das Gute daran | das gute daran |
| "beim essen" | beim Essen | beim essen |
| "die fantastischen vier" as the group name | Die Fantastischen Vier | Die Fantastischen 4 |

#### 2. German Orthography and Capitalization

Use current standard German spelling:

- Capitalize the first word of a sentence or segment, unless the segment explicitly continues a previous sentence fragment.
- Capitalize all nouns and nominalized forms.
- Preserve umlauts and `ß` where standard spelling requires them.
- Use conventional capitalization for brand names and product names.
- Do not imitate dialect pronunciation in spelling when the intended standard word is clear and the difference is only phonetic.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Könich" | König | Könich |
| "wenich" | wenig | wenich |
| "Straße" | Straße | Strasse, unless the project explicitly requires Swiss spelling |
| "i phone zehn" | iPhone zehn | iPhone 10 / iPhone X |

#### 3. Numbers

Spell out all digits and numeric expressions as spoken German words. Do not write Arabic numerals for transcription text.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "vierzehn" | vierzehn | 14 |
| "null Komma null fünf" | null Komma null fünf | 0,05 / 0.05 |
| "eintausenddreißig Komma fünf" | eintausenddreißig Komma fünf | 1.030,5 |
| "zwanzig vierundzwanzig" as a year | zwanzig vierundzwanzig | 2024 |
| "zwei null zwei vier" | zwei null zwei vier | 2024 |
| "neun drei sechs Bindestrich eins eins" | neun drei sechs Bindestrich eins eins | 936-11 |
| "neun zwo eins null" as a postal code | neun zwo eins null | 90210 |

#### 4. Non-Numeral Usage

Do not convert number words to Arabic numerals when they are part of natural language and not intended to communicate a specific numeric value.

This includes idioms, determiner-like uses, conventional expressions, proper nouns, and many compounds.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Du bist die Einzige für mich" | Du bist die Einzige für mich | Du bist die 1-zige für mich |
| "auf der einen Seite" | auf der einen Seite | auf der 1 Seite |
| "zuallererst" | zuallererst | zualler-1. |
| "Die Fantastischen Vier" | Die Fantastischen Vier | Die Fantastischen 4 |
| "Ocean's Eleven" | Ocean's Eleven | Ocean's 11, unless that is the official title style |
| "Siebenschläfer" | Siebenschläfer | 7-Schläfer |
| "eine Drei-Zimmer-Wohnung" | eine Drei-Zimmer-Wohnung | eine 3-Zimmer-Wohnung |
| "ein Siebenjähriger" | ein Siebenjähriger | ein 7-Jähriger |

When a disfluency occurs before a non-numeral expression, keep the disfluent portion as spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "e- e- einhundertfünf" | e- e- einhundertfünf | e- e- 105 |
| "v- v- vierzehn" | v- v- vierzehn | v- v- 14 |

#### 5. Ordinals, Decades, and Age Ranges

Spell out ordinals, decades, and age ranges as spoken German words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "der dritte" | der dritte | der 3. |
| "einundzwanzigster" | einundzwanzigster | 21. / 21st |
| "fünfzigster Geburtstag" | fünfzigster Geburtstag | 50. Geburtstag |
| "die Siebziger" | die Siebziger | die 70er |
| "in den Zwanzigern" | in den Zwanzigern | in den 20ern |

Do not use numerals inside fixed expressions or names where the word form is conventional.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Die Fantastischen Vier" | Die Fantastischen Vier | Die Fantastischen 4 |
| "Drei Fragezeichen" as the series name | Die drei ??? / Die drei Fragezeichen | Die 3 Fragezeichen |

#### 6. Dates

Write dates as spoken German words. Do not convert day, month, or year into digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "erster Mai" as a date | erster Mai | 1. Mai |
| "neunundzwanzigster April zweitausendvierundzwanzig" | neunundzwanzigster April zweitausendvierundzwanzig | 29. April 2024 |
| "der dritte zehnte neunzehnhundertneunzig" | der dritte zehnte neunzehnhundertneunzig | 3.10.1990 / 03/10/1990 |
| "zweitausendvierundzwanzig" as a year | zweitausendvierundzwanzig | 2024 |

If the speaker reads a date digit by digit, preserve that digit-by-digit spoken form.

#### 7. Time of Day

Write clock times as spoken German words. German commonly uses 24-hour time; do not add AM/PM unless the speaker says it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "acht Uhr dreißig" | acht Uhr dreißig | 8:30 |
| "acht Uhr morgens" | acht Uhr morgens | 8:00 morgens / 8 AM |
| "acht Uhr abends" | acht Uhr abends | 20:00 / 8 PM |
| "viertel nach zehn" | viertel nach zehn | 10:15 |
| "halb acht" | halb acht | 7:30 / 8:30 |
| "null Uhr fünfzehn" | null Uhr fünfzehn | 0:15 |
| "mittags" | mittags | 12:00 |
| "Mitternacht" | Mitternacht | 0:00 |

#### 8. Money / Currency

Spell out money and currency amounts as spoken German words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "zweiundfünfzig Euro" | zweiundfünfzig Euro | 52 € / 52 Euro |
| "tausend Dollar" | tausend Dollar | 1.000 $ / 1.000 Dollar |
| "zwei Euro fünfzig" | zwei Euro fünfzig | 2,50 € |
| "dreißig, vierzig Euro" | dreißig, vierzig Euro | 30 €, 40 € |

Do not normalize informal money words into currency symbols unless the amount and currency are clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "eine Mille" | eine Mille | 1.000 € |
| "ein paar Taler" | ein paar Taler | ein paar € |

#### 9. Percentages

Spell out the number and the word `Prozent`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "null Komma fünf Prozent" | null Komma fünf Prozent | 0,5 % / 0.5% |
| "hundert Prozent" | hundert Prozent | 100 % |
| "zwanzig bis dreißig Prozent" | zwanzig bis dreißig Prozent | 20 % bis 30 % |

#### 10. Measures / Units

Read the number as words and expand the unit abbreviation to its full spoken form. If the speaker reads letters or a technical shorthand, transcribe that spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "fünf Kilogramm" | fünf Kilogramm | 5 Kilogramm / 5 kg |
| "fünf k g" | fünf k g | 5 kg |
| "neunzig Kilometer pro Stunde" | neunzig Kilometer pro Stunde | 90 Kilometer pro Stunde / 90 km/h |
| "fünf Meter vierzig" | fünf Meter vierzig | 5,40 m / 5 Meter 40 |
| "vier ka" | vier ka | 4K |
| "zehn achtzig pe" | zehn achtzig pe | 1080p |

When a technical symbol has multiple possible readings, a `{PRO: ...}` tag is acceptable as a superset annotation.

#### 11. Fractions, Ratios, and Scores

Spell out fractions, ratios, and scores as spoken German words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "drei Viertel" | drei Viertel | 3/4 |
| "eins und drei Viertel" | eins und drei Viertel | 1 3/4 / 1.75 |
| "ein Halb" | ein Halb | 1/2 / 0,5 |
| "fünfzig fünfzig" | fünfzig fünfzig | 50:50 |
| "zwei zu eins" as a score | zwei zu eins | 2:1 / 2-1 |
| "drei gegen zwei" | drei gegen zwei | 3 gegen 2 |

#### 12. Negative Numbers

Spell out negative numbers as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "minus zwölf" | minus zwölf | -12 / minus 12 |
| "minus achtzehn Grad" | minus achtzehn Grad | -18 Grad / -18 °C |
| "achtzehn unter null" | achtzehn unter null | -18 |

Use `minus` when the speaker says `minus`. Use the phrase the speaker used when it is idiomatic rather than a formal numeric value.

#### 13. Phone Numbers, Postal Codes, IDs, and Codes

Read each digit group individually as spoken. Do not write formatted phone numbers, postal codes, or IDs with digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "null dreißig, eins zwei drei vier, fünf sechs sieben acht" | null dreißig, eins zwei drei vier, fünf sechs sieben acht | 030 1234 5678 |
| "neun drei sechs Bindestrich eins eins" | neun drei sechs Bindestrich eins eins | 936-11 |
| "neun zwo eins null" as a postal code | neun zwo eins null | 90210 |
| "A B eins zwei drei" | A B eins zwei drei | AB123 |

#### 14. Electronic Text (URLs, Emails, IPs)

Read all symbols aloud. Do not write URLs, email addresses, IP addresses, usernames, or file paths in their compact written form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "beispiel Punkt de Schrägstrich preise" | beispiel Punkt de Schrägstrich preise | beispiel.de/preise |
| "google Punkt de" | google Punkt de | google.de |
| "max at gmail Punkt com" | max at gmail Punkt com | max@gmail.com |
| "eins neun zwei Punkt eins sechs acht Punkt null Punkt eins" | eins neun zwei Punkt eins sechs acht Punkt null Punkt eins | 192.168.0.1 |

#### 15. Roman Numerals

Use the spoken form after chapter/title keywords and after a person's name. Do not convert spoken Roman numeral readings into Roman numerals.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Star Wars Episode vier" | Star Wars Episode vier | Star Wars Episode IV |
| "GTA fünf" | GTA fünf | GTA V |
| "Elisabeth die Zweite" | Elisabeth die Zweite | Elisabeth II. / Elisabeth 2 |

#### 16. Abbreviations

Expand abbreviations when the speaker says the full words. Keep acronyms, initialisms, and standard technical abbreviations when they are spoken as such.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Gesellschaft mit beschränkter Haftung" | Gesellschaft mit beschränkter Haftung | GmbH |
| "L K W" | LKW | Lastkraftwagen |
| "Lastkraftwagen" | Lastkraftwagen | LKW |
| "zum Beispiel" | zum Beispiel | z. B. |
| "z b" | z b | z. B. / zum Beispiel |
| "Sankt Martin" | Sankt Martin | St. Martin |

#### 17. Addresses

Write addresses as spoken German words. Expand spoken street-type words and do not convert house numbers or postal codes into digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Musterstraße fünf" | Musterstraße fünf | Musterstraße 5 / Musterstr. 5 |
| "Berliner Allee zwölf b" | Berliner Allee zwölf b | Berliner Allee 12b |
| "Postleitzahl eins null eins eins fünf" | Postleitzahl eins null eins eins fünf | Postleitzahl 10115 |

#### 18. Acronyms and Initialisms

Keep spoken acronyms and initialisms in their canonical form. Do not expand them unless the speaker says the expanded form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "A D A C" | ADAC | Allgemeiner Deutscher Automobil-Club |
| "F B I" | FBI | Federal Bureau of Investigation |
| "L K W" | LKW | Lastkraftwagen |
| "S Q L" | SQL | Structured Query Language |
| "Structured Query Language" | Structured Query Language | SQL |

When pronunciation is ambiguous or important, `{PRO: ...}` is an acceptable superset annotation.

#### 19. Foreign Words and Loanwords

Do not mark well-established German loanwords as foreign words. Transcribe them in the standard German form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Café" | Café | <foreign> Cafe </foreign> |
| "Laptop" | Laptop | <foreign> laptop </foreign> |
| "Taco" in ordinary German speech | Taco | <foreign> taco </foreign> |

Use the actual foreign spelling for a foreign-language phrase when the words are clearly spoken and recognizable. If your pipeline supports foreign-language tags, they may be added as a superset annotation.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "Thank you" clearly in English | Thank you | <foreign lang="EN"> Thank you </foreign> |
| "Gracias" clearly in Spanish | Gracias | <foreign lang="ES"> Gracias </foreign> |

Proper nouns are not foreign-language spans just because they come from another language.

#### 20. Ambiguity

Rely on audio context to resolve ambiguous tokens.

| Context | Audio | Correct |
|---------|-------|---------|
| Time | "um acht" | um acht |
| Quantity | "acht" | acht |
| Natural expression | "auf der einen Seite" | auf der einen Seite |
| Proper noun | "Die Fantastischen Vier" | Die Fantastischen Vier |
| Acronym | "L K W" | LKW |

German has homophones where the same pronunciation maps to different spellings and meanings. When pronunciation alone is ambiguous, use the surrounding meaning and context to choose the standard German written form. Only treat words as ambiguous homophones when they sound exactly the same in standard German; do not use this rule for merely similar-sounding words.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Article or pronoun | "das ist gut" | das ist gut | dass ist gut |
| Subordinating conjunction | "ich glaube, dass es stimmt" | ich glaube, dass es stimmt | ich glaube, das es stimmt |
| Time since | "seit gestern" | seit gestern | seid gestern |
| Verb form of `sein` | "ihr seid bereit" | ihr seid bereit | ihr seit bereit |
| Ocean | "das Meer ist ruhig" | das Meer ist ruhig | das mehr ist ruhig |
| Quantity comparison | "ich brauche mehr Zeit" | ich brauche mehr Zeit | ich brauche Meer Zeit |
| Choice/election | "die Wahl war schwer" | die Wahl war schwer | die Wal war schwer |
| Animal | "der Wal schwimmt" | der Wal schwimmt | der Wahl schwimmt |
| Wheel | "das Rad ist kaputt" | das Rad ist kaputt | das Rat ist kaputt |
| Advice/council | "der Rat war hilfreich" | der Rat war hilfreich | der Rad war hilfreich |
| Death | "der Tod kam plötzlich" | der Tod kam plötzlich | der tot kam plötzlich |
| Adjective | "er ist tot" | er ist tot | er ist Tod |
| Again | "wir sehen uns wieder" | wir sehen uns wieder | wir sehen uns wider |
| Against | "wider Erwarten" | wider Erwarten | wieder Erwarten |

If multiple written forms are acceptable after context is considered, choose the form that best preserves the speaker's intended meaning and is most natural in German.

#### 21. Guidelines for Language-specific Issues

The following German-specific issues should follow the same principles above: preserve what was spoken, use standard German spelling when the intended word is clear, and do not invent unsupported written forms.

**Standard spelling vs surface pronunciation:** German pronunciation can obscure spelling through final devoicing and other regular sound patterns. Write the intended standard word from context, not the surface sound alone.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Wheel | "das Rad ist kaputt" | das Rad ist kaputt | das Rat ist kaputt |
| Advice/council | "der Rat war hilfreich" | der Rat war hilfreich | der Rad war hilfreich |
| Federation | "der Bund entscheidet" | der Bund entscheidet | der bunt entscheidet |
| Color adjective | "das ist bunt" | das ist bunt | das ist Bund |

**Unknown proper-name spelling:** German names can have several spellings with the same pronunciation. If the official spelling is not known from context, do not guess a special spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Meyer" with unknown spelling | Meyer / Meier / Maier / Mayer, only if known | Guessing one spelling without evidence |
| "Schmidt" with unknown spelling | Schmidt / Schmitt, only if known | Guessing one spelling without evidence |
| "Müller" with unknown spelling | Müller, if known from context | Mueller, unless that official spelling is known |

**Compound nouns and hyphenation:** German compounds should usually be written as standard compounds. Use hyphens where standard German spelling or the official term requires them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Krankenhausverwaltung" | Krankenhausverwaltung | Krankenhaus Verwaltung |
| "Datenschutzbeauftragter" | Datenschutzbeauftragter | Datenschutz Beauftragter |
| "E-Mail-Adresse" | E-Mail-Adresse | Email Adresse / E Mail Adresse |

**Meaning-sensitive one-word vs two-word forms:** Some German forms differ by meaning depending on whether they are written together or separately. Use context to choose the correct form.

| Context | Correct | Incorrect |
|---------|---------|-----------|
| Meet again | wir werden uns wiedersehen | wir werden uns wieder sehen |
| See something again | ich will das wieder sehen | ich will das wiedersehen |
| Get acquainted | wir möchten Sie kennenlernen | wir möchten Sie kennen lernen, if one-word verb is intended |
| Work collaboratively | wir werden zusammenarbeiten | wir werden zusammen arbeiten |

**Named entities and official stylization:** Brands and products may intentionally use nonstandard casing or spelling. Use official stylization only when it is clearly intended; otherwise use the normal spoken German form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "iPhone" clearly as the product | iPhone | Iphone / Eifon |
| "YouTube" clearly as the service | YouTube | Youtube / Jutjub |
| "BILD" clearly as the newspaper | BILD | Bild, if the official title is intended |
| "dm" clearly as the store | dm | DM, if the store brand is intended |

**Austrian, Swiss, and German regional variants:** This document is for German (Germany). Preserve real regional words when spoken, but do not convert them into unrelated Germany-standard words unless the project explicitly requires normalization.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Jänner" | Jänner | Januar |
| "Velo" | Velo | Fahrrad |
| "Grüezi" | Grüezi | Guten Tag |
| "Servus" | Servus | Hallo |
| "Moin" | Moin | Guten Morgen |

---

## Part 2 - Disfluency

### Disfluency Rules

You are given an audio clip and its existing transcription. Your task is to output the transcription as provided, adding all speech disfluencies that you hear based on the rules below. Return only the transcription text.

#### 1. Filler Words

Words like "ja", "genau", "also", "äh", "ähm", "hm", "mhm", "ach", "na", and "sozusagen" should be added to the transcription when spoken. Keep lexical fillers as spoken, but standardize excessive elongation according to the canonical table below.

| Audio | Correct |
|-------|---------|
| "also ich glaube schon" | also ich glaube schon |
| "äh, das weiß ich nicht" | äh, das weiß ich nicht |
| "ja genau, das passt" | ja genau, das passt |

#### 2. Hesitation Markers and Vocal Fillers

Listen for **non-lexical vocalizations** during pauses, planning, and reactive listening. Standardize spellings to the canonical form for each group. Use normal German capitalization at sentence starts.

**Filled pauses / hesitation** (speaker holds the floor, searching for words):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **äh** | `äh` | `ääh`, `äääh`, drawn-out hesitation |
| **ähm** | `ähm` | `ähmm`, `ääähm`, `ehm` when used as German hesitation |
| **hm** | `hm` | `hmm`, `hmmm`, thinking hums |
| **mm** | `mm` | `mmm` when a closed-mouth hesitation, not agreement |
| **ah** | `ah` | `aah`, `ahh` |
| **ach** | `ach` | `aach`, `achh` |
| **oh** | `oh` | `ohh`, `ooh` when used as German `oh` |
| **uff** | `uff` | `ufff`, `uuff` |

**Backchannel / response** (listener signals agreement, negation, or reaction):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **mhm** | `mhm` | `mm-hmm`, `mhmm`, affirmative nasal response |
| **mh-mh** | `mh-mh` | `mm-mm`, `mh mh`, negative nasal response |
| **aha** | `aha` | `ah-ha`, `ahaa` |
| **hä** | `hä` | `hää` |
| **ne** | `ne` | `nee` when used as a short negative response |
| **puh** | `puh` | `puuh`, `puhh` |
| **boah** | `boah` | `boa`, `boaaah` |
| **aua** | `aua` | `auaa`, pain reaction |
| **autsch** | `autsch` | `autschh` |

When the same phones could be **hesitation** vs **backchannel**, use audio and dialogue role: mid-utterance planning -> hesitation; short reactive assent while the other speaker talks -> backchannel.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Filled pause before content | äh, ich glaube schon | ääh, ich glaube schon |
| Thinking hum | hm, das ist schwierig | hmmm, das ist schwierig |
| Listener yes | mhm, genau | mm-hmm, genau |
| Listener no | mh-mh, das stimmt nicht | mm-mm, das stimmt nicht |
| Surprise | oh, wirklich? | ooh, wirklich? |

#### 3. Repetitions

Consecutive instances of the same word or short phrase spoken unintentionally should be kept as-is with no added punctuation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "i i ich" | i i ich | i- i- ich / ich |
| "den den denke" | den den denke | den- den- denke / denke |
| "wir wir wir" | wir wir wir | wir- wir- wir / wir |
| "Ich will ich will ich will mehr" | Ich will ich will ich will mehr | Ich will- ich will- ich will mehr / Ich will mehr |
| "Das war das war wirklich schlecht" | Das war das war wirklich schlecht | Das war- das war wirklich schlecht / Das war wirklich schlecht |

If a repetition is intentional, rhythmic, or emphatic, use normal German punctuation instead of disfluency dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Ja, ja, ich komme mit" | Ja, ja, ich komme mit | Ja- ja- ich komme mit |
| "Genau, genau, das macht Sinn" | Genau, genau, das macht Sinn | Genau- genau, das macht Sinn |

#### 4. False Starts / Cut-Off Words

Incomplete words or phrases that the speaker abandons should be marked with a single dash followed by a space. If the speaker cuts off and stops entirely, still use a single dash.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Ich wollte die Eiscre- Froyo" | Ich wollte die Eiscre- Froyo | Ich wollte die Eiscreme Froyo |
| "Ich wollte gera- wo wollte ich hin?" | Ich wollte gera- wo wollte ich hin? | Ich wollte gerade, wo wollte ich hin? |
| "Ich wollte die Eiscre-" | Ich wollte die Eiscre- | Ich wollte die Eiscreme |

#### 5. Contractions, Colloquial Forms, and Dialect

Use contractions if that is how it was spoken and the contraction is a standard or accepted written German form. If unsure, default to the standard dictionary spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "'n Kaffee" | 'n Kaffee | ein Kaffee |
| "so 'n Ding" | so 'n Ding | so ein Ding |
| "so 'ne Sache" | so 'ne Sache | so eine Sache |
| "überm Tisch" | überm Tisch | über dem Tisch |
| "ins Haus" | ins Haus | in das Haus |
| "grad" | grad | gerade, if clearly spoken as `grad` |
| "isses" | isses | ist es |

Normalize reduced verb endings when they are only casual pronunciation of the standard form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "wir geh'n" | wir gehen | wir geh'n |
| "ich geh" | ich gehe | ich geh |

Do not rewrite dialectal or colloquial grammar into formal standard German if the form is a real spoken form and not merely a dropped sound.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ick bin da" | ick bin da | ich bin da |
| "net schlecht" | net schlecht | nicht schlecht |
| "ham wir" | ham wir, if clearly lexicalized in the dataset style | haben wir, if the style guide treats it as dropped pronunciation |

#### 6. Spelled-Out Words

If a speaker spells out a non-acronym word one letter at a time, use capital letters separated with dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "buchstabiert M A S E G O" | buchstabiert M-A-S-E-G-O | buchstabiert M A S E G O |

If the speaker is saying an acronym or initialism, use the canonical acronym form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "F B I" | FBI | F-B-I |
| "L K W" | LKW | L-K-W |

#### 7. Mispronunciations

Transcribe intelligible real-word substitutions as spoken. Do not correct the word in the base transcript and do not add a tag unless your project uses superset `{MIS: ...}` annotations.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Da wird der Hund in der Pfanne verrührt" where "verrückt" was intended | Da wird der Hund in der Pfanne verrührt | Da wird der Hund in der Pfanne verrückt |
| "Wir gehen heute an den Schrank" where "Strand" was intended | Wir gehen heute an den Schrank | Wir gehen heute an den Strand |
| "Arbeitsehkick" | Arbeitsehkick | Arbeitsethik, unless using superset `Arbeitsethik {MIS: Arbeitsehkick}` |

If the sound is intelligible but not a real word and the intended word is unclear, transcribe the sound phonetically.

| Audio | Correct |
|-------|---------|
| "dorpklogh" | dorpklogh |

#### 8. Wrong Grammar

Grammatical errors, dialectal grammar, and non-standard morphology should be faithfully captured. Do not correct them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "dem sein Auto" | dem sein Auto | sein Auto |
| "ich bin größer wie du" | ich bin größer wie du | ich bin größer als du |
| "wegen dem Wetter" | wegen dem Wetter | wegen des Wetters |

---

## Part 3 - Rich Transcription: Paralinguistic Tokens

### Non-Speech Sound Tokens

Bracket tokens mark **audible non-lexical or non-linguistic events** that are **not** regular words. Write each tag **exactly** as listed (square brackets included). Prefer **one tag per distinct event**; if several happen in sequence, repeat tags in **time order**, separated by spaces.

Use the NeMo canonical English tag names below, even in German transcripts.

#### Rules for this section

1. **Tag vs words** - If the speaker says a word, transcribe the word. Use a bracket tag only for the sound event itself.
2. **No invented words** - Do not replace a tag with a phonetic guess unless the sound is a lexical filler covered in Part 2.
3. **Placement** - Put the tag where the sound occurs in the word stream, usually as its own token between words.
4. **Overlap** - If a sound overlaps speech, place the tag at the start of the overlap window unless your time-aligned format specifies otherwise.
5. **Sequences** - Use `[laugh] [laugh]` for two separate laugh bursts, not a single stretched token.
6. **Unknown / generic background** - Use `[other-noise]` for audible non-speech you cannot classify; use `[unintelligible]` only when linguistic content was likely present but cannot be recovered.
7. **Minor mouth sounds** - Do not tag faint natural mouth clicks, lip noise, or routine breathing unless they are prominent or communicative.

#### Token list and descriptions

Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into German or replace them with local-language labels.

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
| Speaker laughs before speaking | [laugh] Das ist lustig. | [Lachen] Das ist lustig. |
| Speaker coughs mid-sentence | Das ist [cough] kein Problem. | Das ist Husten kein Problem. |
| Speech is masked and unrecoverable | Das war [unintelligible] gestern. | Das war gestern. |
| Background object noise | [other-noise] Können Sie das wiederholen? | [Geräusch] Können Sie das wiederholen? |

#### Quick reference (canonical spellings)

- `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`, `[sniff]`, `[gasp]`, `[blow]`
- `[laugh]`, `[chuckle]`, `[giggle]`, `[snort]`, `[scoff]`, `[grunt]`, `[groan]`, `[cry]`
- `[hum-tune]`, `[whoop]`, `[whistle]`, `[tongue-click]`, `[tsk]`, `[lip-smack]`, `[teeth-suck]`, `[lip-trill]`, `[shush]`, `[swallow]`, `[clear-throat]`
- `[cough]`, `[sneeze]`, `[yawn]`, `[hiccup]`, `[unintelligible]`, `[other-noise]`

---
