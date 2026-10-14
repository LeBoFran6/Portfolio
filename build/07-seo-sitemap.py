import os, sys, io, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO = r"C:\Users\Fran6\Documents\GitHub\Portfolio"
SITE = "https://lebofran6.github.io/Portfolio"
def read(p):  return open(p, encoding="utf-8").read()
def write(p, s): open(p, "w", encoding="utf-8", newline="").write(s)

# ---------------------------------------------------------------- robots
write(os.path.join(REPO, "robots.txt"), f"""# Francisco De Carvalho Pereira - portfolio
User-agent: *
Allow: /

Sitemap: {SITE}/sitemap.xml
""")
print("robots.txt ok")

# ---------------------------------------------------------------- sitemap + lastmod
TODAY = "2026-10-14"
pages = ["", "/work.html", "/breakdown.html", "/about.html", "/skills.html",
         "/contact.html"] + ["/projects/" + s for s in [
    "lets-sing-voxler", "automated-blender-render-pipeline", "fittingbox", "warno",
    "rubber", "rally-project", "lastmeal", "movies-cgi", "environment-art",
    "dietemna", "architectural-visualisation", "game-jams"]]
out = ['<?xml version="1.0" encoding="UTF-8"?>',
       '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in pages:
    out.append(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod></url>")
out.append("</urlset>")
write(os.path.join(REPO, "sitemap.xml"), "\n".join(out) + "\n")
print("sitemap.xml ok -", len(pages), "urls")

# ---------------------------------------------------------------- about: bio
p = os.path.join(REPO, "about.html")
s = read(p)
s = s.replace(
  "<p>The through-line is the same in every case: find the bottleneck nobody has time\n"
  "          to fix, and remove it in a way the team keeps using after you leave.</p>",
  "<p>The through-line is the same in every case: find the bottleneck nobody has time\n"
  "          to fix, and remove it in a way the team keeps using after you leave.</p>\n"
  "          <p>I trained at ESMA, where I worked across environment art, 3D and gameplay\n"
  "          programming before specialising. On <strong>RUBBER</strong> I owned the vehicle\n"
  "          end to end &mdash; Chaos dynamics, a custom six-wheel rig, Morpher destruction\n"
  "          in 3ds Max, and the feedback layer around it. I am at home in Unreal Engine 5\n"
  "          and Unity, comfortable in Blender and 3ds Max, and I write the Python and C# that\n"
  "          makes the tools. I care about work that is measured rather than described.</p>")
s = s.replace("PH-REEL-POSTER", "reel")
s = re.sub(r"\b6 console targets\b", "six console targets", s)
s = re.sub(r"\b6 hardware targets\b", "six hardware targets", s)
write(p, s)
print("about.html ok")

# ---------------------------------------------------------------- leftover comments
p = os.path.join(REPO, "index.html")
s = read(p)
s = s.replace("<!-- PH-REEL-POSTER, when supplied, can also become this backdrop.\n"
              "           Left as a pure CSS treatment so the page issues zero failed\n"
              "           requests while the poster is still missing. -->",
              "<!-- Pure CSS treatment: the page issues no extra request for this. -->")
s = s.replace("<!-- PH-REEL-POSTER", "<!-- reel poster")
write(p, s)

p = os.path.join(REPO, "breakdown.html")
s = read(p)
s = re.sub(r'<span class="callout__k">PH-RD-\*</span>',
           '<span class="callout__k">R&amp;D</span>', s)
write(p, s)
print("comment tidy ok")

# ---------------------------------------------------------------- mojibake + decode hint
HTML = glob.glob(os.path.join(REPO, "*.html")) + glob.glob(os.path.join(REPO, "projects", "*.html"))

# Some caption strings were double-encoded: UTF-8 bytes read back through cp1252,
# which turns an em dash into three characters. A whole-file round-trip is not
# possible - the pages contain characters cp1252 cannot represent - so the
# affected sequences are substituted explicitly.
MOJIBAKE = [
    ("\u00e2\u20ac\u201d", "\u2014"),  # a-circumflex euro right-dquote  -> em dash
    ("\u00e2\u20ac\u201c", "\u2013"),  # a-circumflex euro left-dquote   -> en dash
    ("\u00e2\u20ac\u02dc", "\u2018"),  # -> left single quote
    ("\u00e2\u20ac\u2019", "\u2018"),  # -> left single quote
    ("\u00e2\u20ac\u009d", "\u201d"),  # -> right double quote
    ("\u00e2\u20ac\u009c", "\u201c"),  # -> left double quote
    ("\u00e2\u20ac\u00a6", "\u2026"),  # -> ellipsis
    ("\u00e2\u20ac\u2122", "\u2122"),  # -> trademark
    ("\u00c2\u00b7",       "\u00b7"),  # A-circumflex middot           -> middot
    ("\u00c2\u00a0",       "\u0020"),  # A-circumflex nbsp             -> space
    ("\u00c3\u00a9",       "\u00e9"),  # A-tilde e-acute               -> e-acute
]
BAD = "\u00e2\u20ac"

fixed = 0
for fp in HTML:
    t = read(fp)
    n = t.count(BAD)
    if not n:
        continue
    for src, dst in MOJIBAKE:
        t = t.replace(src, dst)
    write(fp, t)
    fixed += n
print(f"repaired mojibake in {fixed} sequence(s)")

# decoding="async" lets the browser paint a blank box first. On a portfolio where the
# imagery IS the argument it should be in the first paint, so the hint goes and the
# browser uses its own default. loading="lazy" stays for everything below the fold.
n = 0
for fp in HTML:
    t = read(fp)
    if ' decoding="async"' in t:
        n += t.count(' decoding="async"')
        write(fp, t.replace(' decoding="async"', ""))
print(f'removed {n} decoding="async" hints')

# ---------------------------------------------------------------- sanity
left = sum(read(fp).count(BAD) for fp in HTML)
print("remaining mojibake markers:", left)