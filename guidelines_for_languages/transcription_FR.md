# French Transcription Guidelines

Language: French (France)

## Part 1 - Text normalization

### Superset principle

The transcription rules below define the **minimum required coverage**. Annotation vendors are expected to deliver transcriptions that are a **superset** of these rules - any additional detail, markup, or tagging beyond what is specified here is encouraged and acceptable, as long as it does not contradict the rules.

Examples of acceptable superset additions include (but are not limited to):

- **Pronunciation variants** for acronyms or proper nouns annotated inline:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "SNCF" said as "esse enne ce effe" | SNCF {PRO: esse enne ce effe} |
| "SQL" said as "esse cu elle" | SQL {PRO: esse cu elle} |

- **Mispronunciation tags** to flag non-standard renderings:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "bibliotheque" intended as "bibliothèque" but pronounced non-standardly | bibliothèque {MIS: bibliotheque} |

- **Additional hesitation markers, dialect notes, confidence flags, or emotion tags** are acceptable as long as they do not alter the base transcription text.

In short: **do not remove detail that is present in the audio**. The rules below set the floor, not the ceiling.

---

### Text Normalization Rules

Transcribe the audio in standard French orthography. Convert numeric, symbolic, and abbreviated tokens to their fully spoken French form using the rules below. Return transcription only.

#### 1. Broad Principles

With the exception of acronyms, initialisms, and clearly intended official spellings, everything should be written out in full spoken words. Abbreviations, symbols, shorthand, and numerals should all be expanded.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "docteur Martin" | docteur Martin | Dr Martin |
| "beaucoup de kilogrammes" | beaucoup de kilogrammes | beaucoup de kg |
| "et cetera" | et cetera | etc. |
| "saint Michel" | saint Michel | St Michel |
| "iPhone quinze" | iPhone quinze | iPhone 15 |

Use standard French spelling, accents, apostrophes, and word boundaries. Do not over-normalize into a form that changes spoken content.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "j'aime Paris" | j'aime Paris | je aime Paris |
| "c'est évident" | c'est évident | cest evident |
| "aujourd'hui" | aujourd'hui | aujourd hui |
| "peut-être" | peut-être | peut etre |
| "qu'est-ce que tu fais" | qu'est-ce que tu fais | quest ce que tu fais |

#### 2. French Orthography, Accents, and Punctuation

Use current standard French spelling:

- Preserve accents and diacritics where standard spelling requires them: `é`, `è`, `ê`, `ë`, `à`, `ù`, `ç`, `î`, `ï`, `ô`.
- Use apostrophes for standard elisions: `l'homme`, `j'arrive`, `qu'il`, `c'est`.
- Use hyphens in conventional compounds and questions where required: `peut-être`, `celui-ci`, `dit-il`.
- Capitalize proper nouns, brand names, and the first word of a sentence or segment. Do not capitalize common nouns or month names just because they appear in a date.
- Use standard spelling rather than surface pronunciation when the intended word is clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ecole" meaning "école" | école | ecole |
| "francais" meaning "français" | français | francais |
| "j'suis arrivé" as ordinary fast speech | je suis arrivé | j'suis arrivé |
| "y a un problème" as a colloquial construction | il y a un problème | y a un problème, unless the colloquial wording is intentionally preserved |
| "tu es là" | tu es là | t'es là, unless that contraction is the intended colloquial form |

Preserve real colloquial, slang, or regional vocabulary when it is what the speaker says, not merely a predictable phonetic reduction.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ouais" | ouais | oui |
| "boulot" | boulot | travail |
| "meuf" | meuf | femme |
| "ça craint" | ça craint | c'est mauvais |

#### 3. Numbers

Spell out all digits and numeric expressions as spoken French words. Do not write Arabic numerals for transcription text.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "quatorze" | quatorze | 14 |
| "zéro virgule zéro cinq" | zéro virgule zéro cinq | 0,05 / 0.05 |
| "mille trente virgule cinq" | mille trente virgule cinq | 1 030,5 |
| "deux mille vingt-quatre" | deux mille vingt-quatre | 2024 |
| "vingt vingt-quatre" as a year | vingt vingt-quatre | 2024 |
| "deux zéro deux quatre" | deux zéro deux quatre | 2024 |
| "neuf trois six tiret un un" | neuf trois six tiret un un | 936-11 |
| "moins douze" | moins douze | -12 |

