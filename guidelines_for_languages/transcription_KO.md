# Korean Transcription Guidelines

Language: Korean (Korea)

## Part 1 - Text normalization

### Superset principle

The transcription rules below define the **minimum required coverage**. Annotation vendors are expected to deliver transcriptions that are a **superset** of these rules - any additional detail, markup, or tagging beyond what is specified here is encouraged and acceptable, as long as it does not contradict the rules.

Examples of acceptable superset additions include (but are not limited to):

- **Pronunciation variants** for acronyms or proper nouns annotated inline:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "SQL" said as "에스큐엘" | SQL {PRO: 에스큐엘} |
| "SQL" said as "시퀄" | SQL {PRO: 시퀄} |

- **Mispronunciation tags** to flag non-standard renderings:

| Audio | Acceptable (superset) |
|-------|----------------------|
| "김치" intended but pronounced "긴치" | 김치 {MIS: 긴치} |

- **Additional hesitation markers, dialect notes, confidence flags, or emotion tags** are acceptable as long as they do not alter the base transcription text.

In short: **do not remove detail that is present in the audio**. The rules below set the floor, not the ceiling.

---

### Text Normalization Rules

Transcribe the audio in standard Korean orthography. Convert numeric, symbolic, and abbreviated tokens to their fully spoken Korean form using the rules below. Return transcription only.

#### 1. Broad Principles

With the exception of acronyms and established proper-name spellings, everything should be written out in full spoken words. Abbreviations, symbols, shorthand, and numerals should all be expanded.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "김 선생님" | 김 선생님 | 김쌤, unless that is what was spoken |
| "킬로그램" | 킬로그램 | kg |
| "그리고" | 그리고 | & |
| "서울특별시" | 서울특별시 | 서울시, unless that is what was spoken |
| "아이폰 십오" | 아이폰 십오 | iPhone 15 |

Use standard spacing and spelling. Do not over-normalize into a form that changes spoken content.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "저는 학교에 갑니다" | 저는 학교에 갑니다 | 저 는 학교 에 갑니다 |
| "할 수 있다" | 할 수 있다 | 할수 있다 |
| "것 같아요" | 것 같아요 | 것같아요 |
| "서울역에서 만나요" | 서울역에서 만나요 | 서울 역 에서 만나요 |

#### 2. Korean Orthography and Spacing

Use standard Korean spelling and spacing:

- Write Korean words in **Hangul** unless a Latin-script form is the conventional spelling.
- Attach particles to the preceding word: `저는`, `학교에`, `친구와`.
- Separate auxiliary constructions and dependent nouns according to standard Korean spacing: `할 수 있다`, `먹은 것 같다`.
- Use conventional spacing for proper nouns and organization names.
- Do not imitate purely phonetic reductions when the intended standard word is clear and the difference is only casual pronunciation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "안냐세요" meaning "안녕하세요" | 안녕하세요 | 안냐세요 |
| "머라고" meaning "뭐라고" | 뭐라고 | 머라고 |
| "거에요" | 거예요 | 거에요 |
| "되요" | 돼요 | 되요 |
| "할게요" | 할게요 | 할께요 |

Preserve dialect or colloquial vocabulary when it is a real spoken form and not merely a spelling error.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "아이다" in dialect | 아이다 | 아니다 |
| "뭐라카노" | 뭐라카노 | 뭐라고 하니 |
| "겁나 좋다" | 겁나 좋다 | 매우 좋다 |

#### 3. Numbers

Spell out all digits and numeric expressions as spoken Korean words. Preserve the speaker's actual reading where Korean has more than one natural number system.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "열네" | 열네 | 14 |
| "십사" | 십사 | 14 |
| "영 점 영오" | 영 점 영오 | 0.05 |
| "천삼십 점 오" | 천삼십 점 오 | 1,030.5 |
| "이천이십사" | 이천이십사 | 2024 |
| "이공이사" | 이공이사 | 2024 |
| "구삼육 다시 일일" | 구삼육 다시 일일 | 936-11 |
| "마이너스 십이" | 마이너스 십이 | -12 |

