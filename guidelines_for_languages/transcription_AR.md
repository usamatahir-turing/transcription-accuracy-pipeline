# Arabic Transcription Guidelines

Language: Arabic (Modern Standard Arabic, Saudi Arabia, United Arab Emirates)

## Part 1 - Text normalization

### Superset principle

The transcription rules below define the **minimum required coverage**. Annotation vendors are expected to deliver transcriptions that are a **superset** of these rules - any additional detail, markup, or tagging beyond what is specified here is encouraged and acceptable, as long as it does not contradict the rules.

Examples of acceptable superset additions include (but are not limited to):

- **Pronunciation variants** for acronyms or proper nouns annotated inline:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "SQL" said as "إس كيو إل" | SQL {PRO: إس كيو إل} |
| "SQL" said as "سيكويل" | SQL {PRO: سيكويل} |

- **Mispronunciation tags** to flag non-standard renderings:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "المملكة" intended but pronounced "الممكلة" | المملكة {MIS: الممكلة} |

- **Additional hesitation markers, dialect notes, confidence flags, or emotion tags** are acceptable as long as they do not alter the base transcription text.

In short: **do not remove detail that is present in the audio**. The rules below set the floor, not the ceiling.

---

### Text Normalization Rules

Transcribe the audio in Arabic script using the speaker's actual variety: Modern Standard Arabic, Saudi Arabic, Emirati Arabic, Gulf Arabic, or any other Arabic dialect that is present. Convert numeric, symbolic, and abbreviated tokens to their fully spoken Arabic form using the rules below. Return transcription only.

#### 1. Broad Principles

With the exception of acronyms, initialisms, official brand spellings, and clearly intended written forms, everything should be written out in full spoken words. Abbreviations, symbols, shorthand, and numerals should all be expanded.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "كيلوغرام" | كيلوغرام | kg |
| "درهم إماراتي" | درهم إماراتي | AED |
| "وريال سعودي" | وريال سعودي | وSAR |
| "آيفون خمسة عشر" | آيفون خمسة عشر | iPhone 15 |
| "إم بي سي" | MBC | إم بي سي, if the broadcaster acronym is intended |
| "مجلس التعاون الخليجي" | مجلس التعاون الخليجي | GCC |

Use standard Arabic spelling for the variety being spoken. Do not over-normalize dialect into Modern Standard Arabic, and do not write predictable surface pronunciation when the intended standard spelling is clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "أنا أريد هذا" in MSA | أنا أريد هذا | أنا أبغى هذا |
| "أبغى هذا" in Saudi or Emirati speech | أبغى هذا | أريد هذا |
| "شو تبى" in Emirati speech | شو تبى | ماذا تريد |
| "وش تبي" in Saudi speech | وش تبي | ماذا تريد |
| "المدرسة" pronounced with sun-letter assimilation | المدرسة | المدّرسة, unless diacritics are explicitly required |

#### 2. Arabic Orthography and Script Choice

Use Arabic script for Arabic speech. Use Latin letters only for acronyms, official product names, usernames, URLs, codes, file names, or foreign-language speech that is clearly intended as foreign.

- Write ordinary Arabic without short-vowel diacritics.
- Do not add tashkeel, tanween, shadda, or sukun unless the speaker is explicitly discussing them, reciting a fixed vocalized text, or the project requires vocalized Arabic.
- Use standard spelling for hamza, taa marbuta, alif maqsura, yaa, and alif forms when the intended word is clear.
- Use Arabic comma `،` and Arabic question mark `؟` when punctuation is needed.
- Do not use tatweel, decorative ligatures, emoji, or phonetic respelling for ordinary Arabic words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "مسؤول" | مسؤول | مسوول / مسئول, unless that spelling is the project standard |
| "شيء" | شيء | شئ, unless preserving a quoted written form |
| "مدرسة" | مدرسة | مدرسه, unless dialectal final ه is intentionally written |
| "على" as a preposition | على | علا |
| "هدى" as a person's name | هدى | هدا |
| "إلى البيت" | إلى البيت | الى البيت, if standard hamza spelling is expected |

Arabic dialects do not have one universal written standard. Use a consistent, readable Arabic-script spelling that preserves the actual words and morphology. Do not convert one dialect into another.

| Variety | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| MSA | "ماذا تريد الآن" | ماذا تريد الآن | وش تبي الحين |
| Saudi Najdi | "وش تبي الحين" | وش تبي الحين | ماذا تريد الآن |
| Saudi Hijazi | "إيش تبغى دحين" | إيش تبغى دحين | ماذا تريد الآن |
| Saudi Eastern / Gulf | "شنو تبي الحين" | شنو تبي الحين | ماذا تريد الآن |
| Emirati / UAE | "شو تبى الحين" | شو تبى الحين | ماذا تريد الآن |
| Egyptian | "إنت عايز إيه دلوقتي" | إنت عايز إيه دلوقتي | ماذا تريد الآن |
| Levantine | "شو بدك هلأ" | شو بدك هلأ | ماذا تريد الآن |
| Iraqi | "شنو تريد هسه" | شنو تريد هسه | ماذا تريد الآن |
| Yemeni | "إيش تشتي الحين" | إيش تشتي الحين | ماذا تريد الآن |
| Sudanese | "عايز شنو هسه" | عايز شنو هسه | ماذا تريد الآن |
| Maghrebi | "شنو بغيتي دابا" | شنو بغيتي دابا | ماذا تريد الآن |

