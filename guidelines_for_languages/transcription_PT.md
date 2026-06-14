# Portuguese Transcription Guidelines

Language: Portuguese (Brazil, Portugal)

## Part 1 - Text normalization

### Superset principle

The transcription rules below define the **minimum required coverage**. Annotation vendors are expected to deliver transcriptions that are a **superset** of these rules - any additional detail, markup, or tagging beyond what is specified here is encouraged and acceptable, as long as it does not contradict the rules.

Examples of acceptable superset additions include (but are not limited to):

- **Pronunciation variants** for acronyms or proper nouns annotated inline:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "SQL" said as "esse cu ele" | SQL {PRO: esse cu ele} |
| "SQL" said as "siquel" | SQL {PRO: siquel} |

- **Mispronunciation tags** to flag non-standard renderings:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "problema" intended but pronounced "pobrema" | problema {MIS: pobrema} |

- **Additional hesitation markers, dialect notes, confidence flags, or emotion tags** are acceptable as long as they do not alter the base transcription text.

In short: **do not remove detail that is present in the audio**. The rules below set the floor, not the ceiling.

---

### Text Normalization Rules

Transcribe the audio in standard Portuguese orthography. Convert numeric, symbolic, and abbreviated tokens to their fully spoken Portuguese form using the rules below. Return transcription only.

#### 1. Broad Principles

With the exception of acronyms, initialisms, and established proper-name spellings, everything should be written out in full spoken words. Abbreviations, symbols, shorthand, and numerals should all be expanded.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "senhor Silva" | senhor Silva | Sr. Silva |
| "doutora Souza" | doutora Souza | Dra. Souza |
| "quilogramas" | quilogramas | kg |
| "e" | e | & |
| "avenida Paulista" | avenida Paulista | Av. Paulista |
| "iPhone quinze" | iPhone quinze | iPhone 15 |

Use standard spelling, accents, capitalization, and punctuation. Do not over-normalize into a form that changes spoken content.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "como você está" | como você está | como voce esta, if accents are required by the project |
| "não sei" | não sei | nao sei, if accents are required by the project |
| "São Paulo" | São Paulo | sao paulo |
| "Rio de Janeiro" | Rio de Janeiro | rio de janeiro |
| "tá bom" | tá bom | ta bom, if accents are required by the project |

#### 2. Portuguese Orthography, Accents, and Punctuation

Use standard Portuguese spelling and punctuation:

- Write Portuguese in the Latin alphabet with standard Portuguese letters, including `ç` and the accents `á`, `à`, `â`, `ã`, `é`, `ê`, `í`, `ó`, `ô`, `õ`, `ú`.
- Use accents and the cedilla where they are part of standard spelling or disambiguate meaning.
- Capitalize proper nouns, official names, brands, acronyms, and sentence starts according to Portuguese norms.
- Apply the post-2009 *Acordo Ortográfico* spellings (for example, write `ideia`, `voo`, `linguística` without the older diacritics) unless the project specifies pre-reform spelling.
- Preserve regional spelling differences where the variants are still standard (for example, BR `econômico` vs PT `económico`, BR `recepção` vs PT `receção`, BR `time` vs PT `equipa`, BR `ônibus` vs PT `autocarro`).
- Do not imitate predictable casual pronunciation when the intended standard word is clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "coração" | coração | coracao |
| "construção" | construção | construcao |
| "açúcar" | açúcar | acucar |
| "informação" | informação | informacao |
| "pão" | pão | pao |
| "BR speaker: ônibus" | ônibus | autocarro |
| "PT speaker: autocarro" | autocarro | ônibus |
| "BR speaker: trem" | trem | comboio |
| "PT speaker: comboio" | comboio | trem |
| "BR speaker: celular" | celular | telemóvel |
| "PT speaker: telemóvel" | telemóvel | celular |

Preserve regional vocabulary, colloquial words, and dialectal grammar when they are real spoken forms and not merely spelling errors.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "tu sabes" in PT or southern BR | tu sabes | você sabe |
| "você sabe" | você sabe | tu sabes |
| "a gente vai" | a gente vai | nós vamos, unless that was spoken |
| "nós vamos" | nós vamos | a gente vai, unless that was spoken |
| "bah, tchê" | bah, tchê | nossa, unless that was spoken |
| "uai" in mineiro speech | uai | nossa, unless that was spoken |

#### 3. Numbers

Spell out all digits and numeric expressions as spoken Portuguese words. Preserve the speaker's actual reading where Portuguese has more than one natural wording. Use `e` between number groups when the speaker says it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "catorze" | catorze | 14 |
| "quatorze" | quatorze | 14 / catorze |
| "vinte e um" | vinte e um | 21 |
| "cento e vinte" | cento e vinte | 120 |
| "mil e trinta vírgula cinco" | mil e trinta vírgula cinco | 1.030,5 / 1,030.5 |
| "zero vírgula zero cinco" | zero vírgula zero cinco | 0,05 / 0.05 |
| "dois mil e vinte e quatro" | dois mil e vinte e quatro | 2024 |
| "novecentos e trinta e seis traço onze" | novecentos e trinta e seis traço onze | 936-11 |
| "menos doze" | menos doze | -12 |

#### 4. Gender, Agreement, and Decimal Conventions