#### 4. Native Korean and Sino-Korean Number Readings

Korean may use native Korean or Sino-Korean numerals depending on the counter and context. Transcribe the form that was spoken; do not convert one system into the other.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "두 명" | 두 명 | 이 명 / 2명 |
| "이 명" in a formal count | 이 명 | 두 명 / 2명 |
| "세 개" | 세 개 | 삼 개 / 3개 |
| "삼 개" in a serial or code-like context | 삼 개 | 세 개 / 3개 |
| "스무 살" | 스무 살 | 이십 살 / 20살 |

Do not change the grammatical form of the spoken counter. Preserve context in the surrounding Korean text.

#### 5. Non-Numeral Usage

Do not convert number words to Arabic numerals when they are part of natural language and not intended to communicate a specific numeric value.

This includes idioms, determiner-like uses, conventional expressions, proper nouns, and many compounds.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "너는 나한테 하나뿐인 사람이야" | 너는 나한테 하나뿐인 사람이야 | 너는 나한테 1뿐인 사람이야 |
| "일단 들어 봐" | 일단 들어 봐 | 1단 들어 봐 |
| "일석이조" | 일석이조 | 1석2조 |
| "삼성전자" | 삼성전자 | 3성전자 |
| "세븐틴" as a group name | 세븐틴 | 17 / seventeen |
| "원피스" as a title | 원피스 | 1피스 |

When a disfluency occurs before a non-numeral expression, keep the disfluent portion as spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "하, 하, 하나뿐" | 하- 하- 하나뿐 | 하- 하- 1뿐 |
| "이, 일단" | 이- 일단 | 이- 1단 |

#### 6. Ordinals, Counters, Decades, and Age Ranges

Spell out ordinal expressions, counters, decades, and age ranges as spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "첫 번째" | 첫 번째 | 1번째, unless a numbered list is being read |
| "두 번째" | 두 번째 | 2번째 / 둘째 if not spoken |
| "제삼 장" | 제삼 장 | 제3장 |
| "삼 명" | 삼 명 | 3명 / 세 명 |
| "세 명" | 세 명 | 3명 / 삼 명 |
| "칠십 년대" | 칠십 년대 | 70년대 |
| "이십 대" as an age range | 이십 대 | 20대 |

Use the official spelling for titles, laws, chapters, and product names.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "제이차 세계 대전" | 제이차 세계 대전 | 제2차 세계 대전 |
| "Windows eleven" | Windows eleven | Windows 11 |
| "갤럭시 S 이십사" | 갤럭시 S 이십사 | Galaxy S24 / 갤럭시 S24 |

#### 7. Dates

Write dates as spoken Korean words. Do not convert month, day, or year into digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "이천이십사 년 사 월 이십구 일" | 이천이십사 년 사 월 이십구 일 | 2024년 4월 29일 |
| "사 월 일 일" | 사 월 일 일 | 4월 1일 |
| "천구백구십칠 년 십이 월 십이 일" | 천구백구십칠 년 십이 월 십이 일 | 1997년 12월 12일 |
| "구 일일 테러" as spoken | 구 일일 테러 | 9.11 테러 / 9/11 테러 |

If the speaker reads a date digit by digit, preserve that digit-by-digit spoken form.

#### 8. Time of Day

Write clock times as spoken Korean words. Include `오전`, `오후`, `새벽`, `아침`, `저녁`, or `밤` only if spoken.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "오후 두 시 삼십 분" | 오후 두 시 삼십 분 | 2:30 PM / 오후 2시 30분 |
| "오후 두 시 반" | 오후 두 시 반 | 오후 2시 반 / 오후 2시 30분 |
| "한 시 사십오 분" | 한 시 사십오 분 | 1시 45분 |
| "열네 시 삼십 분" | 열네 시 삼십 분 | 14시 30분 |
| "정오" | 정오 | 12:00 |
| "자정" | 자정 | 0:00 |
| "여덟 시부터 다섯 시까지" | 여덟 시부터 다섯 시까지 | 8시부터 5시까지 |
| "두 시 삼십" while reading "2:30" | 두 시 삼십 | 2:30 |
| "영 시 십오 분" | 영 시 십오 분 | 0:15 |

