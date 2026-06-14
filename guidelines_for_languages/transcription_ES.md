# Spanish Transcription Guidelines

Language: Spanish (Spain, United States, Latin America, Central America)

## Part 1 - Text normalization

### Superset principle

The transcription rules below define the **minimum required coverage**. Annotation vendors are expected to deliver transcriptions that are a **superset** of these rules - any additional detail, markup, or tagging beyond what is specified here is encouraged and acceptable, as long as it does not contradict the rules.

Examples of acceptable superset additions include (but are not limited to):

- **Pronunciation variants** for acronyms or proper nouns annotated inline:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "SQL" said as "ese cu ele" | SQL {PRO: ese cu ele} |
| "SQL" said as "sequel" | SQL {PRO: sequel} |

- **Mispronunciation tags** to flag non-standard renderings:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "murciélago" intended but pronounced "murciégalo" | murciélago {MIS: murciégalo} |

- **Additional hesitation markers, dialect notes, confidence flags, or emotion tags** are acceptable as long as they do not alter the base transcription text.

In short: **do not remove detail that is present in the audio**. The rules below set the floor, not the ceiling.

---

### Text Normalization Rules

Transcribe the audio in standard Spanish orthography. Convert numeric, symbolic, and abbreviated tokens to their fully spoken Spanish form using the rules below. Return transcription only.

#### 1. Broad Principles

With the exception of acronyms, initialisms, and established proper-name spellings, everything should be written out in full spoken words. Abbreviations, symbols, shorthand, and numerals should all be expanded.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "señor Gómez" | señor Gómez | Sr. Gómez |
| "kilogramos" | kilogramos | kg |
| "y" | y | & |
| "avenida de América" | avenida de América | Av. de América |
| "iPhone quince" | iPhone quince | iPhone 15 |

Use standard spelling, accents, capitalization, and punctuation. Do not over-normalize into a form that changes spoken content.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cómo estás" | ¿Cómo estás? | como estas |
| "qué pasó" as a question | ¿Qué pasó? | que paso? |
| "Ciudad de México" | Ciudad de México | ciudad de mexico |
| "Estados Unidos" | Estados Unidos | estados unidos |

#### 2. Spanish Orthography, Accents, and Punctuation

Use standard Spanish spelling and punctuation:

- Write Spanish in the Latin alphabet with standard Spanish letters, including `ñ`.
- Use accents where they are part of standard spelling or disambiguate meaning.
- Capitalize proper nouns, official names, brands, acronyms, and sentence starts according to Spanish norms.
- Use inverted question and exclamation marks in fully standard Spanish punctuation.
- Do not imitate predictable casual pronunciation when the intended standard word is clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "mañana nos vemos" | mañana nos vemos | manana nos vemos |
| "año nuevo" | año nuevo | ano nuevo |
| "México" | México | mexico |
| "¿Qué quieres?" | ¿Qué quieres? | Ke quieres? |
| "¿por qué no viniste?" | ¿Por qué no viniste? | xq no viniste? |

Preserve regional vocabulary, colloquial words, and dialectal grammar when they are real spoken forms and not merely spelling errors.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "vos tenés razón" | vos tenés razón | tú tienes razón |
| "ustedes van mañana" | ustedes van mañana | vosotros vais mañana |
| "vosotros vais mañana" | vosotros vais mañana | ustedes van mañana |
| "chamba" | chamba | trabajo, unless that was spoken |
| "guagua" meaning bus | guagua | autobús |

#### 3. Numbers

Spell out all digits and numeric expressions as spoken Spanish words. Preserve the speaker's actual reading where Spanish has more than one natural wording.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "catorce" | catorce | 14 |
| "veintiuno" | veintiuno | 21 |
| "veinte y uno" | veinte y uno | 21 / veintiuno |
| "cero coma cero cinco" | cero coma cero cinco | 0.05 |
| "cero punto cero cinco" | cero punto cero cinco | 0.05 |
| "mil treinta coma cinco" | mil treinta coma cinco | 1,030.5 |
| "dos mil veinticuatro" | dos mil veinticuatro | 2024 |
| "nueve tres seis guion once" | nueve tres seis guion once | 936-11 |
| "menos doce" | menos doce | -12 |

#### 4. Gender, Agreement, and Regional Number Readings