Portuguese numbers can change form by gender, noun agreement, and regional preference. Transcribe the form that was spoken; do not silently change it. Portuguese normally uses `vírgula` for decimals and `ponto` only when the speaker says it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "vinte e um livros" | vinte e um livros | vinte e uma livros / 21 livros |
| "vinte e uma casas" | vinte e uma casas | vinte e um casas / 21 casas |
| "duzentas pessoas" | duzentas pessoas | duzentos pessoas / 200 pessoas |
| "trezentos reais" | trezentos reais | trezentas reais / 300 reais |
| "um milhão de reais" | um milhão de reais | 1 milhão de reais |
| "uma hora da tarde" | uma hora da tarde | um hora da tarde / 1:00 |

Preserve the speaker's decimal and thousands wording.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "três vírgula catorze" | três vírgula catorze | 3,14 / três ponto catorze |
| "três ponto catorze" | três ponto catorze | 3.14 / três vírgula catorze |
| "mil e duzentos" | mil e duzentos | 1.200 / 1,200 |
| "dois mil e quinhentos" | dois mil e quinhentos | 2.500 / 2,500 |

#### 5. Non-Numeral Usage

Do not convert number words to Arabic numerals when they are part of natural language and not intended to communicate a specific numeric value.

This includes idioms, determiner-like uses, conventional expressions, proper nouns, and many compounds.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "te falei mil vezes" | te falei mil vezes | te falei 1000 vezes |
| "um monte" | um monte | 1 monte |
| "de primeira" | de primeira | de 1a |
| "mais uma vez" | mais uma vez | mais 1 vez |
| "Os Três Mosqueteiros" as a title | Os Três Mosqueteiros | Os 3 Mosqueteiros |
| "Fórmula Um" as spoken title | Fórmula Um | Fórmula 1 |
| "Sete de Setembro" as a holiday | Sete de Setembro | 7 de Setembro |

When a disfluency occurs before a non-numeral expression, keep the disfluent portion as spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "u, um monte" | u- um monte | u- 1 monte |
| "mi, mil vezes" | mi- mil vezes | mi- 1000 vezes |

#### 6. Ordinals, Decades, and Age Ranges

Spell out ordinal expressions, decades, and age ranges as spoken. Preserve gender and number agreement.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "primeiro" | primeiro | 1o / 1º |
| "primeira vez" | primeira vez | 1a vez / 1ª vez |
| "segundo andar" | segundo andar | 2o andar / 2º andar |
| "décimo capítulo" | décimo capítulo | capítulo X / 10o capítulo |
| "vigésimo aniversário" | vigésimo aniversário | 20o aniversário |
| "anos setenta" | anos setenta | anos 70 |
| "década de noventa" | década de noventa | década de 90 |
| "pessoas de vinte a trinta anos" | pessoas de vinte a trinta anos | pessoas de 20 a 30 anos |
| "trintões" | trintões | gente de 30 |

Use the spoken form for official titles, laws, chapters, and product names unless a canonical written brand form is clearly intended.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Segunda Guerra Mundial" | Segunda Guerra Mundial | 2a Guerra Mundial |
| "Windows onze" | Windows onze | Windows 11 |
| "Galaxy S vinte e quatro" | Galaxy S vinte e quatro | Galaxy S24 |
| "PlayStation cinco" | PlayStation cinco | PlayStation 5 |

#### 7. Dates

Write dates as spoken Portuguese words. Do not convert day, month, or year into digits. Use `de` between day, month, and year as spoken; the day is normally read as a cardinal number except for the first day of the month, which is commonly read as `primeiro` in BR or `um` in PT.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "vinte e nove de abril de dois mil e vinte e quatro" | vinte e nove de abril de dois mil e vinte e quatro | 29 de abril de 2024 / 29/04/2024 |
| "primeiro de maio" in BR | primeiro de maio | 1 de maio / 1º de maio |
| "um de maio" in PT | um de maio | 1 de maio |
| "doze de dezembro de mil novecentos e noventa e sete" | doze de dezembro de mil novecentos e noventa e sete | 12 de dezembro de 1997 |
| "sete de setembro" | sete de setembro | 7 de setembro / 07/09 |
| "Dia das Mães" | Dia das Mães | Dia das Maes |

If the speaker reads a date digit by digit, preserve that digit-by-digit spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "zero sete barra zero nove" | zero sete barra zero nove | 07/09 |
| "dois zero dois quatro" as a year | dois zero dois quatro | 2024 |

#### 8. Time of Day

Write clock times as spoken Portuguese words. Include `da manhã`, `da tarde`, `da noite`, `da madrugada`, `meio-dia`, or `meia-noite` only if spoken. The expression `e meia` is common for `:30`; `e quinze` or `e um quarto` for `:15`; `quinze para` or `um quarto para` for `:45` (BR also uses `para as`).

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "duas e meia da tarde" | duas e meia da tarde | 2:30 PM / 14:30 |
| "duas e trinta" | duas e trinta | 2:30 |
| "uma e quarenta e cinco" | uma e quarenta e cinco | 1:45 |
| "quinze para as duas" | quinze para as duas | 1:45 |
| "catorze e trinta" | catorze e trinta | 14:30 |
| "meio-dia" | meio-dia | 12:00 |
| "meia-noite" | meia-noite | 0:00 / 24:00 |
| "das oito às cinco" | das oito às cinco | das 8 às 5 |
| "zero hora e quinze" | zero hora e quinze | 0:15 |

