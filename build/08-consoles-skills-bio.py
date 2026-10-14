import os, sys, io, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = r"C:\Users\Fran6\Documents\GitHub\Portfolio"
def read(p):  return open(p, encoding="utf-8").read()
def write(p, s): open(p, "w", encoding="utf-8", newline="").write(s)
FILES = glob.glob(os.path.join(REPO, "*.html")) + glob.glob(os.path.join(REPO, "projects", "*.html"))

SEP = "·"

# =========================================================== 1. console targets
# The site claimed six targets and named five. The sixth is Xbox One. Every
# enumeration on the site now reads the same six, in the same order.
SUBS = [
 (f"PS4 {SEP} PS5 {SEP} Switch {SEP} Switch 2 {SEP} Xbox Series X|S",
  f"PS4 {SEP} PS5 {SEP} Switch {SEP} Switch 2 {SEP} Xbox Series X|S {SEP} Xbox One"),
 (f"PS4 {SEP} PS5 {SEP} Xbox Series X|S {SEP} Nintendo Switch {SEP} Switch 2<br>"
  f'<span class="tag">PH-11</span> <span class="dim">sixth target to confirm</span>',
  f"PS4 {SEP} PS5 {SEP} Switch {SEP} Switch 2 {SEP} Xbox Series X|S {SEP} Xbox One"),
 (f"PS4 {SEP} PS5 {SEP} Nintendo Switch {SEP} Switch 2 {SEP} Xbox Series X|S",
  f"PS4 {SEP} PS5 {SEP} Switch {SEP} Switch 2 {SEP} Xbox Series X|S {SEP} Xbox One"),
 ("across PS4, PS5, Xbox Series X|S, Switch and Switch 2, whose runtime budgets",
  "across PS4, PS5, Xbox Series X|S, Xbox One, Switch and Switch 2, whose runtime budgets"),
 ("Four editions had to land together on PS4, PS5, Xbox Series X|S, Nintendo Switch\n"
  "and Switch 2. Character content",
  "Four editions had to land together on PS4, PS5, Xbox Series X|S, Xbox One,\n"
  "Nintendo Switch and Switch 2. Character content"),
 ("Four editions had to land together on PS4, PS5, Xbox Series X|S, Nintendo Switch and Switch 2.",
  "Four editions had to land together on PS4, PS5, Xbox Series X|S, Xbox One, Nintendo Switch and Switch 2."),
 ("six hardware targets: PS4, PS5, Switch, Switch 2, Xbox Series X/S.",
  "six hardware targets: PS4, PS5, Switch, Switch 2, Xbox Series X/S, Xbox One."),
]

# The same six, however the page happened to wrap or encode the separator.
RX = [
 # about.html facts panel, HTML-encoded middot
 (re.compile(r"PS4 &middot; PS5 &middot; Xbox Series X\|S &middot; Nintendo Switch &middot; Switch 2"
             r"<br>\s*<span class=\"tag\">PH-11</span>\s*<span class=\"dim\">[^<]*</span>"),
  f"PS4 &middot; PS5 &middot; Switch &middot; Switch 2 &middot; "
  f"Xbox Series X|S &middot; Xbox One"),
 # lets-sing case study body, wrapped across lines
 (re.compile(r"Four editions had to land together on PS4, PS5, Xbox Series X\|S,\s*"
             r"Nintendo Switch\s*and Switch 2\."),
  "Four editions had to land together on PS4, PS5, Xbox Series X|S, Xbox One, "
  "Nintendo Switch and Switch 2."),
 (re.compile(r"across PS4, PS5, Xbox Series X\|S,\s*Nintendo Switch and Switch 2\."),
  "across PS4, PS5, Xbox Series X|S, Xbox One, Nintendo Switch and Switch 2."),
 (re.compile(r"across PS4, PS5, Xbox Series X\|S, Switch and Switch 2,"),
  "across PS4, PS5, Xbox Series X|S, Xbox One, Switch and Switch 2,"),
 (re.compile(r"PS4, PS5, Xbox Series X\|S,\s*Nintendo Switch and Switch 2"),
  "PS4, PS5, Xbox Series X|S, Xbox One, Nintendo Switch and Switch 2"),
 (re.compile(r"PS4, PS5, Xbox Series X\|S, Switch and Switch 2"),
  "PS4, PS5, Xbox Series X|S, Xbox One, Switch and Switch 2"),
 (re.compile(r"PS4, PS5, Switch, Switch 2, Xbox Series X/S"),
  "PS4, PS5, Switch, Switch 2, Xbox Series X/S, Xbox One"),
]
n = 0
for f in FILES:
    s = read(f); o = s
    for a, b in SUBS:
        if a in s:
            s = s.replace(a, b); n += 1
    for rx, rep in RX:
        s, k = rx.subn(rep, s)
        n += k
    if s != o:
        write(f, s)
