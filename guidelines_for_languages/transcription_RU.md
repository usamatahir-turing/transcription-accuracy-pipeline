# Russian Transcription Guidelines

Language: Russian (Russia)

## Part 1 - Text normalization

### Superset principle

The transcription rules below define the **minimum required coverage**. Annotation vendors are expected to deliver transcriptions that are a **superset** of these rules - any additional detail, markup, or tagging beyond what is specified here is encouraged and acceptable, as long as it does not contradict the rules.

Examples of acceptable superset additions include (but are not limited to):

- **Pronunciation variants** for acronyms, symbols, or proper nouns annotated inline:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "PDF" said as "пэ-дэ-эф" | PDF {PRO: пэ-дэ-эф} |
| "PDF" said as "пидиэф" | PDF {PRO: пидиэф} |

- **Mispronunciation tags** to flag non-standard renderings:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "равота" intended as "работа" | работа {MIS: равота} |

- **Additional hesitation markers, dialect notes, confidence flags, or emotion tags** are acceptable as long as they do not alter the base transcription text.

In short: **do not remove detail that is present in the audio**. The rules below set the floor, not the ceiling.

---

### Text Normalization Rules

Transcribe the audio in standard Russian orthography. Convert numeric, symbolic, and abbreviated tokens to their fully spoken Russian form using the rules below. Return transcription only.

#### 1. Broad Principles

With the exception of acronyms, initialisms, and clearly intended proper-name spellings, everything should be written out in full spoken words. Abbreviations, symbols, shorthand, and numerals should all be expanded.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "доктор Иванов" | Доктор Иванов | Др. Иванов |
| "много килограммов" | много килограммов | много кг |
| "много кэ гэ" | много кэ гэ | много кг |
| "улица Ленина" | улица Ленина | ул. Ленина |
| "и так далее" | и так далее | и т. д. |

Use standard capitalization for sentence starts and proper nouns. Do not over-normalize into a form that changes spoken content.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "москва - столица России" | Москва - столица России | москва - столица России |
| "Вторая мировая война" | Вторая мировая война | 2-я мировая война |
| "Федеральная служба безопасности" | Федеральная служба безопасности | ФСБ |

#### 2. Russian Orthography and Script Choice

Use the script and spelling that are most natural for standard written Russian:

- Use **Cyrillic** for ordinary Russian words and established Russian spellings.
- Use **Latin script** for international brand names, product names, domains, usernames, and technical strings when that is the conventional written form.
- Preserve established capitalization for brands and proper names.
- Do not imitate purely phonetic reductions when the intended standard word is clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "грю" meaning "говорю" | говорю | грю |
| "вощем" meaning "в общем" | в общем | вощем |
| "пожалста" | пожалуйста | пожалста |
| "город" pronounced with regional reduction | город | хород |
| "Айфон десять" | Айфон десять | iPhone X / iPhone 10 |

#### 3. Letter Ё

Use `ё` when it is needed to disambiguate meaning, preserve a proper name, or avoid a likely pronunciation error. In other ordinary cases, `е` is acceptable and often preferred by Russian typographic convention.

Use `ё` in:

- Words where `е` would create another word or meaning.
- Rare or potentially ambiguous words where pronunciation matters.
- Proper names, surnames, and place names where `ё` is part of the established spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "всё" | всё | все |
| "нёбо" | нёбо | небо |
| "совершённый" | совершённый | совершенный |
| "сёрфинг" | сёрфинг | серфинг |
| "Киселёв" | Киселёв | Киселев |
| "Шрёдингер" | Шрёдингер | Шредингер |

#### 4. Proper Nouns and Brand Names

Use established Russian spelling when a foreign brand or title is pronounced in Russian and has a conventional Russian form. Use quotation marks for brand/product names when that is natural in Russian prose.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Порошок persil" pronounced in Russian | Порошок "Персил" | Порошок Persil |
| "Мебель ikea" pronounced in Russian | Мебель "Икея" | Мебель IKEA |
| "Звёздные войны эпизод четыре" | Звёздные войны эпизод четыре | Звёздные войны. Эпизод IV / Звёздные войны эпизод 4 |
| "GTA пять" | GTA пять | GTA V / GTA 5 |

