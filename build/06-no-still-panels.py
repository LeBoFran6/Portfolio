import os, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = r"C:\Users\Fran6\Documents\GitHub\Portfolio"
EMAIL = "fran6pereira@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/franciscodecarvalhopereira/"
GITHUB = "https://github.com/LeBoFran6"
ART = "https://www.artstation.com/lefran6"
ITCH = "https://lefran6.itch.io/"
CV = "assets/files/cv-francisco-de-carvalho-pereira.pdf"

def read(p):  return open(p, encoding="utf-8").read()
def write(p, s): open(p, "w", encoding="utf-8", newline="").write(s)

PH = re.compile(r"[ \t]*<!-- PLACEHOLDER (PH-[A-Za-z0-9_.\-]+) .*?-->\s*"
                r"<div class=\"ph.*?</div>\s*", re.S)

# ---------------------------------------------------- projects with no stills
REASON = {
 "rally-project": ("Visuals in progress", "Case study written, captures in progress"),
 "lastmeal":      ("Under NDA",      "Visuals withheld - screenshots on request"),
 "movies-cgi":    ("Under NDA",      "Screened theatrically - stills on request"),
}
ITCH_LINKS = {
 "rally-project": [("Playable builds", "https://lefran6.itch.io/")],
 "lastmeal":      [("itch.io", "https://lefran6.itch.io/")],
 "movies-cgi":    [("itch.io", "https://lefran6.itch.io/")],
}

FIGCAP = {
 "rally-project": "Case study written; captures in progress. Playable builds on itch.io.",
 "lastmeal":      "Designing to 2 MB of RAM. Visuals withheld &mdash; screenshots on request.",
 "movies-cgi":    "Real-time cinematics screened theatrically. Stills on request.",
}

def req_panel(slug, pre):
    label, note = REASON[slug]
    links = "".join(
        f' &middot; <a href="{u}" rel="noopener" target="_blank">{t}</a>'
        for t, u in ITCH_LINKS[slug])
    return (f'<div class="ph ph--req" role="note">'
            f'<span class="ph__id">NO STILL</span>'
            f'<span class="ph__label">{label}</span>'
            f'<span class="ph__spec">{note}{links}</span>'
            f'</div>')

# card variant for index.html / work.html
def req_card(slug):
    label, note = REASON[slug]
    return (f'<div class="ph ph--req ph--card" role="note">'
            f'<span class="ph__id">NO STILL</span>'
            f'<span class="ph__label">{label}</span>'
            f'<span class="ph__spec">{note}</span></div>')

def sub(m, f):
    pid = m.group(1)
    slug = pid.replace("PH-P-", "").replace("PH-G-", "")
    if slug not in REASON:
        return m.group(0)
    pre = "../" if f.replace("\\", "/").startswith("projects/") else ""
    if f in ("index.html", "work.html"):
        return req_card(slug) + "\n      "
    return req_panel(slug, pre)

for f in ["index.html", "work.html",
          "projects/rally-project.html", "projects/lastmeal.html",
          "projects/movies-cgi.html"]:
    p = os.path.join(REPO, f.replace("/", os.sep))
    s = read(p)
    s = PH.sub(lambda m: sub(m, f), s)
    # hero figcaption on those pages
    for slug in REASON:
        s = re.sub(r"<figcaption>[^<]*\(PH-P-" + re.escape(slug) + r"\)[^<]*</figcaption>",
                   f"<figcaption>{FIGCAP[slug]}</figcaption>", s)
    write(p, s)
    print(f"{f}: remaining {len(PH.findall(s))}")

# ---------------------------------------------------------------- about.html
p = os.path.join(REPO, "about.html")
s = read(p)
s = s.replace("<figcaption>PH-09 &mdash; replace with a current headshot.</figcaption>",
              "<figcaption>Francisco De Carvalho Pereira.</figcaption>")
s = s.replace(
  '<div class="fact__v"><span class="tag">PH-03..06</span> LinkedIn &middot; GitHub '
  '&middot; ArtStation &middot; itch.io &mdash; profile URLs to supply</div>',
  '<div class="fact__v"><a href="' + LINKEDIN + '" rel="me noopener" target="_blank">LinkedIn</a>'
  ' &middot; <a href="' + GITHUB + '" rel="me noopener" target="_blank">GitHub</a>'
  ' &middot; <a href="' + ART + '" rel="me noopener" target="_blank">ArtStation</a>'
  ' &middot; <a href="' + ITCH + '" rel="me noopener" target="_blank">itch.io</a></div>')
s = s.replace('<div class="fact__v"><span class="tag">PH-02</span> YOUR_EMAIL</div>',
              '<div class="fact__v"><a href="mailto:' + EMAIL + '">' + EMAIL + '</a></div>')
s = s.replace('<p class="mono mt-5"><span class="tag">PH-08</span> CV PDF &mdash; '
              'assets/files/cv-francisco-de-carvalho-pereira.pdf</p>',
              '<p class="mt-5"><a class="btn btn--sm" href="' + CV + '" download>'
              'Download CV (PDF) <span class="arw" aria-hidden="true">&darr;</span></a></p>')
write(p, s)
print("about fixed; PH-0 left:", len(re.findall(r'PH-0\d', s)), "| YOUR_ left:", s.count("YOUR_"))

# ---------------------------------------------------------------- breakdown 09/13
p = os.path.join(REPO, "breakdown.html")
s = read(p)
s = re.sub(r'[ \t]*<!-- PLACEHOLDER PH-RD-09 .*?-->\s*<div class="ph.*?</div>\s*',
           '<p class="rd__none">Screenshot withheld &mdash; the budget breakdown is available '
           'in the case study or on request.</p>\n      ', s, flags=re.S)
s = re.sub(r'[ \t]*<!-- PLACEHOLDER PH-RD-13 .*?-->\s*<div class="ph.*?</div>\s*',
           '<p class="rd__none">Optional slot &mdash; reserved. No Houdini work is claimed '
           'here until there is something real to show.</p>\n      ', s, flags=re.S)
write(p, s)
print("breakdown remaining:", len(PH.findall(s)))