#### 9. Money / Currency

Spell out money and currency amounts as spoken Korean words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "오십이 원" | 오십이 원 | 52원 |
| "천 원" | 천 원 | 1,000원 |
| "이 달러 오십 센트" | 이 달러 오십 센트 | 2달러 50센트 / $2.50 |
| "삼십 원, 사십 원" | 삼십 원, 사십 원 | 30원, 40원 |
| "삼사십 원" | 삼사십 원 | 30-40원 / 3, 40원 |

Do not normalize informal money words into exact currency if the amount or currency is not clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "몇 푼" | 몇 푼 | 몇 원 |
| "한 푼도 없어" | 한 푼도 없어 | 1원도 없어 |

#### 10. Percentages

Spell out the number and the word `퍼센트`.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "영 점 오 퍼센트" | 영 점 오 퍼센트 | 0.5% |
| "백 퍼센트" | 백 퍼센트 | 100% |
| "이십에서 삼십 퍼센트" | 이십에서 삼십 퍼센트 | 20%에서 30% |

#### 11. Measures / Units

Read the number as words and expand the unit abbreviation to its full spoken form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "오 킬로그램" | 오 킬로그램 | 5kg / 5킬로그램 |
| "오 케이지" | 오 케이지 | 5kg |
| "구십 킬로미터 매 시간" | 구십 킬로미터 매 시간 | 90km/h |
| "일 미터 칠십 센티" | 일 미터 칠십 센티 | 1미터 70센티 / 1m 70cm |
| "팔 비트" | 팔 비트 | 8비트 |
| "포케이" | 포케이 | 4K |
| "백 와트" | 백 와트 | 100W / 100와트 |

#### 12. Fractions, Ratios, and Scores

Spell out fractions, ratios, and scores as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "사 분의 삼" | 사 분의 삼 | 4분의 3 / 3/4 |
| "일과 사 분의 삼" | 일과 사 분의 삼 | 1과 4분의 3 / 1 3/4 |
| "이 분의 일" | 이 분의 일 | 2분의 1 / 1/2 |
| "오십 대 오십" | 오십 대 오십 | 50:50 / 50 대 50 |
| "이 대 일" as a score | 이 대 일 | 2:1 / 2 대 1 |

#### 13. Negative Numbers

Spell out negative numbers as spoken words.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "마이너스 십이" | 마이너스 십이 | -12 / 마이너스 12 |
| "영하 십팔 도" | 영하 십팔 도 | 영하 18도 / -18도 |
| "마이너스 오 도" | 마이너스 오 도 | -5도 / 마이너스 5도 |

Use `마이너스` when the speaker says `마이너스`. Use `영하` when the speaker says `영하`.

#### 14. Phone Numbers, Postal Codes, IDs, and Codes

Read each digit group individually as spoken. Do not write formatted phone numbers, postal codes, or IDs with digits.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "공일공 일이삼사 오육칠팔" | 공일공 일이삼사 오육칠팔 | 010-1234-5678 |
| "구삼육 다시 일일" | 구삼육 다시 일일 | 936-11 |
| "우편번호 영사오이사" | 우편번호 영사오이사 | 우편번호 04524 |
| "에이비 일이삼" | 에이비 일이삼 | AB123 |

#### 15. Electronic Text (URLs, Emails, IPs)

Read all symbols aloud. Do not write URLs, email addresses, IP addresses, usernames, or file paths in their compact written form.