Spanish numbers may change form by gender, noun agreement, regional preference, and context. Transcribe the form that was spoken; do not silently change it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "veintiún libros" | veintiún libros | veintiuno libros / 21 libros |
| "veintiuna casas" | veintiuna casas | veintiún casas / 21 casas |
| "doscientas personas" | doscientas personas | doscientos personas / 200 personas |
| "un millón de pesos" | un millón de pesos | uno millón de pesos / 1 millón de pesos |
| "la una" for clock time | la una | el uno / 1:00 |

Preserve the speaker's regional decimal and thousands terms.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "tres coma catorce" | tres coma catorce | 3,14 / tres punto catorce |
| "tres punto catorce" | tres punto catorce | 3.14 / tres coma catorce |
| "mil doscientos" | mil doscientos | 1.200 / 1,200 |

#### 5. Non-Numeral Usage

Do not convert number words to Arabic numerals when they are part of natural language and not intended to communicate a specific numeric value.

This includes idioms, determiner-like uses, conventional expressions, proper nouns, and many compounds.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "te lo dije mil veces" | te lo dije mil veces | te lo dije 1000 veces |
| "un montón" | un montón | 1 montón |
| "de primera" | de primera | de 1.ª |
| "una vez más" | una vez más | 1 vez más |
| "Los Tres" as a band name | Los Tres | Los 3 |
| "Fórmula Uno" as a spoken title | Fórmula Uno | Fórmula 1 |

When a disfluency occurs before a non-numeral expression, keep the disfluent portion as spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "u, un montón" | u- un montón | u- 1 montón |
| "mi, mil veces" | mi- mil veces | mi- 1000 veces |

#### 6. Ordinals, Decades, and Age Ranges

Spell out ordinal expressions, decades, and age ranges as spoken. Preserve gender and number agreement.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "primero" | primero | 1o |
| "primera vez" | primera vez | 1a vez |
| "segundo piso" | segundo piso | 2o piso |
| "décimo capítulo" | décimo capítulo | capítulo X / 10.º capítulo |
| "los años setenta" | los años setenta | los años 70 |
| "personas de veinte a treinta años" | personas de veinte a treinta años | personas de 20 a 30 años |
| "treintañeros" | treintañeros | gente de 30 |

Use the spoken form for official titles, laws, chapters, and product names unless a canonical written brand form is clearly intended.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Segunda Guerra Mundial" | Segunda Guerra Mundial | 2a Guerra Mundial |
| "Windows once" | Windows once | Windows 11 |
| "Galaxy S veinticuatro" | Galaxy S veinticuatro | Galaxy S24 |

#### 7. Dates

Write dates as spoken Spanish words. Do not convert day, month, or year into digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "veintinueve de abril de dos mil veinticuatro" | veintinueve de abril de dos mil veinticuatro | 29 de abril de 2024 |
| "primero de mayo" | primero de mayo | 1 de mayo |
| "uno de mayo" | uno de mayo | 1 de mayo |
| "doce de diciembre de mil novecientos noventa y siete" | doce de diciembre de mil novecientos noventa y siete | 12 de diciembre de 1997 |
| "once de septiembre" | once de septiembre | 11-S / 9/11 |

If the speaker reads a date digit by digit, preserve that digit-by-digit spoken form.

#### 8. Time of Day

Write clock times as spoken Spanish words. Include `de la mañana`, `de la tarde`, `de la noche`, `mediodía`, or `medianoche` only if spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "dos y media de la tarde" | dos y media de la tarde | 2:30 PM |
| "las dos treinta" | las dos treinta | 2:30 |
| "la una cuarenta y cinco" | la una cuarenta y cinco | 1:45 |
| "catorce treinta" | catorce treinta | 14:30 |
| "mediodía" | mediodía | 12:00 |
| "medianoche" | medianoche | 0:00 |
| "de ocho a cinco" | de ocho a cinco | de 8 a 5 |
| "cero horas quince" | cero horas quince | 0:15 |

#### 9. Money / Currency

Spell out money and currency amounts as spoken Spanish words. Preserve the currency name the speaker used.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cincuenta y dos pesos" | cincuenta y dos pesos | 52 pesos |
| "mil euros" | mil euros | 1.000 euros / 1,000 euros |
| "dos dólares con cincuenta centavos" | dos dólares con cincuenta centavos | $2.50 |
| "treinta o cuarenta pesos" | treinta o cuarenta pesos | 30 o 40 pesos |
| "tres cuarenta" as a price | tres cuarenta | 3.40 |
| "un palo" as informal money | un palo | un millón, unless that was spoken |

