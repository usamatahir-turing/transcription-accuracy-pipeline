# Japanese Transcription Guidelines

Language: Japanese (Japan)

## Part 1 - Text normalization

### Superset principle

The transcription rules below define the **minimum required coverage**. Annotation vendors are expected to deliver transcriptions that are a **superset** of these rules - any additional detail, markup, or tagging beyond what is specified here is encouraged and acceptable, as long as it does not contradict the rules.

Examples of acceptable superset additions include (but are not limited to):

- **Pronunciation variants** for acronyms or proper nouns annotated inline:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "SQL" said as "エスキューエル" | SQL {PRO: エスキューエル} |
| "SQL" said as "シークエル" | SQL {PRO: シークエル} |

- **Mispronunciation tags** to flag non-standard renderings:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "しゃしみ" intended as "刺身" | 刺身 {MIS: しゃしみ} |

- **Additional hesitation markers, dialect notes, confidence flags, or emotion tags** are acceptable as long as they do not alter the base transcription text.

In short: **do not remove detail that is present in the audio**. The rules below set the floor, not the ceiling.

---

### Text Normalization Rules

Transcribe the audio in standard Japanese orthography. Convert numeric, symbolic, and abbreviated tokens to their fully spoken Japanese form using the rules below. Return transcription only.

#### 1. Broad Principles

With the exception of acronyms, initialisms, and clearly intended proper-name spellings, everything should be written out in full spoken words. Abbreviations, symbols, shorthand, and numerals should all be expanded.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "株式会社" | 株式会社 | （株） |
| "キログラム" | キログラム | kg |
| "テレビ" | テレビ | TV |
| "パーソナルコンピューター" | パーソナルコンピューター | PC |
| "アイフォン十五" | アイフォン十五 | iPhone 15 |

Use standard Japanese spelling. Do not over-normalize into a form that changes what was spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "今日は会議です" | 今日は会議です | 今日わ会議です |
| "学校へ行きます" | 学校へ行きます | 学校え行きます |
| "それは違います" | それは違います | それわ違います |
| "できる" | できる | 出来る, if the speaker's style/context does not call for kanji |

#### 2. Japanese Script Choice: Kanji, Hiragana, Katakana, Latin Letters

Japanese has multiple writing systems. Choose the script that is most natural for standard Japanese while preserving what was spoken.

- Use **kanji** for common content words normally written in kanji.
- Use **hiragana** for particles, inflections, auxiliary verbs, function words, and words commonly written in hiragana.
- Use **katakana** for established loanwords, many foreign names written phonetically, sound-symbolic words when conventional, and technical terms commonly written in katakana.
- Use **Latin letters** for acronyms, initialisms, and official names only when the Latin spelling is clearly intended or conventional.
- Do not insert spaces between ordinary Japanese words. Use spaces only around inline tags or between clearly separate Latin-script tokens when needed.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "きょうは会議です" | 今日は会議です | きょうは会議です, if standard kanji is expected |
| "だいたい分かりました" | だいたい分かりました / 大体分かりました | だい体分かりました |
| "カフェに行きます" | カフェに行きます | cafeに行きます |
| "エフビーアイ" | FBI | エフ・ビー・アイ |
| "ユニバーサルスタジオジャパン" | ユニバーサルスタジオジャパン | USJ |

Use consistent character representation for the same word within the same speaker's transcript when multiple spellings are acceptable.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Same speaker uses the same word repeatedly | 大体 ... 大体 | 大体 ... だいたい |
| Different speakers naturally differ | Speaker 1: 大体 / Speaker 2: だいたい | Force both speakers into one spelling without context |

#### 3. Particles, Okurigana, and Inflections

Use standard particles and okurigana. Do not spell particles phonetically when standard written Japanese uses a different character.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "私は学生です" | 私は学生です | 私わ学生です |
| "学校へ行きます" | 学校へ行きます | 学校え行きます |
| "本を読む" | 本を読む | 本お読む |
| "話しています" | 話しています | 話して居ます, unless that style is required |
| "食べられる" | 食べられる | 食べれる, unless that is the grammar actually spoken |