#### 9. Money / Currency

Spell out money and currency amounts as spoken Portuguese words. Preserve the currency name the speaker used (`real`, `reais`, `centavos`, `euro`, `euros`, `cêntimos` in PT or `centavos` in BR, `dólares`, `escudos` historically, etc.).

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cinquenta e dois reais" | cinquenta e dois reais | 52 reais / R$ 52 |
| "mil reais" | mil reais | 1.000 reais / R$1000 |
| "dois dólares e cinquenta centavos" | dois dólares e cinquenta centavos | $2.50 / 2 dólares e 50 centavos |
| "três e quarenta" as a price | três e quarenta | 3,40 / R$ 3,40 |
| "trinta ou quarenta reais" | trinta ou quarenta reais | 30 ou 40 reais |
| "um conto" as informal money in BR | um conto | mil reais, unless that was spoken |
| "uma pila" as informal money in PT | uma pila | um euro, unless that was spoken |

Do not normalize informal money words into exact currency if the amount or currency is not clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "uns trocados" | uns trocados | algumas moedas exatas |
| "nem um centavo" | nem um centavo | nem 1 centavo |

#### 10. Percentages

Spell out the number and the words `por cento`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "zero vírgula cinco por cento" | zero vírgula cinco por cento | 0,5% / 0.5% |
| "cem por cento" | cem por cento | 100% |
| "de vinte a trinta por cento" | de vinte a trinta por cento | de 20% a 30% |
| "meio por cento" | meio por cento | 0,5% |

#### 11. Measures / Units

Read the number as words and expand the unit abbreviation to its full spoken form. Preserve common spoken unit shortcuts when the speaker says them (for example, `quilo` for `quilograma`, `ka` for `K`, `ká-emê` for `km`).

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "cinco quilogramas" | cinco quilogramas | 5 kg / 5 quilogramas |
| "cinco quilos" | cinco quilos | 5 kg |
| "noventa quilômetros por hora" in BR | noventa quilômetros por hora | 90 km/h |
| "noventa quilómetros por hora" in PT | noventa quilómetros por hora | 90 km/h |
| "um metro e setenta" | um metro e setenta | 1,70 m / 1 metro e 70 |
| "oito bits" | oito bits | 8 bits |
| "quatro ka" | quatro ka | 4K |
| "cem watts" | cem watts | 100 W |
| "trinta graus Celsius" | trinta graus Celsius | 30 °C |
| "menos cinco graus" | menos cinco graus | -5 °C |

#### 12. Fractions, Ratios, and Scores

Spell out fractions, ratios, and scores as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "três quartos" | três quartos | 3/4 |
| "um quarto" | um quarto | 1/4 |
| "um e três quartos" | um e três quartos | 1 3/4 |
| "metade" | metade | 1/2 |
| "meio" as half | meio | 1/2 |
| "cinquenta cinquenta" | cinquenta cinquenta | 50:50 |
| "dois a um" as a score | dois a um | 2-1 / 2:1 |
| "três a dois" | três a dois | 3-2 |
| "placar de dois a zero" | placar de dois a zero | placar de 2-0 |

#### 13. Negative Numbers

Spell out negative numbers as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "menos doze" | menos doze | -12 / menos 12 |
| "dezoito graus negativos" | dezoito graus negativos | -18 graus / 18 graus negativos |
| "menos cinco graus" | menos cinco graus | -5 graus / menos 5 graus |
| "negativo três" | negativo três | -3 |

Use `menos` when the speaker says `menos`. Use `negativo` or `negativos` when the speaker says it.

#### 14. Phone Numbers, Postal Codes, IDs, and Codes

Read each digit group individually as spoken. Do not write formatted phone numbers, postal codes, or IDs with digits. Brazilian Portuguese commonly says `meia` for `6` in phone numbers; preserve that wording.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "onze nove oito sete seis cinco quatro três dois um" | onze nove oito sete seis cinco quatro três dois um | (11) 98765-4321 |
| "dois um três quatro cinco seis sete oito" | dois um três quatro cinco seis sete oito | 2134-5678 |
| "três meia meia oito nove zero" with `meia` for six | três meia meia oito nove zero | 366-890 / 3 6 6 8 9 0 |
| "CEP zero um três um zero traço cem" | CEP zero um três um zero traço cem | CEP 01310-100 |
| "código postal mil duzentos traço cento e cinquenta" in PT | código postal mil duzentos traço cento e cinquenta | código postal 1200-150 |
| "CPF um dois três ponto quatro cinco seis ponto sete oito nove traço zero zero" | CPF um dois três ponto quatro cinco seis ponto sete oito nove traço zero zero | CPF 123.456.789-00 |
| "a bê um dois três" | A B um dois três | AB123 |

#### 15. Electronic Text (URLs, Emails, IPs)

Read all symbols aloud. Do not write URLs, email addresses, IP addresses, usernames, or file paths in their compact written form.

