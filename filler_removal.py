"""Per-language filler / disfluency / backchannel removal for ASR evaluation.

Supported pipeline language codes (delivery folder convention):

    EN  US English
    ES  Spanish
    FR  French
    GR  German  (delivery code; not ISO ``de``)
    IT  Italian
    PT  Portuguese (Brazil)
    AR  Arabic
    JA  Japanese
    KO  Korean
    RU  Russian

Pipeline (matches Sample_review_report_06042026.md):
  1. Whisper ``BasicTextNormalizer`` (``remove_diacritics=False``).
  2. Whitespace languages: greedy multi-token strip, then single-token strip.
  3. Japanese: regex filler strip on Whisper-normalized text, whole-utterance
     aizuchi drop (no inline substring removal of short backchannels). Matches
     the client ``filler_words_remover`` path (no morpheme-space collapse here;
     char-level retokenization for scoring happens later in ``scoring_repr``).

Public API
----------
* :func:`normalize_text` — Whisper normalization only.
* :func:`strip_fillers` — normalize + strip.
* :func:`strip_fillers_from_normalized` — strip on already-normalized text.
* :func:`canonicalize_lang` — map aliases to a pipeline language code.
"""

from __future__ import annotations

import re
from typing import Iterable

from whisper.normalizers import BasicTextNormalizer

_NORMALIZER = BasicTextNormalizer(remove_diacritics=False)

SUPPORTED_LANGUAGES: tuple[str, ...] = (
    "EN", "ES", "FR", "GR", "IT", "PT", "AR", "JA", "KO", "RU",
)

# Aliases from ISO / folder variants → pipeline code.
_LANG_ALIASES: dict[str, str] = {
    "EN": "EN", "EN-US": "EN", "EN-GB": "EN", "ENG": "EN",
    "ES": "ES", "ES-ES": "ES", "ES-MX": "ES", "SPA": "ES", "SP": "ES",
    "FR": "FR", "FR-FR": "FR", "FRA": "FR",
    "GR": "GR", "DE": "GR", "DE-DE": "GR", "DEU": "GR", "GER": "GR",
    "IT": "IT", "IT-IT": "IT", "ITA": "IT",
    "PT": "PT", "PT-BR": "PT", "PT-PT": "PT", "POR": "PT",
    "AR": "AR", "AR-SA": "AR", "ARA": "AR",
    "JA": "JA", "JA-JP": "JA", "JPN": "JA", "JP": "JA",
    "KO": "KO", "KO-KR": "KO", "KOR": "KO", "KR": "KO",
    "RU": "RU", "RU-RU": "RU", "RUS": "RU",
}


def canonicalize_lang(lang: str) -> str:
    """Map a language code to a pipeline language code (e.g. ``GR``, ``JA``)."""
    if not isinstance(lang, str):
        raise TypeError(f"lang must be str, got {type(lang).__name__}")
    key = lang.strip().replace("_", "-").upper()
    code = _LANG_ALIASES.get(key, key)
    if code not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Unsupported language code {lang!r}. Supported: {SUPPORTED_LANGUAGES}"
        )
    return code


def normalize_text(text: str) -> str:
    """Apply Whisper ``BasicTextNormalizer`` (multilingual, diacritics kept)."""
    if text is None:
        return ""
    return _NORMALIZER(str(text)).strip()


def _prolong(*bases: str, extras: int = 6) -> set[str]:
    """Generate prolongation variants for each base form."""
    out: set[str] = set()
    for base in bases:
        if not base:
            continue
        out.add(base)
        for i, char in enumerate(base):
            for k in range(1, extras + 1):
                out.add(base[:i] + char * (k + 1) + base[i + 1:])
    return out


# ---------------------------------------------------------------------------
# Single-token filler sets (post Whisper normalization).
# ---------------------------------------------------------------------------

_EN_FILLERS = frozenset(
    _prolong("hm", "mm", "hmm", "mmm", "mmh", "hmmm", "hmhmm", "hmmhmm")
    | _prolong("um", "umm", "uhm", "umh", "ummh")
    | _prolong("uh", "uhh", "uuh")
    | _prolong("ah", "ahh", "aah", "ahhh")
    | _prolong("er", "err", "erm")
    | _prolong("oh", "ohh")
    | _prolong("eh", "ehh")
    | _prolong("ooh", "oooh", "aw", "awe", extras=5)
    | _prolong("mn", "mmn", "mnn", extras=5)
    | _prolong("mhm", "mhmm", "mmhm", "mmhmm", extras=5)
    | _prolong("uhhuh", "uhhum", extras=5)
    | _prolong("uhuh", "unhuh", extras=5)
    | _prolong("nuhuh", extras=5)
)