When okurigana affects meaning or readability, use the standard form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "行った" | 行った | 行た |
| "分かる" | 分かる | 分る |
| "申し込む" | 申し込む | 申込む, unless the official noun form is intended |

#### 4. Numbers

Spell out all digits and numeric expressions as spoken Japanese words. Do not write Arabic numerals for transcription text.

Use kanji numerals, kana, or mixed standard Japanese spelling based on what best preserves the spoken form and is readable in context. If the reading itself matters, kana is acceptable.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "じゅうよん" | 十四 / じゅうよん | 14 |
| "れいてんれいご" | れい点れいご / 零点零五 | 0.05 |
| "せんさんじゅってんご" | 千三十点五 | 1,030.5 |
| "にせんにじゅうよん" | 二千二十四 | 2024 |
| "きゅうさんろくのいちいち" | 九三六の一一 | 936-11 |
| "きゅうまるにいちまる" | 九まる二一まる | 90210 |
| "マイナスじゅうに" | マイナス十二 | -12 |

Preserve the speaker's number reading when Japanese has multiple possible readings.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "よん" | よん | 四, if exact reading matters |
| "し" | し | よん |
| "なな" | なな | しち |
| "しち" | しち | なな |
| "まる" for zero | まる | ゼロ / 0 |
| "ゼロ" | ゼロ | まる / 0 |

#### 5. Non-Numeral Usage

Number words should be written out as words when they are part of natural speech and not intended to communicate a specific numeric value.

This includes idioms, determiner-like uses, conventional expressions, proper nouns, and approximate quantities.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "あなたは私にとって唯一の存在です" | あなたは私にとって唯一の存在です | あなたは私にとって唯1の存在です |
| "それが一番最後でした" | それが一番最後でした | それが1番最後でした |
| "まず第一に" | まず第一に | まず第1に |
| "一休さん" | 一休さん | 1休さん |
| "三代目 J SOUL BROTHERS" | 三代目 J SOUL BROTHERS | 3代目 J SOUL BROTHERS |
| "十数人" | 十数人 | 10数人 |
| "数千円" | 数千円 | 数1000円 |

When a disfluency occurs before a non-numeral expression, keep the disfluent portion as spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ひ ひ 一つ" | ひ ひ 一つ | ひ- ひ- 1つ |
| "い い 一番最後" | い い 一番最後 | い- い- 1番最後 |

#### 6. Ordinals, Counters, Decades, and Age Ranges

Spell out ordinal expressions, counters, decades, and age ranges as spoken Japanese words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "さんにん" | 三人 / さんにん | 3人 |
| "じゅうよんこ" | 十四個 / じゅうよんこ | 14個 |
| "ごじゅっしゅうねん" | 五十周年 / ごじゅっしゅうねん | 50周年 |
| "ななじゅうねんだい" | 七十年代 / ななじゅうねんだい | 70年代 |
| "にじゅうだい" | 二十代 / にじゅうだい | 20代 |
| "だいにじせかいたいせん" | 第二次世界大戦 | 第2次世界大戦 |

Use official spelling for titles and names only when the written form is clearly a proper title convention; otherwise preserve spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ウィンドウズ イレブン" | ウィンドウズ イレブン | Windows 11 |
| "楽天にじゅうよん" | 楽天二十四 / 楽天にじゅうよん | 楽天24 |
| "のぞみいちごう" | のぞみ一号 | のぞみ1号 |

#### 7. Dates

Write dates as spoken Japanese words. Do not convert year, month, or day into Arabic numerals.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "にせんにじゅうよねんしがつにじゅうくにち" | 二千二十四年四月二十九日 | 2024年4月29日 |
| "れいわろくねん" | 令和六年 | 令和6年 |
| "しがつついたち" | 四月一日 | 4月1日 |
| "くがつじゅういちにち" as spoken | 九月十一日 | 9月11日 / 9.11 |

If the speaker reads a date digit by digit, preserve that digit-by-digit spoken form.

#### 8. Time of Day