If the name is spoken in its original form, clearly sounds foreign, or does not have an established Russian form, use the official original spelling without Russian quotation marks.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Мы всё ведём в ноушн" | Мы всё ведём в Notion | Мы всё ведём в "Ноушн" |
| "Мы используем страйп" | Мы используем Stripe | Мы используем "Страйп" |
| "Кроссовки олбёрдс" | кроссовки Allbirds | кроссовки "Олбёрдс" |

Look up official spelling and capitalization when needed, but do not replace spoken numbers with digit forms.

#### 5. Numbers

Spell out all digits and numeric expressions as spoken Russian words. Do not write Arabic numerals for transcription text.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "четырнадцать" | четырнадцать | 14 |
| "пять сотых" | пять сотых | 0,05 / 0.05 |
| "тысяча тридцать и пять десятых" | тысяча тридцать и пять десятых | 1030,5 / 1 030,5 |
| "две тысячи двадцать четыре" | две тысячи двадцать четыре | 2024 |
| "девять три шесть тире один один" | девять три шесть тире один один | 936-11 |
| "пять джи" | пять джи | 5G |
| "минус двенадцать" | минус двенадцать | -12 |

#### 6. Non-Numeral Usage

Do not convert number words to Arabic numerals when they are part of natural language and not intended to communicate a specific numeric value.

This includes idioms, determiner-like uses, conventional expressions, proper nouns, and many compounds.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ты для меня один единственный" | ты для меня один единственный | ты для меня 1 единственный |
| "убить двух зайцев" | убить двух зайцев | убить 2 зайцев |
| "в один миг" | в один миг | в 1 миг |
| "Одиннадцать друзей Оушена" | Одиннадцать друзей Оушена | 11 друзей Оушена |
| "Великолепная семёрка" | Великолепная семёрка | Великолепная 7 |
| "двадцатиминутный" | двадцатиминутный | 20-минутный |
| "семилетний ребёнок" | семилетний ребёнок | 7-летний ребёнок |

When a disfluency occurs before a non-numeral expression, keep the disfluent portion as spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "с- с- сто пять" | с- с- сто пять | с- с- 105 |
| "о- о- один" | о- о- один | о- о- 1 |

#### 7. Ordinals, Decades, and Age Ranges

Spell out ordinals, decades, and age ranges as spoken Russian words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "пятидесятый" | пятидесятый | 50-й / 50 |
| "семидесятые" | семидесятые | 70-е |
| "двадцатые" as an age range | двадцатые | 20-е |
| "в тысяча девятьсот девяносто седьмом году" | в тысяча девятьсот девяносто седьмом году | в 1997 году / в 1997-м году |
| "словарь в четырёх томах" | словарь в четырёх томах | словарь в 4 томах / словарь в 4-х томах |

Preserve the grammatical form the speaker used; do not convert it into digit-plus-ending notation.

#### 8. Dates

Write dates as spoken Russian words. Do not convert day, month, or year into digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "двенадцатого декабря тысяча девятьсот девяносто седьмого года" | двенадцатого декабря тысяча девятьсот девяносто седьмого года | 12 декабря 1997 года |
| "двадцать девятое апреля две тысячи двадцать четвёртого года" | двадцать девятое апреля две тысячи двадцать четвёртого года | 29 апреля 2024 года |
| "первое мая" as a holiday/date | первое мая | 1 мая |
| "девятое одиннадцатое" as an event name | девятое одиннадцатое | 9/11 |

If the speaker reads a date digit by digit, preserve that digit-by-digit spoken form.

#### 9. Time of Day

Write clock times as spoken Russian words. Keep natural Russian words such as `утра`, `дня`, `вечера`, `ночи`, `полдень`, and `полночь` when spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "два тридцать дня" | два тридцать дня | 2:30 дня |
| "час сорок пять" | час сорок пять | 1:45 |
| "четырнадцать тридцать" | четырнадцать тридцать | 14:30 |
| "полдень" | полдень | 12:00 |
| "полночь" | полночь | 0:00 |
| "с восьми до пяти" | с восьми до пяти | 8:00-5:00 / с 8 до 5 |