_ES_FILLERS = frozenset(
    _prolong("eh", "eeh", "ehh")
    | _prolong("em", "emm", "ehm", "ehmm")
    | _prolong("mm", "mmm")
    | _prolong("ah", "ahh", "ahmm")
    | _prolong("aja", "ajá", "ajam", "ajám", extras=4)
    | _prolong("ajaja", "ajajá", extras=4)
    | _prolong("aha", "ajá", extras=4)
    | _prolong("mhm", "mhmm", extras=4)
    | _prolong("ujum", "ujumm", "uja", "ujá", extras=4)
)

_FR_FILLERS = frozenset(
    _prolong("euh", "euhh")
    | _prolong("eh", "ehh")
    | _prolong("hm", "hmm")
    | _prolong("mm", "mmm")
    | _prolong("ah", "ahh")
    | _prolong("oh", "ohh")
    | _prolong("mh", "mhm", "mhmm", extras=4)
    | _prolong("hum", "humhum", extras=4)
    | {"hein"}
)

_GR_FILLERS = frozenset(
    _prolong("ähm", "ähmm", "ähhm", "ähhmm")
    | _prolong("äh", "ähh")
    | _prolong("öhm", "öh", "öhh")
    | _prolong("hm", "hmm")
    | _prolong("mm", "mmm")
    | _prolong("ah", "ahh")
    | _prolong("aha", "ahah", extras=4)
    | _prolong("mhm", "mhmm", "mmh", extras=4)
)

_IT_FILLERS = frozenset(
    _prolong("eh", "eeh", "ehh")
    | _prolong("ehm", "ehmm")
    | _prolong("mh", "mhm", "mhmm", extras=4)
    | _prolong("mm", "mmm")
    | _prolong("ah", "ahh")
    | _prolong("oh", "ohh")
    | _prolong("uhm", "uhmm", extras=4)
)

_PT_FILLERS = frozenset(
    _prolong("ah", "ahh")
    | _prolong("hm", "hmm")
    | _prolong("hum", "humm")
    | _prolong("mm", "mmm")
    | _prolong("uh", "uhh")
    | _prolong("uhm", "uhmm", extras=4)
    | _prolong("uhum", "uhumm", extras=5)
    | _prolong("ahã", "ahan", "ahn", "ahám", extras=4)
    | _prolong("mhm", "mhmm", extras=4)
)

_AR_FILLERS = frozenset(
    _prolong("آه", "أه", "اه", extras=5)
    | _prolong("آآه", "أأه", "اااه", extras=4)
    | _prolong("أم", "أمم", "إم", "إمم", "امم", extras=5)
    | {"إيه", "ايه"}
    | _prolong("مم", "ممم", extras=5)
    | _prolong("ah", "ahh", "uh", "uhh")
    | _prolong("um", "umm")
    | _prolong("mm", "mmm")
    | _prolong("eh", "eeh", "ehh")
    | _prolong("ehmm", extras=4)
)

_KO_FILLERS = frozenset(
    {"어", "응", "엉", "옹", "음", "오", "아", "으"}
    | {
        "어어", "어어어", "어어어어",
        "응응", "응응응",
        "엉엉",
        "어응", "응어",
        "아아", "아아아",
        "음음", "음음음",
        "으응", "으음", "으으",
        "오오",
    }
    | _prolong("어흠", "음흠", "흠", extras=4)
)

_RU_FILLERS = frozenset(
    _prolong("э", "ээ")
    | _prolong("эм", "эмм", "эмхм")
    | _prolong("м", "мм", "ммм")
    | _prolong("хм", "хмм")
    | _prolong("а", "аа")
    | _prolong("о", "оо")
    | _prolong("у", "уу")
    | _prolong("ы", "ыы")
    | {"ах", "ох", "уф"}
    | _prolong("угу", "ага", "ахах", extras=4)
    | _prolong("мхм", "мхмм", extras=4)
)

SINGLE_TOKEN_FILLERS: dict[str, frozenset[str]] = {
    "EN": _EN_FILLERS,
    "ES": _ES_FILLERS,
    "FR": _FR_FILLERS,
    "GR": _GR_FILLERS,
    "IT": _IT_FILLERS,
    "PT": _PT_FILLERS,
    "AR": _AR_FILLERS,
    "KO": _KO_FILLERS,
    "RU": _RU_FILLERS,
    "JA": frozenset(),
}

