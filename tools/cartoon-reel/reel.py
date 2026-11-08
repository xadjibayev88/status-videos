#!/usr/bin/env python3
"""2D multfilm uslubidagi 30 soniyalik vertikal reel (1080x1920) — kod bilan chiziladi.

Uslub (egasi ko'rsatgan namunadan): to'q ko'k fon, tekis chizilgan katta boshli qahramonlar,
olomon, katta hisoblagich raqamlar, tepada 2-3 so'zli katta oq yozuv (Anton), har sahnada
yengil "punch" zoom, oxirida qahramon tomoshabinga savol beradi.

Ishlatish:
    python3 reel.py storyboard.json voice.mp3 out.mp4
storyboard.json: {"scenes": [{"type": ..., "caption": "...", "dur": 2.5, ...}, ...]}
Sahna turlari: number, year, character, crowd, icon, split, ending.
Bog'liqlik: Pillow, ffmpeg. Tashqi API yo'q, pul sarflanmaydi.
"""
import json
import math
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
HERE = Path(__file__).resolve().parent
FONT = str(HERE / "fonts" / "Anton-Regular.ttf")
BG_TOP, BG_BOTTOM = (10, 14, 40), (28, 22, 70)
SKINS = [(241, 194, 150), (224, 172, 125), (198, 140, 96), (250, 210, 170)]
SHIRTS = [(200, 30, 45), (30, 90, 200), (240, 200, 40), (30, 150, 70), (240, 240, 240), (120, 60, 170)]


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size)


def ease_out(t: float) -> float:
    return 1 - (1 - min(max(t, 0), 1)) ** 3


# ---------------------------------------------------------------- fon
def background() -> Image.Image:
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        k = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * k) for a, b in zip(BG_TOP, BG_BOTTOM)))
    rnd = random.Random(7)
    for _ in range(140):
        x, y, r = rnd.randrange(W), rnd.randrange(H), rnd.choice([1, 1, 2, 3])
        c = rnd.randrange(120, 255)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(c, c, min(255, c + 20)))
    return img


# ---------------------------------------------------------------- qahramon
def draw_person(d: ImageDraw.ImageDraw, cx: float, cy: float, s: float, skin, shirt, *,
                mood="happy", mouth_open=False, blink=False, hair=(30, 25, 25), label="",
                hat=None, arm_up=False, tear=False):
    """Tekis 2D qahramon: katta bosh, katta ko'zlar, oddiy tana. (cx, cy) — bosh markazi, s — o'lcham."""
    hr = 1.0 * s  # bosh radiusi
    # tana
    bw, bh = 1.25 * s, 1.7 * s
    by = cy + hr * 0.9
    d.rounded_rectangle([cx - bw / 2, by, cx + bw / 2, by + bh], radius=int(0.3 * s), fill=shirt, outline=(0, 0, 0), width=max(2, int(s * 0.05)))
    # qo'llar
    aw = max(6, int(s * 0.22))
    if arm_up:
        d.line([cx + bw / 2 - 5, by + 20, cx + bw / 2 + 0.55 * s, by - 0.9 * s], fill=skin, width=aw)
        d.ellipse([cx + bw / 2 + 0.55 * s - aw, by - 0.9 * s - aw, cx + bw / 2 + 0.55 * s + aw, by - 0.9 * s + aw], fill=skin)
    else:
        d.line([cx + bw / 2 - 5, by + 20, cx + bw / 2 + 0.25 * s, by + bh * 0.8], fill=skin, width=aw)
    d.line([cx - bw / 2 + 5, by + 20, cx - bw / 2 - 0.25 * s, by + bh * 0.8], fill=skin, width=aw)
    if label:
        size = int(s * 0.75)
        f = font(size)
        while d.textlength(label, font=f) > bw * 0.82 and size > 12:  # yozuv ko'ylakdan chiqmasin
            size -= 4
            f = font(size)
        tw = d.textlength(label, font=f)
        d.text((cx - tw / 2, by + bh * 0.22), label, font=f, fill=(255, 255, 255) if sum(shirt) < 500 else (20, 20, 20))
    # bosh
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=skin, outline=(0, 0, 0), width=max(2, int(s * 0.05)))
    # soch / shapka
    if hat:
        d.chord([cx - hr * 1.02, cy - hr * 1.15, cx + hr * 1.02, cy + hr * 0.2], 180, 360, fill=hat, outline=(0, 0, 0), width=3)
    else:
        d.chord([cx - hr, cy - hr, cx + hr, cy + hr * 0.1], 180, 360, fill=hair)
    # ko'zlar
    ex, ey, er = 0.38 * hr, cy + 0.05 * hr, 0.26 * hr
    for sx in (-1, 1):
        x = cx + sx * ex
        if blink:
            d.line([x - er, ey, x + er, ey], fill=(0, 0, 0), width=max(3, int(s * 0.07)))
        else:
            d.ellipse([x - er, ey - er, x + er, ey + er], fill=(255, 255, 255), outline=(0, 0, 0), width=3)
            pr = er * 0.5
            d.ellipse([x - pr, ey - pr + 2, x + pr, ey + pr + 2], fill=(0, 0, 0))
            if mood == "sad":
                d.chord([x - er, ey - er, x + er, ey + er], 180, 360, fill=skin, outline=(0, 0, 0), width=3)
    # og'iz
    my, mw = cy + 0.55 * hr, 0.35 * hr
    if mouth_open:
        d.ellipse([cx - mw * 0.6, my - mw * 0.35, cx + mw * 0.6, my + mw * 0.55], fill=(120, 20, 30), outline=(0, 0, 0), width=3)
    elif mood == "sad":
        d.arc([cx - mw, my, cx + mw, my + mw], 200, 340, fill=(0, 0, 0), width=4)
    else:
        d.arc([cx - mw, my - mw, cx + mw, my + mw * 0.6], 20, 160, fill=(0, 0, 0), width=4)
    if tear:
        d.ellipse([cx + ex - 8, ey + er + 4, cx + ex + 10, ey + er + 30], fill=(80, 170, 255))