Write clock times as spoken Japanese words. Include 午前 / 午後 only if the speaker explicitly says it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ごごにじさんじゅっぷん" | 午後二時三十分 | 午後2時30分 / 2:30 PM |
| "ごごにじはん" | 午後二時半 | 午後2時半 / 午後2:30 |
| "いちじよんじゅうごふん" | 一時四十五分 | 1時45分 |
| "じゅうよじさんじゅっぷん" | 十四時三十分 | 14時30分 |
| "しょうご" | 正午 | 12:00 |
| "ごぜんれいじじゅうごふん" | 午前零時十五分 | 0:15 |
| "はちじからごじまで" | 八時から五時まで | 8時から5時まで |

#### 9. Money / Currency

Spell out money and currency amounts as spoken Japanese words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ごじゅうにえん" | 五十二円 / ごじゅうにえん | 52円 |
| "せんえん" | 千円 | 1000円 |
| "にドルごじゅっセント" | 二ドル五十セント | $2.50 / 2ドル50セント |
| "さんじゅうえん、よんじゅうえん" | 三十円、四十円 | 30円、40円 |
| "さん、よんじゅうえん" | 三、四十円 | 3、40円 |

Do not normalize informal money words into exact currency if the amount or currency is not clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "小銭" | 小銭 | 数円 |
| "一文無し" | 一文無し | 1円無し |

#### 10. Percentages

Spell out the number and the word `パーセント`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "れいてんごパーセント" | れい点五パーセント / 零点五パーセント | 0.5% |
| "ひゃくパーセント" | 百パーセント | 100% |
| "にじゅうからさんじゅっパーセント" | 二十から三十パーセント | 20%から30% |

#### 11. Measures / Units

Read the number as words and expand the unit abbreviation to its full spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ごキログラム" | 五キログラム / ごキログラム | 5kg / 5キログラム |
| "きゅうじゅっキロメートルまいじ" | 九十キロメートル毎時 | 90km/h |
| "いちメートルななじゅっセンチ" | 一メートル七十センチ | 1m70cm |
| "はちビット" | 八ビット | 8ビット |
| "よんけい" | よんけい | 4K |
| "ひゃくワット" | 百ワット | 100W / 100ワット |

#### 12. Fractions, Ratios, and Scores

Spell out fractions, ratios, and scores as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "よんぶんのさん" | 四分の三 / よんぶんのさん | 4分の3 / 3/4 |
| "いちとよんぶんのさん" | 一と四分の三 | 1と4分の3 / 1 3/4 |
| "にぶんのいち" | 二分の一 | 2分の1 / 1/2 |
| "ごじゅうたいごじゅう" | 五十対五十 | 50:50 / 50対50 |
| "にたいち" as a score | 二対一 | 2:1 / 2対1 |

#### 13. Negative Numbers

Spell out negative numbers as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "マイナスじゅうに" | マイナス十二 | -12 / マイナス12 |
| "れいかじゅうはちど" | 零下十八度 | -18度 / 零下18度 |
| "マイナスごど" | マイナス五度 | -5度 / マイナス5度 |

Use `マイナス` when the speaker says `マイナス`. Use `零下` when the speaker says `れいか`.

#### 14. Phone Numbers, Postal Codes, IDs, and Codes

Read each digit group individually as spoken. Do not write formatted phone numbers, postal codes, or IDs with digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ゼロサン、いちにさんよん、ごろくななはち" | ゼロサン、いちにさんよん、ごろくななはち | 03-1234-5678 |
| "きゅうさんろくのいちいち" | きゅうさんろくのいちいち | 936-11 |
| "きゅうまるにいちまる" | きゅうまるにいちまる | 90210 |
| "エービーいちにさん" | エービーいちにさん | AB123 |

#### 15. Electronic Text (URLs, Emails, IPs)

Read all symbols aloud. Do not write URLs, email addresses, IP addresses, usernames, or file paths in their compact written form.

| Symbol | Spoken As |
|--------|-----------|
| @ | アット |
| . | ドット / 点, as spoken |
| / | スラッシュ |
| : | コロン |
| - | ハイフン / ダッシュ, as spoken |

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "example ドット com スラッシュ pricing" | example ドット com スラッシュ pricing | example.com/pricing |
| "ネイバー ドット com" | ネイバー ドット com | naver.com |
| "john アット gmail ドット com" | john アット gmail ドット com | john@gmail.com |
| "いちきゅうに ドット いちろくはち ドット ゼロ ドット いち" | いちきゅうに ドット いちろくはち ドット ゼロ ドット いち | 192.168.0.1 |