| Symbol | Spoken As |
|--------|-----------|
| @ | 골뱅이 / 앳, as spoken |
| . | 점 / 닷, as spoken |
| / | 슬래시 |
| : | 콜론 |
| - | 대시 / 하이픈, as spoken |

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "example 점 com 슬래시 pricing" | example 점 com 슬래시 pricing | example.com/pricing |
| "네이버 점 com" | 네이버 점 com | naver.com |
| "john 골뱅이 gmail 점 com" | john 골뱅이 gmail 점 com | john@gmail.com |
| "일구이 점 일육팔 점 영 점 일" | 일구이 점 일육팔 점 영 점 일 | 192.168.0.1 |

#### 16. Roman Numerals

Use cardinal form after chapter/title keywords. Use ordinal or dynasty/regnal spoken form after a person's name.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "스타워즈 에피소드 포" | 스타워즈 에피소드 포 | Star Wars Episode IV / 스타워즈 에피소드 IV |
| "GTA 파이브" | GTA 파이브 | GTA V |
| "엘리자베스 이세" | 엘리자베스 이세 | 엘리자베스 2세 / Elizabeth II |

#### 17. Abbreviations and Initialisms

Keep spoken acronyms and initialisms in their canonical form. Do not expand them unless the speaker says the expanded form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "나사" as NASA | NASA | 미국 항공 우주국 |
| "에프비아이" | FBI | 연방수사국 |
| "케이티엑스" | KTX | 한국고속철도 |
| "에스큐엘" | SQL | Structured Query Language |
| "구조적 질의 언어" | 구조적 질의 언어 | SQL |

When pronunciation is ambiguous or important, `{PRO: ...}` is an acceptable superset annotation.

#### 18. Foreign Words and Loanwords

Loanwords and foreign words do not have a strict boundary, and some cases are gray areas. As a general rule, if a word is commonly used in everyday Korean and is listed in standard Korean dictionaries, treat it as a Korean loanword, not as foreign speech. Write these words in the Korean writing system (Hangul).

Do not mark established Korean loanwords as foreign words. Use the standard Hangul spelling unless the speaker is clearly giving an official Latin-script name, spelling, URL, username, code, or other written form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "카페" | 카페 | <foreign> cafe </foreign> |
| "컴퓨터" | 컴퓨터 | <foreign> computer </foreign> |
| "아이스크림" | 아이스크림 | <foreign> ice cream </foreign> |
| "오케이" | 오케이 | <foreign> okay </foreign> |
| "미팅" | 미팅 | <foreign> meeting </foreign> |
| "버스" | 버스 | <foreign> bus </foreign> |
| "초콜릿" | 초콜릿 | <foreign> chocolate </foreign> |
| "인터넷" | 인터넷 | <foreign> internet </foreign> |

Use the actual foreign spelling only when the speaker is clearly saying a foreign-language word or phrase as foreign speech, rather than using a Korean loanword. If your pipeline supports foreign-language tags, they may be added as a superset annotation.

| Audio | Correct | Acceptable Superset |
|-------|---------|---------------------|
| "Thank you" clearly in English | Thank you | <foreign lang="EN"> Thank you </foreign> |
| "Gracias" clearly in Spanish | Gracias | <foreign lang="ES"> Gracias </foreign> |
| "I love you" clearly in English | I love you | <foreign lang="EN"> I love you </foreign> |
| "bonjour" clearly in French | bonjour | <foreign lang="FR"> bonjour </foreign> |

If a word could be either a Korean loanword or foreign speech, choose based on how it is used and pronounced in context.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Korean loanword pronunciation | 샌드위치 먹었어요 | sandwich 먹었어요 |
| English phrase pronunciation | sandwich, please | 샌드위치, please |
| Official product or brand spelling is intended | iPhone 샀어요 | 아이폰 샀어요, if the official written form is clearly intended |
| Ordinary Koreanized product reference | 아이폰 샀어요 | iPhone 샀어요, if no Latin written form is intended |