Use the number words the speaker actually says. Do not convert a digit-by-digit reading into a full cardinal number, or a full cardinal number into a digit-by-digit reading.

#### 4. French Number Readings and Agreement

French number words may vary by region, register, gender, and grammatical role. Transcribe the form spoken and use standard spelling for that form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "soixante-dix" | soixante-dix | septante, unless spoken |
| "quatre-vingts" as a standalone count | quatre-vingts | 80 |
| "quatre-vingt-un" | quatre-vingt-un | 81 |
| "une minute" | une minute | un minute |
| "vingt et un euros" | vingt et un euros | 21 euros |
| "cent quatre-vingts euros" | cent quatre-vingts euros | 180 euros |
| "cent quatre-vingt-deux euros" | cent quatre-vingt-deux euros | 182 euros |

For France French, `soixante-dix`, `quatre-vingts`, and `quatre-vingt-dix` are normal. Preserve `septante`, `huitante`, `octante`, or `nonante` only if the speaker actually uses them.

#### 5. Non-Numeral Usage

Do not convert number words to Arabic numerals when they are part of natural language and not intended to communicate a specific numeric value.

This includes idioms, determiner-like uses, conventional expressions, proper nouns, and compounds.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "tu es la seule pour moi" | tu es la seule pour moi | tu es la 1 seule pour moi |
| "un de ces jours" | un de ces jours | 1 de ces jours |
| "les quatre vérités" | les quatre vérités | les 4 vérités |
| "les Trois Mousquetaires" | les Trois Mousquetaires | les 3 Mousquetaires |
| "le onze de France" | le onze de France | le 11 de France |
| "un deux-pièces" | un deux-pièces | un 2-pièces |

When a disfluency occurs before a non-numeral expression, keep the disfluent portion as spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "u- un instant" | u- un instant | u- 1 instant |
| "qu- quatre vérités" | qu- quatre vérités | qu- 4 vérités |

#### 6. Ordinals, Counters, Decades, and Age Ranges

Spell out ordinals, rank expressions, decades, and age ranges as spoken French words, preserving agreement when audible.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "premier" | premier | 1er |
| "première" | première | 1re |
| "deuxième" | deuxième | 2e |
| "vingt et unième" | vingt et unième | 21e |
| "les années quatre-vingt" | les années quatre-vingt | les années 80 |
| "dans les années deux mille" | dans les années deux mille | dans les années 2000 |
| "il a la trentaine" | il a la trentaine | il a 30 ans environ |
| "une femme d'une vingtaine d'années" | une femme d'une vingtaine d'années | une femme de 20 ans environ |

Use the official spelling for titles, laws, chapters, and product names when clearly intended, but still write spoken numbers as words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "chapitre trois" | chapitre trois | chapitre 3 |
| "la Troisième République" | la Troisième République | la 3e République |
| "Windows onze" | Windows onze | Windows 11 |
| "Galaxy S vingt-quatre" | Galaxy S vingt-quatre | Galaxy S24 |

#### 7. Dates

Write dates as spoken French words. Do not convert day, month, or year into digit notation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "le vingt-neuf avril deux mille vingt-quatre" | le vingt-neuf avril deux mille vingt-quatre | 29 avril 2024 |
| "le premier mai" | le premier mai | 1er mai |
| "le trois octobre mille neuf cent quatre-vingt-dix" | le trois octobre mille neuf cent quatre-vingt-dix | 03/10/1990 |
| "deux mille vingt-quatre" as a year | deux mille vingt-quatre | 2024 |
| "le onze septembre" | le onze septembre | le 11 septembre |

If the speaker reads a date digit by digit, preserve that digit-by-digit spoken form.

#### 8. Time of Day

Write clock times as spoken French words. French commonly uses both twelve-hour and twenty-four-hour readings; preserve what the speaker says and do not add context that was not spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "huit heures trente" | huit heures trente | 8 h 30 / 8:30 |
| "huit heures et demie" | huit heures et demie | 8 h 30 |
| "deux heures moins le quart" | deux heures moins le quart | 1 h 45 / 2 h moins le quart |
| "quatorze heures trente" | quatorze heures trente | 14 h 30 |
| "midi" | midi | 12:00 |
| "minuit" | minuit | 0:00 |
| "huit heures du matin" | huit heures du matin | 8 AM |
| "huit heures du soir" | huit heures du soir | 20 h |
| "zéro heure quinze" | zéro heure quinze | 0 h 15 |