#### 16. Roman Numerals

Use cardinal form after chapter/title keywords. Use ordinal or regnal spoken form after a person's name.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "スターウォーズ エピソード フォー" | スターウォーズ エピソード フォー | Star Wars Episode IV / スター・ウォーズ エピソード4 |
| "ファイナルファンタジー セブン" | ファイナルファンタジー セブン | FINAL FANTASY VII |
| "エリザベスにせい" | エリザベス二世 | エリザベス2世 / Elizabeth II |

#### 17. Abbreviations and Initialisms

Keep spoken acronyms and initialisms in their canonical form. Do not expand them unless the speaker says the expanded form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ナサ" | NASA | アメリカ航空宇宙局 |
| "エフビーアイ" | FBI | 連邦捜査局 |
| "ユーエスジェイ" | USJ | ユニバーサルスタジオジャパン |
| "ユニバーサルスタジオジャパン" | ユニバーサルスタジオジャパン | USJ |
| "エスキューエル" | SQL | Structured Query Language |

When pronunciation is ambiguous or important, `{PRO: ...}` is an acceptable superset annotation.

#### 18. Foreign Words and Loanwords

Loanwords and foreign words do not have a strict boundary, and some cases are gray areas. As a general rule, if a word is commonly used in everyday Japanese and is listed in standard Japanese dictionaries, treat it as a Japanese loanword, not as foreign speech. Write these words in the Japanese writing system, usually katakana.

Do not mark established Japanese loanwords as foreign words. Use the standard Japanese spelling unless the speaker is clearly giving an official Latin-script name, spelling, URL, username, code, or other written form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "カフェ" | カフェ | <foreign> cafe </foreign> |
| "コンピューター" | コンピューター | <foreign> computer </foreign> |
| "アイスクリーム" | アイスクリーム | <foreign> ice cream </foreign> |
| "オーケー" | オーケー | <foreign> okay </foreign> |
| "ミーティング" | ミーティング | <foreign> meeting </foreign> |
| "バス" | バス | <foreign> bus </foreign> |
| "チョコレート" | チョコレート | <foreign> chocolate </foreign> |
| "インターネット" | インターネット | <foreign> internet </foreign> |

Use the actual foreign spelling only when the speaker is clearly saying a foreign-language word or phrase as foreign speech, rather than using a Japanese loanword. If your pipeline supports foreign-language tags, they may be added as a superset annotation.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "Thank you" clearly in English | Thank you | <foreign lang="EN"> Thank you </foreign> |
| "Gracias" clearly in Spanish | Gracias | <foreign lang="ES"> Gracias </foreign> |
| "I love you" clearly in English | I love you | <foreign lang="EN"> I love you </foreign> |
| "bonjour" clearly in French | bonjour | <foreign lang="FR"> bonjour </foreign> |

If a word could be either a Japanese loanword or foreign speech, choose based on how it is used and pronounced in context.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Japanese loanword pronunciation | サンドイッチを食べました | sandwichを食べました |
| English phrase pronunciation | sandwich, please | サンドイッチ, please |
| Official product or brand spelling is intended | iPhoneを買いました | アイフォンを買いました, if the official written form is clearly intended |
| Ordinary Japanese loanword reference | アイフォンを買いました | iPhoneを買いました, if no Latin written form is intended |

Proper nouns are not foreign-language spans just because they come from another language.

#### 19. Ambiguity

Rely on audio context to resolve ambiguous tokens.

| Context | Audio | Correct |
|---------|-------|---------|
| Time | "いちじ" | 一時 / いちじ |
| Quantity | "いち" | 一 / いち |
| Natural expression | "一番いい" | 一番いい |
| Proper noun | "一休さん" | 一休さん |
| Acronym | "ジフ" used for image format | GIF |