# ---------------------------------------------------------------- yozuv
def caption(img: Image.Image, text: str, t: float):
    if not text:
        return
    d = ImageDraw.Draw(img)
    size = 150 if len(text) <= 12 else 120 if len(text) <= 18 else 96
    k = 0.85 + 0.15 * ease_out(t / 0.25)
    f = font(int(size * k))
    lines = text.upper().split("\n")
    y = 170
    for line in lines:
        tw = d.textlength(line, font=f)
        d.text(((W - tw) / 2, y), line, font=f, fill=(255, 255, 255), stroke_width=8, stroke_fill=(0, 0, 0))
        y += int(size * k * 1.15)


def big_text(d, text, y, size, color=(255, 255, 255), stroke=8):
    f = font(size)
    tw = d.textlength(text, font=f)
    d.text(((W - tw) / 2, y), text, font=f, fill=color, stroke_width=stroke, stroke_fill=(0, 0, 0))


# ---------------------------------------------------------------- sahnalar
def scene_number(img, sc, t, dur, talk):
    d = ImageDraw.Draw(img)
    a, b = sc.get("from", 0), sc["value"]
    v = round(a + (b - a) * ease_out(t / max(dur * 0.7, 0.1)))
    # tablo
    d.rounded_rectangle([190, 640, 890, 1260], radius=40, fill=(18, 22, 45), outline=(255, 200, 40), width=10)
    big_text(d, sc.get("top", ""), 690, 80, (255, 200, 40), 0)
    big_text(d, f"{v:,}".replace(",", " ") + sc.get("suffix", ""), 790, 300 if b < 10000 else 230)
    big_text(d, sc.get("label", ""), 1120, 90, (255, 255, 255), 0)


def scene_year(img, sc, t, dur, talk):
    d = ImageDraw.Draw(img)
    y0, y1 = sc.get("from", sc["value"] - 20), sc["value"]
    v = round(y0 + (y1 - y0) * ease_out(t / max(dur * 0.6, 0.1)))
    d.rounded_rectangle([240, 700, 840, 1200], radius=36, fill=(25, 30, 70), outline=(255, 255, 255), width=8)
    big_text(d, sc.get("top", "YIL"), 740, 90, (255, 200, 40), 0)
    big_text(d, str(v), 850, 260)