#### 10. Money / Currency

Spell out money and currency amounts as spoken Russian words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "пятьдесят долларов" | пятьдесят долларов | $50 / 50 долларов |
| "тысяча долларов" | тысяча долларов | 1000 долларов / 1 000 долларов |
| "двадцать, сорок долларов" | двадцать, сорок долларов | 20, 40 долларов |
| "пять рублей пятьдесят копеек" | пять рублей пятьдесят копеек | 5 рублей 50 копеек / 5,50 ₽ |

Do not normalize informal money words into exact currency if the amount or currency is not clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "пять лямов" | пять лямов | 5 000 000 рублей |
| "сто баксов" | сто баксов | 100 долларов |

#### 11. Percentages

Spell out the number and the word `процент` in the form spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ноль целых пять десятых процента" | ноль целых пять десятых процента | 0,5 % / 0.5% |
| "сто процентов" | сто процентов | 100 % |
| "двадцать-тридцать процентов" | двадцать-тридцать процентов | 20-30 % |

#### 12. Measures / Units

Read the number as words and expand the unit abbreviation to its full spoken form. If the speaker reads letters or a technical shorthand, transcribe that spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "пять килограммов" | пять килограммов | 5 килограммов / 5 кг |
| "пять кэ гэ" | пять кэ гэ | 5 кг |
| "девяносто километров в час" | девяносто километров в час | 90 километров в час / 90 км/ч |
| "пять с половиной километров" | пять с половиной километров | 5,5 километра |
| "восемь бит" | восемь бит | 8-бит / 8 бит |

When a technical symbol has multiple possible readings, a `{PRO: ...}` tag is acceptable as a superset annotation.

#### 13. Fractions, Ratios, and Scores

Spell out fractions, ratios, and scores as spoken Russian words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "одна целая три четверти" | одна целая три четверти | 1 3/4 / 1-3/4 |
| "три четверти" | три четверти | 3/4 / 0,75 |
| "пятьдесят на пятьдесят" | пятьдесят на пятьдесят | 50/50 / 50 на 50 |
| "два один" as a match score | два один | 2:1 |
| "два к одному" as a score or ratio | два к одному | 2:1 / 2 к 1 |

#### 14. Negative Numbers

Spell out negative numbers as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "минус пять" | минус пять | -5 / минус 5 |
| "минус пять градусов" | минус пять градусов | -5 градусов / -5 °C |
| "десять градусов мороза" | десять градусов мороза | 10 градусов мороза / -10 °C |

Use `минус` when the speaker says `минус`. Use the phrase the speaker used when it is idiomatic rather than a formal numeric value.

#### 15. Phone Numbers, Postal Codes, IDs, and Codes

Read each digit group individually as spoken. Do not write formatted phone numbers, postal codes, or IDs with digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "плюс семь девятьсот пятнадцать..." | плюс семь девятьсот пятнадцать | +7 915 ... |
| "девять три шесть тире один один" | девять три шесть тире один один | 936-11 |
| "девяносто двести десять" as a postal code | девяносто двести десять | 90210 |
| "А Б один два три" | А Б один два три | АБ123 / AB123 |

#### 16. Electronic Text (URLs, Emails, IPs)

Read all symbols aloud. Do not write URLs, email addresses, IP addresses, usernames, or file paths in their compact written form.

Latin script may be used for English-language and international domain tokens when the speaker says them as Latin-script names, but symbols such as dots, slashes, and `@` should remain in spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "пример точка ру слэш прайс" | пример точка ру слэш прайс | пример.ру/прайс |
| "гугл точка ком" | гугл точка ком | google.com |
| "джон собака джимейл точка ком" | джон собака джимейл точка ком | john@gmail.com |
| "МВД точка рф" | МВД точка рф | МВД.рф |