print(f"console substitutions applied: {n}")
for f in FILES:
    s = read(f)
    if "PH-11" in s: print("  !! PH-11 still in", os.path.relpath(f, REPO))
    for m in re.finditer(r"PS4[^<.]{0,90}", s):
        if "Xbox One" not in m.group(0) and "SHIPPED on" not in m.group(0):
            print("  ?? ", os.path.relpath(f, REPO), "|", m.group(0)[:100])

# =========================================================== 2. about: long bio
BIO = """<p>Growing up I played everything and built things from the first one. The
          games I kept returning to were the ones you could feel the shape of &mdash; the
          ones where a system was doing something clever under a fixed budget. That is
          still the pull: the machinery underneath, not the surface.</p>
          <p>ESMA gave me three years of shipping with teams under deadlines, as
          environment artist, 3D modeller and gameplay programmer. <strong>RUBBER</strong>
          was the project that turned that into a direction. I owned the taxi end to end
          &mdash; Chaos Vehicle dynamics, a custom six-wheel rig built in Blender, Morpher
          destruction authored in 3ds Max, and the whole feedback layer around it &mdash; and
          discovering that I cared more about making the car feel right than about the
          surface it lived on.</p>
          <p>Production taught me the rest. At <strong>Eugen Systems</strong>, learning an
          in-house engine well enough to ship complete maps on it. At <strong>VOXLER</strong>,
          building a pipeline the art team ran without me in the loop &mdash; which is the
          only kind of tooling work that counts. At <strong>FittingBox</strong>, holding
          studio-grade product fidelity on web and mobile budgets that do not move.</p>
          <p>What I want next is a team where the technical art is treated as engineering
          rather than overhead, and where the person who writes the tool is also the person
          who has to use it. I am most useful on anything that crosses the DCC/engine line:
          automation, optimisation, rendering, and the awkward parts in between.</p>"""

p = os.path.join(REPO, "about.html")
s = read(p)
s = re.sub(r'<span class="callout__k">PH-10</span>\s*', '', s, count=1)
s = re.sub(r'<h3 class="mt-3">The longer version</h3>', '<h3 class="mt-3">The longer version</h3>', s)
s = re.sub(
  r'<p><strong>Biography to be added\.</strong>.*?</p>',
  BIO, s, flags=re.S)
write(p, s)
print("about: PH-10 left =", s.count("PH-10"), "| long bio in =", "Growing up I played" in s)

