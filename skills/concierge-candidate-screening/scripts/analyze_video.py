#!/usr/bin/env python3
"""Turn a recruiter interview video into evidence Claude can review without anyone watching it.

Outputs (in --out):
  contact_sheet.jpg   12 frames sampled evenly across the call, tiled 4x3 (for the setup check)
  voice_metrics.json  pitch variation, loudness variation and pause ratio, with plain-language bands

Usage:
  python analyze_video.py interview.mp4 --out workdir/Ana_Torres_video \
      [--segments "02:10-03:40,05:00-07:30"]   # candidate's speaking turns, from transcript timestamps

Needs only ffmpeg/ffprobe and numpy. Voice metrics are a proxy for energy and warmth, not for accent.
Without --segments the numbers mix the recruiter's voice with the candidate's.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

import numpy as np

SR = 16000


def ts(s):
    parts = [float(p) for p in s.strip().split(":")]
    sec = 0.0
    for p in parts:
        sec = sec * 60 + p
    return sec


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def has_stream(path, kind):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", kind, "-show_entries",
                          "stream=index", "-of", "csv=p=0", path], capture_output=True, text=True)
    return bool(out.stdout.strip())


def contact_sheet(path, dur, out):
    n = 12
    rate = n / max(dur, 1.0)
    target = os.path.join(out, "contact_sheet.jpg")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", path, "-vf",
           f"fps={rate:.6f},scale=360:-2,tile=4x3:padding=4:color=white", "-frames:v", "1", target]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return target if r.returncode == 0 and os.path.exists(target) else None


def load_audio(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR),
                        "-f", "s16le", "-"], capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[:300])
    return np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32) / 32768.0


def frame_pitch(x):
    """Autocorrelation pitch for one frame; returns (f0 or None, periodicity strength)."""
    x = x - x.mean()
    if not np.any(x):
        return None, 0.0
    ac = np.correlate(x, x, mode="full")[len(x) - 1:]
    ac /= ac[0] + 1e-9
    lo, hi = int(SR / 400), int(SR / 75)
    seg = ac[lo:hi]
    if len(seg) == 0:
        return None, 0.0
    k = int(np.argmax(seg))
    strength = float(seg[k])
    return (SR / (lo + k) if strength > 0.45 else None), strength


def analyze(audio, segments):
    if segments:
        parts = [audio[int(a * SR):int(b * SR)] for a, b in segments]
        audio = np.concatenate([p for p in parts if len(p)]) if parts else audio
    win, hop = int(0.04 * SR), int(0.01 * SR)
    n = max(0, (len(audio) - win) // hop)
    if n < 50:
        return {"error": "not enough audio to analyze"}
    rms = np.array([np.sqrt(np.mean(audio[i * hop:i * hop + win] ** 2)) for i in range(n)])
    db = 20 * np.log10(rms + 1e-6)
    floor = np.percentile(db, 15)
    speech = db > max(floor + 12, -50)
    f0s, speech_db = [], db[speech]
    for i in np.where(speech)[0][::2]:  # every other frame is plenty
        f0, _ = frame_pitch(audio[i * hop:i * hop + win])
        if f0:
            f0s.append(f0)
    res = {
        "analyzed_seconds": round(len(audio) / SR, 1),
        "speech_seconds": round(float(speech.sum()) * hop / SR, 1),
        "pause_ratio": round(1 - float(speech.mean()), 2),
    }
    if len(f0s) < 30:
        res["pitch"] = {"error": "too few voiced frames (bad audio?)"}
    else:
        f0s = np.array(f0s)
        med = float(np.median(f0s))
        st = 12 * np.log2(f0s / med)
        st = st[np.abs(st) < 12]  # drop octave errors
        sd = float(np.std(st))
        band = "flat" if sd < 1.8 else ("normal" if sd < 4.0 else "lively")
        res["pitch"] = {"variation_semitones": round(sd, 2), "band": band}
    ld = float(np.std(speech_db)) if len(speech_db) else 0.0
    res["loudness"] = {"variation_db": round(ld, 1),
                       "band": "flat" if ld < 4 else ("normal" if ld < 8 else "lively")}
    res["pauses_band"] = ("very halting" if res["pause_ratio"] > 0.6 else
                          "frequent pauses" if res["pause_ratio"] > 0.45 else "fluent")
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", required=True)
    ap.add_argument("--segments", default="", help="comma-separated mm:ss-mm:ss candidate turns")
    a = ap.parse_args()
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("ffmpeg/ffprobe not installed; cannot analyze video"); sys.exit(1)
    os.makedirs(a.out, exist_ok=True)
    dur = duration(a.video)
    if dur is None:
        print("Could not read video (corrupted or unsupported)"); sys.exit(1)
    segs = []
    for s in filter(None, (p.strip() for p in a.segments.split(","))):
        b, e = s.split("-")
        segs.append((ts(b), ts(e)))

    report = {"video": os.path.basename(a.video), "duration_seconds": round(dur, 1),
              "segments_used": a.segments or None,
              "note": ("Metrics cover only the candidate segments given." if segs else
                       "No segments given: metrics mix recruiter and candidate voices; weigh lightly.")}
    if has_stream(a.video, "v"):
        cs = contact_sheet(a.video, dur, a.out)
        report["contact_sheet"] = cs or "failed"
    else:
        report["contact_sheet"] = "no video stream (audio only)"
    if has_stream(a.video, "a"):
        try:
            report["voice"] = analyze(load_audio(a.video), segs)
        except Exception as e:  # noqa: BLE001
            report["voice"] = {"error": str(e)}
    else:
        report["voice"] = {"error": "no audio stream"}
    out = os.path.join(a.out, "voice_metrics.json")
    json.dump(report, open(out, "w"), indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