def scene_character(img, sc, t, dur, talk):
    d = ImageDraw.Draw(img)
    bob = math.sin(t * 6) * 6
    blink = (t % 2.6) < 0.12
    if sc.get("ground", True):
        d.ellipse([-200, 1450, W + 200, 2300], fill=tuple(sc.get("ground_color", (40, 140, 70))))
    for i, extra in enumerate(sc.get("crowd_back", 0) and range(8) or []):
        pass
    draw_person(d, W / 2, 900 + bob, 190, tuple(sc.get("skin", SKINS[0])), tuple(sc.get("shirt", SHIRTS[0])),
                mood=sc.get("mood", "happy"), mouth_open=talk and int(t * 8) % 2 == 0, blink=blink,
                hair=tuple(sc.get("hair", (30, 25, 25))), label=sc.get("label", ""),
                hat=tuple(sc["hat"]) if sc.get("hat") else None, arm_up=sc.get("arm_up", False), tear=sc.get("tear", False))
    if sc.get("prop"):
        draw_prop(d, sc["prop"], 820, 1180 + bob, 1.0)


def scene_crowd(img, sc, t, dur, talk):
    d = ImageDraw.Draw(img)
    rnd = random.Random(sc.get("seed", 3))
    rows = 7
    for r in range(rows):
        s = 42 + r * 9
        y = 560 + r * 175
        n = int(W / (s * 2.3)) + 1
        for i in range(n):
            x = (i + 0.5 + (r % 2) * 0.5) * (W / n)
            jump = abs(math.sin(t * 7 + i * 1.3 + r)) * 18 if sc.get("cheer", True) else 0
            draw_person(d, x, y - jump, s, rnd.choice(SKINS), rnd.choice(SHIRTS), mouth_open=(i + r) % 3 == 0,
                        blink=False, arm_up=(i + r) % 2 == 0)


PROPS = {}