| Symbol | Spoken As |
|--------|-----------|
| @ | arroba |
| . | ponto |
| / | barra |
| : | dois pontos |
| - | traço / hífen, as spoken |
| _ | underline / sublinhado, as spoken |
| # | cerquilha (BR) / cardinal (PT) / hashtag, as spoken |

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "example ponto com barra pricing" | example ponto com barra pricing | example.com/pricing |
| "globo ponto com" | globo ponto com | globo.com |
| "joão arroba gmail ponto com" | joão arroba gmail ponto com | joão@gmail.com |
| "cento e noventa e dois ponto cento e sessenta e oito ponto zero ponto um" | cento e noventa e dois ponto cento e sessenta e oito ponto zero ponto um | 192.168.0.1 |
| "usuário sublinhado vendas" | usuário sublinhado vendas | usuario_vendas |
| "dáblio dáblio dáblio ponto uol ponto com ponto bê erre" | dáblio dáblio dáblio ponto uol ponto com ponto bê erre | www.uol.com.br |

#### 16. Roman Numerals

Use the spoken title, regnal, ordinal, or cardinal form. Do not write Roman numerals in `Correct` unless the speaker is explicitly spelling the written symbol.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Star Wars episódio quatro" | Star Wars episódio quatro | Star Wars Episode IV |
| "GTA cinco" | GTA cinco | GTA V |
| "Dom Pedro segundo" | Dom Pedro segundo | Dom Pedro II |
| "Papa João Paulo segundo" | Papa João Paulo segundo | Papa João Paulo II |
| "século vinte e um" | século vinte e um | século XXI |
| "capítulo dez" | capítulo dez | capítulo X |
| "Luís catorze" | Luís catorze | Luís XIV |

#### 17. Abbreviations and Initialisms

Keep spoken acronyms and initialisms in their canonical form. Do not expand them unless the speaker says the expanded form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "NASA" as the acronym | NASA | Administração Nacional da Aeronáutica e Espaço |
| "efe bê i" | FBI | Departamento Federal de Investigação |
| "ibama" as a word | IBAMA | Instituto Brasileiro do Meio Ambiente e dos Recursos Naturais Renováveis |
| "ibgê" said as a word | IBGE | Instituto Brasileiro de Geografia e Estatística |
| "esse pê cê" | SPC | Serviço de Proteção ao Crédito |
| "esse u esse" | SUS | Sistema Único de Saúde |
| "Sistema Único de Saúde" | Sistema Único de Saúde | SUS |
| "esse cê u" | SCU | Structured Query Language |
| "esse cu ele" | SQL | Structured Query Language |

When pronunciation is ambiguous or important, `{PRO: ...}` is an acceptable superset annotation.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "óvni" as the acronym | OVNI | OVNI {PRO: óvni} |
| "ó vê ene i" spelled as letters | OVNI | OVNI {PRO: ó vê ene i} |

#### 18. Foreign Words and Loanwords

Loanwords and foreign words do not have a strict boundary, and some cases are gray areas. As a general rule, if a word is commonly used in everyday Portuguese, treat it as a Portuguese loanword or borrowed everyday word, not as a foreign-language span. Write established Portuguese forms in standard Portuguese orthography.

Do not mark established Portuguese loanwords as foreign words. Use the standard Portuguese spelling unless the speaker is clearly giving an official foreign spelling, URL, username, code, or other written form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "futebol" | futebol | <foreign> football </foreign> |
| "líder" | líder | <foreign> leader </foreign> |
| "marketing" as an everyday Portuguese loanword | marketing | <foreign> marketing </foreign> |
| "internet" | internet | <foreign> internet </foreign> |
| "uísque" in BR | uísque | <foreign> whiskey </foreign> |
| "sanduíche" | sanduíche | <foreign> sandwich </foreign> |
| "ok" or "okay" pronounced casually | ok | <foreign> okay </foreign> |
| "shopping" as everyday loanword | shopping | <foreign> shopping </foreign> |
| "delivery" as everyday loanword | delivery | <foreign> delivery </foreign> |
| "site" as everyday loanword | site | <foreign> site </foreign> |
| "mouse" for computer mouse | mouse | <foreign> mouse </foreign> |

Use the actual foreign spelling only when the speaker is clearly saying a foreign-language word or phrase as foreign speech, rather than using a Portuguese loanword. If your pipeline supports foreign-language tags, they may be added as a superset annotation.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "Thank you" clearly in English | Thank you | <foreign lang="EN"> Thank you </foreign> |
| "Merci" clearly in French | Merci | <foreign lang="FR"> Merci </foreign> |
| "Guten Morgen" clearly in German | Guten Morgen | <foreign lang="DE"> Guten Morgen </foreign> |
| "buongiorno" clearly in Italian | buongiorno | <foreign lang="IT"> buongiorno </foreign> |
| "gracias" clearly in Spanish | gracias | <foreign lang="ES"> gracias </foreign> |

If a word could be either a Portuguese loanword or foreign speech, choose based on how it is used and pronounced in context.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Portuguese loanword pronunciation | comi um sanduíche | comi um <foreign> sandwich </foreign> |
| English phrase pronunciation | sandwich, please | sanduíche, please |
| Official product or brand spelling is intended | comprei um iPhone | comprei um aifone, if `iPhone` is clearly intended |
| Ordinary Portuguesized product reference | comprei um celular | comprei um smartphone, if that was not spoken |

Proper nouns are not foreign-language spans just because they come from another language.

