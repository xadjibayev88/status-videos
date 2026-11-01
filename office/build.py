#!/usr/bin/env python3
"""Reads CLAUDE.md (the team table) and .claude/agents/*.md, writes office/agents.json for the 3D office.

usage: python3 office/build.py        (run from the repo root, or anywhere: paths are relative to this file)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS = os.path.join(ROOT, ".claude", "agents")
OUT = os.path.join(ROOT, "office", "agents.json")


def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2).strip()


def departments():
    """Parse the team table in CLAUDE.md: | Team | Head | Workers |  (a row without a backticked head is the lobby)"""
    deps = []
    for line in open(os.path.join(ROOT, "CLAUDE.md"), encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in ("Team", "Department", "") or set(cells[0]) <= {"-"}:
            continue
        head = re.findall(r"`([a-z0-9-]+)`", cells[1])
        workers = re.findall(r"`([a-z0-9-]+)`", cells[2])
        deps.append({"name": cells[0], "head": head[0] if head else None, "workers": workers})
    return deps


def main():
    files = {f[:-3]: os.path.join(AGENTS, f) for f in sorted(os.listdir(AGENTS)) if f.endswith(".md")}
    deps = departments()
    placed = set()
    out = {"departments": []}
    for d in deps:
        members = []
        if not d["head"]:
            members.append({"name": "chief-of-staff", "role": "head", "description": "Routes work, runs departments in parallel, reviews, reports.", "tools": "everything", "model": "the session"})
        for name in ([d["head"]] if d["head"] else []) + d["workers"]:
            if name not in files:
                print(f"warning: {name} is in CLAUDE.md but has no file", file=sys.stderr)
                continue
            meta, body = frontmatter(files[name])
            members.append({"name": name, "role": "head" if name == d["head"] else "worker",
                            "description": meta.get("description", ""), "tools": meta.get("tools", ""),
                            "model": meta.get("model", "inherit")})
            placed.add(name)
        out["departments"].append({"name": d["name"], "agents": members})
    missing = sorted(set(files) - placed)
    if missing:
        print(f"warning: not in any team, placed in the lobby: {missing}", file=sys.stderr)
        for name in missing:
            meta, _ = frontmatter(files[name])
            out["departments"][0]["agents"].append({"name": name, "role": "worker", "description": meta.get("description", ""), "tools": meta.get("tools", ""), "model": meta.get("model", "inherit")})
    out["count"] = sum(len(d["agents"]) for d in out["departments"])
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1)
    print(json.dumps({"agents": out["count"], "departments": len(out["departments"]), "out": os.path.relpath(OUT, ROOT)}))


if __name__ == "__main__":
    main()


def write_stats():
    """Copy the newest channel numbers from a sibling shorts-agent checkout into office/stats.json (wall screens)."""
    import glob
    files = sorted(glob.glob(os.path.join(ROOT, "..", "shorts-agent", "data", "stats", "*.json")))
    if not files:
        return
    with open(files[-1], encoding="utf-8") as f:
        data = json.load(f)
    with open(os.path.join(ROOT, "office", "stats.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(json.dumps({"stats": os.path.basename(files[-1])}))


if __name__ == "__main__":
    write_stats()


def write_activity():
    """Recent real work for the office feed: commit subjects from the sibling repos (last 3 days)."""
    import subprocess
    rules = [  # (repo, subject prefix or word, agent, Uzbek text)
        ("shorts-agent", "history:", "social-publishing-publisher", "YouTube/Instagram'ga video joyladi"),
        ("Apex_Agent_Gemini", "update history", "social-media-manager", "Telegram kanaliga post joyladi"),
        ("status-agent", None, "community-manager", "@h6yotiy Reels yangilandi"),
        ("shorts-agent", "stats:", "data-analyst", "kanal statistikasini yig'di"),
        ("status-videos", "brain", "chief-of-staff", "xotiraga yangi qoida yozdi"),
        ("status-videos", "office", "frontend-dev", "3D ofisni yangiladi"),
        (None, "fix", "backend-dev", "xatoni tuzatdi"),
        (None, "feat", "engineering-lead", "yangi imkoniyat qo'shdi"),
        (None, "docs", "project-manager", "qo'llanma yozdi"),
    ]
    out = []
    for repo in ["shorts-agent", "Apex_Agent_Gemini", "status-agent", "status-videos"]:
        path = os.path.join(ROOT, "..", repo) if repo != "status-videos" else ROOT
        if not os.path.isdir(os.path.join(path, ".git")):
            continue
        try:
            log = subprocess.run(["git", "-C", path, "log", "--since=3.days", "--format=%ct|%s", "-n", "40"],
                                 capture_output=True, text=True, timeout=20).stdout
        except Exception:
            continue
        for line in log.splitlines():
            ts, _, subj = line.partition("|")
            for r_repo, key, agent, text in rules:
                if r_repo not in (None, repo):
                    continue
                if key is None or subj.lower().startswith(key) or (key in ("brain", "office") and subj.lower().startswith(key)):
                    detail = subj.split(":", 1)[1].strip() if ":" in subj and key in ("fix", "feat", "docs") else ""
                    out.append({"ts": int(ts), "agent": agent, "text": text + ""})
                    break
    out.sort(key=lambda e: -e["ts"])
    import time
    for e in out:
        e["when"] = time.strftime("%d.%m %H:%M", time.gmtime(e.pop("ts") + 5 * 3600))
    with open(os.path.join(ROOT, "office", "activity.json"), "w", encoding="utf-8") as f:
        json.dump(out[:30], f, ensure_ascii=False, indent=1)
    print(json.dumps({"activity": len(out[:30])}))


if __name__ == "__main__":
    write_activity()


def write_tasks():
    """Office task board: today's schedule, queue sizes and what is waiting on whom."""
    import subprocess
    def count(repo, path):
        out = subprocess.run(["git", "-C", os.path.join(ROOT, "..", repo), "ls-tree", "--name-only", "origin/main", path + "/"],
                             capture_output=True, text=True).stdout.split()
        return len([o for o in out if o.endswith(".json")])
    q, qa = count("shorts-agent", "queue"), count("shorts-agent", "queue_apex")
    schedule = [
        ("07:41", "chief-of-staff", "Ertalabki reja: xatolarni tekshirish, navbatlarni to'ldirish"),
        ("07:41", "trend-scout", "Har kanal uchun 10 ta yangi trend mavzu"),
        ("08:00", "community-manager", "@h6yotiy iqtibos Reels (kuniga 9 marta)"),
        ("09:11", "social-media-manager", "Telegram: bozor yangiligi (har soat 20:59 gacha)"),
        ("12:43", "social-publishing-publisher", "apex_wealths Instagram Reels"),
        ("14:53", "social-publishing-publisher", "apex_wealths YouTube + Instagram"),
        ("15:47", "social-publishing-publisher", "Bilarmidingiz YouTube Short"),
        ("16:57", "social-publishing-publisher", "apex_wealths Instagram Reels"),
        ("18:47", "social-publishing-publisher", "apex_wealths YouTube + Instagram"),
        ("21:37", "data-analyst", "Kanal statistikasi"),
        ("21:41", "analytics-lead", "Kechki tahlil, o'sish tavsiyalari"),
        ("21:41", "marketing-video-optimization-specialist", "Sarlavha va hook bo'yicha 3 ta o'zgarish"),
    ]
    tasks = [{"time": t, "agent": a, "text": x} for t, a, x in schedule]
    queue = [
        {"agent": "script-writer", "text": f"Bilarmidingiz navbati: {q} ta ssenariy (maqsad 6+)", "ok": q >= 6},
        {"agent": "script-writer", "text": f"apex_wealths navbati: {qa} ta ssenariy (maqsad 8+)", "ok": qa >= 8},
        {"agent": "fact-checker", "text": "Har bir ssenariy internet orqali tekshiriladi", "ok": True},
    ]
    with open(os.path.join(ROOT, "office", "tasks.json"), "w", encoding="utf-8") as f:
        json.dump({"schedule": tasks, "queue": queue}, f, ensure_ascii=False, indent=1)
    print(json.dumps({"tasks": len(tasks), "queue": [q, qa]}))


if __name__ == "__main__":
    write_tasks()