Proper nouns are not foreign-language spans just because they come from another language.

#### 19. Ambiguity

Rely on audio context to resolve ambiguous tokens.

| Context | Audio | Correct |
|---------|-------|---------|
| Time | "두 시" | 두 시 |
| Quantity | "두 개" | 두 개 |
| Natural expression | "하나뿐" | 하나뿐 |
| Proper noun | "세븐틴" | 세븐틴 |
| Acronym | "에스큐엘" | SQL |

Korean has homophones where the same pronunciation can map to different spellings depending on meaning. When pronunciation alone is ambiguous, use the surrounding meaning and context to choose the standard Korean written form.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Tree | "나무를 심었어요" | 나무를 심었어요 | 남우를 심었어요 |
| Actor | "그 남우가 유명해요" | 그 남우가 유명해요 | 그 나무가 유명해요 |
| Number two | "이 번" | 이 번 | 이번 |
| This time | "이번" | 이번 | 이 번 |
| Oyster | "굴을 먹어요" | 굴을 먹어요 | 구를 먹어요 |
| Cave | "굴에 들어가요" | 굴에 들어가요 | 구레 들어가요 |
| Dog | "개가 짖어요" | 개가 짖어요 | 게가 짖어요 |
| Crab | "게를 먹어요" | 게를 먹어요 | 개를 먹어요 |

Use standard spelling for words that sound similar in casual speech. Do not write purely phonetic spellings when the intended standard word is clear.

| Context | Audio | Correct | Incorrect |
|---------|-------|---------|-----------|
| Greeting | "안녕하세요" casually pronounced "안냐세요" | 안녕하세요 | 안냐세요 |
| Question word | "뭐라고" casually pronounced "머라고" | 뭐라고 | 머라고 |
| Polite ending | "거예요" | 거예요 | 거에요 |
| Verb form | "돼요" | 돼요 | 되요 |

If multiple written forms are acceptable after context is considered, choose the form that best preserves the speaker's intended meaning and is most natural in Korean.

#### 20. Guidelines for Language-specific Issues

The following Korean-specific issues should follow the same principles above: preserve what was spoken, use standard Korean spelling and spacing when the intended word is clear, and do not invent unsupported written forms.

**Systematic pronunciation changes vs standard spelling:** Korean pronunciation often changes through liaison, batchim neutralization, nasalization, and tensification. Write the standard spelling, not the surface pronunciation, when the intended word is clear.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "꼬치" meaning "꽃이" | 꽃이 | 꼬치 |
| "궁물" meaning "국물" | 국물 | 궁물 |
| "멍는" meaning "먹는" | 먹는 | 멍는 |
| "가치" meaning "같이" | 같이 | 가치 |

**Spacing that changes meaning:** Use context to choose the correct Korean spacing when spacing changes meaning or grammar.

| Context | Correct | Incorrect |
|---------|---------|-----------|
| Cannot do something | 못 하다 | 못하다, if the meaning is inability to perform an action |
| Is bad at something | 못하다 | 못 하다, if the meaning is poor quality or lack of skill |
| One occurrence | 한 번 가 봤어요 | 한번 가 봤어요 |
| Casual "try doing" expression | 한번 해 보세요 | 한 번 해 보세요, if no literal count is intended |
| Process succeeds | 잘되다 | 잘 되다, if used as one lexical verb |
| Only / nothing but | 이것밖에 없어요 | 이것 밖에 없어요 |

**Unknown proper-name spelling:** Korean names and business names may have official spellings. If the official spelling is not known from context, do not invent a special spelling or Latin form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "민지 씨" with no official spelling given | 민지 씨 | Minji 씨 / 민智 씨 |
| "하나 회사" with no brand spelling given | 하나 회사 | HANA 회사, unless the official Latin spelling is known |
| Known official spelling | HYBE에 갔어요 | 하이브에 갔어요, if `HYBE` is clearly intended |