Japanese has many homophones: the same pronunciation can map to different kanji, kana, or proper-name spellings. When pronunciation alone is ambiguous, use the surrounding meaning and context to choose the natural written Japanese form.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Park | "こうえんに行く" | 公園に行く | 講演に行く |
| Lecture | "こうえんを聞く" | 講演を聞く | 公園を聞く |
| Medical doctor | "いしに相談する" | 医師に相談する | 意思に相談する |
| Intention | "いしを確認する" | 意思を確認する | 医師を確認する |
| City | "しに住む" | 市に住む | 死に住む / 詩に住む |
| Death | "しを恐れる" | 死を恐れる | 市を恐れる / 詩を恐れる |
| Poem | "しを書く" | 詩を書く | 市を書く / 死を書く |

If multiple written forms are acceptable after context is considered, choose the form that best preserves the speaker's intended meaning and is most natural in Japanese.

#### 20. Guidelines for Language-specific Issues

The following Japanese-specific issues should follow the same principles above: preserve what was spoken, use standard Japanese orthography, do not invent unsupported detail, and choose the written form from context.

**Unknown proper-name kanji:** Japanese names often have many possible kanji for the same pronunciation. If the official spelling is not known from context, do not guess kanji; write the name in kana.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "しょうたさん" with unknown kanji | しょうたさん | 翔太さん, unless known |
| "ゆうこさん" with unknown kanji | ゆうこさん | 裕子さん, unless known |
| Known company/person spelling | 佐藤さん | さとうさん, if `佐藤` is known from context |

**Long vowels, small kana, and geminate consonants:** Preserve distinctions that change the word. Use standard spelling for long vowels, contracted sounds, and small `っ`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "おばあさん" | おばあさん | おばさん |
| "ビール" | ビール | ビル |
| "きって" meaning postage stamp | 切手 | 来て |
| "きゃく" meaning customer | 客 | きやく |

**Moraic nasal `ん`:** Write the standard `ん` even when its sound changes before different consonants.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "しんぶん" | 新聞 | しむぶん |
| "かんぱい" | 乾杯 | かむぱい |

**Irregular readings:** Some counters, dates, and age expressions have conventional readings. Preserve the reading that was spoken; do not normalize it into a different number form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ひとり" | 一人 / ひとり | いち人 / 1人 |
| "ふたり" | 二人 / ふたり | に人 / 2人 |
| "はたち" | 二十歳 / はたち | 二十さい / 20歳 |
| "ついたち" | 一日 / ついたち | いちにち, unless that was spoken |

**Onomatopoeia and mimetic words:** Japanese sound-symbolic words are lexical words. Transcribe them as words when spoken; do not replace them with non-speech tags.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "雨がザーザー降っている" | 雨がザーザー降っている | 雨が [other-noise] 降っている |
| "胸がドキドキする" | 胸がドキドキする | 胸が [heartbeat] する |
| "しーんとしている" | しーんとしている | [other-noise] としている |

**Japanese punctuation and spacing:** Do not insert spaces between ordinary Japanese words. Use `、` and `。` for Japanese punctuation when punctuation is needed. Spaces may be used only for repetitions, inline tags, or clearly separate Latin-script tokens.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Ordinary sentence | 今日は学校へ行きます | 今日 は 学校 へ 行きます |
| Repetition as spoken | 私 私 私も行きます | 私私私も行きます |
| Non-speech tag placement | それは [cough] 問題ないです | それは[cough]問題ないです |

---

## Part 2 - Disfluency

### Disfluency Rules

You are given an audio clip and its existing transcription. Your task is to output the transcription as provided, adding all speech disfluencies that you hear based on the rules below. Return only the transcription text.

#### 1. Filler Words

Words like "はい", "うん", "まあ", "あの", "えっと", "なんか", and "そうですね" should be added to the transcription when spoken. Keep lexical fillers as spoken, but standardize excessive elongation according to the canonical table below.

| Audio | Correct |
|-------|---------|
| "まあそうですね" | まあそうですね |
| "あの、ちょっと待ってください" | あの、ちょっと待ってください |
| "なんか違う気がします" | なんか違う気がします |

#### 2. Hesitation Markers and Vocal Fillers

Listen for **non-lexical vocalizations** during pauses, planning, and reactive listening. Standardize spellings to the canonical form for each group.