Do not normalize informal money words into exact currency if the amount or currency is not clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "unos cuantos pesos" | unos cuantos pesos | varios pesos exactos |
| "ni un centavo" | ni un centavo | ni 1 centavo |

#### 10. Percentages

Spell out the number and the word `por ciento`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cero coma cinco por ciento" | cero coma cinco por ciento | 0.5% |
| "cero punto cinco por ciento" | cero punto cinco por ciento | 0.5% |
| "cien por ciento" | cien por ciento | 100% |
| "del veinte al treinta por ciento" | del veinte al treinta por ciento | del 20% al 30% |

#### 11. Measures / Units

Read the number as words and expand the unit abbreviation to its full spoken form. Preserve common spoken unit shortcuts when the speaker says them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cinco kilogramos" | cinco kilogramos | 5 kg / 5 kilogramos |
| "cinco kilos" | cinco kilos | 5 kg |
| "noventa kilómetros por hora" | noventa kilómetros por hora | 90 km/h |
| "un metro setenta" | un metro setenta | 1.70 m / 1 metro 70 |
| "ocho bits" | ocho bits | 8 bits |
| "cuatro ka" | cuatro ka | 4K |
| "cien vatios" | cien vatios | 100 W |
| "treinta grados Celsius" | treinta grados Celsius | 30 °C |

#### 12. Fractions, Ratios, and Scores

Spell out fractions, ratios, and scores as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "tres cuartos" | tres cuartos | 3/4 |
| "un cuarto" | un cuarto | 1/4 |
| "uno y tres cuartos" | uno y tres cuartos | 1 3/4 |
| "cincuenta cincuenta" | cincuenta cincuenta | 50:50 |
| "dos a uno" as a score | dos a uno | 2-1 / 2:1 |
| "tres contra dos" | tres contra dos | 3 contra 2 |

#### 13. Negative Numbers

Spell out negative numbers as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "menos doce" | menos doce | -12 / menos 12 |
| "dieciocho bajo cero" | dieciocho bajo cero | -18 grados / 18 bajo cero |
| "menos cinco grados" | menos cinco grados | -5 grados / menos 5 grados |

Use `menos` when the speaker says `menos`. Use `bajo cero` when the speaker says `bajo cero`.

#### 14. Phone Numbers, Postal Codes, IDs, and Codes

Read each digit group individually as spoken. Do not write formatted phone numbers, postal codes, or IDs with digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "seis cero cero uno dos tres cuatro cinco seis" | seis cero cero uno dos tres cuatro cinco seis | 600 123 456 |
| "cinco cinco cinco uno dos uno dos" | cinco cinco cinco uno dos uno dos | 555-1212 |
| "código postal cero ocho cero cero uno" | código postal cero ocho cero cero uno | código postal 08001 |
| "a be uno dos tres" | a be uno dos tres | AB123 |
| "número de pasaporte equis a nueve cero" | número de pasaporte equis a nueve cero | pasaporte XA90 |

#### 15. Electronic Text (URLs, Emails, IPs)

Read all symbols aloud. Do not write URLs, email addresses, IP addresses, usernames, or file paths in their compact written form.

| Symbol | Spoken As |
|--------|-----------|
| @ | arroba |
| . | punto |
| / | barra / slash, as spoken |
| : | dos puntos |
| - | guion |
| _ | guion bajo |

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "example punto com barra pricing" | example punto com barra pricing | example.com/pricing |
| "gmail punto com" | gmail punto com | gmail.com |
| "juan arroba gmail punto com" | juan arroba gmail punto com | juan@gmail.com |
| "ciento noventa y dos punto ciento sesenta y ocho punto cero punto uno" | ciento noventa y dos punto ciento sesenta y ocho punto cero punto uno | 192.168.0.1 |
| "usuario guion bajo ventas" | usuario guion bajo ventas | usuario_ventas |

#### 16. Roman Numerals

Use the spoken title, regnal, ordinal, or cardinal form. Do not write Roman numerals in `Correct` unless the speaker is explicitly spelling the written symbol.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Star Wars episodio cuatro" | Star Wars episodio cuatro | Star Wars Episode IV |
| "GTA cinco" | GTA cinco | GTA V |
| "Carlos quinto" | Carlos quinto | Carlos V |
| "siglo veintiuno" | siglo veintiuno | siglo XXI |
| "capítulo diez" | capítulo diez | capítulo X |

