"""Wrap the artifact page into a full HTML document for GitHub Pages: python3 build_pages.py <out_dir>"""
import pathlib, sys
src = pathlib.Path(__file__).with_name("index.html").read_text(encoding="utf-8")
head = ('<!doctype html><html lang="uz"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="description" content="Koreys tilini noldan TOPIK 5 gacha o\'rgatadigan o\'zbekcha platforma.">'
        '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>')
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
(out / "index.html").write_text(head + src + "</body></html>", encoding="utf-8")
print("ok", (out / "index.html").stat().st_size)