#### 3. Arabic Variant and Dialect Policy

Arabic transcription must be variety-preserving. The base transcript should represent the Arabic actually spoken, not a translated or corrected version.

Priority order for choosing a written form:

1. If the speaker is reading or clearly intending a written form, use that written form in spoken words.
2. If the speaker uses Modern Standard Arabic, use standard MSA orthography.
3. If the speaker uses Saudi, Emirati, Gulf, or another dialect, preserve the dialectal words, particles, clitics, and grammar.
4. If the speaker code-switches between varieties, preserve each switch in place.
5. If a dialect word has multiple common spellings, choose the clearest Arabic-script form and keep it consistent within the same transcript.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| MSA "سوف أذهب غدا" | سوف أذهب غدا | بروح بكرة |
| Saudi "بروح بكرة" | بروح بكرة | سوف أذهب غدا |
| Emirati "بسير باجر" | بسير باجر | سوف أذهب غدا |
| Levantine "رح روح بكرا" | رح روح بكرا | سوف أذهب غدا |
| Egyptian "هروح بكرة" | هروح بكرة | سوف أذهب غدا |

For the requested Arabic scope, give special attention to:

| Variety | Preserve examples | Do not replace with |
|---------|-------------------|---------------------|
| Modern Standard Arabic | ماذا، أريد، الآن، جدا، سوف، ليس | Gulf or Saudi colloquial forms |
| Saudi Najdi | وش، تبي، أبي، الحين، مرة، واجد | MSA paraphrases |
| Saudi Hijazi | إيش، تبغى، أبغى، دحين، مره | MSA paraphrases |
| Saudi Eastern / Gulf | شنو، تبي، أبي، الحين، واجد | MSA paraphrases |
| Emirati / UAE | شو، تبى، أبغي، أبا، الحين، وايد، بسير، باجر | MSA paraphrases |

If the speaker's exact subdialect is uncertain, do not label it. Transcribe the words as heard using consistent Arabic spelling.

#### 4. Numbers

Spell out all digits and numeric expressions as spoken Arabic words. Preserve the speaker's actual reading, including MSA, Saudi, Emirati, Gulf, English-influenced, or digit-by-digit readings.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "أربعة عشر" | أربعة عشر | 14 |
| "أربعطعش" in dialect | أربعطعش | 14 / أربعة عشر |
| "صفر فاصلة صفر خمسة" | صفر فاصلة صفر خمسة | 0.05 |
| "ألف وثلاثون فاصلة خمسة" | ألف وثلاثون فاصلة خمسة | 1,030.5 |
| "ألفين وأربعة وعشرين" | ألفين وأربعة وعشرين | 2024 |
| "اثنين صفر اثنين أربعة" | اثنين صفر اثنين أربعة | 2024 |
| "تسعة ثلاثة ستة شرطة واحد واحد" | تسعة ثلاثة ستة شرطة واحد واحد | 936-11 |
| "ناقص اثني عشر" | ناقص اثني عشر | -12 |

#### 5. Arabic Number Readings, Gender, and Case

Arabic number forms vary by gender, case, register, and dialect. Transcribe the form that was spoken; do not convert it into another grammatical form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ثلاثة كتب" | ثلاثة كتب | ثلاث كتب |
| "ثلاث سيارات" | ثلاث سيارات | ثلاثة سيارات |
| "اثنا عشر طالبا" in MSA | اثنا عشر طالبا | اثنين عشر طالب |
| "اثني عشر ريالا" in MSA | اثني عشر ريالا | اثنا عشر ريالا, if accusative/genitive was clearly spoken |
| "ثلاث طعش سيارة" in dialect | ثلاث طعش سيارة | ثلاث عشرة سيارة |
| "خمسطعش ريال" in dialect | خمسطعش ريال | خمسة عشر ريالا |
| "صفر" | صفر | زيرو |
| "زيرو" | زيرو | صفر |
| "نقطة" for decimal point | نقطة | فاصلة |
| "فاصلة" for decimal point | فاصلة | نقطة |

Do not add Arabic case endings or diacritics that were not required by the transcript style. If final case vowels are clearly pronounced in formal Arabic, preserve the word sequence but normally keep it unvocalized.

#### 6. Non-Numeral Usage

Do not convert number words to digits when they are part of natural language and not intended as a numeric expression. This includes idioms, names, titles, fixed phrases, approximations, and compounds.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "أنت واحد من الناس" | أنت واحد من الناس | أنت 1 من الناس |
| "أول شيء" | أول شيء | 1 شيء |
| "ألف مبروك" | ألف مبروك | 1000 مبروك |
| "مليون مرة قلت لك" | مليون مرة قلت لك | 1000000 مرة قلت لك |
| "سوق الاثنين" | سوق الاثنين | سوق 2 |
| "ألف ليلة وليلة" | ألف ليلة وليلة | 1000 ليلة وليلة |