#### 19. Ambiguity

Rely on audio context to resolve ambiguous tokens.

| Context | Audio | Correct |
|---------|-------|---------|
| Clock time | "uma hora" | uma hora |
| Quantity | "uma pessoa" | uma pessoa |
| Natural expression | "mil obrigados" | mil obrigados |
| Proper noun | "Os Mutantes" | Os Mutantes |
| Acronym | "esse cu ele" | SQL |

Portuguese has homophones where the same pronunciation can map to different spellings depending on meaning. When pronunciation alone is ambiguous, use the surrounding meaning and context to choose the standard Portuguese written form.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Verb "to exist" | "há muitas pessoas" | há muitas pessoas | a muitas pessoas |
| Preposition | "vou a casa" | vou a casa | vou há casa |
| Time elapsed | "há dois anos" | há dois anos | a dois anos |
| Future direction | "daqui a dois dias" | daqui a dois dias | daqui há dois dias |
| Section / department | "seção de eletrônicos" | seção de eletrônicos | sessão de eletrônicos |
| Movie / meeting session | "sessão das oito" | sessão das oito | seção das oito |
| Legal transfer | "cessão de direitos" | cessão de direitos | sessão de direitos |
| Bad / wicked | "ele é mau" | ele é mau | ele é mal |
| Adverb "badly" | "ele canta mal" | ele canta mal | ele canta mau |
| Census | "censo demográfico" | censo demográfico | senso demográfico |
| Common sense | "senso comum" | senso comum | censo comum |
| Why (question) | "por que você foi?" | por que você foi? | porque você foi? |
| Because | "fui porque quis" | fui porque quis | fui por que quis |
| Reason (noun) | "não sei o porquê" | não sei o porquê | não sei o por quê |
| End-of-question | "você foi por quê?" | você foi por quê? | você foi por que? |
| Verb "to come" | "ele veio" | ele veio | ele vejo |
| Verb "to see" | "eu vejo" | eu vejo | eu veio |
| Verb form past | "eu vim ontem" | eu vim ontem | eu vi ontem |
| Verb form past | "eu vi o filme" | eu vi o filme | eu vim o filme |
| Conjunction "if" | "se ele vier" | se ele vier | si ele vier |
| Reflexive | "ele se machucou" | ele se machucou | ele si machucou |
| Reflexive plural | "elas se viram" | elas se viram | elas si viram |
| Verb "to go" 1pl future | "nós vamos" | nós vamos | nós vão |
| Music note | "a nota si" | a nota si | a nota se |

Use standard spelling for words that sound similar in casual speech. Do not write purely phonetic spellings when the intended standard word is clear.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| `está` reduced casually | "tá bom" | tá bom, if `tá` is the intended colloquial form | está bom, if `tá` was clearly spoken |
| `você` reduced casually | "cê vai?" | cê vai?, if `cê` is the intended colloquial form | você vai?, if `cê` was clearly spoken |
| `para` reduced casually | "vou pra casa" | vou pra casa, if `pra` is the intended colloquial form | vou para casa, if `pra` was clearly spoken |
| `para o` reduced casually | "vou pro mercado" | vou pro mercado, if `pro` is the intended colloquial form | vou para o mercado, if `pro` was clearly spoken |
| Standard word intended | "verdade" pronounced "verdade" with reduced `e` | verdade | verdadi |
| Standard word intended | "muito" pronounced casually | muito | muinto |
| Standard word intended | "também" pronounced casually | também | tambêi |

If multiple written forms are acceptable after context is considered, choose the form that best preserves the speaker's intended meaning and is most natural in Portuguese.

#### 20. Guidelines for Language-specific Issues

The following Portuguese-specific issues should follow the same principles above: preserve what was spoken, use standard Portuguese spelling when the intended word is clear, and do not invent unsupported written forms.

**Brazilian vs European Portuguese spelling and vocabulary:** Both BR and PT spellings are valid standard Portuguese. Choose the standard form for the speaker's variety. Do not silently convert one variety into the other.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| BR speaker: "ato" | ato | acto |
| PT speaker: "ato" | ato | acto, since the post-2009 reform also drops the silent c |
| BR speaker: "fato" | fato | facto |
| PT speaker: "facto" still pronounced with c | facto | fato |
| BR speaker: "Antônio" | Antônio | António |
| PT speaker: "António" | António | Antônio |
| BR speaker: "ônibus" | ônibus | autocarro / onibus |
| PT speaker: "autocarro" | autocarro | ônibus |
| BR speaker: "trem" | trem | comboio |
| PT speaker: "comboio" | comboio | trem |
| BR speaker: "bonde" | bonde | elétrico |
| PT speaker: "elétrico" as a tram | elétrico | bonde |
| BR speaker: "geladeira" | geladeira | frigorífico |
| PT speaker: "frigorífico" | frigorífico | geladeira |
| BR speaker: "açougue" | açougue | talho |
| PT speaker: "talho" | talho | açougue |

**Nasal vowels and tildes:** Always preserve the tilde for nasal vowels when the standard spelling requires it. Do not strip tildes from words like `não`, `mão`, `pão`, `irmã`, `coração`, `nações`, `põe`, or `mãe`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "não" | não | nao |
| "mão" | mão | mao |
| "irmã" | irmã | irma |
| "coração" | coração | coracao |
| "limões" | limões | limoes |
| "põe" | põe | poe |