**Filled pauses / hesitation** (speaker holds the floor, searching for words):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **え** | `え` | `えー`, `ええー` when used as short hesitation |
| **ええ** | `ええ` | elongated agreement or thinking form when clearly `ええ` |
| **あ** | `あ` | `あー` when used as short hesitation |
| **ああ** | `ああ` | elongated realization or mild reaction when clearly `ああ` |
| **あの** | `あの` | `あのー`, `あのお` |
| **えっと** | `えっと` | `えっとー`, `えーっと` |
| **まあ** | `まあ` | `まぁ`, `まー` |
| **ま** | `ま` | shortened `まあ` when actually clipped |
| **うーん** | `うーん` | `うーーん`, `んー`, long nasal thinking sounds |
| **ふーん** | `ふーん` | `ふーーん` when used as mild reaction |

**Backchannel / response** (listener signals agreement, negation, or reaction):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **うん** | `うん` | `うーん` only when affirmative, not thinking |
| **はい** | `はい` | `はいー`, `はーい`, `はぃ` |
| **ええ** | `ええ` | polite affirmative response |
| **へえ** | `へえ` | `へー`, `へぇ` |
| **おお** | `おお` | `おー` |
| **いや** | `いや` | hesitation or disagreement marker when spoken |

When the same phones could be **hesitation** vs **backchannel**, use audio and dialogue role: mid-utterance planning -> hesitation; short reactive assent while the other speaker talks -> backchannel.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Filled pause before content | えっと、明日行きます | えーっと、明日行きます |
| Thinking / nasal mulling | うーん、それは難しいですね | んーー、それは難しいですね |
| Listener yes | うん、そうですね | うーん、そうですね if affirmative |
| Polite acknowledgment | はい、分かりました | はーい、分かりました |
| Mild surprise | あ、そうなんですね | あー、そうなんですね |

#### 3. Repetitions

Consecutive instances of the same word or short phrase spoken unintentionally should be kept as-is with no added punctuation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "私 私 私も" | 私 私 私も | 私- 私- 私も / 私も |
| "お 思います" | お 思います | お- 思います / 思います |
| "それは それは違います" | それは それは違います | それは- それは違います / それは違います |
| "私はほし 私はほし 私はもっと欲しい" | 私はほし 私はほし 私はもっと欲しい | 私はほし- 私はほし- 私はもっと欲しい / 私はもっと欲しい |

If a repetition is intentional, rhythmic, or emphatic, use normal Japanese punctuation instead of disfluency dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "いいよ、いいよ、一緒に行くよ" | いいよ、いいよ、一緒に行くよ | いいよ- いいよ- 一緒に行くよ |
| "そうだね、そうだね" | そうだね、そうだね | そうだね- そうだね |

#### 4. False Starts / Cut-Off Words

Incomplete words or phrases that the speaker abandons should be marked with a single dash followed by a space. If the speaker cuts off and stops entirely, still use a single dash.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "アイスクリ- フローズンヨーグルトです" | アイスクリ- フローズンヨーグルトです | アイスクリームフローズンヨーグルトです |
| "これから行こ- どこに行くんだっけ" | これから行こ- どこに行くんだっけ | これから行く、どこに行くんだっけ |
| "私が買おうとしていたのはアイスクリ-" | 私が買おうとしていたのはアイスクリ- | 私が買おうとしていたのはアイスクリーム |

#### 5. Casual Forms, Contractions, and Slang

Use casual forms if that is how they were spoken and the form is clearly audible. If unsure, default to the standard dictionary spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "してる" | してる | している |
| "そうっすね" | そうっすね | そうですね |
| "やっぱ" | やっぱ | やはり |
| "めっちゃ" | めっちゃ | とても |

Preserve colloquial reductions when they are real spoken forms. Do not expand them into formal Japanese.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "あざっす" in a casual context | あざっす | ありがとうございます |
| "すいません" | すいません | すみません |
| "なんつうか" | なんつうか | 何と言うか |

Do not rewrite dialectal or colloquial grammar into formal standard Japanese if the form is a real spoken form and not merely a dropped sound.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "行かへん" | 行かへん | 行かない |
| "見とる" | 見とる | 見ている |
| "食べれる" | 食べれる | 食べられる |

#### 6. Spelled-Out Words

If a speaker spells out a non-acronym word one letter at a time using Latin letters, use capital letters separated with dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "スペルは M A S E G O です" | スペルはM-A-S-E-G-Oです | スペルはM A S E G Oです |

