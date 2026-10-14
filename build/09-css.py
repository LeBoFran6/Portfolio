"""CSS fixes that are not derived from the Wix export but are needed for the
real-asset build. Idempotent: safe to re-run."""
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

CSS = r"C:\Users\Fran6\Documents\GitHub\Portfolio\assets\css\site.css"
s = open(CSS, encoding="utf-8").read()
orig = s

# 0. The components the real-asset build introduces (evidence gallery, portrait,
#    "no still" panel, R&D shot). Inserted before the print block, once.
BLOCK = """
/* =============================================================================
   19b. EVIDENCE GALLERY, PORTRAIT & "NO STILL" PANELS
   Added when the real assets replaced the placeholders. Kept in the DA language:
   square corners, 2px structural borders, monospace captions, hard shadows.
   ========================================================================== */
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  align-items: start;
  gap: var(--bw);
}
.shot {
  margin: 0;
  display: flex;
  flex-direction: column;
  background: var(--panel);
  border: var(--bw) solid var(--border);
  box-shadow: 4px 4px 0 var(--graphite);
  transition: transform var(--dur) var(--ease), box-shadow var(--dur) var(--ease);
}
.shot:hover { transform: translate(-3px, -3px); box-shadow: 7px 7px 0 var(--graphite); }
.shot img {
  display: block;
  width: 100%;
  height: auto;
  background: var(--dark);
  border-bottom: var(--bw) solid var(--border);
}
.shot figcaption {
  padding: 10px 12px;
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.55;
  color: var(--muted);
}

/* Hero still on a case study */
.wrap > figure > img {
  display: block;
  width: 100%;
  height: auto;
  border: var(--bw) solid var(--border);
  box-shadow: 6px 6px 0 var(--graphite);
  background: var(--dark);
}
figure figcaption {
  margin-top: 10px;
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.55;
  color: var(--muted);
}

/* About page portrait */
.portrait {
  display: block;
  width: 100%;
  height: auto;
  border: var(--bw) solid var(--border);
  box-shadow: 6px 6px 0 var(--graphite);
  background: var(--dark);
}

/* "No still" - an intentional, designed absence rather than a missing asset.
   Used only where the work genuinely has no publishable capture. */
.ph--req {
  aspect-ratio: auto;
  border-style: solid;
  border-color: var(--graphite);
  background: var(--bg-raised);
  box-shadow: none;
  padding: 18px 20px;
  gap: 8px;
}
.ph--req .ph__id { background: var(--panel-2); color: var(--accent); }
.ph--req .ph__label { font-size: 15px; }
.ph--card {
  height: 100%;
  align-items: center;
  justify-content: center;
  text-align: center;
  border: 0;
  background: var(--bg-raised);
}
.ph--card .ph__spec { max-width: 34ch; }

/* R&D card evidence shot + the "nothing to show yet" line */
.rd__shot {
  display: block;
  width: 100%;
  height: auto;
  border-top: var(--bw) solid var(--border);
  border-bottom: var(--bw) solid var(--border);
  background: var(--dark);
}
.rd__none {
  margin: 0;
  padding: 14px 16px;
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.6;
  color: var(--muted);
  background: var(--bg-raised);
  border-top: var(--bw) solid var(--border);
  border-bottom: var(--bw) solid var(--border);
}

@media (max-width: 620px) {
  .gallery { grid-template-columns: 1fr; }
}

"""
ANCHOR = "/* =============================================================================\n   20. PRINT"
if "19b. EVIDENCE GALLERY" not in s and ANCHOR in s:
    s = s.replace(ANCHOR, BLOCK.lstrip("\n") + ANCHOR, 1)

# 1. .step__t / .step__d were inline <span>s, so "PROBLEM" ran straight into the
#    body text on every work-index card and every case study.
s = s.replace(
""".step__t {
  font-family: var(--font-display);""",
""".step__t {
  display: block;
  font-family: var(--font-display);""")
s = s.replace(
".step__d { color: var(--muted); font-size: 14px; margin-top: 3px; }",
".step__d { display: block; color: var(--muted); font-size: 14px; margin-top: 3px; }")

# 3. `.nav > a` sets `color: var(--accent)` at specificity (0,1,1) and beat
#    `.btn--primary` at (0,1,0), so the header's "Get in touch" button rendered
#    yellow-on-yellow with no visible label. Give the button its own colour.
s = s.replace(
""".btn--primary.btn--sm { box-shadow: 3px 3px 0 var(--text); }""",
""".nav > a.btn,
.nav > a.btn:visited {
  color: var(--accent-ink);
  font-family: var(--font-display);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-color: var(--accent-ink);
}
.nav > a.btn:hover { color: var(--accent-ink); }
.btn--primary.btn--sm { box-shadow: 3px 3px 0 var(--text); }""")

# 2. `.reel__poster > *` stretched the Play button across the whole poster,
#    hiding the poster frame behind a solid accent block.
s = s.replace(
".reel__poster > * { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }",
".reel__poster > img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }")
s = s.replace(
""".reel__play {
  position: absolute;
  left: 50%; top: 50%;
  transform: translate(-50%, -50%);""",
""".reel__play {
  position: absolute;
  left: 50%; top: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;""")

if s == orig:
    print("CSS: already applied (no change)")
else:
    open(CSS, "w", encoding="utf-8", newline="").write(s)
    print("CSS: patches applied")

for probe in ['.step__t {\n  display: block;',
              '.step__d { display: block;',
              '.reel__poster > img {',
              'z-index: 2;\n  display: inline-flex;',
              '19b. EVIDENCE GALLERY',
              '.gallery {',
              '.shot figcaption {',
              '.portrait {',
              '.ph--req {',
              '.rd__shot {',
              '.rd__none {',
              '.nav > a.btn,']:
    print(("  ok   " if probe in s else "  MISS ") + probe.replace("\n", " ")[:48])