#### 17. Abbreviations and Initialisms

Keep spoken acronyms and initialisms in their canonical form. Do not expand them unless the speaker says the expanded form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "NASA" as the acronym | NASA | Administración Nacional de Aeronáutica y el Espacio |
| "efe be i" | FBI | Oficina Federal de Investigación |
| "ese cu ele" | SQL | Structured Query Language |
| "u ene a eme" | UNAM | Universidad Nacional Autónoma de México |
| "organización de las Naciones Unidas" | Organización de las Naciones Unidas | ONU |

When pronunciation is ambiguous or important, `{PRO: ...}` is an acceptable superset annotation.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "ovni" as the acronym | OVNI | OVNI {PRO: ovni} |
| "o ve ene i" spelled as letters | OVNI | OVNI {PRO: o ve ene i} |

#### 18. Foreign Words and Loanwords

Loanwords and foreign words do not have a strict boundary, and some cases are gray areas. As a general rule, if a word is commonly used in everyday Spanish, treat it as a Spanish loanword or borrowed everyday word, not as a foreign-language span. Write established Spanish forms in standard Spanish orthography.

Do not mark established Spanish loanwords as foreign words. Use the standard Spanish spelling unless the speaker is clearly giving an official foreign spelling, URL, username, code, or other written form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "fútbol" | fútbol | <foreign> football </foreign> |
| "líder" | líder | <foreign> leader </foreign> |
| "marketing" as an everyday Spanish loanword | marketing | <foreign> marketing </foreign> |
| "internet" | internet | <foreign> internet </foreign> |
| "whisky" | whisky | <foreign> whiskey </foreign> |
| "sándwich" | sándwich | <foreign> sandwich </foreign> |
| "okey" | okey | <foreign> okay </foreign> |

Use the actual foreign spelling only when the speaker is clearly saying a foreign-language word or phrase as foreign speech, rather than using a Spanish loanword. If your pipeline supports foreign-language tags, they may be added as a superset annotation.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "Thank you" clearly in English | Thank you | <foreign lang="EN"> Thank you </foreign> |
| "Merci" clearly in French | Merci | <foreign lang="FR"> Merci </foreign> |
| "Guten Morgen" clearly in German | Guten Morgen | <foreign lang="DE"> Guten Morgen </foreign> |
| "buongiorno" clearly in Italian | buongiorno | <foreign lang="IT"> buongiorno </foreign> |

If a word could be either a Spanish loanword or foreign speech, choose based on how it is used and pronounced in context.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Spanish loanword pronunciation | comí un sándwich | comí un <foreign> sandwich </foreign> |
| English phrase pronunciation | sandwich, please | sandwich plis |
| Official product or brand spelling is intended | compré un iPhone | compré un aifon, if `iPhone` is clearly intended |
| Ordinary Spanishized product reference | compré un celular | compré un smartphone, if that was not spoken |

Proper nouns are not foreign-language spans just because they come from another language.

#### 19. Ambiguity

Rely on audio context to resolve ambiguous tokens.

| Context | Audio | Correct |
|---------|-------|---------|
| Clock time | "la una" | la una |
| Quantity | "una persona" | una persona |
| Natural expression | "mil gracias" | mil gracias |
| Proper noun | "Los Tres" | Los Tres |
| Acronym | "ese cu ele" | SQL |

Spanish has homophones where the same pronunciation can map to different spellings depending on meaning. When pronunciation alone is ambiguous, use the surrounding meaning and context to choose the standard Spanish written form.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Verb "to have" | "yo he comido" | yo he comido | yo e comido |
| Conjunction | "padre e hijo" | padre e hijo | padre he hijo |
| Preposition | "voy a casa" | voy a casa | voy ha casa |
| Verb form | "ha llegado" | ha llegado | a llegado |
| Existence | "hay pan" | hay pan | ay pan |
| Exclamation | "ay, me duele" | ay, me duele | hay, me duele |
| Verb "to go" | "voy a ir" | voy a ir | voy a hir |
| To see | "a ver qué pasa" | a ver qué pasa | haber qué pasa |
| To have | "tiene que haber" | tiene que haber | tiene que a ver |

