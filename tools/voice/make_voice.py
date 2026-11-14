"""Make voice.mp3 + words.json (word timings) for every voices/<name>/script.txt that has no voice yet.
Runs on GitHub Actions (Microsoft Edge neural voices are not reachable from every sandbox)."""
import asyncio, json, pathlib, sys
import edge_tts

VOICE = "uz-UZ-SardorNeural"

async def make(folder: pathlib.Path):
    text = (folder / "script.txt").read_text(encoding="utf-8").strip()
    cfg = folder / "voice.json"
    opts = json.loads(cfg.read_text()) if cfg.exists() else {}
    com = edge_tts.Communicate(text, opts.get("voice", VOICE), rate=opts.get("rate", "+0%"), boundary="WordBoundary")
    words, audio = [], bytearray()
    async for chunk in com.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
        elif chunk["type"] == "WordBoundary":
            words.append({"w": chunk["text"], "t0": round(chunk["offset"] / 1e7, 3), "t1": round((chunk["offset"] + chunk["duration"]) / 1e7, 3)})
    (folder / "voice.mp3").write_bytes(bytes(audio))
    (folder / "words.json").write_text(json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")
    print(folder.name, len(words), "words", round(words[-1]["t1"], 2) if words else 0, "s")

async def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "voices")
    for f in sorted(root.glob("*/script.txt")):
        d = f.parent
        if not (d / "voice.mp3").exists() or (d / "voice.mp3").stat().st_mtime < f.stat().st_mtime:
            await make(d)

asyncio.run(main())