If a speaker spells out Japanese kana or characters one by one, transcribe the character names or readings as spoken. Do not infer the full word unless the speaker clearly provides it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "ひらがなで あ い う" | ひらがなで あ-い-う | あいう, unless the intended string is explicitly stated |
| "カタカナで ア イ ス" | カタカナで ア-イ-ス | アイス, unless the intended word is explicitly stated |

If the speaker is saying an acronym or initialism, use the canonical acronym form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "エフビーアイ" | FBI | F-B-I |
| "ジーピーティー" | GPT | G-P-T |

#### 7. Mispronunciations

Transcribe intelligible real-word substitutions as spoken. Do not correct the word in the base transcript and do not add a tag unless your project uses superset `{MIS: ...}` annotations.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "この資料はポストがかかります" where "コスト" was intended | この資料はポストがかかります | この資料はコストがかかります |
| "分析用のメーターを渡す" where "データ" was intended | 分析用のメーターを渡す | 分析用のデータを渡す |
| "しゃしみ" | しゃしみ | 刺身, unless using superset `刺身 {MIS: しゃしみ}` |

If the sound is intelligible but not a real word and the intended word is unclear, transcribe the sound phonetically in kana.

| Audio | Correct |
|-------|---------|
| "ドープクロッグ" | ドープクロッグ |

#### 8. Wrong Grammar

Grammatical errors, dialectal grammar, and non-standard morphology should be faithfully captured. Do not correct them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "全然大丈夫じゃないです" | 全然大丈夫じゃないです | 全く大丈夫ではありません |
| "私が行けれると思った" | 私が行けれると思った | 私が行けると思った |
| "先生に言わさせてください" | 先生に言わさせてください | 先生に言わせてください |

---

## Part 3 - Rich Transcription: Paralinguistic Tokens

### Non-Speech Sound Tokens

Bracket tokens mark **audible non-lexical or non-linguistic events** that are **not** regular words. Write each tag **exactly** as listed (square brackets included). Prefer **one tag per distinct event**; if several happen in sequence, repeat tags in **time order**, separated by spaces.

Use the NeMo canonical English tag names below, even in Japanese transcripts.

#### Rules for this section

1. **Tag vs words** - If the speaker says a word, transcribe the word. Use a bracket tag only for the sound event itself.
2. **No invented words** - Do not replace a tag with a phonetic guess unless the sound is a lexical filler covered in Part 2.
3. **Placement** - Put the tag where the sound occurs in the word stream, usually as its own token between words.
4. **Overlap** - If a sound overlaps speech, place the tag at the start of the overlap window unless your time-aligned format specifies otherwise.
5. **Sequences** - Use `[laugh] [laugh]` for two separate laugh bursts, not a single stretched token.
6. **Unknown / generic background** - Use `[other-noise]` for audible non-speech you cannot classify; use `[unintelligible]` only when linguistic content was likely present but cannot be recovered.
7. **Minor mouth sounds** - Do not tag faint natural mouth clicks, lip noise, or routine breathing unless they are prominent or communicative.

#### Token list and descriptions

Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into Japanese or replace them with local-language labels.

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
| Speaker laughs before speaking | [laugh] それは面白いですね | [笑い] それは面白いですね |
| Speaker coughs mid-sentence | それは [cough] 問題ないと思います | それは咳問題ないと思います |
| Speech is masked and unrecoverable | それは [unintelligible] だと思います | それは だと思います |
| Background object noise | [other-noise] もう一度お願いします | [noise] もう一度お願いします |

#### Quick reference (canonical spellings)

- `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`, `[sniff]`, `[gasp]`, `[blow]`
- `[laugh]`, `[chuckle]`, `[giggle]`, `[snort]`, `[scoff]`, `[grunt]`, `[groan]`, `[cry]`
- `[hum-tune]`, `[whoop]`, `[whistle]`, `[tongue-click]`, `[tsk]`, `[lip-smack]`, `[teeth-suck]`, `[lip-trill]`, `[shush]`, `[swallow]`, `[clear-throat]`
- `[cough]`, `[sneeze]`, `[yawn]`, `[hiccup]`, `[unintelligible]`, `[other-noise]`