Use standard spelling for words that sound similar in casual speech. Do not write purely phonetic spellings when the intended standard word is clear.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| "para" reduced casually | "pa la casa" | pa la casa, if `pa` is the intended colloquial form | para la casa, if `pa` was intentionally spoken |
| "pues" reduced casually | "pos no sé" | pos no sé, if `pos` is the intended colloquial form | pues no sé, if `pos` was intentionally spoken |
| Standard word intended | "verdad" pronounced casually | verdad | verda |
| Standard word intended | "usted" pronounced casually | usted | uste |

If multiple written forms are acceptable after context is considered, choose the form that best preserves the speaker's intended meaning and is most natural in Spanish.

#### 20. Guidelines for Language-specific Issues

The following Spanish-specific issues should follow the same principles above: preserve what was spoken, use standard Spanish spelling when the intended word is clear, and do not invent unsupported written forms.

**Accent marks and meaning:** Accents can distinguish otherwise identical forms. Use context to choose the correct standard spelling.

| Context | Correct | Incorrect |
|---------|---------|-----------|
| Question | ¿Qué quieres? | que quieres? |
| Relative clause | el libro que quiero | el libro qué quiero |
| Pronoun | él vino conmigo | el vino conmigo |
| Article | el vino está frío | él vino está frío |
| Affirmation | sí, voy | si, voy |
| Conditional | si voy, te aviso | sí voy, te aviso |

**Regional second-person pronouns and verb forms:** Preserve `tú`, `vos`, `usted`, `ustedes`, and `vosotros` as spoken. Do not convert one regional system into another.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "vos sabés" | vos sabés | tú sabes |
| "tú sabes" | tú sabes | vos sabés |
| "usted sabe" | usted sabe | tú sabes |
| "ustedes saben" | ustedes saben | vosotros sabéis |
| "vosotros sabéis" | vosotros sabéis | ustedes saben |

**Seseo, ceceo, yeísmo, and regional pronunciation:** Regional pronunciations often merge sounds such as `s`, `c`, `z`, `ll`, and `y`. Write the standard word intended by context, not a phonetic spelling.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Hunting | "caza" pronounced like "casa" in seseo | caza | casa |
| House | "casa" | casa | caza |
| Callo | "callo" and "cayo" may sound alike | callo | cayo, if the noun is intended |
| Verb "fell" | "cayó" and "calló" may sound alike | cayó | calló, if the verb is intended |
| Chicken | "pollo" | pollo | poyo |

**Clitics, contractions, and spacing:** Write clitic pronouns and contractions according to standard Spanish spelling when the intended form is clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "dímelo" | dímelo | di me lo |
| "se lo dije" | se lo dije | selo dije |
| "al cine" | al cine | a el cine |
| "del norte" | del norte | de el norte |
| "dárselo" | dárselo | dar se lo |

**Nonstandard contractions, slang, and messaging shorthand:** Preserve real spoken colloquial forms, but do not use text-message shorthand unless the speaker is literally reading it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "pa que veas" | pa que veas | para que veas, if `pa` was clearly spoken |
| "ta bueno" | ta bueno | está bueno, if `ta` was clearly spoken |
| "qué onda" | qué onda | qué sucede |
| "por qué" | por qué | xq |
| "te quiero mucho" | te quiero mucho | tqm |

**Onomatopoeia and lexical sound words:** Spanish sound-symbolic words are lexical words. Transcribe them as words when spoken; do not replace them with non-speech tags.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "hizo pum" | hizo pum | hizo [other-noise] |
| "toc toc en la puerta" | toc toc en la puerta | [other-noise] en la puerta |
| "miau dijo el gato" | miau dijo el gato | [other-noise] dijo el gato |
| "ja ja qué risa" as spoken laughter words | ja ja qué risa | [laugh] qué risa |

---

## Part 2 - Disfluency

### Disfluency Rules

You are given an audio clip and its existing transcription. Your task is to output the transcription as provided, adding all speech disfluencies that you hear based on the rules below. Return only the transcription text.

#### 1. Filler Words

Words like "eh", "em", "este", "pues", "o sea", "bueno", "a ver", "digamos", "tipo", "como", and "viste" should be added to the transcription when spoken. Keep lexical fillers as spoken, but standardize excessive elongation according to the canonical table below.