#### 9. Money / Currency

Spell out money and currency amounts as spoken French words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cinquante-deux euros" | cinquante-deux euros | 52 € / 52 euros |
| "mille euros" | mille euros | 1 000 € |
| "deux euros cinquante" | deux euros cinquante | 2,50 € |
| "deux euros et cinquante centimes" | deux euros et cinquante centimes | 2,50 € |
| "trente, quarante euros" | trente, quarante euros | 30 €, 40 € |
| "cinq dollars" | cinq dollars | $5 |

Do not normalize informal money words into exact currency if the amount or currency is not clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "quelques balles" | quelques balles | quelques euros |
| "ça coûte une blinde" | ça coûte une blinde | ça coûte beaucoup d'euros |

#### 10. Percentages

Spell out the number and the words `pour cent`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "zéro virgule cinq pour cent" | zéro virgule cinq pour cent | 0,5 % / 0.5% |
| "cent pour cent" | cent pour cent | 100 % |
| "vingt à trente pour cent" | vingt à trente pour cent | 20 % à 30 % |

#### 11. Measures / Units

Read the number as words and expand the unit abbreviation to its full spoken form. If the speaker reads letters or a technical shorthand, transcribe that spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cinq kilogrammes" | cinq kilogrammes | 5 kg / 5 kilogrammes |
| "cinq kilos" | cinq kilos | 5 kg |
| "quatre-vingt-dix kilomètres heure" | quatre-vingt-dix kilomètres heure | 90 km/h |
| "un mètre soixante-dix" | un mètre soixante-dix | 1 m 70 |
| "cent vingt centimètres" | cent vingt centimètres | 120 cm |
| "quatre ka" | quatre ka | 4K |
| "dix quatre-vingts p" | dix quatre-vingts p | 1080p |
| "cent watts" | cent watts | 100 W |

When a technical symbol has multiple possible readings, a `{PRO: ...}` tag is acceptable as a superset annotation.

#### 12. Fractions, Ratios, and Scores

Spell out fractions, ratios, and scores as spoken French words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "trois quarts" | trois quarts | 3/4 |
| "un et trois quarts" | un et trois quarts | 1 3/4 |
| "un demi" | un demi | 1/2 |
| "cinquante cinquante" | cinquante cinquante | 50/50 |
| "deux à un" as a score | deux à un | 2-1 / 2 à 1 |
| "un partout" | un partout | 1-1 |

#### 13. Negative Numbers

Spell out negative numbers as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "moins douze" | moins douze | -12 / moins 12 |
| "moins dix-huit degrés" | moins dix-huit degrés | -18 °C |
| "dix-huit en dessous de zéro" | dix-huit en dessous de zéro | -18 |

Use `moins` when the speaker says `moins`. Use a phrase like `en dessous de zéro` only when the speaker says it.

#### 14. Phone Numbers, Postal Codes, IDs, and Codes

Read each digit group as spoken. Do not write formatted phone numbers, postal codes, license plates, or IDs with digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "zéro six douze trente-quatre cinquante-six soixante-dix-huit" | zéro six douze trente-quatre cinquante-six soixante-dix-huit | 06 12 34 56 78 |
| "zéro un quarante-deux vingt-quatre zéro un zéro un" | zéro un quarante-deux vingt-quatre zéro un zéro un | 01 42 24 01 01 |
| "code postal soixante-quinze zéro zéro un" | code postal soixante-quinze zéro zéro un | code postal 75001 |
| "A B cent vingt-trois C D" | A B cent vingt-trois C D | AB-123-CD |
| "dossier F R vingt-quatre zéro neuf" | dossier F R vingt-quatre zéro neuf | dossier FR2409 |

For phone numbers in France, speakers often group digits by pairs. Preserve the spoken grouping as words; do not force digit-by-digit readings unless that is what was spoken.

#### 15. Electronic Text (URLs, Emails, IPs)

Read all symbols aloud. Do not write URLs, email addresses, IP addresses, usernames, or file paths in their compact written form.