# =========================================================== 3. skills: rate them
# Levels are read off the shipped work each row already cites - not invented.
LEVELS = {
 "Unreal Engine 5":                    (4, "Advanced &mdash; shipped in production on four titles"),
 "Unity":                              (4, "Advanced &mdash; editor and runtime tooling in production"),
 "Proprietary in-house engine":        (4, "Advanced &mdash; shipped maps on Eugen's engine"),
 "PS1 (PSXSplash toolchain)":          (3, "Working &mdash; shipped on real 1994 hardware"),
 "Consoles":                           (4, "Advanced &mdash; optimisation held across six targets"),
 "Python":                             (4, "Advanced &mdash; pipeline tool in continuous production use"),
 "C#":                                 (4, "Advanced &mdash; editor tooling adopted by the animation team"),
 "Blueprints":                         (4, "Advanced &mdash; vehicle systems built in Blueprint"),
 "Lua":                                (3, "Working &mdash; gameplay scripting on the PS1 target"),
 "Batch / .bat orchestration":         (4, "Advanced &mdash; the one-click artist entry point"),
 "Blender":                            (4, "Advanced &mdash; headless scripting and rigging"),
 "3ds Max":                            (4, "Advanced &mdash; vehicle modelling and Morpher destruction"),
 "Substance Painter":                  (4, "Advanced &mdash; 300+ material assets a month in production"),
 "Alembic (.abc) / FBX":               (3, "Working &mdash; engine-ready interchange inside the pipeline"),
 "World Machine":                      (4, "Advanced &mdash; terrain and layout for shipped maps"),
 "Lumen &amp; Megascans":              (3, "Working &mdash; arch-viz delivered as final stills"),
 "Lighting &amp; post":                (4, "Advanced &mdash; glow, bloom and VFX under fixed budgets"),
 "Scene Capture 2D":                   (4, "Advanced &mdash; multi-view at 13 ms inside a 16.6 ms budget"),
 "Deterministic material generation":  (4, "Advanced &mdash; regenerated from source, not by hand"),
 "Draw call reduction":                (4, "Advanced &mdash; LOD and batching across a wide hardware spread"),
 "Memory &amp; VRAM budgeting":        (3, "Working &mdash; every scene budgeted to 2 MB RAM / 1 MB VRAM"),
 "Multi-target profiling":             (4, "Advanced &mdash; visual targets held across six configurations"),
 "World streaming":                    (4, "Advanced &mdash; large-scale worlds sustained at runtime"),
 "Automated asset ingestion":          (4, "Advanced &mdash; delivery validated without an engineer"),
 "Deterministic batch rendering":      (4, "Advanced &mdash; same input, same output, every run"),
 "Artist-facing tools":                (4, "Advanced &mdash; adopted to fit the existing workflow"),
 "Naming conventions &amp; rollout":  (4, "Advanced &mdash; defined, coached, then maintained to handoff"),
}

p = os.path.join(REPO, "skills.html")
s = read(p)
rated = []

def rate(m):
    blk = m.group(0)
    nm = re.search(r'<div class="skillrow__name">(.*?)</div>', blk, re.S)
    if not nm:
        return blk
    label = nm.group(1).strip()
    if label not in LEVELS:
        print("  ?? unmatched skill row:", repr(label))
        return blk
    lvl, legend = LEVELS[label]
    word = legend.split(" &mdash; ")[0]
    blk = blk.replace('<div class="meter meter--unrated" data-level="" role="img"\n               aria-label="Proficiency not rated yet for ' + label + '">',
                      f'<div class="meter" data-level="{lvl}" role="img"\n               aria-label="Proficiency: {word.lower()}">')
    blk = re.sub(r'<div class="meter__legend">[^<]*</div>',
                 f'<div class="meter__legend">{legend}</div>', blk)
    rated.append(label)
    return blk

s = re.sub(r'<div class="skillrow">.*?(?=<div class="skillrow">|<div class="skillgroup">|</div>\s*</section>)',
           rate, s, flags=re.S)

s = re.sub(r'<div class="callout[^"]*"[^>]*>\s*<span class="callout__k">PH-LEVELS</span>\s*'
           r'<p>.*?</p>\s*</div>',
           '<div class="callout">\n'
           '        <p><strong>How to read these:</strong> every level is taken from the shipped '
           'work in the row beside it, not from opinion. <strong>4</strong> means the work shipped '
           'and someone else came to depend on it; <strong>3</strong> means shipped or used in a '
           'real project. Each row links to the case study that demonstrates it.</p>\n'
           '      </div>', s, flags=re.S)
write(p, s)
print(f"skills rated: {len(rated)}/{len(LEVELS)}  unrated left: "
      f"{s.count('meter--unrated')}  PH-LEVELS: {s.count('PH-LEVELS')}")