import os, sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from html.parser import HTMLParser

REPO = r"C:\Users\Fran6\Documents\GitHub\Portfolio"
FILES = []
for dp, dn, fs in os.walk(REPO):
    if ".git" in dp: continue
    for f in fs:
        if f.endswith(".html"): FILES.append(os.path.join(dp, f))
FILES.sort()

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []          # (kind, value)
        self.ids = []
        self.h1 = 0
        self.img_noalt = 0
        self.imgs = 0
        self.title = ""
        self._intitle = False
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d: self.ids.append(d["id"])
        if tag == "h1": self.h1 += 1
        if tag == "title": self._intitle = True
        if tag == "img":
            self.imgs += 1
            if "alt" not in d: self.img_noalt += 1
            if d.get("src"): self.refs.append(("img", d["src"]))
            if not d.get("width") or not d.get("height"):
                self.refs.append(("MISSING-DIM", d.get("src", "?")))
        for k in ("src", "href", "poster"):
            if d.get(k): self.refs.append((tag + ":" + k, d[k]))
    def handle_endtag(self, tag):
        if tag == "title": self._intitle = False
    def handle_data(self, data):
        if self._intitle: self.title += data

problems = []
titles = {}
for f in FILES:
    rel = os.path.relpath(f, REPO)
    p = P()
    src = open(f, encoding="utf-8").read()
    p.feed(src)

    if p.h1 != 1:
        problems.append(f"{rel}: {p.h1} <h1> (expected 1)")
    if p.img_noalt:
        problems.append(f"{rel}: {p.img_noalt} <img> without alt")
    if not p.title.strip():
        problems.append(f"{rel}: no <title>")
    if p.title.strip() in titles:
        problems.append(f"{rel}: duplicate <title> with {titles[p.title.strip()]}")
    titles[p.title.strip()] = rel

    dup = {i for i in p.ids if p.ids.count(i) > 1}
    if dup:
        problems.append(f"{rel}: duplicate id {sorted(dup)}")

    for kind, val in p.refs:
        if kind == "MISSING-DIM":
            problems.append(f"{rel}: <img> without width/height: {val}")
            continue
        if val.startswith(("http://", "https://", "mailto:", "#", "data:")):
            continue
        target = val.split("#")[0].split("?")[0]
        if not target: continue
        tp = os.path.normpath(os.path.join(os.path.dirname(f), target))
        if not os.path.exists(tp):
            problems.append(f"{rel}: BROKEN {kind} -> {val}")

    # in-page anchors
    for kind, val in p.refs:
        if val.startswith("#") and len(val) > 1 and val[1:] not in p.ids:
            problems.append(f"{rel}: dead anchor {val}")

print(f"pages checked: {len(FILES)}")
print(f"problems: {len(problems)}")
for x in problems:
    print("  -", x)

# external refs
ext = set()
for f in FILES:
    for m in re.finditer(r'href="(https?://[^"]+)"', open(f, encoding="utf-8").read()):
        u = m.group(1)
        if "schema.org" not in u: ext.add(u)
print(f"\nexternal links: {len(ext)}")
for u in sorted(ext): print("  ", u)

# weight
tot = sum(os.path.getsize(os.path.join(dp, fn))
          for dp, dn, fs in os.walk(REPO) if ".git" not in dp for fn in fs)
html = sum(os.path.getsize(f) for f in FILES)
img = 0
for dp, dn, fs in os.walk(os.path.join(REPO, "assets")):
    for fn in fs: img += os.path.getsize(os.path.join(dp, fn))
print(f"\ntotal repo: {tot/1048576:.2f} MB | html {html/1024:.0f} KB | assets {img/1048576:.2f} MB")

# biggest assets
big = sorted(((os.path.getsize(os.path.join(dp, fn)), os.path.relpath(os.path.join(dp, fn), REPO))
              for dp, dn, fs in os.walk(REPO) if ".git" not in dp for fn in fs), reverse=True)[:12]
print("\nlargest files:")
for s, n in big: print(f"  {s/1024:8.0f} KB  {n}")