| Symbol | Spoken As |
|--------|-----------|
| @ | arobase / at, as spoken |
| . | point / dot, as spoken |
| / | slash / barre oblique, as spoken |
| : | deux-points |
| - | tiret / trait d'union, as spoken |
| _ | underscore / tiret bas, as spoken |

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "exemple point com slash tarifs" | exemple point com slash tarifs | exemple.com/tarifs |
| "service arobase gmail point com" | service arobase gmail point com | service@gmail.com |
| "jean point dupont arobase exemple point fr" | jean point dupont arobase exemple point fr | jean.dupont@exemple.fr |
| "cent quatre-vingt-douze point cent soixante-huit point zéro point un" | cent quatre-vingt-douze point cent soixante-huit point zéro point un | 192.168.0.1 |

#### 16. Roman Numerals

Use the spoken title, regnal, ordinal, or cardinal form. Do not convert the spoken form into Roman numerals in the transcription.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Star Wars épisode quatre" | Star Wars épisode quatre | Star Wars épisode IV |
| "GTA cinq" | GTA cinq | GTA V |
| "Louis quatorze" | Louis quatorze | Louis XIV |
| "Henri quatre" | Henri quatre | Henri IV |
| "la Seconde Guerre mondiale" | la Seconde Guerre mondiale | la IIe Guerre mondiale |

#### 17. Abbreviations and Initialisms

Keep spoken acronyms and initialisms in their canonical form. Do not expand them unless the speaker says the expanded form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "SNCF" said as letters | SNCF | Société nationale des chemins de fer français |
| "TGV" said as letters | TGV | train à grande vitesse |
| "RER" said as letters | RER | réseau express régional |
| "FBI" said as letters | FBI | bureau fédéral d'enquête |
| "ONU" pronounced as a word | ONU | Organisation des Nations unies |
| "Organisation des Nations unies" | Organisation des Nations unies | ONU |

When pronunciation is ambiguous or important, `{PRO: ...}` is an acceptable superset annotation.

#### 18. Foreign Words and Loanwords

Loanwords and foreign words do not have a strict boundary, and some cases are gray areas. As a general rule, if a word is commonly used in everyday French and has a conventional French spelling, treat it as a French word or loanword, not as foreign speech.

Do not mark established French loanwords as foreign words. Use the conventional French spelling unless the speaker is clearly giving an official foreign spelling, URL, username, code, or other written form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "week-end" | week-end | <foreign> weekend </foreign> |
| "parking" | parking | <foreign> parking </foreign> |
| "sandwich" | sandwich | <foreign> sandwich </foreign> |
| "email" | email | <foreign> email </foreign> |
| "business" | business | <foreign> business </foreign> |
| "OK" as an established interjection | OK | <foreign> okay </foreign> |

Use the actual foreign spelling only when the speaker is clearly saying a foreign-language word or phrase as foreign speech, rather than using a French loanword. If your pipeline supports foreign-language tags, they may be added as a superset annotation.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "thank you" clearly in English | thank you | <foreign lang="EN"> thank you </foreign> |
| "gracias" clearly in Spanish | gracias | <foreign lang="ES"> gracias </foreign> |
| "buongiorno" clearly in Italian | buongiorno | <foreign lang="IT"> buongiorno </foreign> |

If a word could be either a French loanword or foreign speech, choose based on how it is used and pronounced in context.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| French loanword pronunciation | j'ai mangé un sandwich | j'ai mangé un <foreign> sandwich </foreign> |
| English phrase pronunciation | sandwich, please | sandwich, s'il vous plaît if the English phrase was spoken |
| Official product or brand spelling is intended | iPhone quinze | i phone quinze, if `iPhone` is clearly intended |
| Ordinary Frenchized product reference | un iPhone | un aïe phone |

Proper nouns are not foreign-language spans just because they come from another language.

#### 19. Ambiguity

Rely on audio context to resolve ambiguous tokens.

| Context | Audio | Correct |
|---------|-------|---------|
| Conjunction | "et" | et |
| Verb | "est" | est |
| Location | "là" | là |
| Article | "la" | la |
| Possession | "son" | son |
| Verb form | "sont" | sont |

French has many homophones where the same pronunciation maps to different spellings depending on meaning. Use the surrounding meaning and syntax to choose the standard written form.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Place | "il est là" | il est là | il est la |
| Article | "la porte" | la porte | là porte |
| Plural possessive | "leurs amis" | leurs amis | leur amis |
| Singular possessive | "leur ami" | leur ami | leurs ami |
| Verb | "ils sont venus" | ils sont venus | ils son venus |
| Possessive | "son livre" | son livre | sont livre |