**Compound words and 사이시옷:** Spoken form may not make compound spelling obvious. Use context and standard dictionary spelling for compounds, including 사이시옷.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "나문닙" meaning tree leaf | 나뭇잎 | 나무잎 / 나문닙 |
| "해삗" meaning sunlight | 햇빛 | 해빛 / 해삗 |
| "회쑤" meaning number of times | 횟수 | 회수, if `횟수` is meant |
| "깬닙" meaning perilla leaf | 깻잎 | 깨잎 / 깬닙 |

**Onomatopoeia and mimetic words:** Korean sound-symbolic words are lexical words. Transcribe them as words when spoken; do not replace them with non-speech tags.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "쿵 소리가 났어요" | 쿵 소리가 났어요 | [other-noise] 소리가 났어요 |
| "문이 쾅 닫혔어요" | 문이 쾅 닫혔어요 | 문이 [other-noise] 닫혔어요 |
| "반짝반짝 빛나요" | 반짝반짝 빛나요 | [other-noise] 빛나요 |
| "가슴이 두근두근해요" | 가슴이 두근두근해요 | 가슴이 [heartbeat] 해요 |

**Sentence-final endings and politeness forms:** Preserve the spoken ending and speech style, but use standard spelling when the intended form is clear. Do not replace casual or dialectal endings with formal standard Korean.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "거예요" | 거예요 | 거에요 |
| "아니에요" | 아니에요 | 아니예요 |
| "맞죠" | 맞죠 | 맞지요, unless that was spoken |
| "맞지요" | 맞지요 | 맞죠 |
| "했어여" as an intentional casual spelling/style | 했어여 | 했어요, if the casual ending is clearly intended |

---

## Part 2 - Disfluency

### Disfluency Rules

You are given an audio clip and its existing transcription. Your task is to output the transcription as provided, adding all speech disfluencies that you hear based on the rules below. Return only the transcription text.

#### 1. Filler Words

Words like "어", "음", "아", "저", "그", "뭐", "그러니까", "이제", "막", and "약간" should be added to the transcription when spoken. Keep lexical fillers as spoken, but standardize excessive elongation according to the canonical table below.

| Audio | Correct |
|-------|---------|
| "어, 저는 잘 모르겠어요" | 어, 저는 잘 모르겠어요 |
| "음, 그건 아닌 것 같아요" | 음, 그건 아닌 것 같아요 |
| "그러니까 다시 말하면" | 그러니까 다시 말하면 |

#### 2. Hesitation Markers and Vocal Fillers

Listen for **non-lexical vocalizations** during pauses, planning, and reactive listening. Standardize spellings to the canonical form for each group. Use normal Korean sentence spacing and punctuation.

**Filled pauses / hesitation** (speaker holds the floor, searching for words):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **어** | `어` | `어어`, `어...`, `어어어` when used as hesitation |
| **음** | `음` | `으음`, `음음`, `음...` |
| **아** | `아` | `아아`, `아...` when used as realization or hesitation |
| **에** | `에` | `에에`, formal hesitation |
| **저** | `저` | `저기` when used as a hesitation may be kept as `저기` |
| **그** | `그` | `그...` when used as a hesitation |
| **뭐** | `뭐` | `뭐어`, `머` when used as filler |
| **그러니까** | `그러니까` | `그니까`, if the project normalizes to standard form |

**Backchannel / response** (listener signals agreement, negation, or reaction):

| Group | Canonical form | Typical variants to normalize |
|-------|----------------|-------------------------------|
| **응** | `응` | `응응`, affirmative response when not repeated intentionally |
| **네** | `네` | `네에`, `네네` when a single acknowledgment is intended |
| **예** | `예` | `예에` |
| **아하** | `아하` | `아하아` |
| **어휴** | `어휴` | `어휴우` |
| **아이고** | `아이고` | `아이고오` |
| **흠** | `흠` | `흐음`, thinking sound |