When a disfluency occurs before a non-numeral expression, keep the disfluent portion as spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "أ أ أول شيء" | أ أ أول شيء | أ- أ- 1 شيء |
| "وا واحد من الناس" | وا- واحد من الناس | وا- 1 من الناس |

#### 7. Ordinals, Counters, Decades, and Age Ranges

Spell out ordinal expressions, counted items, decades, centuries, and age ranges as spoken Arabic words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "الأول" | الأول | 1st / 1 |
| "الثاني" | الثاني | 2nd |
| "الفصل الثالث" | الفصل الثالث | الفصل 3 |
| "ثلاثة أشخاص" | ثلاثة أشخاص | 3 أشخاص |
| "ثلاث سيارات" | ثلاث سيارات | 3 سيارات |
| "السبعينات" | السبعينات | السبعينيات / 70s, if not spoken |
| "في العشرينات من عمره" | في العشرينات من عمره | في 20s من عمره |
| "الحرب العالمية الثانية" | الحرب العالمية الثانية | الحرب العالمية 2 |

Use the official spelling for titles, laws, chapters, and product names only when the speaker is clearly referring to that official written form. Otherwise preserve the spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ويندوز إلفن" | ويندوز إلفن | Windows 11 |
| "آيفون خمسة عشر" | آيفون خمسة عشر | iPhone 15 |
| "رؤية السعودية عشرين ثلاثين" as a digit-by-digit name | رؤية السعودية عشرين ثلاثين | رؤية السعودية 2030 |

#### 8. Dates

Write dates as spoken Arabic words. Do not convert day, month, year, Hijri dates, Gregorian dates, or regional month names into digit notation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "التاسع والعشرين من أبريل ألفين وأربعة وعشرين" | التاسع والعشرين من أبريل ألفين وأربعة وعشرين | 2024-04-29 |
| "تسعة وعشرين أبريل ألفين وأربعة وعشرين" | تسعة وعشرين أبريل ألفين وأربعة وعشرين | 29 أبريل 2024 |
| "واحد رمضان ألف وأربعمئة وخمسة وأربعين" | واحد رمضان ألف وأربعمئة وخمسة وأربعين | 1 رمضان 1445 |
| "الأول من يناير" | الأول من يناير | 1 يناير |
| "كانون الثاني" | كانون الثاني | يناير, if the speaker said كانون الثاني |
| "جانفي" in North African speech | جانفي | يناير, if the speaker said جانفي |
| "تسعة أحد عشر" as spoken for an event | تسعة أحد عشر | 9/11 |

If the speaker reads a date digit by digit, preserve that digit-by-digit spoken form.

#### 9. Time of Day

Write clock times as spoken Arabic words. Include صباحا، مساء، الظهر، العصر، المغرب، الليل, or dialectal equivalents only if spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "الساعة الثانية والنصف مساء" | الساعة الثانية والنصف مساء | 2:30 PM |
| "اثنين ونص" in dialect | اثنين ونص | 2:30 / الثانية والنصف |
| "الساعة الواحدة وخمس وأربعون دقيقة" | الساعة الواحدة وخمس وأربعون دقيقة | 1:45 |
| "الساعة الرابعة عشرة وثلاثون دقيقة" | الساعة الرابعة عشرة وثلاثون دقيقة | 14:30 |
| "الظهر" | الظهر | 12:00 |
| "منتصف الليل" | منتصف الليل | 00:00 |
| "من ثمانية إلى خمسة" | من ثمانية إلى خمسة | من 8 إلى 5 |
| "صفر صفر وخمسة عشر" | صفر صفر وخمسة عشر | 00:15 |

#### 10. Money / Currency

Spell out money and currency amounts as spoken Arabic words. Preserve the currency word and the regional form that was spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "اثنان وخمسون ريالا" | اثنان وخمسون ريالا | 52 ريال |
| "اثنين وخمسين ريال" in dialect | اثنين وخمسين ريال | 52 ريال |
| "ألف درهم" | ألف درهم | 1,000 درهم |
| "درهمين وخمسين فلس" | درهمين وخمسين فلس | 2.50 درهم |
| "دولارين وخمسين سنت" | دولارين وخمسين سنت | $2.50 |
| "ثلاثين أربعين ريال" | ثلاثين أربعين ريال | 30-40 ريال |
| "خمس هللات" | خمس هللات | 5 هللات |

Do not normalize informal money words into exact currency if the amount or currency is not clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "كم فلس" in Gulf speech | كم فلس | كم درهم |
| "ما عندي ولا ريال" | ما عندي ولا ريال | ما عندي 1 ريال |
| "قرشين" as an idiom | قرشين | ريالين, unless exact currency is meant |

#### 11. Percentages

Spell out the number and the percent word exactly as spoken: بالمئة، في المئة، بالمية, بيرسنت, or another spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "صفر فاصلة خمسة بالمئة" | صفر فاصلة خمسة بالمئة | 0.5% |
| "مئة بالمئة" | مئة بالمئة | 100% |
| "مية بالمية" in dialect | مية بالمية | 100% / مئة بالمئة |
| "عشرين إلى ثلاثين في المئة" | عشرين إلى ثلاثين في المئة | 20% إلى 30% |
| "خمسة بيرسنت" | خمسة بيرسنت | 5% |

