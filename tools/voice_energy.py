#!/usr/bin/env python3
"""Measure whether a voice track sounds ENERGETIC, without being able to hear it.

WHY THIS EXISTS (2026-08-22)
----------------------------
A reel shipped with a voiceover the user called "completely flat, slow and low
energy". The session caused it by lowering speed 1.15 -> 1.10 in answer to an
earlier note about clarity — treating the single `speed` dial as an energy dial,
twice, in opposite directions, with no way to check either.

Measuring four takes settled it in one pass, and the answer was not rate:

    take              voiced  longest pause  pitch var  words/sec
    1.15 plain          69%       0.59s       2.02 st     3.18
    1.10 plain          64%       0.88s       2.12 st     2.67   <- "flat"
    1.15 SSML+breaks    67%       0.78s       2.15 st     2.87
    1.20 plain          71%       0.49s       2.04 st     3.48   <- shipped

PITCH VARIATION IS FLAT ACROSS ALL FOUR. The take that sounded lifeless has the
same inflection as the one that did not; what it has is DEAD AIR — nearly twice
the pauses, with gaps up to 0.88s landing mid-thought. Energy in a TTS read is
pause structure, not rate.

Also settled here: SSML <break> ADDS to the engine's own sentence pause instead
of replacing it, so breaks lengthen a read you are trying to tighten. To remove
dead air, drop sentence boundaries (commas for periods) or raise speed.

    python3 tools/voice_energy.py a.mp3=label b.mp3=other-label

Read `voiced %` and `longest pause` first — they move with perceived energy.
Compare VO-ONLY files: on a finished master the music bed fills every gap, so
voiced% and the pause counts stop meaning anything.
"""
import sys, subprocess, numpy as np
def load(p, sr=16000):
    raw = subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar",str(sr),
                          "-f","s16le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(np.float32)/32768.0, sr

def f0_track(x, sr, fmin=70, fmax=320, hop=0.010, win=0.040):
    H,W = int(sr*hop), int(sr*win)
    lo,hi = int(sr/fmax), int(sr/fmin)
    out=[]
    for i in range(0, len(x)-W, H):
        f = x[i:i+W]
        e = float(np.sqrt(np.mean(f**2)))
        if e < 0.012: out.append(0.0); continue
        f = f - f.mean()
        ac = np.correlate(f, f, 'full')[W-1:]
        if ac[0] <= 0: out.append(0.0); continue
        seg = ac[lo:hi]
        if len(seg)==0: out.append(0.0); continue
        k = int(np.argmax(seg))+lo
        out.append(sr/k if ac[k]/ac[0] > 0.32 else 0.0)
    return np.array(out)

def rms_track(x, sr, hop=0.010, win=0.040):
    H,W=int(sr*hop),int(sr*win)
    return np.array([np.sqrt(np.mean(x[i:i+W]**2)) for i in range(0,len(x)-W,H)])

def report(path,label):
    x,sr = load(path)
    f0 = f0_track(x,sr); v = f0[f0>0]
    r  = rms_track(x,sr); rv = r[r>1e-4]
    semis = 12*np.log2(v/np.median(v)) if len(v) else np.array([0.0])
    db = 20*np.log10(rv/np.max(rv))
    # pauses
    thr = 0.012; quiet = r < thr
    runs=[];c=0
    for q in quiet:
        if q: c+=1
        else:
            if c: runs.append(c*0.010)
            c=0
    if c: runs.append(c*0.010)
    pauses=[p for p in runs if p>=0.18]
    print(f"\n=== {label} ===")
    print(f"  duration          {len(x)/sr:6.2f}s   voiced {100*len(v)/max(1,len(f0)):.0f}%")
    print(f"  pitch median      {np.median(v):6.1f} Hz")
    print(f"  PITCH VARIATION   {np.std(semis):6.2f} semitones (std)   p5-p95 span {np.percentile(semis,95)-np.percentile(semis,5):5.2f} st")
    print(f"  LOUDNESS DYNAMICS {np.std(db):6.2f} dB (std)            p5-p95 span {np.percentile(db,95)-np.percentile(db,5):5.2f} dB")
    print(f"  pauses >=0.18s    {len(pauses):3d}   median {np.median(pauses) if pauses else 0:.2f}s  longest {max(pauses) if pauses else 0:.2f}s")

for a in sys.argv[1:]:
    p,l = a.split("=",1); report(p,l)