| Audio | Correct |
|-------|---------|
| "eh, no estoy seguro" | eh, no estoy seguro |
| "este, vamos a empezar" | este, vamos a empezar |
| "o sea, no era eso" | o sea, no era eso |

#### 2. Hesitation Markers and Vocal Fillers

Listen for **non-lexical vocalizations** during pauses, planning, and reactive listening. Standardize spellings to the canonical form for each group. Use normal Spanish sentence spacing and punctuation.

**Filled pauses / hesitation** (speaker holds the floor, searching for words):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **eh** | `eh` | `eeh`, `eh...`, `eeeh` when used as hesitation |
| **em** | `em` | `emm`, `em...`, `mmm` when used as hesitation |
| **mmm** | `mmm` | thinking hum when lexical content is absent |
| **este** | `este` | `esteee` when used as filler |
| **pues** | `pues` | `pueees`, `ps`, if the project normalizes to standard form |
| **o sea** | `o sea` | `osea`, `o seaa` |
| **bueno** | `bueno` | `buenooo` |

**Backchannel / response** (listener signals agreement, negation, or reaction):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **sí** | `sí` | `sii`, `si si` when a single acknowledgment is intended |
| **no** | `no` | `noo`, when one response is intended |
| **ajá** | `ajá` | `ajaa`, affirmative response |
| **uh-huh** | `uh-huh` | Spanish or bilingual backchannel as spoken |
| **claro** | `claro` | `clarooo` |
| **vale** | `vale` | `valeee` |
| **ya** | `ya` | `yaa` |
| **ay** | `ay` | pain, surprise, or reaction word |

When the same phones could be **hesitation** vs **backchannel**, use audio and dialogue role: mid-utterance planning -> hesitation; short reactive assent while the other speaker talks -> backchannel.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Filled pause before content | eh, mañana voy | eeh, mañana voy |
| Thinking hum | mmm, no sé | mmmm, no sé |
| Listener yes | sí, claro | sii, claro if only one acknowledgment |
| Agreement in Spain | vale, perfecto | valeee, perfecto |
| Surprise | ay, ¿de verdad? | ayyy, ¿de verdad? |

#### 3. Repetitions

Consecutive instances of the same word or short phrase spoken unintentionally should be kept as-is with no added punctuation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "yo yo yo quería" | yo yo yo quería | yo- yo- yo quería / yo quería |
| "la la casa" | la la casa | la- la casa / la casa |
| "quiero ir quiero ir quiero ir mañana" | quiero ir quiero ir quiero ir mañana | quiero ir- quiero ir- quiero ir mañana / quiero ir mañana |
| "eso fue eso fue raro" | eso fue eso fue raro | eso fue- eso fue raro / eso fue raro |

If a repetition is intentional, rhythmic, or emphatic, use normal Spanish punctuation instead of disfluency dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "sí, sí, vamos" | sí, sí, vamos | sí- sí- vamos |
| "no, no, no" | no, no, no | no- no- no |

#### 4. False Starts / Cut-Off Words

Incomplete words or phrases that the speaker abandons should be marked with a single dash followed by a space. If the speaker cuts off and stops entirely, still use a single dash.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "helad- yogur congelado" | helad- yogur congelado | helado yogur congelado |
| "yo iba a sal- ¿dónde estábamos?" | yo iba a sal- ¿dónde estábamos? | yo iba a salir, ¿dónde estábamos? |
| "quería comprar un teléfon-" | quería comprar un teléfon- | quería comprar un teléfono |

#### 5. Casual Forms, Slang, and Dialect

Use casual forms if that is how they were spoken and the form is clearly audible. If unsure, default to the standard dictionary spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "qué onda" | qué onda | qué sucede |
| "chido" | chido | bueno |
| "guay" | guay | genial, unless that was spoken |
| "chévere" | chévere | bueno |
| "dale" | dale | de acuerdo, unless that was spoken |

Normalize pure phonetic reductions when the intended word is clear and the difference is only casual pronunciation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "verda" meaning "verdad" | verdad | verda |
| "uste" meaning "usted" | usted | uste |
| "pa" as a real colloquial form | pa | para, if `pa` was clearly spoken |

Do not rewrite dialectal or colloquial grammar into another regional standard if the form is a real spoken form and not merely a dropped sound.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "vos tenés razón" | vos tenés razón | tú tienes razón |
| "vosotros vais" | vosotros vais | ustedes van |
| "ustedes van" | ustedes van | vosotros vais |