**Open vs closed vowels (acute vs circumflex):** Use the standard accent that matches the intended word. The accent can change meaning.

| Context | Correct | Incorrect |
|---------|---------|-----------|
| First-person past "I traveled" | viajei | viagei |
| Adjective "secret" | secreto | secrêto |
| Verb "to read" past 3sg in BR | leu | lêu |
| Noun "color" | cor | côr |
| Verb "can" 3sg present | pode | pôde, if the present is intended |
| Verb "could" 3sg past | pôde | pode, if the past is intended |
| Verb "to put" 3sg present | põe | poe |
| Verb "to stop" 3sg present | para | pára, since the post-2009 reform drops the accent |
| Adverb "by, for" preposition | por | pôr, if the preposition is intended |
| Verb "to put" infinitive | pôr | por, if the infinitive verb is intended |

**Cedilla (`ç`):** Use `ç` only before `a`, `o`, or `u`, never before `e` or `i`. The cedilla is required when the standard spelling has it; do not replace `ç` with `c` or `s`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "moça" | moça | mossa / moca |
| "começo" | começo | comesso / comeco |
| "açúcar" | açúcar | assucar / acucar |
| "informação" | informação | informasao / informacao |
| "cabeça" | cabeça | cabessa / cabeca |

**Hyphenation:** Use the standard post-reform hyphenation for compounds. Common cases include `meio-dia`, `meia-noite`, `guarda-chuva`, `couve-flor`, `bem-vindo`, `super-homem`. Do not invent hyphens that the standard spelling no longer requires (for example, write `autoescola`, `antiaéreo`, `extraordinário` without a hyphen under the post-2009 rules).

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "meio-dia" | meio-dia | meio dia |
| "guarda-chuva" | guarda-chuva | guarda chuva / guardachuva |
| "bem-vindo" | bem-vindo | bem vindo / benvindo |
| "autoescola" | autoescola | auto-escola |
| "antiaéreo" | antiaéreo | anti-aéreo |

**Crase (`à`):** Use the grave accent on `à` only when standard Portuguese requires it (preposition `a` plus feminine article `a`). Do not invent crase where it is not warranted; do not omit it where it disambiguates meaning.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "vou à praia" | vou à praia | vou a praia |
| "à uma hora da tarde" | à uma hora da tarde | a uma hora da tarde |
| "vou a Roma" with no article | vou a Roma | vou à Roma |
| "às vezes" | às vezes | as vezes |
| "fui ao parque" | fui ao parque | fui à parque |

**Unknown proper-name spelling:** Portuguese names and business names may have official spellings (e.g., `Wilson`, `Wagner`, `Kátia`, `Klaus` in BR; `Filomena`, `Manuela` in PT). If the official spelling is not known from context, do not invent a special spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "Bruno" with no further context | Bruno | Brunno |
| "Vitor" or "Victor" - unknown spelling | Vitor | Victtor / Vyctor |
| "Itaú" as the bank | Itaú | Itau / ITAU |
| "Magalu" as the brand | Magalu | Magazine Luiza, unless `Magalu` was clearly spoken |
| Known official spelling | "iFood" said as a brand | iFood | ifood / Ifood, if the official capitalization is clearly intended |

**Onomatopoeia and lexical sound words:** Portuguese sound-symbolic words are lexical words. Transcribe them as words when spoken; do not replace them with non-speech tags.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "fez tchau" | fez tchau | fez [other-noise] |
| "toc toc na porta" | toc toc na porta | [other-noise] na porta |
| "miau, disse o gato" | miau, disse o gato | [other-noise], disse o gato |
| "hahaha que engraçado" as spoken laughter words | hahaha que engraçado | [laugh] que engraçado |
| "tchibum" diving sound | tchibum | [other-noise] |

---

## Part 2 - Disfluency

### Disfluency Rules

You are given an audio clip and its existing transcription. Your task is to output the transcription as provided, adding all speech disfluencies that you hear based on the rules below. Return only the transcription text.

#### 1. Filler Words

Words like "é", "ah", "eh", "hum", "tipo", "tipo assim", "tipo que", "então", "daí", "aí", "sabe", "né", "olha", "pô", "bem", "bom", "pois", and "pronto" should be added to the transcription when spoken. Keep lexical fillers as spoken, but standardize excessive elongation according to the canonical table below.

| Audio | Correct |
|-------|---------|
| "é, eu acho que sim" | é, eu acho que sim |
| "tipo, eu não sei" | tipo, eu não sei |
| "então, vamos começar" | então, vamos começar |
| "ah, entendi" | ah, entendi |
| "né, foi isso mesmo" | né, foi isso mesmo |

#### 2. Hesitation Markers and Vocal Fillers

Listen for **non-lexical vocalizations** during pauses, planning, and reactive listening. Standardize spellings to the canonical form for each group. Use normal Portuguese sentence spacing and punctuation.

