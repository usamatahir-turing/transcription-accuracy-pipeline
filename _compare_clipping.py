"""Compare DNSMOS clipping stats vs batch8and9reference."""
import json
import math
from pathlib import Path

REF = Path("batch8and9review/batch_8_9_numeric_results/dnsmos/individual/batch9")
CONV_ROOT = Path("Conversations/delivery_batch_08082026")
SESSIONS = ["NV-GR-SS13-CONVO22", "NV-GR-SS19-CONVO32", "NV-PT-SS19-CONVO41"]


def load_ref(session_id: str) -> dict | None:
    for path in REF.glob("*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            if rec.get("session_id") == session_id:
                return rec
    return None


def peak_close(a: float | None, b: float | None, tol: float = 0.001) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return abs(a - b) < tol


def main() -> None:
    mismatches: list[str] = []
    for sid in SESSIONS:
        ref = load_ref(sid)
        if not ref:
            print(f"{sid}: NO REF")
            continue
        print(f"=== {sid} ===")
        ref_by = {c["speaker"]: c for c in ref["channels"]}
        conv = CONV_ROOT / sid
        for spk in sorted(ref_by):
            r = ref_by[spk]
            ours_path = conv / f"{spk}_dnsmos.json"
            if not ours_path.exists():
                print(f"  {spk}: MISSING")
                continue
            data = json.loads(ours_path.read_text(encoding="utf-8"))
            o_dns = data["dnsmos"]
            o_wins = data.get("windows", [])

            ref_peak = r.get("speech_peak_dbfs")
            our_peak = o_dns.get("speech_peak_dbfs")
            ref_fs = r.get("full_scale_samples")
            our_fs = o_dns.get("full_scale_samples")
            ref_ratio = r.get("full_scale_clipped_sample_ratio")
            our_ratio = o_dns.get("full_scale_clipped_sample_ratio")

            r_cw = sum(1 for w in r["windows"] if w.get("full_scale_samples", 0) > 0)
            o_cw = sum(1 for w in o_wins if w.get("full_scale_samples", 0) > 0)

            ok = (
                peak_close(ref_peak, our_peak)
                and ref_fs == our_fs
                and r_cw == o_cw
                and (
                    ref_ratio is None or our_ratio is None
                    or abs(ref_ratio - our_ratio) < 1e-9
                )
            )
            print(
                f"  {spk}: peak ref={ref_peak!r} ours={our_peak!r} "
                f"fs ref={ref_fs} ours={our_fs} clipped_w ref={r_cw} ours={o_cw} "
                f"{'OK' if ok else 'MISMATCH'}"
            )
            if not ok:
                mismatches.append(f"{sid}/{spk}")
                ref_w_by = {(w["start_sec"], w["end_sec"]): w for w in r["windows"]}
                for ow in o_wins:
                    key = (ow["start_sec"], ow["end_sec"])
                    rw = ref_w_by.get(key)
                    if not rw:
                        continue
                    if rw.get("full_scale_samples") != ow.get("full_scale_samples"):
                        print(
                            f"    win {key}: ref_fs={rw.get('full_scale_samples')} "
                            f"ours={ow.get('full_scale_samples')} "
                            f"ref_peak={rw.get('speech_peak')} "
                            f"ours={ow.get('speech_peak')}"
                        )
                        break
                    ref_pk = rw.get("speech_peak")
                    our_pk = ow.get("speech_peak")
                    if ref_pk is not None and our_pk is not None:
                        if abs(ref_pk - our_pk) > 1e-4:
                            print(
                                f"    win {key}: peak ref={ref_pk} ours={our_pk}"
                            )
                            break

    print(f"\nTotal mismatches: {len(mismatches)}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