#### 6. Spelled-Out Words

If a speaker spells out a non-acronym word one letter at a time using Latin letters, use capital letters separated with dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "se escribe M A S E G O" | se escribe M-A-S-E-G-O | se escribe M A S E G O |

If a speaker spells out Spanish letters with letter names, transcribe the letter names or letters as spoken. Do not infer a full word unless the speaker clearly provides it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "eme a ese a" | eme a ese a | masa |
| "equis a nueve cero" | equis a nueve cero | XA90 |
| "ene con tilde" | ene con tilde | n, unless the letter name was spoken that way |

If the speaker is saying an acronym or initialism, use the canonical acronym form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "efe be i" | FBI | F-B-I |
| "u ene a eme" | UNAM | U-N-A-M |

#### 7. Mispronunciations

Transcribe intelligible real-word substitutions as spoken. Do not correct the word in the base transcript and do not add a tag unless your project uses superset `{MIS: ...}` annotations.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cocer" where "coser" was intended | cocer | coser |
| "apto" where "acto" was intended by context | apto | acto |
| "murciégalo" | murciégalo | murciélago, unless using superset `murciélago {MIS: murciégalo}` |

If the sound is intelligible but not a real word and the intended word is unclear, transcribe the sound phonetically in Spanish orthography.

| Audio | Correct |
|-------|---------|
| "trusquele" | trusquele |

#### 8. Wrong Grammar

Grammatical errors, dialectal grammar, and non-standard morphology should be faithfully captured. Do not correct them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "habían muchas personas" | habían muchas personas | había muchas personas |
| "dijistes eso" | dijistes eso | dijiste eso |
| "la problema era grande" | la problema era grande | el problema era grande |
| "yo no sabo" | yo no sabo | yo no sé |

---

## Part 3 - Rich Transcription: Paralinguistic Tokens

### Non-Speech Sound Tokens

Bracket tokens mark **audible non-lexical or non-linguistic events** that are **not** regular words. Write each tag **exactly** as listed (square brackets included). Prefer **one tag per distinct event**; if several happen in sequence, repeat tags in **time order**, separated by spaces.

Use the NeMo canonical English tag names below, even in Spanish transcripts.

#### Rules for this section

1. **Tag vs words** - If the speaker says a word, transcribe the word. Use a bracket tag only for the sound event itself.
2. **No invented words** - Do not replace a tag with a phonetic guess unless the sound is a lexical filler covered in Part 2.
3. **Placement** - Put the tag where the sound occurs in the word stream, usually as its own token between words.
4. **Overlap** - If a sound overlaps speech, place the tag at the start of the overlap window unless your time-aligned format specifies otherwise.
5. **Sequences** - Use `[laugh] [laugh]` for two separate laugh bursts, not a single stretched token.
6. **Unknown / generic background** - Use `[other-noise]` for audible non-speech you cannot classify; use `[unintelligible]` only when linguistic content was likely present but cannot be recovered.
7. **Minor mouth sounds** - Do not tag faint natural mouth clicks, lip noise, or routine breathing unless they are prominent or communicative.

#### Token list and descriptions

Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into Spanish or replace them with local-language labels.

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
| Speaker laughs before speaking | [laugh] eso fue gracioso. | [risa] eso fue gracioso. |
| Speaker coughs mid-sentence | eso no es [cough] problema. | eso no es tos problema. |
| Speech is masked and unrecoverable | creo que [unintelligible] mañana. | creo que mañana. |
| Background object noise | [other-noise] ¿puedes repetirlo? | [ruido] ¿puedes repetirlo? |

#### Quick reference (canonical spellings)

- `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`, `[sniff]`, `[gasp]`, `[blow]`
- `[laugh]`, `[chuckle]`, `[giggle]`, `[snort]`, `[scoff]`, `[grunt]`, `[groan]`, `[cry]`
- `[hum-tune]`, `[whoop]`, `[whistle]`, `[tongue-click]`, `[tsk]`, `[lip-smack]`, `[teeth-suck]`, `[lip-trill]`, `[shush]`, `[swallow]`, `[clear-throat]`
- `[cough]`, `[sneeze]`, `[yawn]`, `[hiccup]`, `[unintelligible]`, `[other-noise]`
