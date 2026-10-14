import os, sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = r"C:\Users\Fran6\Documents\GitHub\Portfolio"
A = json.load(open(os.path.join(REPO, "_assets.json")))

SITE   = "https://lebofran6.github.io/Portfolio"
EMAIL  = "fran6pereira@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/francisco-de-carvalho-pereira-aa0458196/"
GITHUB   = "https://github.com/LeBoFran6"
ARTSTATION = "https://www.artstation.com/lefran6"
ITCH   = "https://lefran6.itch.io/"
CV     = "assets/files/cv-francisco-de-carvalho-pereira.pdf"

SLUGS = ["warno", "rubber", "fittingbox", "automated-blender-render-pipeline",
         "lets-sing-voxler", "environment-art", "architectural-visualisation",
         "dietemna", "game-jams"]

FILES = ["index.html", "work.html", "about.html", "skills.html", "contact.html",
         "breakdown.html", "404.html"] + [f"projects/{s}.html" for s in [
    "architectural-visualisation", "automated-blender-render-pipeline", "dietemna",
    "environment-art", "fittingbox", "game-jams", "lastmeal", "lets-sing-voxler",
    "movies-cgi", "rally-project", "rubber", "warno"]]

def read(p):  return open(p, encoding="utf-8").read()
def write(p, s): open(p, "w", encoding="utf-8", newline="").write(s)

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))

def prefix(fp):
    """Pages under projects/ sit one level down, so their relative paths need ../"""
    return "../" if fp.replace("\\", "/").startswith("projects/") else ""

# ---------------------------------------------------------------- images
def img_html(rel, w, h, alt, cap=None, lazy=True, cls=""):
    p = rel                                     # already site-relative
    a = f' alt="{esc(alt)}"' if alt else ' alt=""'
    lz = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{p}"{a} width="{w}" height="{h}"{lz}>')

def gallery_html(slug, fp):
    pre = prefix(fp)
    rows = A[slug]["gallery"]
    out = ['<div class="gallery">']
    for g in rows:
        out.append(
            '<figure class="shot">'
            f'<img src="{pre}{g["rel"]}" alt="{esc(g["alt"])}" '
            f'width="{g["w"]}" height="{g["h"]}" loading="lazy" decoding="async">'
            f'<figcaption>{esc(g["cap"])}</figcaption>'
            '</figure>')
    out.append('</div>')
    return "\n       ".join(out)

def hero_html(slug, fp, lazy=True):
    pre = prefix(fp)
    h = A[slug]["hero"]
    return (f'<img src="{pre}{h[0]}" alt="{esc(A[slug]["hero_alt"])}" '
            f'width="{h[1]}" height="{h[2]}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">')

PH = re.compile(r"[ \t]*<!-- PLACEHOLDER (PH-[A-Za-z0-9_.\-]+) .*?-->\s*"
                r"<div class=\"ph.*?</div>\s*", re.S)

def replace_ph(m, fp):
    pid = m.group(1)
    slug = pid.replace("PH-P-", "").replace("PH-G-", "")
    if slug not in A:
        return m.group(0)
    pre = prefix(fp)
    if pid.startswith("PH-G-"):
        return gallery_html(slug, fp) + "\n      "
    h = A[slug]["hero"]
    if fp in ("index.html", "work.html"):
        return (f'<img src="{pre}{h[0]}" alt="{esc(A[slug]["hero_alt"])}" '
                f'width="{h[1]}" height="{h[2]}" loading="lazy" decoding="async">\n      ')
    return hero_html(slug, fp) + "\n    "

# ---------------------------------------------------------------- contacts
def channel(k, v, note, href, external=False):
    if href:
        attrs = f' href="{href}"'
        if external:
            attrs += ' rel="me noopener" target="_blank"'
        arrow = '<span class="arw" aria-hidden="true">&nearr;</span>'
        disp = v
    else:
        attrs = ""
        arrow = '<span class="arw" aria-hidden="true" style="color:var(--dim)">&#8226;</span>'
        disp = v
    inner = (f'<span><span class="channel__k">{k}</span>'
             f'<span class="channel__v">{esc(disp)}</span>'
             f'<span class="channel__note">{note}</span></span>')
    if href:
        return f'<a class="channel"{attrs}>{inner}{arrow}</a>'
    return f'<div class="channel">{inner}{arrow}</div>'

CHANNELS = [
    ("Email", EMAIL, "Best for roles and freelance", f"mailto:{EMAIL}", False),
    ("LinkedIn", "linkedin.com/in/francisco-de-carvalho-pereira",
     "Profile", LINKEDIN, True),
    ("GitHub", "github.com/LeBoFran6", "Tools and scripts", GITHUB, True),
    ("ArtStation", "artstation.com/lefran6", "Renders and breakdowns", ARTSTATION, True),
    ("itch.io", "lefran6.itch.io", "Play the shipped games", ITCH, True),
    ("CV", "cv-francisco-de-carvalho-pereira.pdf", "A4 PDF, two pages", CV, False),
]

