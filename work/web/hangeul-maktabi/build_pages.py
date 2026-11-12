"""Wrap the artifact page into a full HTML document for GitHub Pages: python3 build_pages.py <out_dir>"""
import pathlib, sys
src = pathlib.Path(__file__).with_name("index.html").read_text(encoding="utf-8")
head = ('<!doctype html><html lang="uz"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<meta name="description" content="Koreys tilini noldan TOPIK 5 gacha o\'rgatadigan o\'zbekcha platforma.">'
        '<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#0d1226">'
        '<link rel="icon" href="icon-192.png"><link rel="apple-touch-icon" href="icon-192.png">'
        '<meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">'
        '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style></head><body>')
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
(out / "index.html").write_text(head + src + "</body></html>", encoding="utf-8")
print("ok", (out / "index.html").stat().st_size)

import json, hashlib
(out / "manifest.webmanifest").write_text(json.dumps({
    "name": "Hangeul Maktabi", "short_name": "Hangeul", "lang": "uz", "start_url": "./", "scope": "./",
    "display": "standalone", "orientation": "portrait", "background_color": "#0d1226", "theme_color": "#0d1226",
    "description": "Koreys tilini noldan TOPIK 5 gacha o'rganish",
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
              {"src": "icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]},
    ensure_ascii=False, indent=1), encoding="utf-8")
ver = hashlib.sha1(src.encode()).hexdigest()[:10]
(out / "sw.js").write_text("""const C="hm-%s";
self.addEventListener("install",e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(["./","manifest.webmanifest","icon-192.png"])).then(()=>self.skipWaiting()))});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{const u=new URL(e.request.url);if(e.request.method!=="GET"||u.origin!==location.origin)return;
 e.respondWith(fetch(e.request).then(r=>{const cp=r.clone();caches.open(C).then(c=>c.put(e.request,cp));return r}).catch(()=>caches.match(e.request).then(r=>r||caches.match("./"))))});
""" % ver, encoding="utf-8")
print("pwa files written", ver)