If the word `точка` is not spoken, do not infer a dot. Preserve what was spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Яндекс ру" | Яндекс ру | Яндекс.ру |
| "МВД рф" | МВД рф | МВД.рф |

#### 17. Roman Numerals

Use the spoken form after title keywords and after a person's name. Do not convert spoken Roman numeral readings into Roman numerals.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Звёздные войны эпизод четыре" | Звёздные войны эпизод четыре | Звёздные войны. Эпизод IV / Звёздные войны эпизод 4 |
| "GTA пять" | GTA пять | GTA V / GTA 5 |
| "Екатерина вторая" | Екатерина Вторая | Екатерина II / Екатерина 2 |

#### 18. Abbreviations and Initialisms

Keep spoken acronyms and initialisms in their canonical form. Do not expand them unless the speaker says the expanded form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "НАСА" | НАСА | Национальное управление по аэронавтике и исследованию космического пространства |
| "Федеральная служба безопасности" | Федеральная служба безопасности | ФСБ |
| "ФСБ" | ФСБ | Федеральная служба безопасности |
| "пэ-дэ-эф" | PDF | Пэ-Дэ-Эф |
| "пидиэф" | PDF | пидиэф |

When pronunciation is ambiguous or important, `{PRO: ...}` is an acceptable superset annotation.

#### 19. Foreign Words and Loanwords

Do not mark well-established Russian loanwords as foreign words. Transcribe them in the standard Russian form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "селфи" | селфи | <foreign> selfie </foreign> |
| "окей" | окей | <foreign> okay </foreign> |
| "дедлайн" | дедлайн | <foreign> deadline </foreign> |
| "Макдоналдс" | Макдоналдс | <foreign> McDonald's </foreign> |

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
| Time | "два тридцать" | два тридцать |
| Quantity | "два" | два |
| Natural expression | "убить двух зайцев" | убить двух зайцев |
| Proper noun | "Великолепная семёрка" | Великолепная семёрка |
| Acronym | "пэ-дэ-эф" | PDF |

Russian has homophones where the same pronunciation maps to different spellings and meanings. When pronunciation alone is ambiguous, use the surrounding meaning and context to choose the standard Russian written form. Only treat words as ambiguous homophones when they sound exactly the same in standard Russian; do not use this rule for merely similar-sounding words.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Meadow | "зелёный луг" | зелёный луг | зелёный лук |
| Onion | "репчатый лук" | репчатый лук | репчатый луг |
| Young forest | "молодой лес" | молодой лес | молодой лез |
| Verb form from `лезть` | "он лез вверх" | он лез вверх | он лес вверх |
| Raft | "деревянный плот" | деревянный плот | деревянный плод |
| Fruit/result | "сладкий плод" | сладкий плод | сладкий плот |
| Threshold | "высокий порог" | высокий порог | высокий порок |
| Vice/flaw | "старый порок" | старый порок | старый порог |
| Code | "секретный код" | секретный код | секретный кот |
| Animal | "чёрный кот" | чёрный кот | чёрный код |

If multiple written forms are acceptable after context is considered, choose the form that best preserves the speaker's intended meaning and is most natural in Russian.

#### 21. Guidelines for Language-specific Issues

The following Russian-specific issues should follow the same principles above: preserve what was spoken, use standard Russian spelling when the intended word is clear, and do not invent unsupported written forms.

**Akanye (unstressed O pronounced as A):** Write the standard spelling with "o", not the phonetic pronunciation with "a".

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "молоко" pronounced "малако" | молоко | малако |

**Devoicing of final consonants:** Write the standard spelling, not the phonetic devoiced consonant.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "зуб" pronounced "зуп" | зуб | зуб, unless "зуп" is intended |

---

## Part 2 - Disfluency

### Disfluency Rules

You are given an audio clip and its existing transcription. Your task is to output the transcription as provided, adding all speech disfluencies that you hear based on the rules below. Return only the transcription text.

#### 1. Filler Words

Words like "а", "ага", "ну", "вот", "типа", "как бы", "значит", "м", "мгм", and "угу" should be added to the transcription when spoken. Keep lexical fillers as spoken, but standardize excessive elongation according to the canonical table below.

