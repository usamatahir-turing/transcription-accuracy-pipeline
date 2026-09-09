"""Unit tests for mute_failing_regions helpers."""

from __future__ import annotations

from pathlib import Path

from conversation_structure_pipeline.mute_failing_regions import (
    MuteCandidate,
    breaches_overlap_floor,
    channel_sig_scores,
    discover_dnsmos_individual_jsonl,
    group_csv_rows,
    index_failing_windows_from_jsonl,
    load_csv,
    muted_segment_stats,
    og_path,
    overlap_target_pct,
    peak_dbfs,
    pick_next_candidate,
    row_key,
    segments_without_row,
    speech_spans_excluding_mutes,
    weighted_mean_sig,
    would_exceed_speech_cap,
)


def test_og_path_suffix_before_extension() -> None:
    path = Path("laurentina.c@turing.com.wav")
    assert og_path(path).name == "laurentina.c@turing.com_og.wav"


def test_peak_dbfs_zero_at_full_scale() -> None:
    assert peak_dbfs(1.0) == 0.0


def test_overlap_target_six_speakers() -> None:
    assert overlap_target_pct(6, 2.0) == 14.0


def test_breaches_overlap_floor() -> None:
    assert breaches_overlap_floor(15.0, 11.0, 12.0) is True
    assert breaches_overlap_floor(15.0, 13.0, 12.0) is False
    assert breaches_overlap_floor(10.48, 10.48, 12.0) is False
    assert breaches_overlap_floor(41.0, 41.0, 12.0) is False
    assert breaches_overlap_floor(41.0, 38.0, 12.0) is False


def test_would_exceed_speech_cap() -> None:
    assert would_exceed_speech_cap(100.0, 15.0, 5.0) is False
    assert would_exceed_speech_cap(100.0, 19.0, 2.0) is True
    assert would_exceed_speech_cap(100.0, 0.0, 20.0) is False
    assert would_exceed_speech_cap(100.0, 0.0, 20.01) is True


def test_pick_next_candidate_round_robin() -> None:
    c1 = MuteCandidate(
        "a", "a@turing.com", "dnsmos_sig", 0, 9, 2.0, None, 1, 2, "w1",
    )
    c2 = MuteCandidate(
        "b", "b@turing.com", "dnsmos_sig", 0, 9, 2.0, None, 3, 4, "w2",
    )
    picked, rr = pick_next_candidate([c1, c2], ["a", "b"], 0)
    assert picked is not None
    assert picked.channel_local == "a"
    picked2, _ = pick_next_candidate([c1, c2], ["a", "b"], rr)
    assert picked2 is not None
    assert picked2.channel_local == "b"


def test_segments_without_row() -> None:
    segments = [(0.0, 2.0, "SPK01"), (5.0, 1.0, "SPK02")]
    out = segments_without_row(segments, speaker="SPK01", start=0.0, end=2.0)
    assert out == [(5.0, 1.0, "SPK02")]


def test_weighted_mean_sig_reweights_after_span_removal() -> None:
    windows = [
        {"start_sec": 0.0, "end_sec": 9.01, "sig": 2.0, "speech_weight_sec": 5.0},
        {"start_sec": 1.0, "end_sec": 10.01, "sig": 4.0, "speech_weight_sec": 8.0},
    ]
    all_spans = [(0.0, 6.0), (1.0, 10.0)]
    reduced_spans = [(1.0, 10.0)]
    old = weighted_mean_sig(windows, all_spans)
    new = weighted_mean_sig(windows, reduced_spans)
    assert old is not None and new is not None
    assert new > old


def test_muted_segment_stats() -> None:
    segments = [
        {"seglst_start_sec": 1.0, "seglst_end_sec": 3.5},
        {"seglst_start_sec": 10.0, "seglst_end_sec": 12.25},
    ]
    assert muted_segment_stats(segments) == (2, 4.75)


def test_row_key() -> None:
    assert row_key("NV-EN-SS01-CONVO01", "joseph.b8") == "NV-EN-SS01-CONVO01|joseph.b8"


def test_discover_dnsmos_jsonl_includes_rework_exports() -> None:
    root = Path("numerical_results")
    if not root.is_dir():
        return
    files = discover_dnsmos_individual_jsonl(root)
    assert files, "expected at least one dnsmos/individual JSONL under numerical_results"
    assert any("rework_08282026_numerical_results" in p.as_posix() for p in files)


def test_index_includes_nv_pt_ss19_convo41_laurentina() -> None:
    root = Path("numerical_results")
    if not root.is_dir():
        return
    idx = index_failing_windows_from_jsonl(
        root, sig_threshold=3.0, peak_threshold_dbfs=0.0,
    )
    windows = idx.get("NV-PT-SS19-CONVO41", {}).get("laurentina.c", [])
    assert windows, "expected failing windows for NV-PT-SS19-CONVO41 laurentina.c"


def test_group_csv_rows_preserves_order(tmp_path: Path) -> None:
    csv_path = tmp_path / "queue.csv"
    csv_path.write_text(
        "session_id,channel\n"
        "S1,a\n"
        "S2,b\n"
        "S1,c\n",
        encoding="utf-8",
    )
    rows = load_csv(csv_path)
    grouped = group_csv_rows(rows)
    assert [sid for sid, _ in grouped] == ["S1", "S2"]
    assert len(grouped[0][1]) == 2