**Filled pauses / hesitation** (speaker holds the floor, searching for words):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **é** | `é` | `ééé`, `é...`, when used as hesitation |
| **eh** | `eh` | `ehh`, `eh...`, hesitation breath |
| **ah** | `ah` | `ahhh`, `ah...` when used as filler |
| **hum** | `hum` | `humm`, `hummm`, thinking hum |
| **mmm** | `mmm` | thinking hum when lexical content is absent |
| **uhm** | `uhm` | `uhmm`, `uhm...` |
| **então** | `então` | `entãão`, when used as a filler |
| **tipo** | `tipo` | `tipoo`, when used as a filler |
| **tipo assim** | `tipo assim` | `tipo assiim` |
| **sabe** | `sabe` | `sabee`, when used as a filler |
| **né** | `né` | `nééé`, `né`, when used as a tag question filler |
| **pois** in PT | `pois` | `poiis`, when used as a filler |

**Backchannel / response** (listener signals agreement, negation, or reaction):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **sim** | `sim` | `siim`, `sim sim`, when a single acknowledgment is intended |
| **não** | `não` | `nãão`, when one response is intended |
| **aham** | `aham` | `ahamm`, affirmative response |
| **uhum** | `uhum` | `uhumm`, affirmative response |
| **hum-hum** | `hum-hum` | affirmative humming |
| **claro** | `claro` | `clarooo` |
| **certo** | `certo` | `certoo` |
| **tá** | `tá` | `táá` (BR colloquial acknowledgment) |
| **ok** | `ok` | `okay`, `okk`, when one acknowledgment is intended |
| **nossa** | `nossa` | `nossaa`, surprise reaction word |
| **ai** | `ai` | pain, surprise, or reaction word |
| **pô** in BR | `pô` | mild surprise or emphasis filler |

When the same phones could be **hesitation** vs **backchannel**, use audio and dialogue role: mid-utterance planning -> hesitation; short reactive assent while the other speaker talks -> backchannel.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Filled pause before content | é, amanhã eu vou | éé, amanhã eu vou |
| Thinking hum | hum, não sei | humm, não sei |
| Listener yes | sim, claro | siim, claro if only one acknowledgment |
| Acknowledgment in BR | tá, beleza | táá, beleza |
| Surprise | nossa, sério? | nossaa, sério? |
| Polite acknowledgment in PT | está bem | estaa bem |

#### 3. Repetitions

Consecutive instances of the same word or short phrase spoken unintentionally should be kept as-is with no added punctuation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "eu eu eu queria" | eu eu eu queria | eu- eu- eu queria / eu queria |
| "a a casa" | a a casa | a- a casa / a casa |
| "quero ir quero ir quero ir amanhã" | quero ir quero ir quero ir amanhã | quero ir- quero ir- quero ir amanhã / quero ir amanhã |
| "isso foi isso foi estranho" | isso foi isso foi estranho | isso foi- isso foi estranho / isso foi estranho |

If a repetition is intentional, rhythmic, or emphatic, use normal Portuguese punctuation instead of disfluency dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "sim, sim, vamos" | sim, sim, vamos | sim- sim- vamos |
| "não, não, não" | não, não, não | não- não- não |
| "calma, calma" | calma, calma | calma- calma |

#### 4. False Starts / Cut-Off Words

Incomplete words or phrases that the speaker abandons should be marked with a single dash followed by a space. If the speaker cuts off and stops entirely, still use a single dash.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "sorve- iogurte congelado" | sorve- iogurte congelado | sorvete iogurte congelado |
| "eu ia sa- onde a gente estava?" | eu ia sa- onde a gente estava? | eu ia sair, onde a gente estava? |
| "queria comprar um telefon-" | queria comprar um telefon- | queria comprar um telefone |
| "amanhã eu vo- não, depois" | amanhã eu vo- não, depois | amanhã eu vou, não, depois |

#### 5. Casual Forms, Slang, and Dialect

Use casual forms if that is how they were spoken and the form is clearly audible. If unsure, default to the standard dictionary spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "beleza" | beleza | tudo bem |
| "valeu" | valeu | obrigado, unless that was spoken |
| "massa" | massa | legal, unless that was spoken |
| "demais" as slang for "great" | demais | muito bom |
| "fixe" in PT | fixe | legal, unless that was spoken |
| "giro" in PT | giro | bonito, unless that was spoken |
| "bué" in PT | bué | muito, unless that was spoken |
| "uai" in mineiro speech | uai | nossa, unless that was spoken |
| "tchê" in gaúcho speech | tchê | cara, unless that was spoken |
| "bah" in gaúcho speech | bah | nossa, unless that was spoken |

Normalize pure phonetic reductions when the intended word is clear and the difference is only casual pronunciation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "tava" meaning "estava" | estava | tava, unless `tava` is the intended colloquial form |
| "tô" meaning "estou" | tô, if intended colloquial | estou, if `tô` was clearly spoken |
| "vô" meaning "vou" in casual reduction | vou | vô, unless intended as the kinship word `grandfather` |
| "muinto" meaning "muito" | muito | muinto |
| "menas" meaning "menos" (colloquial) | menos | menas, unless intentionally non-standard |

Do not rewrite dialectal or colloquial grammar into formal standard Portuguese if the form is a real spoken form and not merely a dropped sound.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "nóis vai" in colloquial BR | nóis vai | nós vamos |
| "tu sabe" in northeastern BR | tu sabe | tu sabes / você sabe |
| "vocês fica" colloquial | vocês fica | vocês ficam |
| "tem muitos carros" existential | tem muitos carros | há muitos carros, unless `há` was spoken |