When the same phones could be **hesitation** vs **backchannel**, use audio and dialogue role: mid-utterance planning -> hesitation; short reactive assent while the other speaker talks -> backchannel.

| Situation | Correct | Incorrect |
|-----------|---------|-----------|
| Filled pause before content | 어, 내일 갈게요 | 어어, 내일 갈게요 |
| Thinking hum | 음, 그건 어렵네요 | 음음, 그건 어렵네요 |
| Listener yes | 응, 맞아요 | 응응, 맞아요 if only one acknowledgment |
| Polite acknowledgment | 네, 알겠습니다 | 네에, 알겠습니다 |
| Surprise | 아, 진짜요? | 아아, 진짜요? |

#### 3. Repetitions

Consecutive instances of the same word or short phrase spoken unintentionally should be kept as-is with no added punctuation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "저 저 저는" | 저 저 저는 | 저- 저- 저는 / 저는 |
| "그 그게" | 그 그게 | 그- 그게 / 그게 |
| "저는 가 저는 가 저는 가고 싶어요" | 저는 가 저는 가 저는 가고 싶어요 | 저는 가- 저는 가- 저는 가고 싶어요 / 저는 가고 싶어요 |
| "그건 정말 그건 정말 이상했어요" | 그건 정말 그건 정말 이상했어요 | 그건 정말- 그건 정말 이상했어요 / 그건 정말 이상했어요 |

If a repetition is intentional, rhythmic, or emphatic, use normal Korean punctuation instead of disfluency dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "그래, 그래, 같이 가자" | 그래, 그래, 같이 가자 | 그래- 그래- 같이 가자 |
| "맞아, 맞아" | 맞아, 맞아 | 맞아- 맞아 |

#### 4. False Starts / Cut-Off Words

Incomplete words or phrases that the speaker abandons should be marked with a single dash followed by a space. If the speaker cuts off and stops entirely, still use a single dash.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "아이스크- 프로즌 요거트요" | 아이스크- 프로즌 요거트요 | 아이스크림 프로즌 요거트요 |
| "제가 가려- 어디 가려고 했죠?" | 제가 가려- 어디 가려고 했죠? | 제가 가려고, 어디 가려고 했죠? |
| "제가 아이스크-" | 제가 아이스크- | 제가 아이스크림 |

#### 5. Casual Forms, Slang, and Dialect

Use casual forms if that is how they were spoken and the form is clearly audible. If unsure, default to the standard dictionary spelling.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "뭐야" | 뭐야 | 무엇이야 |
| "그니까" | 그니까 | 그러니까, unless the project normalizes this filler |
| "엄청" | 엄청 | 매우 |
| "대박" | 대박 | 굉장함 |
| "아니거든" | 아니거든 | 아닙니다 |

Normalize pure phonetic reductions when the intended word is clear and the difference is only casual pronunciation.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "안냐세요" | 안녕하세요 | 안냐세요 |
| "머라고" | 뭐라고 | 머라고 |
| "일케" | 이렇게 | 일케, unless intentionally slang in context |

Do not rewrite dialectal or colloquial grammar into formal standard Korean if the form is a real spoken form and not merely a dropped sound.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "뭐라카노" | 뭐라카노 | 뭐라고 하니 |
| "아이다" | 아이다 | 아니다 |
| "했당께" | 했당께 | 했다고 |

#### 6. Spelled-Out Words

If a speaker spells out a non-acronym word one letter at a time using Latin letters, use capital letters separated with dashes.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "스펠링은 M A S E G O예요" | 스펠링은 M-A-S-E-G-O예요 | 스펠링은 M A S E G O예요 |

If a speaker spells out Korean jamo, transcribe the jamo names or letters as spoken. Do not infer a full Korean word unless the speaker clearly provides it.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "기역 이응 미음" | 기역 이응 미음 | 김 |
| "ㄱ ㅣ ㅁ" | ㄱ-ㅣ-ㅁ | 김, unless the intended word is explicitly stated |

