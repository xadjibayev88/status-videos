"""Original light, playful music bed + a few SFX for the Pet Rock short (numpy synthesis, 48 kHz).
Usage: python3 audio/petrock_music.py <words.json> <out.wav>"""
import json, sys, wave
import numpy as np

SR = 48000
words = json.load(open(sys.argv[1]))
DUR = words[-1]["t1"] + 1.6
N = int(DUR * SR)
t = np.arange(N) / SR
out = np.zeros(N)

def note(f, t0, dur, amp=0.25, kind="pluck"):
    i0 = int(t0 * SR); n = int(dur * SR)
    if i0 >= N: return
    n = min(n, N - i0); tt = np.arange(n) / SR
    if kind == "pluck":
        env = np.exp(-tt * 9.0); w = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) + 0.12 * np.sin(6 * np.pi * f * tt)
    elif kind == "bass":
        env = np.exp(-tt * 5.0); w = np.sin(2 * np.pi * f * tt) + 0.2 * np.sin(4 * np.pi * f * tt)
    else:  # bell
        env = np.exp(-tt * 3.0); w = np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 6)
    a = np.minimum(1, tt / 0.004)
    out[i0:i0 + n] += amp * env * a * w

mid = lambda m: 440 * 2 ** ((m - 69) / 12)
BPM = 112; Q = 60 / BPM
# I - vi - IV - V in C, light staccato comping + a whistly melody
prog = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62])]
mel = [72, 74, 76, 79, 77, 76, 74, 72, 74, 76, 72, 69, 71, 72, 74, 79]
bar, k = 0, 0
while bar * 4 * Q < DUR:
    root, ch = prog[bar % 4]
    for beat in range(4):
        tb = (bar * 4 + beat) * Q
        if beat % 2 == 0: note(mid(root), tb, Q * 1.6, 0.30, "bass")
        else:
            for m in ch: note(mid(m), tb, Q * 0.5, 0.07)
    for half in range(2):
        tm = (bar * 4 + half * 2 + 1.5) * Q
        note(mid(mel[k % len(mel)]), tm, Q * 0.9, 0.06, "bell"); k += 1
    bar += 1
# SFX at story beats
def at(i): return words[i]["t0"]
def sparkle(t0):
    for j, m in enumerate([84, 88, 91, 96]): note(mid(m), t0 + j * 0.05, 0.6, 0.12, "bell")
def thud(t0):
    i0 = int(t0 * SR); n = int(0.25 * SR); tt = np.arange(n) / SR
    out[i0:i0 + n] += 0.5 * np.exp(-tt * 25) * np.sin(2 * np.pi * (90 - 60 * tt) * tt)
def ding(t0):
    note(mid(93), t0, 1.2, 0.2, "bell"); note(mid(100), t0 + 0.08, 1.0, 0.12, "bell")
sparkle(at(5)); thud(at(45) + 0.25); ding(at(55)); sparkle(at(68)); ding(at(72)); sparkle(at(88))
# fade in/out, normalise to a quiet bed
fade = np.minimum(1, t / 0.4) * np.minimum(1, (DUR - t) / 1.2)
out *= fade
out = out / max(1e-6, np.max(np.abs(out))) * 0.5
st = np.stack([out, out], 1)
pcm = (np.clip(st, -1, 1) * 32767).astype(np.int16)
with wave.open(sys.argv[2], "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("music", round(DUR, 2), "s")