def draw_prop(d, kind, x, y, k):
    if kind == "trophy":
        d.polygon([(x - 90 * k, y - 160 * k), (x + 90 * k, y - 160 * k), (x + 55 * k, y - 20 * k), (x - 55 * k, y - 20 * k)], fill=(255, 200, 40), outline=(0, 0, 0))
        d.rectangle([x - 18 * k, y - 20 * k, x + 18 * k, y + 50 * k], fill=(230, 170, 30), outline=(0, 0, 0))
        d.rectangle([x - 70 * k, y + 50 * k, x + 70 * k, y + 85 * k], fill=(120, 70, 30), outline=(0, 0, 0))
    elif kind == "medal":
        d.polygon([(x - 50 * k, y - 220 * k), (x - 15 * k, y - 220 * k), (x + 10 * k, y - 80 * k), (x - 25 * k, y - 80 * k)], fill=(200, 30, 45))
        d.polygon([(x + 50 * k, y - 220 * k), (x + 15 * k, y - 220 * k), (x - 10 * k, y - 80 * k), (x + 25 * k, y - 80 * k)], fill=(30, 90, 200))
        d.ellipse([x - 70 * k, y - 110 * k, x + 70 * k, y + 30 * k], fill=(255, 200, 40), outline=(0, 0, 0), width=4)
    elif kind == "car":
        d.rounded_rectangle([x - 200 * k, y - 60 * k, x + 200 * k, y + 40 * k], radius=20, fill=(20, 20, 20))
        d.rounded_rectangle([x - 110 * k, y - 140 * k, x + 90 * k, y - 50 * k], radius=20, fill=(30, 30, 30))
        for wx in (-120, 120):
            d.ellipse([x + (wx - 45) * k, y + 5 * k, x + (wx + 45) * k, y + 95 * k], fill=(60, 60, 60), outline=(0, 0, 0), width=6)
    elif kind == "dish":
        d.ellipse([x - 160 * k, y - 60 * k, x + 160 * k, y + 60 * k], fill=(220, 235, 245), outline=(0, 0, 0), width=5)
        d.ellipse([x - 110 * k, y - 40 * k, x + 110 * k, y + 40 * k], fill=(240, 200, 120))
        d.ellipse([x - 30 * k, y - 22 * k, x + 50 * k, y + 22 * k], fill=(60, 140, 60))
    elif kind == "book":
        d.rectangle([x - 120 * k, y - 160 * k, x + 120 * k, y + 160 * k], fill=(180, 40, 40), outline=(0, 0, 0), width=5)
        d.rectangle([x - 100 * k, y - 140 * k, x + 100 * k, y - 80 * k], fill=(255, 220, 120))
    elif kind == "mouse":
        for ex in (-70, 70):
            d.ellipse([x + (ex - 55) * k, y - 170 * k, x + (ex + 55) * k, y - 60 * k], fill=(15, 15, 15))
        d.ellipse([x - 80 * k, y - 100 * k, x + 80 * k, y + 60 * k], fill=(15, 15, 15))
        d.ellipse([x - 55 * k, y - 50 * k, x + 55 * k, y + 50 * k], fill=(245, 205, 165))
        for ex in (-22, 22):
            d.ellipse([x + (ex - 10) * k, y - 30 * k, x + (ex + 10) * k, y + 5 * k], fill=(0, 0, 0))
    elif kind == "rabbit":
        for ex in (-35, 35):
            d.ellipse([x + (ex - 22) * k, y - 260 * k, x + (ex + 22) * k, y - 70 * k], fill=(240, 240, 240), outline=(0, 0, 0), width=4)
        d.ellipse([x - 80 * k, y - 100 * k, x + 80 * k, y + 60 * k], fill=(240, 240, 240), outline=(0, 0, 0), width=4)
    elif kind == "x":
        d.line([x - 120, y - 120, x + 120, y + 120], fill=(230, 30, 40), width=28)
        d.line([x + 120, y - 120, x - 120, y + 120], fill=(230, 30, 40), width=28)
    elif kind == "petri":
        d.ellipse([x - 220 * k, y - 220 * k, x + 220 * k, y + 220 * k], fill=(200, 230, 240), outline=(255, 255, 255), width=10)
        rnd = random.Random(5)
        for _ in range(60):
            a, r = rnd.uniform(0, 6.28), rnd.uniform(110, 200)
            px, py = x + math.cos(a) * r * k, y + math.sin(a) * r * k
            d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(230, 210, 80))
        d.ellipse([x - 70 * k, y - 60 * k, x + 80 * k, y + 70 * k], fill=(60, 150, 80))
    elif kind == "clock":
        d.ellipse([x - 150 * k, y - 150 * k, x + 150 * k, y + 150 * k], fill=(255, 255, 255), outline=(0, 0, 0), width=8)
        d.line([x, y, x, y - 110 * k], fill=(0, 0, 0), width=10)
        d.line([x, y, x + 80 * k, y + 20 * k], fill=(200, 30, 45), width=8)
    elif kind == "tv":
        d.rounded_rectangle([x - 200 * k, y - 140 * k, x + 200 * k, y + 140 * k], radius=24, fill=(40, 40, 50), outline=(0, 0, 0), width=6)
        d.rectangle([x - 170 * k, y - 110 * k, x + 170 * k, y + 110 * k], fill=(120, 200, 255))
    elif kind == "brace":
        d.rectangle([x - 18, y - 200, x + 18, y + 200], fill=(170, 170, 180), outline=(0, 0, 0), width=4)
        for yy in (-150, 0, 150):
            d.rectangle([x - 60, y + yy - 12, x + 60, y + yy + 12], fill=(120, 120, 130))


def scene_icon(img, sc, t, dur, talk):
    d = ImageDraw.Draw(img)
    k = 1.6 * (0.6 + 0.4 * ease_out(t / 0.35))
    draw_prop(d, sc["prop"], W / 2, 1050, k)
    if sc.get("sub"):
        big_text(d, sc["sub"], 1420, 90, (255, 200, 40), 6)


