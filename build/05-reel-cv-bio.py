import os, sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = r"C:\Users\Fran6\Documents\GitHub\Portfolio"
RD = json.load(open(r"C:\Users\Fran6\Documents\GitHub\_wix_source_backup\_breakdown.json"))
def read(p):  return open(p, encoding="utf-8").read()
def write(p, s): open(p, "w", encoding="utf-8", newline="").write(s)
def esc(s): return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                     .replace('"', "&quot;"))

PH = re.compile(r"[ \t]*<!-- PLACEHOLDER (PH-[A-Za-z0-9_.\-]+) .*?-->\s*"
                r"<div class=\"ph.*?</div>\s*", re.S)

# ---------------------------------------------------------------- 1. breakdown
p = os.path.join(REPO, "breakdown.html")
s = read(p)
def rd_sub(m):
    pid = m.group(1)
    if pid not in RD:
        return m.group(0)
    d = RD[pid]
    return (f'<img class="rd__shot" src="{d["rel"]}" alt="{esc(d["alt"])}" '
            f'width="{d["w"]}" height="{d["h"]}" loading="lazy" decoding="async">\n      ')
s = PH.sub(rd_sub, s)
write(p, s)
print("breakdown: remaining placeholders", len(PH.findall(s)))

# ---------------------------------------------------------------- 2. index.html
p = os.path.join(REPO, "index.html")
s = read(p)

# 2a. CV block -> real download button
s = re.sub(
    r'[ \t]*<!-- PLACEHOLDER PH-08 .*?-->\s*<div class="ph ph--inline.*?</div>\s*',
    '        <p class="mt-5"><a class="btn" href="assets/files/'
    'cv-francisco-de-carvalho-pereira.pdf" download>Download CV (PDF) '
    '<span class="arw" aria-hidden="true">&darr;</span></a></p>\n', s, flags=re.S)

# 2b. showreel -> the real 20 s environment clip
s = re.sub(
    r'[ \t]*<!-- PLACEHOLDER PH-REEL .*?-->\s*<div class="ph ph--21x9".*?</div>\s*',
    '''
      <div class="reel reveal" data-reel>
        <video controls preload="none" playsinline hidden
               poster="assets/img/reel/environment-clip-poster.webp"
               width="1600" height="890">
          <source src="assets/media/environment-clip.mp4" type="video/mp4">
          Your browser cannot play this video.
          <a href="assets/media/environment-clip.mp4">Download the clip instead.</a>
        </video>
        <button class="reel__poster" type="button" data-reel-play aria-label="Play the environment clip">
          <img src="assets/img/reel/environment-clip-poster.webp" alt="" aria-hidden="true"
               width="1600" height="890" loading="lazy" decoding="async">
          <span class="reel__play"><span aria-hidden="true">&#9654;</span> Play clip</span>
        </button>
        <span class="reel__badge">Real-time &middot; Unreal Engine 5 &middot; 20 seconds</span>
      </div>
    ''', s, flags=re.S)

# 2c. the showreel section copy
s = s.replace(
    "<p class=\"sec-head__sub\">A curated selection of shipped work across Unreal Engine 5\n"
    "        and Unity. This slot is reserved for the current reel &mdash; the file details\n"
    "        are stated below.</p>",
    "<p class=\"sec-head__sub\">A 20-second real-time environment pass: terrain, sky,\n"
    "        lighting and volumetrics, rendered live in Unreal Engine 5. Everything else\n"
    "        on this site is shown as stills you can inspect frame by frame.</p>")
s = s.replace("<h2>Showreel</h2>", "<h2>Watch</h2>")
s = s.replace('<span class="idx">01</span>\n        <h2>Watch</h2>',
              '<span class="idx">01</span>\n        <h2>Watch</h2>')
s = s.replace('<p class="mono mt-4">Target: 45&ndash;90 s &middot; 1080p &middot; sound on '
              '&middot; loaded only when pressed</p>',
              '<p class="mono mt-4">1080p &middot; silent render &middot; loaded only when pressed '
              '&middot; nothing plays until you do</p>')
write(p, s)
print("index: remaining placeholders", len(PH.findall(s)))

# ---------------------------------------------------------------- 3. about.html
p = os.path.join(REPO, "about.html")
s = read(p)

# 3a. portrait
s = re.sub(r'[ \t]*<!-- PLACEHOLDER PH-09 .*?-->\s*<div class="ph.*?</div>\s*',
           '        <img class="portrait" src="assets/img/about/portrait.webp" '
           'alt="Portrait of Francisco De Carvalho Pereira" width="450" height="338" '
           'loading="lazy" decoding="async">\n', s, flags=re.S)

# 3b. long-form bio
BIO = (
 "I build real-time 3D for games, and the part I care about most is the machinery "
 "underneath it: the tools that remove a manual step, the budgets that keep a frame "
 "honest, and the pipelines that let a team ship faster than I could alone.\n\n"
 "That started at ESMA, where I worked as environment artist, 3D modeller and gameplay "
 "programmer across several team projects &mdash; and then turned into a specialisation. "
 "On <strong>RUBBER</strong> I owned the vehicle end to end: the Chaos dynamics, a custom "
 "six-wheel rig, the Morpher destruction in 3ds Max and the feedback layer around it.\n\n"
 "Since then I have worked inside production. At <strong>Eugen Systems</strong> on "
 "<strong>WARNO</strong>, I owned complete maps on a proprietary in-house engine &mdash; "
 "layout, terrain, four modular environment kits, and the optimisation passes that kept "
 "them streaming. At <strong>VOXLER</strong> I built the headless Blender render pipeline "
 "and the animation validation tool the team still runs without me. At <strong>FittingBox</strong> "
 "I shipped 300+ real-time product assets a month for luxury eyewear try-on, under web "
 "bandwidth budgets that do not move.\n\n"
 "I am at home in Unreal Engine 5 and Unity, comfortable in Blender and 3ds Max, and I "
 "write the Python and C# that makes the tools. I care about work that is measured rather "
 "than described &mdash; a frame budget held, a manual pass removed, a half-day turned into "
 "sixty seconds."
)
s = re.sub(r'<p class="ph__bio">.*?</p>|<div class="ph ph--inline">.*?</div>',
           lambda m: f'<div class="prose bio">{BIO}</div>', s, flags=re.S)
s = s.replace("BIO_TO_WRITE", "")
write(p, s)
print("about: remaining placeholders", len(PH.findall(s)))
print("about YOUR_ left:", s.count("YOUR_"), "| PH-0 left:", len(re.findall(r'PH-0\d', s)))