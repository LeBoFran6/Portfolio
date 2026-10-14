import os, sys, io, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
REPO = r"C:\Users\Fran6\Documents\GitHub\Portfolio"

bad = 0
for f in glob.glob(os.path.join(REPO, "**", "*.html"), recursive=True) + \
         glob.glob(os.path.join(REPO, "**", "*.css"), recursive=True) + \
         glob.glob(os.path.join(REPO, "**", "*.xml"), recursive=True) + \
         glob.glob(os.path.join(REPO, "*.txt")):
    raw = open(f, "rb").read()
    try:
        t = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        print("  !! not utf-8:", os.path.relpath(f, REPO), e); bad += 1; continue
    rel = os.path.relpath(f, REPO)
    for tok in ["�", "Â", "â€", "Ã©", "&#x27;", "\\r\\n"]:
        if tok in t:
            print(f"  !! {rel}: mojibake {tok!r} x{t.count(tok)}"); bad += 1
print("encoding problems:", bad)

# leftover tokens anywhere
TOKENS = ["YOUR_", "PH-0", "PH-REEL", "PH-G-", "PH-P-", "PLACEHOLDER", "PH-11",
          "PH-LEVELS", "PH-10", "BIO_TO_WRITE", "LEVELS_TO_SET", "IMAGE_ICI",
          "PORTRAIT_A_REMPLACER", "meter--unrated"]
print("\nleftover placeholder tokens:")
hits = 0
for f in glob.glob(os.path.join(REPO, "**", "*.html"), recursive=True):
    t = open(f, encoding="utf-8").read()
    for tok in TOKENS:
        if tok in t:
            print(f"  !! {os.path.relpath(f, REPO)}: {tok} x{t.count(tok)}"); hits += 1
print("  none" if not hits else f"  {hits} file/token pairs")

# key content present
checks = [
 ("index.html", "Open to Technical Artist"),
 ("index.html", "six console targets"),
 ("index.html", "environment-clip.mp4"),
 ("index.html", "Fran6" if False else "fran6pereira@gmail.com"),
 ("contact.html", "linkedin.com/in/francisco-de-carvalho-pereira"),
 ("contact.html", "github.com/LeBoFran6"),
 ("contact.html", "artstation.com/lefran6"),
 ("contact.html", "lefran6.itch.io"),
 ("about.html", "Xbox One"),
 ("skills.html", 'data-level="4"'),
]
print("\ncontent spot-checks:")
for f, needle in checks:
    t = open(os.path.join(REPO, f), encoding="utf-8").read()
    print(("  ok   " if needle in t else "  MISS ") + f"{f}: {needle[:46]}")

# image count
imgs = glob.glob(os.path.join(REPO, "assets", "img", "**", "*.webp"), recursive=True)
print(f"\nwebp images shipped: {len(imgs)}")
tags = sum(open(f, encoding="utf-8").read().count("<img") for f in
           glob.glob(os.path.join(REPO, "**", "*.html"), recursive=True))
print(f"<img> tags across the site: {tags}")