#### 12. Measures / Units

Read the number as words and expand or preserve the unit according to what was spoken. Common dialectal unit words such as كيلو and سانتي are acceptable when spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "خمسة كيلوغرام" | خمسة كيلوغرام | 5kg / 5 كيلوغرام |
| "خمسة كيلو" | خمسة كيلو | 5kg / خمسة كيلوغرام, if كيلو was spoken |
| "تسعين كيلومتر في الساعة" | تسعين كيلومتر في الساعة | 90km/h |
| "متر وسبعين سانتي" | متر وسبعين سانتي | 1m 70cm |
| "ثمانية بت" | ثمانية بت | 8 بت |
| "فور كي" | فور كي | 4K |
| "مئة واط" | مئة واط | 100W |

If the speaker reads a technical shorthand as letters, transcribe the spoken letters or canonical acronym as appropriate.

#### 13. Fractions, Ratios, and Scores

Spell out fractions, ratios, and scores as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ثلاثة أرباع" | ثلاثة أرباع | 3/4 |
| "ثلاثة على أربعة" | ثلاثة على أربعة | 3/4 |
| "واحد وثلاثة أرباع" | واحد وثلاثة أرباع | 1 3/4 |
| "نصف" | نصف | 1/2 |
| "خمسين خمسين" | خمسين خمسين | 50:50 |
| "اثنين واحد" as a score | اثنين واحد | 2-1 |
| "اثنين مقابل واحد" | اثنين مقابل واحد | 2:1 |

#### 14. Negative Numbers

Spell out negative numbers as spoken words. Preserve whether the speaker says ناقص, سالب, تحت الصفر, or a dialectal equivalent.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ناقص اثني عشر" | ناقص اثني عشر | -12 / ناقص 12 |
| "سالب اثنا عشر" | سالب اثنا عشر | -12 / سالب 12 |
| "ثمانية عشر تحت الصفر" | ثمانية عشر تحت الصفر | -18 |
| "ناقص خمس درجات" | ناقص خمس درجات | -5 درجات |

#### 15. Phone Numbers, Postal Codes, IDs, and Codes

Read each digit group individually as spoken. Do not write formatted phone numbers, postal codes, license plates, national IDs, reservation numbers, or other codes with digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "صفر خمسة صفر واحد اثنين ثلاثة أربعة خمسة ستة سبعة" | صفر خمسة صفر واحد اثنين ثلاثة أربعة خمسة ستة سبعة | 0501234567 |
| "صفر خمسة صفر واحد اثنين ثلاثة أربعة خمسة ستة سبعة" | صفر خمسة صفر واحد اثنين ثلاثة أربعة خمسة ستة سبعة | 050-123-4567 |
| "تسعة ثلاثة ستة شرطة واحد واحد" | تسعة ثلاثة ستة شرطة واحد واحد | 936-11 |
| "الرمز البريدي واحد اثنين ثلاثة أربعة خمسة" | الرمز البريدي واحد اثنين ثلاثة أربعة خمسة | الرمز البريدي 12345 |
| "ألف باء واحد اثنين ثلاثة" as Arabic letter names | ألف باء واحد اثنين ثلاثة | أ ب 123 |
| "A B واحد اثنين ثلاثة" as Latin letters | A B واحد اثنين ثلاثة | AB123 |

If the speaker groups digits as larger numbers, preserve that reading instead of forcing digit-by-digit form.

#### 16. Electronic Text (URLs, Emails, IPs)

Read all symbols aloud. Do not write URLs, email addresses, IP addresses, usernames, handles, or file paths in compact written form.

| Symbol | Spoken As |
|--------|-----------|
| @ | آت / أت / علامة آت, as spoken |
| . | نقطة / دوت, as spoken |
| / | سلاش / شرطة مائلة, as spoken |
| : | نقطتين / كولون, as spoken |
| - | شرطة / داش / هايفن, as spoken |
| _ | أندر سكور / شرطة سفلية, as spoken |

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "example دوت com سلاش pricing" | example دوت com سلاش pricing | example.com/pricing |
| "google نقطة com" | google نقطة com | google.com |
| "ahmed آت gmail دوت com" | ahmed آت gmail دوت com | ahmed@gmail.com |
| "واحد تسعة اثنين نقطة واحد ستة ثمانية نقطة صفر نقطة واحد" | واحد تسعة اثنين نقطة واحد ستة ثمانية نقطة صفر نقطة واحد | 192.168.0.1 |
| "user أندر سكور name" | user أندر سكور name | user_name |

#### 17. Roman Numerals

Use the spoken Arabic title, ordinal, regnal, or cardinal form. Do not write Roman numerals in `Correct`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ستار وورز الجزء الرابع" | ستار وورز الجزء الرابع | Star Wars Episode IV |
| "فاينل فانتسي سبعة" | فاينل فانتسي سبعة | Final Fantasy VII |
| "إليزابيث الثانية" | إليزابيث الثانية | Elizabeth II / إليزابيث 2 |
| "الباب السادس" | الباب السادس | الباب VI |