Use standard spelling for words that sound reduced in casual speech. Do not write purely phonetic spellings when the intended standard word is clear.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Common phrase | "je ne sais pas" casually pronounced fast | je ne sais pas | chais pas, unless that colloquial form is intentionally preserved |
| Subject and verb | "je suis là" casually pronounced fast | je suis là | chuis là, unless the colloquial form is intentionally preserved |
| Negative particle omitted by speaker | "je sais pas" with no audible `ne` | je sais pas | je ne sais pas |
| Informal pronoun | "tu as vu" casually pronounced "t'as vu" | tu as vu | t'as vu, unless the contraction is intentionally preserved |

If multiple written forms are acceptable after context is considered, choose the form that best preserves the speaker's intended meaning and is most natural in French.

#### 20. Guidelines for Language-specific Issues

The following French-specific issues should follow the same principles above: preserve what was spoken, use standard French spelling when the intended word is clear, and do not invent unsupported written forms.

**Silent letters, liaison, and elision:** French pronunciation often includes silent final letters, liaison consonants, and elisions. Write the standard spelling, not a surface phonetic spelling, when the intended words are clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "les amis" with liaison | les amis | les z'amis |
| "grand homme" with liaison | grand homme | grand t'homme |
| "vous avez" | vous avez | vous z'avez |
| "j'arrive" | j'arrive | je arrive |

**Negation in spoken French:** Preserve omitted words when they are truly omitted. Do not add `ne` if the speaker did not say it, but do not remove it if it was spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "je ne veux pas" | je ne veux pas | je veux pas |
| "je veux pas" | je veux pas | je ne veux pas |
| "j'ai rien compris" | j'ai rien compris | je n'ai rien compris |
| "je n'ai rien compris" | je n'ai rien compris | j'ai rien compris |

**Gender, agreement, and homophonous endings:** Choose spelling from grammar and context, but do not rewrite the speaker's grammar if it is non-standard.

| Context | Correct | Incorrect |
|---------|---------|-----------|
| Feminine adjective | elle est prête | elle est prêt |
| Masculine adjective | il est prêt | il est prête |
| Plural noun phrase | les petites maisons | les petite maison |
| Non-standard spoken agreement | elle est prêt | elle est prête, if the speaker clearly used the non-standard form |

**Apostrophes and clitics:** Use standard apostrophe spelling for clear clitic forms, and keep colloquial contractions only when they are the intended spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "l'histoire" | l'histoire | la histoire |
| "qu'il arrive" | qu'il arrive | que il arrive |
| "c'est bon" | c'est bon | ce est bon |
| "t'inquiète" as colloquial imperative | t'inquiète | tu inquiète |

**Onomatopoeia and lexical sound words:** French sound-symbolic words are lexical words. Transcribe them as words when spoken; do not replace them with non-speech tags.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "boum, la porte a claqué" | boum, la porte a claqué | [other-noise], la porte a claqué |
| "toc toc" | toc toc | [knock] |
| "aïe, ça fait mal" | aïe, ça fait mal | [other-noise], ça fait mal |
| "chut, écoute" | chut, écoute | [shush], écoute |

**Proper names and official spellings:** French proper names may have accents, hyphens, particles, or official brand capitalization. Use the official form when known from context; otherwise use the most natural French spelling and do not invent a foreign form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Élodie" | Élodie | Elodie, if the accent is known |
| "Jean-Pierre" | Jean-Pierre | Jean Pierre, if the hyphenated name is intended |
| "de Gaulle" | de Gaulle | De Gaulle, if the particle is lowercase in the intended name |
| "une société appelée Nova" with no official spelling given | une société appelée Nova | une société appelée NOVA, unless official capitalization is known |

---

## Part 2 - Disfluency

### Disfluency Rules

You are given an audio clip and its existing transcription. Your task is to output the transcription as provided, adding all speech disfluencies that you hear based on the rules below. Return only the transcription text.

#### 1. Filler Words

Words like "euh", "ben", "bah", "hein", "bon", "enfin", "quoi", "tu vois", "du coup", and "alors" should be added to the transcription when spoken. Keep lexical fillers as spoken, but standardize excessive elongation according to the canonical table below.

| Audio | Correct |
|-------|---------|
| "euh, je ne sais pas" | euh, je ne sais pas |
| "ben, ce n'est pas évident" | ben, ce n'est pas évident |
| "du coup, on fait comment" | du coup, on fait comment |
| "c'est compliqué, quoi" | c'est compliqué, quoi |

