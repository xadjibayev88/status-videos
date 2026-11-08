---
name: cartoon-reel
description: Make a 30-second vertical 2D cartoon reel (flat code-drawn characters, crowds, number counters, 2-3 word captions, ending question) for apex_wealths or Bilarmidingiz, in the style of the owner's reference video (2026-11-08). Use when the owner asks for "multfilm uslubida", "2D animatsiya", "shu videodagidek" reels, or a story needs a cartoon explainer.
---

# 2D cartoon reel

Renderer: `shorts-agent/cartoon/reel.py` (copy in `status-videos/tools/cartoon-reel/`). Pillow + ffmpeg only, free.
Automation: `shorts-agent/.github/workflows/cartoon.yml` renders every `cartoon/boards/<name>.json` in parallel
with the OmniVoice voice (fallback ElevenLabs, Edge) and writes MP4s to the `cartoon-out` branch. Nothing is published.

## Steps
1. **Facts first.** Take a story that already passed `fact-checker` (queue_apex/, queue/, or their done/). No new claims.
2. **Voice text** `<name>.voice.txt`, 55-70 words (~28-32 s), numbers written as Uzbek words, ElevenLabs v3 tags
   allowed (`[excited]`, `[softly]`, `[slowly]`; stripped automatically for OmniVoice). Shape: hook with the number →
   2-3 story beats with a twist → name reveal → lesson → question to comments ("Izohlarda yozing!").
3. **Storyboard** `<name>.json`: `{"scenes": [...]}`, one scene per phrase, `dur` in seconds (scaled to the voice).
   Scene types: `year` (value, from, top), `number` (value, from, top, label, suffix), `character` (shirt, skin, hair,
   hat, label, mood happy|sad, tear, arm_up, prop), `crowd`, `icon` (prop, sub), `split` (left/right: top, value,
   label, color), `ending`. Props: trophy, medal, car, dish, book, mouse, rabbit, x, petri, clock, tv, brace.
   Every scene has a `caption` of 1-3 words, caps, ≤18 characters.
4. Commit boards to `shorts-agent/cartoon/boards/`, run `cartoon.yml` (input `names` or empty for all),
   fetch `cartoon-out`, check a frame sheet (`ffmpeg -vf fps=1/2,tile=6x2`), `brand-checker`, then hand to the owner
   or add to a queue only if the owner wants it posted.

## Style rules (from the reference)
- Dark navy starry background, flat characters with big heads and eyes, black outlines, bright shirts with a label.
- Big white Anton captions with black stroke at the top; counters count up; quick punch zoom on every cut.
- Real people are drawn as generic cartoons (no photos, no logos); label shirts with a word, not a brand mark.