#### 18. Abbreviations and Initialisms

Keep spoken acronyms and initialisms in their canonical form when the speaker is saying the acronym as such. Expand abbreviations only when the speaker says the expanded form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ناسا" as NASA | NASA | الإدارة الوطنية للملاحة الجوية والفضاء |
| "بي بي سي" | BBC | هيئة الإذاعة البريطانية |
| "إم بي سي" | MBC | مركز تلفزيون الشرق الأوسط, unless the speaker said the full name |
| "إف بي آي" | FBI | مكتب التحقيقات الفدرالي |
| "إس كيو إل" | SQL | Structured Query Language |
| "لغة الاستعلامات المهيكلة" | لغة الاستعلامات المهيكلة | SQL |
| "دكتور أحمد" | دكتور أحمد | د. أحمد |
| "شارع الملك فهد" | شارع الملك فهد | ش. الملك فهد |

When pronunciation is ambiguous or important, `{PRO: ...}` is an acceptable superset annotation.

#### 19. Foreign Words and Loanwords

Loanwords and foreign words do not have a strict boundary, and some cases are gray areas. As a general rule, if a word is commonly used in Arabic speech and has a conventional Arabic spelling, treat it as an Arabic loanword, not as foreign speech. Write these words in Arabic script.

Do not mark established Arabic loanwords as foreign words. Use standard Arabic spelling unless the speaker is clearly giving an official Latin-script name, spelling, URL, username, code, or other written form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "كافيه" | كافيه | <foreign> cafe </foreign> |
| "كمبيوتر" | كمبيوتر | <foreign> computer </foreign> |
| "آيس كريم" | آيس كريم | <foreign> ice cream </foreign> |
| "أوكي" | أوكي | <foreign> okay </foreign> |
| "ميتنج" in Arabic speech | ميتنج | <foreign> meeting </foreign> |
| "باص" | باص | <foreign> bus </foreign> |
| "شوكولاتة" | شوكولاتة | <foreign> chocolate </foreign> |
| "إنترنت" | إنترنت | <foreign> internet </foreign> |

Use the actual foreign spelling only when the speaker is clearly saying a foreign-language word or phrase as foreign speech, rather than using an Arabic loanword. If your pipeline supports foreign-language tags, they may be added as a superset annotation.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "Thank you" clearly in English | Thank you | <foreign lang="EN"> Thank you </foreign> |
| "Gracias" clearly in Spanish | Gracias | <foreign lang="ES"> Gracias </foreign> |
| "I love you" clearly in English | I love you | <foreign lang="EN"> I love you </foreign> |
| "bonjour" clearly in French | bonjour | <foreign lang="FR"> bonjour </foreign> |

If a word could be either an Arabic loanword or foreign speech, choose based on how it is used and pronounced in context.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Arabic loanword pronunciation | أكلت ساندويتش | أكلت sandwich |
| English phrase pronunciation | sandwich, please | ساندويتش, please |
| Official product or brand spelling is intended | اشتريت iPhone | اشتريت آيفون, if the official written form is clearly intended |
| Ordinary Arabicized product reference | اشتريت آيفون | اشتريت iPhone, if no Latin written form is intended |

Proper nouns are not foreign-language spans just because they come from another language.

#### 20. Ambiguity

Rely on audio context to resolve ambiguous tokens. Arabic has ambiguity from dialect variation, unvoweled spelling, hamza spelling, alif maqsura versus yaa, taa marbuta versus haa, and names that share pronunciation with common words. Choose the written form that best reflects the speaker's intended meaning.

| Context | Audio | Correct |
|---------|-------|---------|
| Time | "الساعة اثنين" | الساعة اثنين |
| Quantity | "اثنين أشخاص" in dialect | اثنين أشخاص |
| Natural expression | "أول شيء" | أول شيء |
| Proper noun | "علي" as a name | علي |
| Preposition | "على الطاولة" | على الطاولة |
| Acronym | "إم بي سي" used for the channel | MBC |

Use exact context to distinguish same-sounding forms. Do not use a spelling that changes meaning.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Preposition | "على المكتب" | على المكتب | علا المكتب |
| Person name | "علا وصلت" | علا وصلت | على وصلت |
| Given name | "هدى تكلمت" | هدى تكلمت | هدا تكلمت |
| Demonstrative in dialect | "هدا كتابي" if the speaker says dialectal هدا | هدا كتابي | هذا كتابي, if dialectal form is intended |
| Standard demonstrative | "هذا كتابي" in MSA | هذا كتابي | هدا كتابي |
| Direction | "إلى الرياض" | إلى الرياض | إلا الرياض |
| Exception | "ما حضر إلا أحمد" | ما حضر إلا أحمد | ما حضر إلى أحمد |
| God | "الله أكبر" | الله | اللة |
| Noun with pronoun | "كتابه جديد" | كتابه | كتابة |

If the audio does not provide enough evidence for a proper-name spelling, do not invent a special spelling. Use the most common Arabic spelling only when context supports it; otherwise use a conservative phonetic Arabic spelling.

#### 21. Guidelines for Language-specific Issues

The following Arabic-specific issues should follow the same principles above: preserve what was spoken, use standard Arabic orthography for the variety, do not invent unsupported detail, and choose spelling from context.