#### 2. Hesitation Markers and Vocal Fillers

Listen for **non-lexical vocalizations** during pauses, planning, and reactive listening. Standardize spellings to the canonical form for each group. Use normal French sentence spacing and punctuation.

**Filled pauses / hesitation** (speaker holds the floor, searching for words):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **euh** | `euh` | `euuh`, `euh...`, `euuuuh` when used as hesitation |
| **heu** | `euh` | `heu`, `heuu`, if the project uses `euh` as the canonical hesitation |
| **hum** | `hum` | `hmm`, `hmmm`, thinking hum |
| **bah** | `bah` | `baah`, `bah...` |
| **ben** | `ben` | `bennn`, `ben...` |
| **bon** | `bon` | `boon`, `bon...` when used as filler |
| **alors** | `alors` | `alooors`, filler use |
| **enfin** | `enfin` | `enfiiin`, repair or hesitation use |

**Backchannel / response** (listener signals agreement, negation, or reaction):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **oui** | `oui` | `ouii`, polite affirmative if a single acknowledgment is intended |
| **ouais** | `ouais` | `ouais ouais` only if not intentionally repeated |
| **non** | `non` | `noon`, if only lengthened |
| **hein** | `hein` | `heiiin`, confirmation or reaction |
| **ah** | `ah` | `aaah`, realization or mild reaction |
| **oh** | `oh` | `oooh`, surprise or reaction |
| **hum** | `hum` | `mh`, `mhm`, listener acknowledgment |

When the same phones could be **hesitation** vs **backchannel**, use audio and dialogue role: mid-utterance planning -> hesitation; short reactive assent while the other speaker talks -> backchannel.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Filled pause before content | euh, je vais vérifier | euuh, je vais vérifier |
| Thinking hum | hum, c'est possible | hmmm, c'est possible |
| Listener yes | oui, d'accord | ouii, d'accord |
| Informal agreement | ouais, je vois | ouais ouais, je vois if only one acknowledgment |
| Surprise | ah, vraiment ? | aaah, vraiment ? |

#### 3. Repetitions

Consecutive instances of the same word or short phrase spoken unintentionally should be kept as-is with no added punctuation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "je je je pense" | je je je pense | je- je- je pense / je pense |
| "le le problème" | le le problème | le- le problème / le problème |
| "on va on va commencer" | on va on va commencer | on va- on va commencer / on va commencer |
| "c'est vraiment c'est vraiment étrange" | c'est vraiment c'est vraiment étrange | c'est vraiment- c'est vraiment étrange / c'est vraiment étrange |

If a repetition is intentional, rhythmic, or emphatic, use normal French punctuation instead of disfluency dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "oui, oui, je comprends" | oui, oui, je comprends | oui- oui- je comprends |
| "non, non, pas du tout" | non, non, pas du tout | non- non- pas du tout |

#### 4. False Starts / Cut-Off Words

Incomplete words or phrases that the speaker abandons should be marked with a single dash followed by a space. If the speaker cuts off and stops entirely, still use a single dash.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "je vou- je voulais dire" | je vou- je voulais dire | je voulais dire |
| "on devrait par- repartir demain" | on devrait par- repartir demain | on devrait partir repartir demain |
| "c'était absolu-" | c'était absolu- | c'était absolument |

#### 5. Casual Forms, Slang, and Dialect

Use casual forms if that is how they were spoken and the form is clearly audible. If unsure, default to the standard dictionary spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ouais" | ouais | oui |
| "boulot" | boulot | travail |
| "franchement, c'est relou" | franchement, c'est relou | franchement, c'est ennuyeux |
| "j'ai kiffé" | j'ai kiffé | j'ai aimé |
| "c'est chelou" | c'est chelou | c'est louche |

Normalize pure phonetic reductions when the intended word is clear and the difference is only casual pronunciation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "j'suis fatigué" as ordinary fast speech | je suis fatigué | j'suis fatigué |
| "t'as compris" as ordinary fast speech | tu as compris | t'as compris, unless the contraction is intentionally preserved |
| "chais pas" as casual reduction with no audible `ne` | je sais pas | chais pas, unless the colloquial form is intentionally preserved |

Do not rewrite dialectal or colloquial grammar into formal standard French if the form is a real spoken form and not merely a dropped sound.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "je sais pas" with no audible `ne` | je sais pas | je ne sais pas |
| "y a personne" | y a personne | il n'y a personne |
| "c'est pas grave" | c'est pas grave | ce n'est pas grave |