def scene_split(img, sc, t, dur, talk):
    """Ikki holat yonma-yon (oldin/keyin): chapda va o'ngda qahramon yoki raqam."""
    d = ImageDraw.Draw(img)
    for side, item in ((-1, sc["left"]), (1, sc["right"])):
        cx = W / 2 + side * 270
        d.rounded_rectangle([cx - 240, 620, cx + 240, 1400], radius=30, fill=(25, 30, 70), outline=tuple(item.get("color", (255, 255, 255))), width=8)
        big_text_at(d, item.get("top", ""), cx, 660, 70, tuple(item.get("color", (255, 255, 255))))
        big_text_at(d, item.get("value", ""), cx, 820, 170, (255, 255, 255))
        big_text_at(d, item.get("label", ""), cx, 1060, 70, (255, 255, 255))
    if t > dur * 0.3:
        big_text(d, "→", 900, 140, (255, 200, 40))


def big_text_at(d, text, cx, y, size, color):
    if not text:
        return
    f = font(size)
    tw = d.textlength(text, font=f)
    d.text((cx - tw / 2, y), text, font=f, fill=color, stroke_width=6, stroke_fill=(0, 0, 0))


def scene_ending(img, sc, t, dur, talk):
    """Qahramon tomoshabinga qarab savol beradi; atrofda olomon."""
    d = ImageDraw.Draw(img)
    rnd = random.Random(11)
    for i in range(9):
        x = 60 + i * 120
        draw_person(d, x, 1500 + (i % 2) * 40, 48, rnd.choice(SKINS), rnd.choice(SHIRTS), arm_up=i % 2 == 0)
    draw_person(d, W / 2, 900 + math.sin(t * 5) * 6, 200, SKINS[1], tuple(sc.get("shirt", (25, 25, 30))),
                mouth_open=talk and int(t * 8) % 2 == 0, blink=(t % 2.4) < 0.12, hat=(30, 30, 90), label=sc.get("label", ""))
    big_text(d, "?", 560, 220, (255, 200, 40), 10)


SCENES = {"number": scene_number, "year": scene_year, "character": scene_character, "crowd": scene_crowd,
          "icon": scene_icon, "split": scene_split, "ending": scene_ending}


# ---------------------------------------------------------------- render
def render(board: dict, voice: str, out: str):
    scenes = board["scenes"]
    voice_dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice]).strip())
    total_planned = sum(s["dur"] for s in scenes)
    scale = (voice_dur + 0.6) / total_planned  # sahnalarni ovoz uzunligiga moslash
    bg = background()
    starts, acc = [], 0.0
    for s in scenes:
        starts.append(acc)
        acc += s["dur"] * scale
    total = acc
    talk_ranges = [(0.0, voice_dur)]
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", voice, "-filter_complex", "[1:a]apad=pad_dur=0.6,loudnorm=I=-14:TP=-1.5[a]", "-map", "0:v", "-map", "[a]",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "44100", "-b:a", "160k", "-shortest", out],
                          stdin=subprocess.PIPE)
    n = int(total * FPS)
    for fi in range(n):
        t = fi / FPS
        i = max(j for j, st in enumerate(starts) if st <= t)
        sc, st = scenes[i], starts[i]
        dur = scenes[i]["dur"] * scale
        lt = t - st
        frame = bg.copy()
        talk = any(a <= t <= b for a, b in talk_ranges) and sc["type"] in ("character", "ending")
        SCENES[sc["type"]](frame, sc, lt, dur, talk)
        caption(frame, sc.get("caption", ""), lt)
        # punch zoom: sahna boshida 1.08 -> 1.0, keyin sekin 1.0 -> 1.04
        z = 1.0 + 0.08 * (1 - ease_out(lt / 0.3)) + 0.04 * (lt / max(dur, 0.1))
        if z > 1.001:
            cw, ch = int(W / z), int(H / z)
            frame = frame.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H), Image.BILINEAR)
        ff.stdin.write(frame.tobytes())
    ff.stdin.close()
    ff.wait()
    if ff.returncode:
        sys.exit("ffmpeg xato")
    print(json.dumps({"out": out, "seconds": round(total, 1), "scenes": len(scenes)}))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    render(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")), sys.argv[2], sys.argv[3])