**Modern Standard Arabic versus dialect:** Do not translate or "correct" dialectal speech into MSA. Do not make MSA colloquial.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ليس لدي وقت" in MSA | ليس لدي وقت | ما عندي وقت |
| "ما عندي وقت" in Saudi or Gulf speech | ما عندي وقت | ليس لدي وقت |
| "لا أستطيع" in MSA | لا أستطيع | ما أقدر |
| "ما أقدر" in Saudi or Emirati speech | ما أقدر | لا أستطيع |

**Saudi and Emirati dialect forms:** Preserve regional question words, negation, future markers, and common verbs.

| Variety | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Saudi Najdi | "وش سالفتك" | وش سالفتك | ما قصتك |
| Saudi Hijazi | "إيش تبغى" | إيش تبغى | ماذا تريد |
| Saudi Eastern | "شنو الموضوع" | شنو الموضوع | ما الموضوع |
| Emirati | "شو السالفة" | شو السالفة | ما القصة |
| Emirati | "بسير البيت" | بسير البيت | سأذهب إلى البيت |
| Emirati | "وايد زين" | وايد زين | جيد جدا |

**Other Arabic dialects:** If Egyptian, Levantine, Iraqi, Yemeni, Sudanese, Maghrebi, Omani, Kuwaiti, Bahraini, Qatari, or any other Arabic dialect appears, preserve it as spoken. The file's target emphasis is MSA, Saudi Arabia, and the UAE, but Arabic data may contain pan-Arabic speakers.

| Variety | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Egyptian | "إنت بتعمل إيه" | إنت بتعمل إيه | ماذا تفعل |
| Levantine | "شو عم تعمل" | شو عم تعمل | ماذا تفعل |
| Iraqi | "شنو دا تسوي" | شنو دا تسوي | ماذا تفعل |
| Yemeni | "إيش بتسوي" | إيش بتسوي | ماذا تفعل |
| Sudanese | "بتعمل شنو" | بتعمل شنو | ماذا تفعل |
| Moroccan / Maghrebi | "شنو كتدير" | شنو كتدير | ماذا تفعل |

**Clitics and attached particles:** Arabic attaches many short particles to following or preceding words. Use conventional Arabic spelling and do not split clitics into artificial tokens unless the speaker is spelling them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "وبعدين" | وبعدين | و بعدين |
| "فالبيت" | فالبيت | ف البيت, unless dialectal spacing is required by project style |
| "بالسيارة" | بالسيارة | ب السيارة |
| "للرياض" | للرياض | ل الرياض |
| "ما قلت له" | ما قلت له | ماقلتله, unless the project uses fused dialect spelling |

**Definite article and sun letters:** Write the standard word with ال. Do not respell assimilation phonetically.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "الشمس" pronounced with assimilated ش | الشمس | اششمس / الشّمس, unless vocalized |
| "الرياض" | الرياض | ارياض |
| "الناس" | الناس | انناس |
| "المدرسة" | المدرسة | امدرسة |

**Hamza, alif, yaa, alif maqsura, and taa marbuta:** Use standard spelling when the intended word is clear. Preserve dialectal written forms only when they represent a real dialect word or quoted writing.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "مساء" | مساء | مسا, unless dialectal spelling is intended |
| "شيء" | شيء | شي, unless the speaker said dialectal شي |
| "على" | على | علي, unless the name علي is meant |
| "علي" as a name | علي | على |
| "فتاة" | فتاة | فتاه |
| "مئة" | مئة | 100 / مية, unless dialectal مية was spoken |

**Religious, Quranic, and formal recitation:** If the speaker recites a fixed religious text, quote, poem, or formal line with special pronunciation, transcribe the words faithfully. Do not add full vocalization unless the project requires it or the vocalization itself is being evaluated.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "بسم الله الرحمن الرحيم" | بسم الله الرحمن الرحيم | بسم الله الرحمان الرحيم |
| "إن شاء الله" | إن شاء الله | إنشاء الله |
| "ما شاء الله" | ما شاء الله | ماشاء الله, if standard spacing is expected |

**Names and official spellings:** Arabic personal, tribal, city, and company names may have multiple spellings. Use the official spelling if known from context. If not known, use a common Arabic spelling and do not invent Latin transliteration.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "محمد القحطاني" | محمد القحطاني | Mohammed Alqahtani, unless Latin spelling is given |
| "نورة" with no official spelling given | نورة | نوره, unless that spelling is known |
| "دبي" | دبي | Dubai, unless Latin spelling is intended |
| Known official Latin brand | stc | إس تي سي, if the official Latin brand spelling is clearly intended |

**Onomatopoeia and lexical sound words:** Arabic sound-symbolic words are lexical words when spoken. Transcribe them as words; do not replace them with non-speech tags.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "سمعت صوت طق" | سمعت صوت طق | سمعت صوت [other-noise] |
| "الباب صار يطق طق" | الباب صار يطق طق | الباب صار [other-noise] |
| "قال ههه وهو يضحك" if the speaker says it as lexical laughter text | قال ههه وهو يضحك | قال [laugh] وهو يضحك |

---