#### 6. Spelled-Out Words

If a speaker spells out a non-acronym word one letter at a time using Latin letters, use capital letters separated with dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "se escreve M A S E G O" | se escreve M-A-S-E-G-O | se escreve M A S E G O |
| "soletra-se J O Ã O" | soletra-se J-O-Ã-O | soletra-se J O A O |

If a speaker spells out Portuguese letters with letter names, transcribe the letter names or letters as spoken. Do not infer a full word unless the speaker clearly provides it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "eme a ese a" | eme a ese a | masa |
| "cê a cê á" | cê a cê á | caçá |
| "cê com cedilha" | cê com cedilha | ç, unless the letter name was spoken that way |
| "a til" | a til | ã, unless the letter name was spoken that way |
| "o circunflexo" | o circunflexo | ô, unless the letter name was spoken that way |

If the speaker is saying an acronym or initialism, use the canonical acronym form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "efe bê i" | FBI | F-B-I |
| "u pê erre jota" | UPRJ | U-P-R-J |
| "esse u esse" | SUS | S-U-S |
| "nasa" said as a word | NASA | N-A-S-A |

#### 7. Mispronunciations

Transcribe intelligible real-word substitutions as spoken. Do not correct the word in the base transcript and do not add a tag unless your project uses superset `{MIS: ...}` annotations.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "casso" where "caço" was intended | casso | caço |
| "concerto" where "conserto" was intended by context | concerto | conserto |
| "pobrema" | pobrema | problema, unless using superset `problema {MIS: pobrema}` |
| "trabalio" for "trabalho" | trabalio | trabalho, unless using superset `trabalho {MIS: trabalio}` |
| "rúbrica" for "rubrica" stress shift | rúbrica | rubrica, unless using superset `rubrica {MIS: rúbrica}` |

If the sound is intelligible but not a real word and the intended word is unclear, transcribe the sound phonetically in Portuguese orthography.

| Audio | Correct |
|-------|---------|
| "trusquele" | trusquele |
| "framboji" | framboji |

#### 8. Wrong Grammar

Grammatical errors, dialectal grammar, and non-standard morphology should be faithfully captured. Do not correct them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "haviam muitas pessoas" | haviam muitas pessoas | havia muitas pessoas |
| "fazem dois anos" | fazem dois anos | faz dois anos |
| "para mim fazer isso" | para mim fazer isso | para eu fazer isso |
| "nóis vai" | nóis vai | nós vamos |
| "tu sabe" colloquial | tu sabe | tu sabes |
| "vossa mercê quer" historical | vossa mercê quer | você quer |

---

## Part 3 - Rich Transcription: Paralinguistic Tokens

### Non-Speech Sound Tokens

Bracket tokens mark **audible non-lexical or non-linguistic events** that are **not** regular words. Write each tag **exactly** as listed (square brackets included). Prefer **one tag per distinct event**; if several happen in sequence, repeat tags in **time order**, separated by spaces.

Use the NeMo canonical English tag names below, even in Portuguese transcripts.

#### Rules for this section

1. **Tag vs words** - If the speaker says a word, transcribe the word. Use a bracket tag only for the sound event itself.
2. **No invented words** - Do not replace a tag with a phonetic guess unless the sound is a lexical filler covered in Part 2.
3. **Placement** - Put the tag where the sound occurs in the word stream, usually as its own token between words.
4. **Overlap** - If a sound overlaps speech, place the tag at the start of the overlap window unless your time-aligned format specifies otherwise.
5. **Sequences** - Use `[laugh] [laugh]` for two separate laugh bursts, not a single stretched token.
6. **Unknown / generic background** - Use `[other-noise]` for audible non-speech you cannot classify; use `[unintelligible]` only when linguistic content was likely present but cannot be recovered.
7. **Minor mouth sounds** - Do not tag faint natural mouth clicks, lip noise, or routine breathing unless they are prominent or communicative.

#### Token list and descriptions

Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into Portuguese or replace them with local-language labels.

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
| Speaker laughs before speaking | [laugh] isso foi engraçado. | [risada] isso foi engraçado. |
| Speaker coughs mid-sentence | isso não é [cough] problema. | isso não é tosse problema. |
| Speech is masked and unrecoverable | acho que [unintelligible] amanhã. | acho que amanhã. |
| Background object noise | [other-noise] pode repetir? | [ruído] pode repetir? |
| Speaker sighs and continues | [sigh] enfim, vamos lá. | [suspiro] enfim, vamos lá. |
| Speaker yawns before speaking | [yawn] que sono. | [bocejo] que sono. |

#### Quick reference (canonical spellings)

- `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`, `[sniff]`, `[gasp]`, `[blow]`
- `[laugh]`, `[chuckle]`, `[giggle]`, `[snort]`, `[scoff]`, `[grunt]`, `[groan]`, `[cry]`
- `[hum-tune]`, `[whoop]`, `[whistle]`, `[tongue-click]`, `[tsk]`, `[lip-smack]`, `[teeth-suck]`, `[lip-trill]`, `[shush]`, `[swallow]`, `[clear-throat]`
- `[cough]`, `[sneeze]`, `[yawn]`, `[hiccup]`, `[unintelligible]`, `[other-noise]`