def footer_links(pre):
    cv = pre + CV
    return (
    '<ul class="footer__list">\n          '
    f'<li><a href="{cv}" download>CV (PDF)</a></li>\n          '
    f'<li><a href="{LINKEDIN}" rel="me noopener" target="_blank">LinkedIn</a></li>\n          '
    f'<li><a href="{GITHUB}" rel="me noopener" target="_blank">GitHub</a></li>\n          '
    f'<li><a href="{ARTSTATION}" rel="me noopener" target="_blank">ArtStation</a></li>\n          '
    f'<li><a href="{ITCH}" rel="me noopener" target="_blank">itch.io</a></li>\n          '
    f'<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>\n        </ul>')

AVAIL = ("Available for relocation worldwide, and open to remote. "
         "EU work authorisation &mdash; visa sponsorship considered.")

# ---------------------------------------------------------------- pass
touched = []
for f in FILES:
    p = os.path.join(REPO, f.replace("/", os.sep))
    if not os.path.exists(p):
        print("MISSING", f); continue
    s = read(p)

    # --- site url
    s = s.replace("YOUR_SITE_URL", SITE)

    # --- generic placeholders that are now real
    s = s.replace("<!-- PH-01 is the only value you must set before publishing; see README.md -->\n", "")
    s = re.sub(r"[ \t]*<!-- PLACEHOLDER PH-OG .*?-->\n", "", s, flags=re.S)

    # --- image placeholders
    s = PH.sub(lambda m: replace_ph(m, f), s)

    # --- hero figcaption -> real caption
    for slug in SLUGS:
        s = re.sub(r"<figcaption>[^<]*\(PH-P-" + re.escape(slug) + r"\)[^<]*</figcaption>",
                   f"<figcaption>{esc(A[slug]['hero_cap'])}</figcaption>", s)

    # --- availability (PH-07)
    s = re.sub(r'<div class="callout mt-8">\s*<span class="callout__k">PH-07</span>\s*'
               r'<p><strong>Availability and relocation:</strong>[^<]*</p>\s*</div>',
               '<div class="callout mt-8">\n'
               '        <p><strong>Availability and relocation:</strong> ' + AVAIL + '</p>\n'
               '      </div>', s)
    s = re.sub(r'<div class="callout mt-6" style="max-width:56ch">\s*'
               r'<span class="callout__k">PH-07</span>\s*'
               r'<p><strong>Availability and relocation:</strong>[^<]*</p>\s*</div>',
               '<div class="callout mt-6" style="max-width:56ch">\n'
               '        <p><strong>Availability and relocation:</strong> ' + AVAIL + '</p>\n'
               '      </div>', s)

    # --- contact channels
    if 'class="channels"' in s:
        pre = prefix(f)
        chans = "\n".join(
            channel(k, v, note, (h if not h.startswith("assets") else pre + h), ext)
            for k, v, note, h, ext in CHANNELS)
        s = re.sub(r'<div class="channels">.*?</div>\s*(?=<p class="mono)',
                   '<div class="channels">\n          ' + chans + '\n        </div>\n        ', s, flags=re.S)

    # --- footer "elsewhere" list
    s = re.sub(r'<h2 class="footer__h">Elsewhere[^<]*</h2>.*?<ul class="footer__list">.*?</ul>',
               '<h2 class="footer__h">Elsewhere</h2>\n        ' + footer_links(prefix(f)),
               s, flags=re.S)

    # --- header CV marker
    pre = prefix(f)
    s = s.replace('<span class="tag">PH-08</span><span class="muted" style="font-size:var(--t-xs)">CV PDF</span>',
                  f'<a class="btn btn--sm" href="{pre}{CV}" download>CV</a>')

    # --- form mailto
    s = s.replace('data-mailto="YOUR_EMAIL"', f'data-mailto="{EMAIL}"')

    write(p, s)
    touched.append(f)

print("rewritten:", len(touched))
left = sum(read(os.path.join(REPO, f.replace("/", os.sep))).count("PLACEHOLDER PH-")
           for f in FILES if os.path.exists(os.path.join(REPO, f.replace("/", os.sep))))
print("PLACEHOLDER markers remaining:", left)
for f in FILES:
    p = os.path.join(REPO, f.replace("/", os.sep))
    if not os.path.exists(p):
        continue
    s = read(p)
    for tok in ("YOUR_", "PH-0", "BIO_TO_WRITE", "LEVELS_TO_SET"):
        if tok in s:
            print(f"  !! {f}: {tok} x{s.count(tok)}")