| Audio | Correct |
|-------|---------|
| "ну, я думаю, да" | ну, я думаю, да |
| "вот, это важно" | вот, это важно |
| "как бы не совсем" | как бы не совсем |

#### 2. Hesitation Markers and Vocal Fillers

Listen for **non-lexical vocalizations** during pauses, planning, and reactive listening. Standardize spellings to the canonical form for each group. Use normal Russian capitalization at sentence starts.

**Filled pauses / hesitation** (speaker holds the floor, searching for words):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **а** | `а` | `аа`, `а-а-а` when used as hesitation |
| **э** | `э` | `ээ`, `э-э`, short hesitation |
| **эм** | `эм` | `ээм`, `эмм` |
| **м** | `м` | short closed-mouth hesitation |
| **м-да** | `м-да` | `мда`, `мдя` |
| **ну** | `ну` | `нуу`, `ну-у` |
| **вот** | `вот` | `вооот` |
| **ах** | `ах` | `ахх`, `а-а-ах` |
| **у** | `у` | `уу`, `у-у` |

**Backchannel / response** (listener signals agreement, negation, or reaction):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **ага** | `ага` | `ага-а`, `агаа` |
| **угу** | `угу` | `у-г-у`, `угуу` |
| **мгм** | `мгм` | `мм-гм`, `мхм`, affirmative nasal response |
| **м-м** | `м-м` | `мм`, `м м`, negative nasal response |
| **вау** | `вау` | `уау` |
| **блин** | `блин` | `блиин`, `бли-ин` |
| **ей-богу** | `ей-богу` | `ейбогу`, `ей богу` |

When the same phones could be **hesitation** vs **backchannel**, use audio and dialogue role: mid-utterance planning -> hesitation; short reactive assent while the other speaker talks -> backchannel.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Filled pause before content | э, я не знаю | ээ, я не знаю |
| Thinking hum | м, сложно сказать | ммм, сложно сказать |
| Listener yes | угу, понятно | у-г-у, понятно |
| Listener no | м-м, не думаю | мм, не думаю |
| Elongated filler | вот, поэтому так | вооот, поэтому так |

#### 3. Repetitions

Consecutive instances of the same word or short phrase spoken unintentionally should be kept as-is with no added punctuation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Я я я" | Я я я | Я- я- я / Я |
| "ду думаю" | ду думаю | ду- думаю / думаю |
| "мы мы мы" | мы мы мы | мы- мы- мы / мы |
| "Я хочу я хочу я хочу сказать" | Я хочу я хочу я хочу сказать | Я хочу- я хочу- я хочу сказать / Я хочу сказать |
| "Это было это было очень плохо" | Это было это было очень плохо | Это было- это было очень плохо / Это было очень плохо |

If a repetition is intentional, rhythmic, or emphatic, use normal Russian punctuation instead of disfluency dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Да, да, я пойду" | Да, да, я пойду | Да- да- я пойду |
| "Ладно, ладно" | Ладно, ладно | Ладно- ладно |

#### 4. False Starts / Cut-Off Words

Incomplete words or phrases that the speaker abandons should be marked with a single dash followed by a space. If the speaker cuts off and stops entirely, still use a single dash.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Я купил мороже- пирожное" | Я купил мороже- пирожное | Я купил мороженое, пирожное |
| "Я собирался- куда я собирался?" | Я собирался- куда я собирался? | Я собирался, куда я собирался? |
| "Я купил мороже-" | Я купил мороже- | Я купил мороженое |

#### 5. Reduced Forms, Slang, and Dialect

Use reduced or slang forms only when the form is intentional, clearly audible, and accepted as a real colloquial written form. If unsure, default to the standard spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "щас" | щас | сейчас |
| "чё" | чё | что |
| "чё-то" | чё-то | что-то |
| "ваще" | ваще | вообще |
| "вишь" | вишь | видишь |

Normalize pure phonetic reductions when the intended word is clear and the difference is only dropped sounds.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "грю" | говорю | грю |
| "вощем" | в общем | вощем |
| "пожалста" | пожалуйста | пожалста |
| "хород" | город | хород |