#### 6. Spelled-Out Words

If a speaker spells out a non-acronym word one letter at a time using Latin letters, use capital letters separated with dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "le code est M A S E G O" | le code est M-A-S-E-G-O | le code est M A S E G O |

If a speaker spells out French letters with accents, transcribe the letter names or explicit accent descriptions as spoken. Do not infer the full word unless the speaker clearly provides it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "e accent aigu l o d i e" | e accent aigu l o d i e | Élodie, unless the intended word is explicitly stated |
| "c cédille a" | c cédille a | ça, unless the intended word is explicitly stated |

If the speaker is saying an acronym or initialism, use the canonical acronym form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "SNCF" said as letters | SNCF | S-N-C-F |
| "TGV" said as letters | TGV | T-G-V |
| "RER" said as letters | RER | R-E-R |

#### 7. Mispronunciations

Transcribe intelligible real-word substitutions as spoken. Do not correct the word in the base transcript and do not add a tag unless your project uses superset `{MIS: ...}` annotations.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "verre" where "vert" was intended by context | verre | vert |
| "pause" where "pose" was intended by context | pause | pose |
| "bibliotèque" | bibliotèque | bibliothèque, unless using superset `bibliothèque {MIS: bibliotèque}` |

If the sound is intelligible but not a real word and the intended word is unclear, transcribe the sound phonetically in French orthography as best as possible.

| Audio | Correct |
|-------|---------|
| "blorfadou" | blorfadou |

#### 8. Wrong Grammar

Grammatical errors, dialectal grammar, and non-standard morphology should be faithfully captured. Do not correct them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "les gens ils savent pas" | les gens ils savent pas | les gens ne savent pas |
| "elle est prêt" | elle est prêt | elle est prête |
| "j'ai été au médecin" | j'ai été au médecin | je suis allé chez le médecin |
| "nous on va partir" | nous on va partir | nous allons partir |

---

## Part 3 - Rich Transcription: Paralinguistic Tokens

### Non-Speech Sound Tokens

Bracket tokens mark **audible non-lexical or non-linguistic events** that are **not** regular words. Write each tag **exactly** as listed (square brackets included). Prefer **one tag per distinct event**; if several happen in sequence, repeat tags in **time order**, separated by spaces.

Use the NeMo canonical English tag names below, even in French transcripts.

#### Rules for this section

1. **Tag vs words** - If the speaker says a word, transcribe the word. Use a bracket tag only for the sound event itself.
2. **No invented words** - Do not replace a tag with a phonetic guess unless the sound is a lexical filler covered in Part 2.
3. **Placement** - Put the tag where the sound occurs in the word stream, usually as its own token between words.
4. **Overlap** - If a sound overlaps speech, place the tag at the start of the overlap window unless your time-aligned format specifies otherwise.
5. **Sequences** - Use `[laugh] [laugh]` for two separate laugh bursts, not a single stretched token.
6. **Unknown / generic background** - Use `[other-noise]` for audible non-speech you cannot classify; use `[unintelligible]` only when linguistic content was likely present but cannot be recovered.
7. **Minor mouth sounds** - Do not tag faint natural mouth clicks, lip noise, or routine breathing unless they are prominent or communicative.

#### Token list and descriptions

Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into French or replace them with local-language labels.

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
| Speaker laughs before speaking | [laugh] c'est drôle. | [rire] c'est drôle. |
| Speaker coughs mid-sentence | ce n'est [cough] pas grave. | ce n'est toux pas grave. |
| Speech is masked and unrecoverable | je crois que [unintelligible] demain. | je crois que demain. |
| Background object noise | [other-noise] vous pouvez répéter ? | [bruit] vous pouvez répéter ? |

#### Quick reference (canonical spellings)

- `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`, `[sniff]`, `[gasp]`, `[blow]`
- `[laugh]`, `[chuckle]`, `[giggle]`, `[snort]`, `[scoff]`, `[grunt]`, `[groan]`, `[cry]`
- `[hum-tune]`, `[whoop]`, `[whistle]`, `[tongue-click]`, `[tsk]`, `[lip-smack]`, `[teeth-suck]`, `[lip-trill]`, `[shush]`, `[swallow]`, `[clear-throat]`
- `[cough]`, `[sneeze]`, `[yawn]`, `[hiccup]`, `[unintelligible]`, `[other-noise]`