## Part 2 - Disfluency

### Disfluency Rules

You are given an audio clip and its existing transcription. Your task is to output the transcription as provided, adding all speech disfluencies that you hear based on the rules below. Return only the transcription text.

#### 1. Filler Words

Words like "يعني", "طيب", "خلاص", "بس", "والله", "ما أدري", "شوف", "أقول", "أها", and dialectal fillers such as "عاد", "زين", "حلو", "ترى", "يلا", "ها" should be added to the transcription when spoken. Keep lexical fillers as spoken, but standardize excessive elongation according to the canonical table below.

| Audio | Correct |
|-------|---------|
| "يعني ما أدري" | يعني ما أدري |
| "طيب، خلنا نشوف" | طيب، خلنا نشوف |
| "والله الموضوع صعب" | والله الموضوع صعب |
| "عاد شوف" in Gulf speech | عاد شوف |

#### 2. Hesitation Markers and Vocal Fillers

Listen for **non-lexical vocalizations** during pauses, planning, and reactive listening. Standardize spellings to the canonical form for each group. Use normal Arabic spacing and punctuation.

**Filled pauses / hesitation** (speaker holds the floor, searching for words):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **ام** | `ام` | `اممم`, `ام...`, nasal hesitation |
| **آه** | `آه` | `آآه`, `آه...` when used as hesitation |
| **إيه** | `إيه` | `إيييه`, hesitation or mild reaction depending on context |
| **أا** | `أا` | short open hesitation before a word |
| **يعني** | `يعني` | `يعنيي`, elongated filler |
| **مم** | `مم` | thinking hum when lexical content is absent |
| **ها** | `ها` | short attention or hesitation marker |

**Backchannel / response** (listener signals agreement, negation, or reaction):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **إيه** | `إيه` | affirmative response in many dialects |
| **نعم** | `نعم` | formal affirmative response |
| **أيوه** | `أيوه` | Egyptian/Gulf affirmative as spoken |
| **هيه** | `هيه` | Gulf/Emirati affirmative as spoken |
| **لا** | `لا` | negative response |
| **أها** | `أها` | acknowledgment or realization |
| **همم** | `همم` | listener thinking or mild agreement |

When the same phones could be **hesitation** vs **backchannel**, use audio and dialogue role: mid-utterance planning -> hesitation; short reactive assent while the other speaker talks -> backchannel.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Filled pause before content | ام، ما أدري بالضبط | اممم، ما أدري بالضبط |
| Thinking hum | مم، خلني أفكر | مممم، خلني أفكر |
| Listener yes | إيه، صحيح | إيييه، صحيح if only one acknowledgment |
| Formal acknowledgment | نعم، فهمت | نععم، فهمت |
| Mild realization | آه، فهمت عليك | آآه، فهمت عليك |

#### 3. Repetitions

Consecutive instances of the same word or short phrase spoken unintentionally should be kept as-is with no added punctuation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "أنا أنا أنا رحت" | أنا أنا أنا رحت | أنا- أنا- أنا رحت / أنا رحت |
| "هذا هذا الموضوع" | هذا هذا الموضوع | هذا- هذا الموضوع / هذا الموضوع |
| "كنت أبغى كنت أبغى أقول" | كنت أبغى كنت أبغى أقول | كنت أبغى- كنت أبغى أقول / كنت أبغى أقول |
| "يعني يعني ما أدري" | يعني يعني ما أدري | يعني- يعني ما أدري |

If a repetition is intentional, rhythmic, or emphatic, use normal Arabic punctuation instead of disfluency dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "لا، لا، لا، مو كذا" | لا، لا، لا، مو كذا | لا- لا- لا مو كذا |
| "تمام، تمام" | تمام، تمام | تمام- تمام |

#### 4. False Starts / Cut-Off Words

Incomplete words or phrases that the speaker abandons should be marked with a single dash followed by a space. If the speaker cuts off and stops entirely, still use a single dash.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "أنا كنت أشت- أقصد أدرس" | أنا كنت أشت- أقصد أدرس | أنا كنت أشتغل أقصد أدرس |
| "بنرو- وين كنا بنروح؟" | بنرو- وين كنا بنروح؟ | بنروح، وين كنا بنروح؟ |
| "الشي اللي كنت أقول-" | الشي اللي كنت أقول- | الشي اللي كنت أقول |
| "أبغى آيس كري-" | أبغى آيس كري- | أبغى آيس كريم |

#### 5. Casual Forms, Slang, and Dialect

Use casual forms if that is how they were spoken and the form is clearly audible. If unsure, default to the most standard spelling for the speaker's variety.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "أبغى" | أبغى | أريد |
| "أبا" in Emirati speech | أبا | أريد |
| "وش" in Saudi speech | وش | ماذا |
| "شو" in Emirati or Levantine speech | شو | ماذا |
| "مرة حلو" in Saudi speech | مرة حلو | جميل جدا |
| "وايد زين" in Emirati speech | وايد زين | جيد جدا |

Normalize pure phonetic reductions when the intended standard spelling is clear and the difference is only predictable pronunciation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "الشمس" with assimilated article | الشمس | اششمس |
| "الناس" with assimilated article | الناس | انناس |
| "مدرسة" pronounced with final vowel reduced | مدرسة | مدرسه, unless dialectal ه spelling is intended |