Do not rewrite dialectal or colloquial grammar into formal standard Russian if the form is a real spoken form and not merely a dropped sound.

#### 6. Spelled-Out Words

If a speaker spells out a non-acronym word one letter at a time, use capital letters separated with dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Поищи Э Ч П О Ч М А К" | Поищи Э-Ч-П-О-Ч-М-А-К | Поищи Э Ч П О Ч М А К |

If the speaker is saying an acronym or initialism, use the canonical acronym form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Ф С Б" | ФСБ | Ф-С-Б |
| "М Г У" | МГУ | М-Г-У |
| "пэ-дэ-эф" | PDF | П-Э-Д-Э-Ф |

#### 7. Mispronunciations

Transcribe intelligible real-word substitutions as spoken. Do not correct the word in the base transcript and do not add a tag unless your project uses superset `{MIS: ...}` annotations.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "почти отравился" where "оправился" was intended | почти отравился | почти оправился |
| "до белого колена" where "каления" was intended | до белого колена | до белого каления |
| "равота" | равота | работа, unless using superset `работа {MIS: равота}` |

If the sound is intelligible but not a real word and the intended word is unclear, transcribe the sound phonetically.

| Audio | Correct |
|-------|---------|
| "крумпелятор" | крумпелятор |

#### 8. Wrong Grammar

Grammatical errors, dialectal grammar, and non-standard morphology should be faithfully captured. Do not correct them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ихний дом" | ихний дом | их дом |
| "ложи сюда" | ложи сюда | клади сюда |
| "более лучше" | более лучше | лучше |

---

## Part 3 - Rich Transcription: Paralinguistic Tokens

### Non-Speech Sound Tokens

Bracket tokens mark **audible non-lexical or non-linguistic events** that are **not** regular words. Write each tag **exactly** as listed (square brackets included). Prefer **one tag per distinct event**; if several happen in sequence, repeat tags in **time order**, separated by spaces.

Use the NeMo canonical English tag names below, even in Russian transcripts.

#### Rules for this section

1. **Tag vs words** - If the speaker says a word, transcribe the word. Use a bracket tag only for the sound event itself.
2. **No invented words** - Do not replace a tag with a phonetic guess unless the sound is a lexical filler covered in Part 2.
3. **Placement** - Put the tag where the sound occurs in the word stream, usually as its own token between words.
4. **Overlap** - If a sound overlaps speech, place the tag at the start of the overlap window unless your time-aligned format specifies otherwise.
5. **Sequences** - Use `[laugh] [laugh]` for two separate laugh bursts, not a single stretched token.
6. **Unknown / generic background** - Use `[other-noise]` for audible non-speech you cannot classify; use `[unintelligible]` only when linguistic content was likely present but cannot be recovered.
7. **Minor mouth sounds** - Do not tag faint natural mouth clicks, lip noise, or routine breathing unless they are prominent or communicative.

#### Token list and descriptions

Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into Russian or replace them with local-language labels.

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
| Speaker laughs before speaking | [laugh] Это смешно. | [смех] Это смешно. |
| Speaker coughs mid-sentence | Это [cough] не проблема. | Это кашель не проблема. |
| Speech is masked and unrecoverable | Это было [unintelligible] вчера. | Это было вчера. |
| Background object noise | [other-noise] Повторите, пожалуйста. | [шум] Повторите, пожалуйста. |

#### Quick reference (canonical spellings)

- `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`, `[sniff]`, `[gasp]`, `[blow]`
- `[laugh]`, `[chuckle]`, `[giggle]`, `[snort]`, `[scoff]`, `[grunt]`, `[groan]`, `[cry]`
- `[hum-tune]`, `[whoop]`, `[whistle]`, `[tongue-click]`, `[tsk]`, `[lip-smack]`, `[teeth-suck]`, `[lip-trill]`, `[shush]`, `[swallow]`, `[clear-throat]`
- `[cough]`, `[sneeze]`, `[yawn]`, `[hiccup]`, `[unintelligible]`, `[other-noise]`

---