If the speaker is saying an acronym or initialism, use the canonical acronym form.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "에프비아이" | FBI | F-B-I |
| "케이티엑스" | KTX | K-T-X |

#### 7. Mispronunciations

Transcribe intelligible real-word substitutions as spoken. Do not correct the word in the base transcript and do not add a tag unless your project uses superset `{MIS: ...}` annotations.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "바다" where "받아" was intended | 바다 | 받아 |
| "사과" where "사가" was intended by context | 사과 | 사가 |
| "긴치" | 긴치 | 김치, unless using superset `김치 {MIS: 긴치}` |

If the sound is intelligible but not a real word and the intended word is unclear, transcribe the sound phonetically in Hangul.

| Audio | Correct |
|-------|---------|
| "도르프클로그" | 도르프클로그 |

#### 8. Wrong Grammar

Grammatical errors, dialectal grammar, and non-standard morphology should be faithfully captured. Do not correct them.

| Audio | Correct | Incorrect |
|-------|---------|-----------|
| "나 어제 학교 갔어야 됐었어" | 나 어제 학교 갔어야 됐었어 | 나 어제 학교에 갔어야 했어 |
| "이거 내가 할 수 있어요?" | 이거 내가 할 수 있어요? | 제가 이것을 할 수 있나요? |
| "밥 먹었냐요" | 밥 먹었냐요 | 밥 먹었나요 |

---

## Part 3 - Rich Transcription: Paralinguistic Tokens

### Non-Speech Sound Tokens

Bracket tokens mark **audible non-lexical or non-linguistic events** that are **not** regular words. Write each tag **exactly** as listed (square brackets included). Prefer **one tag per distinct event**; if several happen in sequence, repeat tags in **time order**, separated by spaces.

Use the NeMo canonical English tag names below, even in Korean transcripts.

#### Rules for this section

1. **Tag vs words** - If the speaker says a word, transcribe the word. Use a bracket tag only for the sound event itself.
2. **No invented words** - Do not replace a tag with a phonetic guess unless the sound is a lexical filler covered in Part 2.
3. **Placement** - Put the tag where the sound occurs in the word stream, usually as its own token between words.
4. **Overlap** - If a sound overlaps speech, place the tag at the start of the overlap window unless your time-aligned format specifies otherwise.
5. **Sequences** - Use `[laugh] [laugh]` for two separate laugh bursts, not a single stretched token.
6. **Unknown / generic background** - Use `[other-noise]` for audible non-speech you cannot classify; use `[unintelligible]` only when linguistic content was likely present but cannot be recovered.
7. **Minor mouth sounds** - Do not tag faint natural mouth clicks, lip noise, or routine breathing unless they are prominent or communicative.

#### Token list and descriptions

Use the English token spellings exactly as listed below for all languages. Do not translate these bracket tokens into Korean or replace them with local-language labels.

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
| Speaker laughs before speaking | [laugh] 그거 웃기네요. | [웃음] 그거 웃기네요. |
| Speaker coughs mid-sentence | 그건 [cough] 문제없어요. | 그건 기침 문제없어요. |
| Speech is masked and unrecoverable | 그건 [unintelligible] 같아요. | 그건 같아요. |
| Background object noise | [other-noise] 다시 말씀해 주세요. | [소음] 다시 말씀해 주세요. |

#### Quick reference (canonical spellings)

- `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`, `[sniff]`, `[gasp]`, `[blow]`
- `[laugh]`, `[chuckle]`, `[giggle]`, `[snort]`, `[scoff]`, `[grunt]`, `[groan]`, `[cry]`
- `[hum-tune]`, `[whoop]`, `[whistle]`, `[tongue-click]`, `[tsk]`, `[lip-smack]`, `[teeth-suck]`, `[lip-trill]`, `[shush]`, `[swallow]`, `[clear-throat]`
- `[cough]`, `[sneeze]`, `[yawn]`, `[hiccup]`, `[unintelligible]`, `[other-noise]`