Do not rewrite dialectal or colloquial grammar into formal MSA if the form is a real spoken form and not merely a dropped sound.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ما رحت" | ما رحت | لم أذهب |
| "بروح" | بروح | سأذهب |
| "شو تسوي" | شو تسوي | ماذا تفعل |
| "إيش تبغى" | إيش تبغى | ماذا تريد |

#### 6. Spelled-Out Words

If a speaker spells out a non-acronym word one letter at a time using Latin letters, use capital letters separated with dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "السبلنق M A S E G O" | السبلنق M-A-S-E-G-O | السبلنق M A S E G O |

If a speaker spells out Arabic letters, transcribe the letter names or letters as spoken. Do not infer the full word unless the speaker clearly provides it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ألف لام ميم" | ألف لام ميم | ألم, unless the intended word is explicitly stated |
| "ميم حاء ميم دال" | ميم حاء ميم دال | محمد, unless the intended name is explicitly stated |
| "ا ل ي" as letter names | ا-ل-ي | علي, unless the intended word is explicitly stated |

If the speaker is saying an acronym or initialism, use the canonical acronym form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "بي بي سي" | BBC | B-B-C |
| "إم بي سي" | MBC | M-B-C |
| "جي بي تي" | GPT | G-P-T |

#### 7. Mispronunciations

Transcribe intelligible real-word substitutions as spoken. Do not correct the word in the base transcript and do not add a tag unless your project uses superset `{MIS: ...}` annotations.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "القصب" where "القصد" was intended | القصب | القصد |
| "مكتبة" where "مكتوبة" was intended by context | مكتبة | مكتوبة |
| "الممكلة" | الممكلة | المملكة, unless using superset `المملكة {MIS: الممكلة}` |

If the sound is intelligible but not a real word and the intended word is unclear, transcribe the sound phonetically in Arabic script.

| Audio | Correct |
|-------|---------|
| "دورفكلوغ" | دورفكلوغ |

#### 8. Wrong Grammar

Grammatical errors, dialectal grammar, non-standard morphology, and mixed-register constructions should be faithfully captured. Do not correct them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "أنا ما عندي ولا شي" | أنا ما عندي ولا شي | ليس لدي أي شيء |
| "هو راحوا أمس" | هو راحوا أمس | هو راح أمس |
| "إحنا ذهبت إلى السوق" | إحنا ذهبت إلى السوق | نحن ذهبنا إلى السوق |
| "اثنين أشخاص جو" in dialect | اثنين أشخاص جو | شخصان جاءا |

---

## Part 3 - Rich Transcription: Paralinguistic Tokens

### Non-Speech Sound Tokens

Bracket tokens mark **audible non-lexical or non-linguistic events** that are **not** regular words. Write each tag **exactly** as listed (square brackets included). Prefer **one tag per distinct event**; if several happen in sequence, repeat tags in **time order**, separated by spaces.

Use the NeMo canonical English tag names below, even in Arabic transcripts.

#### Rules for this section

1. **Tag vs words** - If the speaker says a word, transcribe the word. Use a bracket tag only for the sound event itself.
2. **No invented words** - Do not replace a tag with a phonetic guess unless the sound is a lexical filler covered in Part 2.
3. **Placement** - Put the tag where the sound occurs in the word stream, usually as its own token between words.
4. **Overlap** - If a sound overlaps speech, place the tag at the start of the overlap window unless your time-aligned format specifies otherwise.
5. **Sequences** - Use `[laugh] [laugh]` for two separate laugh bursts, not a single stretched token.
6. **Unknown / generic background** - Use `[other-noise]` for audible non-speech you cannot classify; use `[unintelligible]` only when linguistic content was likely present but cannot be recovered.
7. **Minor mouth sounds** - Do not tag faint natural mouth clicks, lip noise, or routine breathing unless they are prominent or communicative.

#### Token list and descriptions

Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into Arabic or replace them with local-language labels.

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
| Speaker laughs before speaking | [laugh] هذا مضحك | [ضحك] هذا مضحك |
| Speaker coughs mid-sentence | هذا [cough] ما فيه مشكلة | هذا كحة ما فيه مشكلة |
| Speech is masked and unrecoverable | أعتقد أنه [unintelligible] اليوم | أعتقد أنه اليوم |
| Background object noise | [other-noise] ممكن تعيد الكلام؟ | [noise] ممكن تعيد الكلام؟ |

#### Quick reference (canonical spellings)

- `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`, `[sniff]`, `[gasp]`, `[blow]`
- `[laugh]`, `[chuckle]`, `[giggle]`, `[snort]`, `[scoff]`, `[grunt]`, `[groan]`, `[cry]`
- `[hum-tune]`, `[whoop]`, `[whistle]`, `[tongue-click]`, `[tsk]`, `[lip-smack]`, `[teeth-suck]`, `[lip-trill]`, `[shush]`, `[swallow]`, `[clear-throat]`
- `[cough]`, `[sneeze]`, `[yawn]`, `[hiccup]`, `[unintelligible]`, `[other-noise]`
