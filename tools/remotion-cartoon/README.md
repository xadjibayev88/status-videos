# remotion-cartoon — 3D dunyoda 2D multfilm qisqa videolar

`cartoon-3d-short` skilli asosida (github.com/mromidev/claude-animated-shorts, MIT). Birinchi video: **Pet Rock** (apex_wealths).

- Ovoz: `voices/<nom>/script.txt` ni push qiling → GitHub Actions (`.github/workflows/voice.yml`) `voice.mp3` va `words.json` (so'z vaqtlari) yaratadi.
- Sahna: `src/petrock/` (story.ts — kadrlar va vaqt, world.ts — dunyo, cards.ts — personajlar, outline.ts — qora konturlar).
- Musiqa: `python3 audio/petrock_music.py src/petrock/words.json out/music.wav` (o'zimiz sintez qilgan, mualliflik muammosi yo'q).
- Render (GPU'siz ham ishlaydi):
  `npx remotion render src/index.ts PetRock out/petrock_raw.mp4 --gl=swangle --browser-executable=<chrome-headless-shell>`
  so'ng ovoz + musiqa: ffmpeg bilan birlashtiriladi.