MULTI_TOKEN_FILLERS: dict[str, frozenset[tuple[str, ...]]] = {
    "EN": frozenset({
        ("mm", "hmm"), ("mm", "hm"), ("m", "hm"),
        ("uh", "huh"), ("uh", "hum"), ("unh", "hun"),
        ("uh", "uh"), ("unh", "uh"),
        ("nuh", "uh"),
        ("mm", "mm"), ("mhm", "mm"),
        ("hm", "mm"), ("hmm", "mm"),
    }),
    "ES": frozenset({("ajá", "ajá"), ("aha", "aha")}),
    "FR": frozenset({("hum", "hum")}),
    "GR": frozenset(),
    "IT": frozenset(),
    "PT": frozenset({("ah", "ah"), ("uh", "hum"), ("uh", "huh")}),
    "AR": frozenset(),
    "KO": frozenset({
        ("아", "응"), ("음", "응"), ("응", "음"),
        ("어", "음"), ("으", "응"), ("응", "응"),
    }),
    "RU": frozenset({("э", "э"), ("м", "м")}),
    "JA": frozenset(),
}

_JA_FILLER_PATTERNS: tuple[str, ...] = (
    r"えーっと",
    r"えっとー*",
    r"えーとー*",
    r"えと",
    r"あのうー*",
    r"あのー+",
    r"そのうー*",
    r"そのー+",
    r"うーんと",
    r"うーん",
    r"んー+",
    r"えー(?![ぁ-んァ-ヴ一-龯ー])",
    r"あー(?![ぁ-んァ-ヴ一-龯ー])",
    r"うー(?![ぁ-んァ-ヴ一-龯ー])",
    r"おー(?![ぁ-んァ-ヴ一-龯ー])",
)
_JA_FILLER_RE = re.compile("|".join(_JA_FILLER_PATTERNS))

_JA_BACKCHANNEL_BASES: tuple[str, ...] = (
    "ん", "うん", "ううん", "うむ",
    "へ", "へえ", "ほ", "ほう", "ほお",
    "は", "はあ", "はい", "ふ", "ふん", "ふうん",
    "あ", "ああ", "え", "ええ", "お", "おお",
    "ね", "ねえ", "なるほど", "ほんと", "そう",
)


def _ja_backchannel_set() -> frozenset[str]:
    out: set[str] = set()
    for base in _JA_BACKCHANNEL_BASES:
        for rep in range(1, 5):
            unit = base * rep
            for k in range(0, 5):
                stem = unit + ("ー" * k)
                out.add(stem)
                out.add(stem + "っ")
    return frozenset(out)


_JA_BACKCHANNELS = _ja_backchannel_set()


def _strip_ja(normalized: str) -> str:
    """Japanese filler strip — same algorithm as the client QA stack."""
    if not normalized:
        return ""
    if normalized in _JA_BACKCHANNELS:
        return ""
    text = _JA_FILLER_RE.sub(" ", normalized)
    text = " ".join(text.split())
    if text in _JA_BACKCHANNELS:
        return ""
    return text


def _strip_whitespace_lang(normalized: str, lang: str) -> str:
    tokens = normalized.split()
    if not tokens:
        return ""

    multi = MULTI_TOKEN_FILLERS.get(lang, frozenset())
    max_n = max((len(t) for t in multi), default=0)
    out: list[str] = []
    i = 0
    n_tokens = len(tokens)
    while i < n_tokens:
        matched = False
        for n in range(min(max_n, n_tokens - i), 1, -1):
            if tuple(tokens[i : i + n]) in multi:
                i += n
                matched = True
                break
        if not matched:
            out.append(tokens[i])
            i += 1

    singles = SINGLE_TOKEN_FILLERS[lang]
    return " ".join(tok for tok in out if tok not in singles)


def strip_fillers_from_normalized(normalized: str, lang: str) -> str:
    """Remove fillers from text already passed through :func:`normalize_text`."""
    lang = canonicalize_lang(lang)
    if not normalized:
        return ""
    if lang == "JA":
        return _strip_ja(normalized)
    return _strip_whitespace_lang(normalized, lang)


def strip_fillers(text: str, lang: str) -> str:
    """Whisper-normalize then strip fillers/backchannels."""
    return strip_fillers_from_normalized(normalize_text(text), lang)


def is_filler_only(text: str, lang: str) -> bool:
    """True iff text has content under Whisper but none left after filler strip."""
    normalized = normalize_text(text)
    if not normalized:
        return False
    return strip_fillers_from_normalized(normalized, lang) == ""


def _cli(argv: Iterable[str]) -> int:
    argv = list(argv)
    if len(argv) < 2:
        print("Usage: filler_removal.py LANG TEXT [TEXT ...]")
        print()
        print("Supported languages:", ", ".join(SUPPORTED_LANGUAGES))
        return 2
    lang, *parts = argv
    print(strip_fillers(" ".join(parts), lang))
    return 0


if __name__ == "__main__":  # pragma: no cover
    import sys

    raise SystemExit(_cli(sys.argv[1:]))
