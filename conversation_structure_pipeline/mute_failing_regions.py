"""Mute seglst/wav regions overlapping failing DNSMOS SIG or clipping windows.

Driven by ``to_be_edited_for_audio_quality.csv``; reads/writes under
``to_be_edited_for_audio_quality/<session_id>/``. Preserves originals as
``*_og.*``; tracks resume state in ``mute_pipeline_state.json``.

Candidates are prioritized by lowest SIG (then clipping severity). Overlap is
not a goal—mutes apply even when overlap is unchanged. Stop when any of:

* every remaining candidate would reduce session overlap below
  ``overlap_threshold + buffer`` (unsafe candidates are skipped until none left)
* no failing DNSMOS / clipping candidates remain on CSV channels
* channel speech removal would exceed ``MAX_SPEECH_REMOVAL_FRACTION`` of original

Usage
-----
    python -m conversation_structure_pipeline.mute_failing_regions
    python -m conversation_structure_pipeline.mute_failing_regions --dry-run
    python -m conversation_structure_pipeline.mute_failing_regions --overwrite
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import soundfile as sf

from audio_quality_pipeline.natural_window_dnsmos import speech_weight_sec
from conversation_structure_pipeline.common import compute_overlap_ratio
from conversation_structure_pipeline.overlap_calculation import (
    OVERLAP_JSON,
    _speech_segments_from_seglst,
)
from diarization_pipeline.common import (
    _TURING_EMAIL_SUFFIX,
    channel_id_from_path,
    speaker_output_name,
)
from diarization_pipeline.seglst_to_rttm import is_speech_segment, load_speech_seglst_rows

STATE_JSON = "mute_pipeline_state.json"
LOG_JSONL = "mute_pipeline_log.jsonl"
DEFAULT_WORKSPACE = Path("to_be_edited_for_audio_quality")
DEFAULT_CSV = Path("to_be_edited_for_audio_quality.csv")
DEFAULT_NUMERICAL_ROOT = Path("numerical_results")
STATE_VERSION = 1
MAX_SPEECH_REMOVAL_FRACTION = 0.20
_SEGLST_SUFFIX = ".seglst.json"
_CANONICAL_SEGLST_REJECT = re.compile(r"_(?:fixed|approved)$", re.I)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def overlap_threshold_pct(n_speakers: int) -> float:
    if n_speakers <= 3:
        return 5.0
    if n_speakers <= 5:
        return 10.0
    return 12.0


def overlap_target_pct(n_speakers: int, buffer_pp: float) -> float:
    return overlap_threshold_pct(n_speakers) + buffer_pp


def row_key(session_id: str, channel: str) -> str:
    return f"{session_id}|{channel}"


def og_path(path: Path) -> Path:
    return path.with_name(f"{path.stem}_og{path.suffix}")


def peak_dbfs(speech_peak: float | None) -> float | None:
    if speech_peak is None or speech_peak <= 0:
        return None
    return round(20.0 * math.log10(float(speech_peak)), 2)


def is_canonical_seglst(path: Path) -> bool:
    name = path.name
    if not name.endswith(_SEGLST_SUFFIX):
        return False
    stem = name[: -len(_SEGLST_SUFFIX)]
    return _CANONICAL_SEGLST_REJECT.search(stem) is None


def _seglst_preference_key(path: Path) -> tuple[int, str]:
    stem = path.name[: -len(_SEGLST_SUFFIX)]
    if is_canonical_seglst(path):
        return (0, stem)
    if stem.endswith("_approved"):
        return (1, stem)
    if stem.endswith("_fixed"):
        return (2, stem)
    return (3, stem)


def effective_seglst_files(session_dir: Path) -> list[Path]:
    """One seglst per speaker; prefer canonical, then _approved, then _fixed."""
    by_speaker: dict[str, Path] = {}
    preference: dict[str, tuple[int, str]] = {}
    for path in sorted(session_dir.glob("*.seglst.json")):
        stem = path.name[: -len(_SEGLST_SUFFIX)]
        speaker_key = speaker_output_name(stem)
        rank = _seglst_preference_key(path)
        if speaker_key not in by_speaker or rank < preference[speaker_key]:
            by_speaker[speaker_key] = path
            preference[speaker_key] = rank
    return sorted(by_speaker.values(), key=lambda p: p.name)


def canonical_seglst_files(session_dir: Path) -> list[Path]:
    return sorted(p for p in session_dir.glob("*.seglst.json") if is_canonical_seglst(p))


@dataclass(frozen=True)
class ChannelFiles:
    channel_local: str
    channel_stem: str
    seglst: Path
    wav: Path
    rttm: Path


def resolve_channel_files(session_dir: Path, channel_local: str) -> ChannelFiles:
    """Resolve canonical wav/rttm and best available seglst for a CSV channel."""
    channel_local = channel_local.strip()
    base_ids = [channel_local, f"{channel_local}{_TURING_EMAIL_SUFFIX}"]
    seglst: Path | None = None
    channel_stem: str | None = None
    for base in base_ids:
        for suffix in ("", "_approved", "_fixed"):
            candidate = session_dir / f"{base}{suffix}{_SEGLST_SUFFIX}"
            if candidate.is_file():
                seglst = candidate
                channel_stem = f"{base}{suffix}"
                break
        if seglst is not None:
            break
    if seglst is None or channel_stem is None:
        for path in session_dir.glob("*.seglst.json"):
            stem = path.name[: -len(_SEGLST_SUFFIX)]
            if speaker_output_name(stem) != channel_local:
                continue
            seglst = path
            channel_stem = stem
            break
    if seglst is None or channel_stem is None:
        raise FileNotFoundError(
            f"{session_dir.name}: no seglst for channel {channel_local!r}",
        )

    wav = session_dir / f"{channel_stem}.wav"
    if not wav.is_file():
        for base in base_ids:
            candidate = session_dir / f"{base}.wav"
            if candidate.is_file():
                wav = candidate
                break
    if not wav.is_file():
        raise FileNotFoundError(
            f"{session_dir.name}: no wav for channel {channel_local!r} ({channel_stem})",
        )

    rttm = session_dir / f"{channel_stem}.rttm"
    if not rttm.is_file():
        for base in base_ids:
            candidate = session_dir / f"{base}.rttm"
            if candidate.is_file():
                rttm = candidate
                break
    if not rttm.is_file():
        rttm = session_dir / f"{channel_stem}.rttm"

    return ChannelFiles(
        channel_local=channel_local,
        channel_stem=channel_stem,
        seglst=seglst,
        wav=wav,
        rttm=rttm,
    )


def resolve_channel_stem(session_dir: Path, channel_local: str) -> str:
    return resolve_channel_files(session_dir, channel_local).channel_stem


def channel_paths(session_dir: Path, channel_stem: str) -> dict[str, Path]:
    return {
        "seglst": session_dir / f"{channel_stem}{_SEGLST_SUFFIX}",
        "wav": session_dir / f"{channel_stem}.wav",
        "rttm": session_dir / f"{channel_stem}.rttm",
    }


def channel_paths_from_files(files: ChannelFiles) -> dict[str, Path]:
    return {"seglst": files.seglst, "wav": files.wav, "rttm": files.rttm}


def preserve_og(path: Path) -> None:
    original = og_path(path)
    if original.is_file():
        return
    if not path.is_file():
        raise FileNotFoundError(f"cannot preserve _og; missing {path}")
    shutil.copy2(path, original)


def restore_from_og(path: Path) -> None:
    original = og_path(path)
    if not original.is_file():
        raise FileNotFoundError(f"cannot restore; missing {original}")
    shutil.copy2(original, path)


def load_csv(csv_path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or "session_id" not in reader.fieldnames:
            raise ValueError(f"{csv_path}: expected columns session_id, channel")
        for line in reader:
            session_id = (line.get("session_id") or "").strip()
            channel = (line.get("channel") or "").strip()
            if not session_id or not channel:
                continue
            rows.append({"session_id": session_id, "channel": channel})
    return rows


def group_csv_rows(rows: list[dict[str, str]]) -> list[tuple[str, list[dict[str, str]]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    order: list[str] = []
    for row in rows:
        sid = row["session_id"]
        if sid not in grouped:
            order.append(sid)
        grouped[sid].append(row)
    return [(sid, grouped[sid]) for sid in order]


def load_state(path: Path) -> dict:
    if not path.is_file():
        return {
            "version": STATE_VERSION,
            "entries": {},
        }
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    data.setdefault("version", STATE_VERSION)
    data.setdefault("entries", {})
    return data


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_log(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_all_speech_segments(
    session_dir: Path,
) -> list[tuple[float, float, str]]:
    segments: list[tuple[float, float, str]] = []
    for seglst_path in effective_seglst_files(session_dir):
        speaker = channel_id_from_path(seglst_path)
        segments.extend(_speech_segments_from_seglst(seglst_path, speaker))
    return segments


def process_conversation_canonical(session_dir: Path) -> dict | None:
    """Like ``process_conversation`` but ignores ``*_approved/_fixed`` seglst copies."""
    seglst_files = effective_seglst_files(session_dir)
    if not seglst_files:
        return None

    all_segments: list[tuple[float, float, str]] = []
    speakers_out: dict[str, dict] = {}
    total_kept = total_dropped = 0

    for seglst_path in seglst_files:
        speaker = channel_id_from_path(seglst_path)
        kept = dropped = 0
        segs = json.loads(seglst_path.read_text(encoding="utf-8-sig"))
        for seg in segs:
            words = seg.get("words", "")
            if not is_speech_segment(words):
                dropped += 1
                continue
            try:
                start = float(seg["start_time"])
                end = float(seg["end_time"])
            except (KeyError, TypeError, ValueError):
                dropped += 1
                continue
            if end <= start:
                dropped += 1
                continue
            kept += 1
        total_kept += kept
        total_dropped += dropped

        speech_segs = _speech_segments_from_seglst(seglst_path, speaker)
        all_segments.extend(speech_segs)
        talk_time = round(sum(d for _s, d, _sp in speech_segs), 3)
        speakers_out[speaker] = {
            "speech_s": talk_time,
            "n_speech_segments": kept,
            "n_dropped_segments": dropped,
            "n_seglst_segments": kept + dropped,
        }

    from conversation_structure_pipeline.common import resolve_total_audio_s

    speech_s, overlap_s, file_span_s, ratio = compute_overlap_ratio(all_segments)
    speaker_stems = [channel_id_from_path(p) for p in seglst_files]
    total_audio_s, total_audio_source = resolve_total_audio_s(session_dir, speaker_stems)

    return {
        "session_id": session_dir.name,
        "method": {
            "metric": "overlap_ratio",
            "definition": "overlap_s / speech_s  (T_overlap / T_speech)",
            "numerator": "overlap_s — wall-clock seconds where >= 2 speakers are active",
            "denominator": "speech_s — wall-clock seconds where >= 1 speaker is active",
            "speech_source": "speech-only canonical seglst segments (NSV-only rows excluded)",
            "total_audio": (
                "duration of *_mixed.wav when present, else max speaker .wav duration"
            ),
            "reference": "chsep_audio_qa/ami_rttm_stats.py compute_overlap_ratio",
        },
        "conversation": {
            "n_speakers": len(seglst_files),
            "total_audio_s": total_audio_s,
            "total_audio_source": total_audio_source,
            "speech_s": round(speech_s, 3),
            "overlap_s": round(overlap_s, 3),
            "overlap_ratio": round(ratio, 6),
            "overlap_ratio_pct": round(ratio * 100, 2),
            "file_span_s": round(file_span_s, 3),
            "n_speech_segments": total_kept,
            "n_dropped_segments": total_dropped,
        },
        "speakers": speakers_out,
    }


def overlap_pct_from_segments(segments: list[tuple[float, float, str]]) -> float:
    speech_s, overlap_s, _, ratio = compute_overlap_ratio(segments)
    if speech_s <= 0:
        return 0.0
    return round(ratio * 100, 6)


def segments_without_row(
    segments: list[tuple[float, float, str]],
    *,
    speaker: str,
    start: float,
    end: float,
) -> list[tuple[float, float, str]]:
    dur = end - start
    if dur <= 0:
        return segments
    out: list[tuple[float, float, str]] = []
    removed = False
    for seg_start, seg_dur, seg_spk in segments:
        seg_end = seg_start + seg_dur
        if (
            not removed
            and seg_spk == speaker
            and abs(seg_start - start) < 0.01
            and abs(seg_end - end) < 0.02
        ):
            removed = True
            continue
        out.append((seg_start, seg_dur, seg_spk))
    return out


@dataclass
class MuteCandidate:
    channel_local: str
    channel_stem: str
    failure_kind: str
    window_start: float
    window_end: float
    window_sig: float | None
    window_peak_dbfs: float | None
    seglst_start: float
    seglst_end: float
    words: str
    sort_key: tuple = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.window_sig is not None and self.window_sig < 999:
            self.sort_key = (0, float(self.window_sig), 0.0)
        else:
            peak = self.window_peak_dbfs if self.window_peak_dbfs is not None else -999.0
            self.sort_key = (1, 0.0, -peak)

    @property
    def row_id(self) -> tuple[str, float, float]:
        return (self.channel_stem, round(self.seglst_start, 2), round(self.seglst_end, 2))


def intervals_overlap(a0: float, a1: float, b0: float, b1: float) -> bool:
    return max(a0, b0) < min(a1, b1)


def speech_rows_in_seglst(seglst_path: Path) -> list[dict]:
    segs = json.loads(seglst_path.read_text(encoding="utf-8-sig"))
    rows: list[dict] = []
    for seg in segs:
        words = seg.get("words", "")
        if not is_speech_segment(words):
            continue
        try:
            start = float(seg["start_time"])
            end = float(seg["end_time"])
        except (KeyError, TypeError, ValueError):
            continue
        if end <= start:
            continue
        rows.append(
            {
                "start": start,
                "end": end,
                "words": words,
                "raw": seg,
            },
        )
    return rows


def build_candidates_for_channel(
    *,
    session_id: str,
    channel_local: str,
    channel_stem: str,
    seglst_path: Path,
    failing_windows: list[dict],
) -> list[MuteCandidate]:
    speech_rows = speech_rows_in_seglst(seglst_path)
    deduped: dict[tuple[str, float, float], MuteCandidate] = {}
    for window in failing_windows:
        w0 = float(window["start_sec"])
        w1 = float(window["end_sec"])
        sig = window.get("sig")
        sig_val = float(sig) if sig is not None else None
        pk = window.get("peak_dbfs")
        if window.get("failure_kind") == "peak_dbfs" and pk is None:
            pk = peak_dbfs(window.get("speech_peak"))
        kind = window.get("failure_kind") or (
            "dnsmos_sig" if sig_val is not None and sig_val < 999 else "peak_dbfs"
        )
        for row in speech_rows:
            if not intervals_overlap(row["start"], row["end"], w0, w1):
                continue
            candidate = MuteCandidate(
                channel_local=channel_local,
                channel_stem=channel_stem,
                failure_kind=kind,
                window_start=w0,
                window_end=w1,
                window_sig=sig_val,
                window_peak_dbfs=pk,
                seglst_start=row["start"],
                seglst_end=row["end"],
                words=row["words"],
            )
            existing = deduped.get(candidate.row_id)
            if existing is None or candidate.sort_key < existing.sort_key:
                deduped[candidate.row_id] = candidate
    return list(deduped.values())


def pick_next_candidate(
    candidates: list[MuteCandidate],
    channel_order: list[str],
    rr_index: int,
) -> tuple[MuteCandidate | None, int]:
    if not candidates:
        return None, rr_index
    best_key = min(c.sort_key for c in candidates)
    tier = [c for c in candidates if c.sort_key == best_key]
    for offset in range(len(channel_order)):
        ch = channel_order[(rr_index + offset) % len(channel_order)]
        for candidate in tier:
            if candidate.channel_local == ch:
                return candidate, rr_index + offset + 1
    return tier[0], rr_index + 1


def breaches_overlap_floor(
    current_pct: float,
    new_pct: float,
    target_pct: float,
) -> bool:
    """True when muting would *reduce* overlap below threshold + buffer."""
    if new_pct + 1e-9 >= current_pct:
        return False
    return new_pct + 1e-9 < target_pct


def channel_speech_duration_s(seglst_path: Path) -> float:
    """Total speech seconds on one channel seglst."""
    return sum(end - start for start, end in speech_spans_from_seglst(seglst_path))


def would_exceed_speech_cap(
    original_speech_s: float,
    muted_speech_s: float,
    segment_s: float,
    *,
    max_removal_fraction: float = MAX_SPEECH_REMOVAL_FRACTION,
) -> bool:
    """True when muting ``segment_s`` more would remove > max_removal_fraction of speech."""
    if original_speech_s <= 0:
        return segment_s > 0
    return muted_speech_s + segment_s > original_speech_s * max_removal_fraction + 1e-9


def original_channel_seglst_path(files: ChannelFiles) -> Path:
    """Prefer ``*_og`` seglst when present (pre-edit baseline)."""
    og = og_path(files.seglst)
    return og if og.is_file() else files.seglst


def mute_segment_record(candidate: MuteCandidate, *, overlap_before: float, overlap_after: float) -> dict:
    return {
        "session_id": None,  # filled by caller
        "channel": candidate.channel_local,
        "channel_stem": candidate.channel_stem,
        "failure_kind": candidate.failure_kind,
        "window_start_sec": candidate.window_start,
        "window_end_sec": candidate.window_end,
        "window_sig": candidate.window_sig,
        "window_peak_dbfs": candidate.window_peak_dbfs,
        "seglst_start_sec": candidate.seglst_start,
        "seglst_end_sec": candidate.seglst_end,
        "words_preview": candidate.words[:200],
        "overlap_before_pct": round(overlap_before, 2),
        "overlap_after_pct": round(overlap_after, 2),
    }


def muted_segment_stats(segments: list[dict]) -> tuple[int, float]:
    """Return (count, total_seconds) from muted segment records."""
    total_s = 0.0
    for seg in segments:
        start = seg.get("seglst_start_sec")
        end = seg.get("seglst_end_sec")
        if start is None or end is None:
            continue
        total_s += max(0.0, float(end) - float(start))
    return len(segments), round(total_s, 3)


def remove_seglst_row(seglst_path: Path, start: float, end: float) -> bool:
    segs = json.loads(seglst_path.read_text(encoding="utf-8-sig"))
    new_segs: list[dict] = []
    removed = False
    for seg in segs:
        try:
            seg_start = float(seg["start_time"])
            seg_end = float(seg["end_time"])
        except (KeyError, TypeError, ValueError):
            new_segs.append(seg)
            continue
        if (
            not removed
            and abs(seg_start - start) < 0.01
            and abs(seg_end - end) < 0.02
        ):
            removed = True
            continue
        new_segs.append(seg)
    if not removed:
        return False
    seglst_path.write_text(
        json.dumps(new_segs, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )
    return True


def mute_wav_region(wav_path: Path, start: float, end: float) -> None:
    data, sr = sf.read(str(wav_path), always_2d=False)
    i0 = int(round(start * sr))
    i1 = int(round(end * sr))
    i0 = max(0, min(i0, len(data)))
    i1 = max(i0, min(i1, len(data)))
    data[i0:i1] = 0
    subtype = sf.info(str(wav_path)).subtype or "PCM_16"
    sf.write(str(wav_path), data, sr, subtype=subtype)


def regenerate_rttm(seglst_path: Path, rttm_path: Path, channel_stem: str) -> None:
    segs = json.loads(seglst_path.read_text(encoding="utf-8-sig"))
    lines: list[str] = []
    for seg in segs:
        start = float(seg["start_time"])
        dur = float(seg["end_time"]) - start
        if dur <= 0:
            continue
        spk = seg.get("speaker", channel_stem)
        lines.append(
            f"SPEAKER {channel_stem} 1 {start:.3f} {dur:.3f} <NA> <NA> "
            f"{spk} <NA> <NA>\n",
        )
    rttm_path.write_text("".join(lines), encoding="utf-8")


def discover_dnsmos_individual_jsonl(numerical_root: Path) -> list[Path]:
    """Find per-session DNSMOS JSONL exports anywhere under ``numerical_root``."""
    if not numerical_root.is_dir():
        return []
    found: dict[str, Path] = {}
    for path in sorted(numerical_root.rglob("dnsmos/individual/*.jsonl")):
        if path.is_file():
            found[str(path.resolve())] = path
    return list(found.values())


def index_dnsmos_channels_from_jsonl(
    numerical_root: Path,
) -> dict[str, dict[str, dict]]:
    """Return {session_id: {channel_local: {sig, windows}}} from JSONL exports."""
    out: dict[str, dict[str, dict]] = defaultdict(dict)
    for path in discover_dnsmos_individual_jsonl(numerical_root):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            session_id = rec.get("session_id") or ""
            if not session_id:
                continue
            for channel in rec.get("channels") or []:
                speaker = channel.get("speaker") or ""
                channel_local = speaker_output_name(speaker)
                out[session_id][channel_local] = {
                    "sig": channel.get("sig"),
                    "windows": list(channel.get("windows") or []),
                }
    return out


def _optional_float(value) -> float | None:
    if value is None:
        return None
    try:
        return round(float(value), 6)
    except (TypeError, ValueError):
        return None


def speech_spans_from_seglst(seglst_path: Path) -> list[tuple[float, float]]:
    rows = load_speech_seglst_rows(seglst_path)
    return [(float(r["start"]), float(r["end"])) for r in rows]


def speech_spans_excluding_mutes(
    seglst_path: Path,
    muted: list[dict],
) -> list[tuple[float, float]]:
    if not muted:
        return speech_spans_from_seglst(seglst_path)
    skip: set[tuple[float, float]] = set()
    for record in muted:
        start = record.get("seglst_start_sec")
        end = record.get("seglst_end_sec")
        if start is None or end is None:
            continue
        skip.add((round(float(start), 2), round(float(end), 2)))
    spans: list[tuple[float, float]] = []
    for start, end in speech_spans_from_seglst(seglst_path):
        key = (round(start, 2), round(end, 2))
        if key in skip:
            continue
        spans.append((start, end))
    return spans


def weighted_mean_sig(
    windows: list[dict],
    spans: list[tuple[float, float]],
) -> float | None:
    """Recompute channel SIG from stored window scores and speech weights."""
    if not windows or not spans:
        return None
    total_weight = 0.0
    weighted_sum = 0.0
    for window in windows:
        sig = window.get("sig")
        start = window.get("start_sec")
        if sig is None or start is None:
            continue
        weight = speech_weight_sec(spans, float(start))
        if weight <= 0:
            continue
        total_weight += weight
        weighted_sum += float(sig) * weight
    if total_weight <= 0:
        return None
    return round(weighted_sum / total_weight, 6)


def channel_sig_scores(
    dnsmos_channels: dict[str, dict[str, dict]],
    session_id: str,
    channel_local: str,
    *,
    seglst_path: Path,
    muted: list[dict],
    dry_run: bool,
) -> tuple[float | None, float | None]:
    """Return (old_sig, new_sig) without re-running DNSMOS."""
    channel_data = dnsmos_channels.get(session_id, {}).get(channel_local) or {}
    old_sig = _optional_float(channel_data.get("sig"))
    windows = channel_data.get("windows") or []
    if not windows:
        return old_sig, None
    if dry_run:
        spans = speech_spans_excluding_mutes(seglst_path, muted)
    else:
        spans = speech_spans_from_seglst(seglst_path)
    new_sig = weighted_mean_sig(windows, spans)
    return old_sig, new_sig


def index_failing_windows_from_jsonl(
    numerical_root: Path,
    *,
    sig_threshold: float,
    peak_threshold_dbfs: float,
) -> dict[str, dict[str, list[dict]]]:
    """Return {session_id: {channel_local: [window dict]}}."""
    out: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    jsonl_files = discover_dnsmos_individual_jsonl(numerical_root)
    for path in jsonl_files:
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            session_id = rec.get("session_id") or ""
            if not session_id:
                continue
            for channel in rec.get("channels") or []:
                speaker = channel.get("speaker") or ""
                channel_local = speaker_output_name(speaker)
                for window in channel.get("windows") or []:
                    start = window.get("start_sec")
                    end = window.get("end_sec")
                    if start is None or end is None:
                        continue
                    sig = window.get("sig")
                    sig_val = float(sig) if sig is not None else None
                    pk = peak_dbfs(window.get("speech_peak"))
                    if sig_val is not None and sig_val < sig_threshold:
                        out[session_id][channel_local].append(
                            {
                                "start_sec": float(start),
                                "end_sec": float(end),
                                "sig": sig_val,
                                "speech_peak": window.get("speech_peak"),
                                "peak_dbfs": pk,
                                "failure_kind": "dnsmos_sig",
                            },
                        )
                    elif pk is not None and pk >= peak_threshold_dbfs:
                        out[session_id][channel_local].append(
                            {
                                "start_sec": float(start),
                                "end_sec": float(end),
                                "sig": sig_val,
                                "speech_peak": window.get("speech_peak"),
                                "peak_dbfs": pk,
                                "failure_kind": "peak_dbfs",
                            },
                        )
    return out


def index_failing_windows_from_session_dnsmos(
    session_dir: Path,
    *,
    sig_threshold: float,
    peak_threshold_dbfs: float,
) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for path in sorted(session_dir.glob("*_dnsmos.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        speaker = data.get("speaker") or path.stem.replace("_dnsmos", "")
        channel_local = speaker_output_name(speaker)
        for window in data.get("windows") or []:
            start = window.get("start_sec")
            end = window.get("end_sec")
            if start is None or end is None:
                continue
            sig = window.get("sig")
            sig_val = float(sig) if sig is not None else None
            pk = peak_dbfs(window.get("speech_peak"))
            if sig_val is not None and sig_val < sig_threshold:
                out[channel_local].append(
                    {
                        "start_sec": float(start),
                        "end_sec": float(end),
                        "sig": sig_val,
                        "speech_peak": window.get("speech_peak"),
                        "peak_dbfs": pk,
                        "failure_kind": "dnsmos_sig",
                    },
                )
            elif pk is not None and pk >= peak_threshold_dbfs:
                out[channel_local].append(
                    {
                        "start_sec": float(start),
                        "end_sec": float(end),
                        "sig": sig_val,
                        "speech_peak": window.get("speech_peak"),
                        "peak_dbfs": pk,
                        "failure_kind": "peak_dbfs",
                    },
                )
    return out


def failing_windows_for_session(
    session_id: str,
    session_dir: Path,
    numerical_index: dict[str, dict[str, list[dict]]],
    *,
    sig_threshold: float,
    peak_threshold_dbfs: float,
) -> dict[str, list[dict]]:
    if session_id in numerical_index:
        return dict(numerical_index[session_id])
    return index_failing_windows_from_session_dnsmos(
        session_dir,
        sig_threshold=sig_threshold,
        peak_threshold_dbfs=peak_threshold_dbfs,
    )


def session_rows_done(state: dict, csv_rows: list[dict[str, str]]) -> bool:
    entries = state.get("entries") or {}
    return all(entries.get(row_key(r["session_id"], r["channel"]), {}).get("status") == "done" for r in csv_rows)


def restore_session_channels(
    session_dir: Path,
    csv_rows: list[dict[str, str]],
    *,
    channels: set[str] | None = None,
) -> None:
    """Restore edited files from ``*_og.*`` for selected CSV channels.

    When ``channels`` is ``None``, every row in ``csv_rows`` is considered.
    Missing ``_og`` backups are skipped (untouched channels keep current files).
    """
    for row in csv_rows:
        ch = row["channel"]
        if channels is not None and ch not in channels:
            continue
        files = resolve_channel_files(session_dir, row["channel"])
        paths = channel_paths_from_files(files)
        for key in ("seglst", "wav", "rttm"):
            path = paths[key]
            if not path.is_file():
                continue
            original = og_path(path)
            if not original.is_file():
                print(f"    skip restore {path.name}: no _og backup")
                continue
            shutil.copy2(original, path)


def prepare_channel_files(files: ChannelFiles) -> None:
    paths = channel_paths_from_files(files)
    for key in ("seglst", "wav", "rttm"):
        if paths[key].is_file():
            preserve_og(paths[key])


def process_session(
    session_id: str,
    csv_rows: list[dict[str, str]],
    *,
    workspace: Path,
    numerical_index: dict[str, dict[str, list[dict]]],
    dnsmos_channels: dict[str, dict[str, dict]],
    sig_threshold: float,
    peak_threshold_dbfs: float,
    overlap_buffer_pp: float,
    dry_run: bool,
    log_path: Path,
) -> dict[str, dict]:
    session_dir = workspace / session_id
    if not session_dir.is_dir():
        raise FileNotFoundError(f"missing session folder {session_dir}")

    overlap_before = process_conversation_canonical(session_dir)
    if overlap_before is None:
        raise ValueError(f"{session_id}: no seglst files for overlap")
    n_speakers = overlap_before["conversation"]["n_speakers"]
    target_pct = overlap_target_pct(n_speakers, overlap_buffer_pp)
    start_pct = float(overlap_before["conversation"]["overlap_ratio_pct"])

    channel_order = [row["channel"] for row in csv_rows]
    channel_file_map = {
        row["channel"]: resolve_channel_files(session_dir, row["channel"])
        for row in csv_rows
    }

    failing_by_channel = failing_windows_for_session(
        session_id,
        session_dir,
        numerical_index,
        sig_threshold=sig_threshold,
        peak_threshold_dbfs=peak_threshold_dbfs,
    )

    candidates: list[MuteCandidate] = []
    for row in csv_rows:
        ch = row["channel"]
        files = channel_file_map[ch]
        windows = failing_by_channel.get(ch, [])
        if not windows:
            continue
        candidates.extend(
            build_candidates_for_channel(
                session_id=session_id,
                channel_local=ch,
                channel_stem=files.channel_stem,
                seglst_path=files.seglst,
                failing_windows=windows,
            ),
        )

    muted_by_channel: dict[str, list[dict]] = {row["channel"]: [] for row in csv_rows}
    removed_ids: set[tuple[str, float, float]] = set()
    rr_index = 0
    skipped_overlap_floor = False
    stopped_reason: str | None = "no_candidates" if not candidates else None

    if not dry_run:
        for files in channel_file_map.values():
            prepare_channel_files(files)

    original_speech_s: dict[str, float] = {}
    muted_speech_s: dict[str, float] = {row["channel"]: 0.0 for row in csv_rows}
    for row in csv_rows:
        ch = row["channel"]
        files = channel_file_map[ch]
        original_speech_s[ch] = channel_speech_duration_s(
            original_channel_seglst_path(files),
        )

    current_segments = load_all_speech_segments(session_dir)
    current_pct = overlap_pct_from_segments(current_segments)

    while candidates:
        candidate, rr_index = pick_next_candidate(candidates, channel_order, rr_index)
        if candidate is None:
            stopped_reason = "no_candidates"
            break

        ch = candidate.channel_local
        segment_s = max(0.0, candidate.seglst_end - candidate.seglst_start)
        if would_exceed_speech_cap(
            original_speech_s.get(ch, 0.0),
            muted_speech_s[ch],
            segment_s,
        ):
            stopped_reason = "speech_cap"
            break

        new_segments = segments_without_row(
            current_segments,
            speaker=candidate.channel_stem,
            start=candidate.seglst_start,
            end=candidate.seglst_end,
        )
        new_pct = overlap_pct_from_segments(new_segments)
        if breaches_overlap_floor(current_pct, new_pct, target_pct):
            skipped_overlap_floor = True
            candidates = [c for c in candidates if c.row_id != candidate.row_id]
            continue

        record = mute_segment_record(
            candidate,
            overlap_before=current_pct,
            overlap_after=new_pct,
        )
        record["session_id"] = session_id

        if dry_run:
            print(
                f"  PLAN mute {session_id}/{candidate.channel_local} "
                f"{candidate.seglst_start:.2f}-{candidate.seglst_end:.2f} "
                f"({candidate.failure_kind}) overlap {current_pct:.2f}% -> {new_pct:.2f}%",
            )
        else:
            files = channel_file_map[candidate.channel_local]
            paths = channel_paths_from_files(files)
            if not remove_seglst_row(
                paths["seglst"],
                candidate.seglst_start,
                candidate.seglst_end,
            ):
                candidates = [c for c in candidates if c.row_id != candidate.row_id]
                continue
            mute_wav_region(paths["wav"], candidate.seglst_start, candidate.seglst_end)
            append_log(
                log_path,
                {"timestamp": utc_now(), "action": "mute", **record},
            )

        muted_by_channel[candidate.channel_local].append(record)
        muted_speech_s[ch] += segment_s
        removed_ids.add(candidate.row_id)
        candidates = [c for c in candidates if c.row_id not in removed_ids]
        current_segments = new_segments
        current_pct = new_pct

    if stopped_reason is None:
        stopped_reason = "overlap_floor" if skipped_overlap_floor else "exhausted"

    if not dry_run:
        touched: set[str] = set()
        for row in csv_rows:
            if muted_by_channel[row["channel"]]:
                touched.add(row["channel"])
        for ch in touched:
            files = channel_file_map[ch]
            regenerate_rttm(files.seglst, files.rttm, files.channel_stem)
        overlap_data = process_conversation_canonical(session_dir)
        if overlap_data is not None:
            (session_dir / OVERLAP_JSON).write_text(
                json.dumps(overlap_data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
        final_pct = float(overlap_data["conversation"]["overlap_ratio_pct"]) if overlap_data else current_pct
    else:
        final_pct = current_pct

    results: dict[str, dict] = {}
    for row in csv_rows:
        ch = row["channel"]
        key = row_key(session_id, ch)
        muted = muted_by_channel[ch]
        num_muted, time_muted = muted_segment_stats(muted)
        old_sig, new_sig = channel_sig_scores(
            dnsmos_channels,
            session_id,
            ch,
            seglst_path=channel_file_map[ch].seglst,
            muted=muted,
            dry_run=dry_run,
        )
        if dry_run:
            speech_after = max(
                0.0,
                original_speech_s.get(ch, 0.0) - muted_speech_s[ch],
            )
        else:
            speech_after = channel_speech_duration_s(channel_file_map[ch].seglst)
        results[key] = {
            "status": "done",
            "started_at": utc_now(),
            "completed_at": utc_now(),
            "overlap_before_pct": round(start_pct, 2),
            "overlap_after_pct": round(final_pct, 2),
            "overlap_target_pct": round(target_pct, 2),
            "stopped_reason": stopped_reason,
            "old_sig": old_sig,
            "new_sig": new_sig,
            "num_muted_segments": num_muted,
            "time_muted_segments": time_muted,
            "total_speech_time_after_muting": round(speech_after, 3),
            "muted_segments": muted,
        }
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=DEFAULT_WORKSPACE,
        help=f"Session folders root (default: {DEFAULT_WORKSPACE})",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help=f"Work queue CSV (default: {DEFAULT_CSV})",
    )
    parser.add_argument(
        "--numerical-root",
        type=Path,
        default=DEFAULT_NUMERICAL_ROOT,
        help=f"numerical_results root (default: {DEFAULT_NUMERICAL_ROOT})",
    )
    parser.add_argument("--sig-threshold", type=float, default=3.0)
    parser.add_argument("--peak-threshold-dbfs", type=float, default=0.0)
    parser.add_argument("--overlap-buffer-pp", type=float, default=2.0)
    parser.add_argument("--overwrite", action="store_true", help="Reprocess done rows from _og originals.")
    parser.add_argument(
        "--overwrite-row",
        action="append",
        default=[],
        metavar="SESSION,CHANNEL",
        help="Reprocess one CSV row (repeatable). Implies restore from _og.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Plan mutes without writing files.")
    args = parser.parse_args(argv)

    csv_path = args.csv
    if not csv_path.is_file():
        print(f"ERROR: CSV not found: {csv_path.resolve()}")
        return 1

    workspace = args.workspace
    workspace.mkdir(parents=True, exist_ok=True)
    state_path = workspace / STATE_JSON
    log_path = workspace / LOG_JSONL

    csv_rows = load_csv(csv_path)
    if not csv_rows:
        print(f"ERROR: no rows in {csv_path}")
        return 1

    overwrite_rows = set()
    for spec in args.overwrite_row:
        if "," not in spec:
            print(f"ERROR: invalid --overwrite-row {spec!r}; use SESSION,CHANNEL")
            return 1
        session_id, channel = spec.split(",", 1)
        overwrite_rows.add(row_key(session_id.strip(), channel.strip()))

    state = load_state(state_path)
    state["csv_path"] = str(csv_path)
    state["sig_threshold"] = args.sig_threshold
    state["peak_threshold_dbfs"] = args.peak_threshold_dbfs
    state["overlap_buffer_pp"] = args.overlap_buffer_pp
    state["updated_at"] = utc_now()

    jsonl_files = discover_dnsmos_individual_jsonl(args.numerical_root)
    print(
        f"Indexing failing DNSMOS windows from {args.numerical_root} "
        f"({len(jsonl_files)} JSONL file(s)) …",
    )
    numerical_index = index_failing_windows_from_jsonl(
        args.numerical_root,
        sig_threshold=args.sig_threshold,
        peak_threshold_dbfs=args.peak_threshold_dbfs,
    )
    dnsmos_channels = index_dnsmos_channels_from_jsonl(args.numerical_root)

    n_done = n_skip = n_fail = 0
    for session_id, session_rows in group_csv_rows(csv_rows):
        keys = [row_key(r["session_id"], r["channel"]) for r in session_rows]
        force = args.overwrite or any(k in overwrite_rows for k in keys)
        if not force and session_rows_done(state, session_rows):
            print(f"  SKIP {session_id} (all channels done)")
            n_skip += 1
            continue

        session_dir = workspace / session_id
        print(f"  RUN  {session_id} ({len(session_rows)} channel(s))")
        restore_channels: set[str] | None = None
        if args.overwrite:
            restore_channels = None
        elif any(k in overwrite_rows for k in keys):
            restore_channels = {
                row["channel"]
                for row in session_rows
                if row_key(row["session_id"], row["channel"]) in overwrite_rows
            }
        if force and not args.dry_run and (
            args.overwrite or (restore_channels is not None and restore_channels)
        ):
            try:
                restore_session_channels(
                    session_dir,
                    session_rows,
                    channels=restore_channels,
                )
            except FileNotFoundError as exc:
                print(f"  FAIL {session_id}: {exc}")
                n_fail += 1
                continue

        try:
            results = process_session(
                session_id,
                session_rows,
                workspace=workspace,
                numerical_index=numerical_index,
                dnsmos_channels=dnsmos_channels,
                sig_threshold=args.sig_threshold,
                peak_threshold_dbfs=args.peak_threshold_dbfs,
                overlap_buffer_pp=args.overlap_buffer_pp,
                dry_run=args.dry_run,
                log_path=log_path,
            )
        except (FileNotFoundError, ValueError) as exc:
            print(f"  FAIL {session_id}: {exc}")
            for key in keys:
                state["entries"][key] = {
                    "status": "failed",
                    "error": str(exc),
                    "updated_at": utc_now(),
                }
            n_fail += 1
            continue

        if not args.dry_run:
            for key, entry in results.items():
                state["entries"][key] = entry
            save_state(state_path, state)

        sample = next(iter(results.values()))
        print(
            f"  OK   {session_id} overlap "
            f"{sample['overlap_before_pct']:.2f}% -> {sample['overlap_after_pct']:.2f}% "
            f"(target {sample['overlap_target_pct']:.2f}%) "
            f"[{sample['stopped_reason']}]",
        )
        n_done += 1

    print(
        f"\nDone. {n_done} session(s) processed, {n_skip} skipped, {n_fail} failed."
        + (" (dry-run — no files written)" if args.dry_run else ""),
    )
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
