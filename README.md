# Portfolio v00 — Francisco De Carvalho Pereira

Technical Artist / Technical Director. Static portfolio, hand-built, **zero dependencies**:
no framework, no CDN, no build step required to view, no trackers, no webfont.

**Art direction:** taken from `Desktop\exemple.txt` and applied site-wide — warm anthracite palette,
Impact + Courier New, zero corner radius, 2px borders, hard offset shadows, dot-matrix ground. The
whole look is the token block at the top of `assets/css/site.css`; see §4.

- **Site:** 19 HTML pages (`index`, `work`, `breakdown`, `about`, `skills`, `contact`, `404` + 12 case studies)
- **Weight:** ~411 KB across 26 files. CSS 42 KB, JS 8 KB, one SVG favicon. That is the whole site.
- **Offline:** works from `file://` with no network at all. Verified: zero external resource references.
- **Read the audit this rebuild answers:** [`AUDIT.md`](AUDIT.md)

---

## 1. Run it

There is nothing to install and nothing to build.

```powershell
# open it directly
start C:\Users\Fran6\Desktop\NewPortfolioV00\index.html
```

Or serve it, which is closer to production and makes relative paths behave exactly as they will online:

```powershell
cd C:\Users\Fran6\Desktop\NewPortfolioV00
python -m http.server 8080
# then open http://localhost:8080
```

## 2. Deploy it

Any static host works. GitHub Pages:

```powershell
cd C:\Users\Fran6\Desktop\NewPortfolioV00
git init
git add .
git commit -m "Portfolio v00"
git branch -M main
git remote add origin https://github.com/LeBoFran6/<repo>.git
git push -u origin main
```

Then **Settings → Pages → Source: `main` / `/ (root)` → Save**.

**Before you push, do step 3.** Canonical URLs and the sitemap are placeholders until you do.

## 3. The one thing you must change before publishing (PH-01)

Every canonical URL, `og:url`, sitemap entry and JSON-LD `url` is built from a single token:
`YOUR_SITE_URL`. Replace it everywhere in one command:

```powershell
cd C:\Users\Fran6\Desktop\NewPortfolioV00
$url = "https://lebo6.github.io/portfolio"     # <- your real URL, no trailing slash
Get-ChildItem -Recurse -Include *.html,*.xml,*.txt |
  ForEach-Object {
    (Get-Content $_.FullName -Raw -Encoding UTF8) -replace 'YOUR_SITE_URL', $url |
      Set-Content $_.FullName -Encoding UTF8 -NoNewline
    Write-Host "updated $($_.Name)"
  }
```

Then open `robots.txt` and confirm the `Sitemap:` line points at your domain. Verify with:

```powershell
Select-String -Path .\index.html -Pattern 'canonical|og:url'
Select-String -Path .\sitemap.xml -Pattern '<loc>'
```

---

## 4. Decisions taken, and why

These are judgement calls. Each is reversible; each is documented so you can overrule it.

**Art direction — taken from `Desktop\exemple.txt`, applied site-wide.** The whole look lives in
one place: the token block at the top of `assets/css/site.css`. Change a value there and all 19
pages follow. As extracted from that page:

- **Palette**, warm anthracite rather than cool grey: `--bg #1A1A1A` · `--panel #333231`
  (anthracite) · `--graphite #4F4F4F` · `--border #999594` · `--text #FFF8F6` (pinkish off-white) ·
  `--muted #CCC7C5` · `--accent #FFDE34` and its pale sibling `--accent2 #FFEF9A`.
- **Type**: Impact / Arial Black, uppercase, for display; Courier New for absolutely everything else.
- **Geometry**: `border-radius: 0` everywhere, 2px solid `#999594` structural borders, and hard
  offset shadows with no blur (3/4/5/6px in accent, off-white or graphite). Hover lifts the element
  `-3px,-3px` and grows the shadow.
- **Texture**: the DA's 20px dot matrix over a `#333231 → #1A1A1A` vertical gradient, both fixed so
  long pages keep the look.
- **Signature devices**: the yellow "kicker" box (used once per page, in the case-study eyebrow), the
  yellow highlight behind a display fragment (`.grad`), and placeholders as 2px dashed boxes on the
  near-black base.

**Two deliberate departures from the DA, both recorded in the stylesheet:**

1. **`--dim` is derived (`#A8A3A0`).** The DA's graphite `#4F4F4F` measures **2.12:1** as text and
   fails WCAG AA, so it is used for shadows and borders only — exactly as the DA itself does. The
   derived value keeps the warm hue and measures 6.97:1 on background, 5.12:1 on panels.
2. **Fonts stay on system stacks.** Impact / Arial Black / Courier New are OS-bundled on Windows and
   macOS (with `sans-serif` / monospace fallbacks elsewhere), so the site is still **zero-webfont,
   zero-request, fully offline** — and still has no font licence to clear.

Applying it cost nothing structurally: no markup was rewritten for the reskin. New CSS gained exactly
one component — the pipeline flow diagram from the DA page — used on the Blender pipeline case study,
where the source copy already describes that exact chain of stages. It could not be reused elsewhere
without inventing content.

**One honest trade-off.** This DA is a strong, deliberate personality: uppercase Impact, hard
shadows, a dot-matrix ground. It reads as a technical zine or an engineer's field notebook — which
suits the tools-and-pipeline story — and it is further from the restrained AAA minimalism many
studio sites use. If you ever want to walk it back, it is a token edit in one file, not a rebuild.

**No web font — system font stack.** The previous build shipped `madefor.woff2` with **no licence
file anywhere in the repository**. "Wix Madefor" is OFL; other fonts named MadeFor are proprietary.
Rather than redistribute a font whose licence cannot be established, this build uses OS-bundled
faces only (the DA's Impact / Courier New, with generic fallbacks). Cost: 0 bytes, 0 requests, no
legal exposure. If you later confirm the licence, add the `@font-face` at the top of
`assets/css/site.css` and put `"Madefor",` in front of `--font-display`. Nothing else moves.

**English only — no FR toggle.** The site is entirely English, including all 12 case studies. There
is **no French content in the source worth keeping** (the only French is in the previous build's
own documentation). A toggle would mean translating 12 detailed case studies and would weaken text
that is already written as strong technical English. If you want a French version later, it can be
added without touching the design.

**No image, video, PDF or font file was copied from the source folder.** Every visual is a
self-documenting placeholder (§6). Two reasons: much of the source imagery is third-party or
client artwork with no usable rights trail, and a published retail boxshot naming a client and an
unannounced edition is a liability. See §7 before you drop any file in.

**Placeholders are rendered as text, not as links.** A "LinkedIn" link pointing at
`YOUR_LINKEDIN_URL` is a broken link — the same defect this rebuild exists to remove. Every
contact entry therefore renders as plain, clearly-marked text until you supply the real value.
§8 has the drop-in markup for each.

**Skill levels are deliberately UNRATED.** Inventing self-scores is the fastest way for a technical
reviewer to stop believing the rest of the page. Every skill row instead links to the case study
that demonstrates it, which is the part that actually persuades. Setting the meters takes one
attribute per row — see §8.5.

**Content is reused, not rewritten.** All twelve case studies come from your own `_data/content.py`
and `build_site.py` — the problem/contribution/result structure and every number are yours. Nothing
was invented, and no metric appears in the new site that is not in the source.

---

## 5. Accessibility and performance, as built

Measured on the built output, not asserted:

- One `<h1>` per page; `<main>`, `<nav>`, `<footer>` landmarks on every page; skip-to-content link on all 19.
- Mobile navigation is a `<details>` element — **it works with JavaScript disabled**. JS only adds Escape-to-close and focus return.
- Every interactive element has a visible `:focus-visible` ring; `prefers-reduced-motion` disables all motion.
- Colour contrast (WCAG 2.x), measured on the DA palette: `--text #FFF8F6` 16.58:1, `--muted #CCC7C5`
  10.40:1, `--dim #A8A3A0` 6.97:1, `--accent #FFDE34` 13.05:1 on `--bg #1A1A1A`; worst pair actually
  used is 5.12:1 (`--dim` on a panel) — all pass AA. The DA's graphite `#4F4F4F` is never used as
  text (it would be 2.12:1); the build gate enforces that.
- Zero external requests. Zero `@font-face`. Zero `@import`. Zero `url(http…)` in the CSS.
- Video is `preload="none"` and click-to-play, so a 25 MB reel costs nothing until a visitor asks for it.
- The filter state is written to `?filter=` so a filtered view can be shared and reloaded.
- A build gate re-checks all of the above. It currently reports **PROBLEMS: none** across 19 pages.

**Once you add real images**, keep the pattern the placeholders document:
`loading="lazy"` (not for above-the-fold hero art), plus `width` and `height` on every `<img>` so the
layout does not shift. §8.4 shows the exact markup.

---

## 6. Placeholder legend

Every asset that could not be produced is a **self-documenting placeholder**. Each one appears in the
page as:

```html
<!-- PLACEHOLDER PH-xx | what goes here | ideal: resolution + format + size | file: where to put it -->
<div class="ph ph--16x9" role="img" aria-label="Placeholder PH-xx: ...">
  <span class="ph__id">PH-xx</span>      <!-- the id, greppable -->
  <span class="ph__label">what goes here</span>
  <span class="ph__spec">resolution, format, file-size budget</span>
  <span class="ph__file">assets/img/…   the exact filename expected</span>
</div>
```

To find every one of them: search the folder for `PLACEHOLDER PH-`. To find one specifically:
search for its id, e.g. `PH-RD-02`. The legend and the pages are generated from one registry, and the
build gate fails if a rendered placeholder is missing from this table.

| ID | Where | What to supply | Ideal spec | Expected file |
|---|---|---|---|---|
| `PH-01` | every page + sitemap.xml + robots.txt | Public site URL (canonical, Open Graph url, sitemap, JSON-LD) | Full https:// URL ending in / (with trailing slash) | `YOUR_SITE_URL` |
| `PH-02` | contact.html + footer | Public contact address | An email address you are happy to publish | `YOUR_EMAIL  (your existing site lists a Gmail address in its mailto links - confirm it)` |
| `PH-03` | contact.html, every footer | LinkedIn profile | One canonical https://www.linkedin.com/in/... URL (your current site lists two) | `YOUR_LINKEDIN_URL` |
| `PH-04` | contact.html, every footer | GitHub profile | https://github.com/... | `YOUR_GITHUB_URL` |
| `PH-05` | contact.html, every footer | ArtStation profile | https://www.artstation.com/... | `YOUR_ARTSTATION_URL` |
| `PH-06` | contact.html, every footer | itch.io profile | https://....itch.io/ | `YOUR_ITCH_URL` |
| `PH-07` | index.html hero, contact.html | Work authorisation / relocation stance (matters for Japan & China studios) | One short factual line, e.g. work permit status, relocation and remote willingness | `AVAILABILITY_TO_CONFIRM` |
| `PH-08` | every page header + about + contact | CV as PDF | A4 portrait, <=2 pages, <800 KB, text layer intact, no phone/home address | `assets/files/cv-francisco-de-carvalho-pereira.pdf` |
| `PH-09` | about.html | Portrait photograph | 4:5 portrait, 1200x1500, jpg/webp, <250 KB, neutral background, eyes to camera | `assets/img/about/portrait-1200x1500.jpg` |
| `PH-10` | about.html | Long-form biography (your own voice) | 200-350 words: where you started, what shaped how you work, what you want next | `BIO_TO_WRITE` |
| `PH-OG` | every page <head> | Open Graph share card | 1.91:1, 1200x630, jpg, <200 KB, must not be the hero still | `assets/img/og/og-cover-1200x630.jpg` |
| `PH-REEL` | index.html showreel | Showreel video | 16:9, 1920x1080, mp4 (H.264+AAC), 45-90 s, <25 MB, sound on | `assets/media/showreel.mp4` |
| `PH-REEL-POSTER` | index.html showreel | Showreel poster frame | 16:9, 1920x1080, jpg/webp, <250 KB, a real frame from the reel | `assets/img/reel/showreel-poster-1920x1080.jpg` |
| `PH-P-lets-sing-voxler` | projects/lets-sing-voxler.html hero + work.html card | Character render pass + tool UI | 16:9, 1920x1080, webp/jpg <350 KB for stills, or mp4 <=20 MB for the render pass | `assets/img/projects/lets-sing-voxler-hero-1920x1080.webp` |
| `PH-G-lets-sing-voxler` | projects/lets-sing-voxler.html gallery | Gallery for Let's Sing | 16:9, 1920x1080, webp/jpg <350 KB for stills, or mp4 <=20 MB for the render pass | `assets/img/projects/lets-sing-voxler-gallery-01..NN.webp` |
| `PH-P-automated-blender-render-pipeline` | projects/automated-blender-render-pipeline.html hero + work.html card | Pipeline diagram / .bat in action | 16:9, 1920x1080, webp/jpg <300 KB; diagrams exported as SVG or PNG | `assets/img/projects/automated-blender-render-pipeline-hero-1920x1080.webp` |
| `PH-G-automated-blender-render-pipeline` | projects/automated-blender-render-pipeline.html gallery | Gallery for Automated Blender Render Pipeline | 16:9, 1920x1080, webp/jpg <300 KB; diagrams exported as SVG or PNG | `assets/img/projects/automated-blender-render-pipeline-gallery-01..NN.webp` |
| `PH-P-fittingbox` | projects/fittingbox.html hero + work.html card | Product stills / browser try-on capture | 16:9, 1920x1080, webp <300 KB; screen capture at device pixel ratio 2 | `assets/img/projects/fittingbox-hero-1920x1080.webp` |
| `PH-G-fittingbox` | projects/fittingbox.html gallery | Gallery for FittingBox — Virtual Try-On | 16:9, 1920x1080, webp <300 KB; screen capture at device pixel ratio 2 | `assets/img/projects/fittingbox-gallery-01..NN.webp` |
| `PH-P-warno` | projects/warno.html hero + work.html card | Production map stills / overview | 16:9, 2560x1440, webp <400 KB; plus one top-down overview of the full map | `assets/img/projects/warno-hero-1920x1080.webp` |
| `PH-G-warno` | projects/warno.html gallery | Gallery for WARNO | 16:9, 2560x1440, webp <400 KB; plus one top-down overview of the full map | `assets/img/projects/warno-gallery-01..NN.webp` |
| `PH-P-rubber` | projects/rubber.html hero + work.html card | Vehicle renders + destruction breakdown | 16:9, 1920x1080, webp <350 KB; rig viewport capture at 100% zoom | `assets/img/projects/rubber-hero-1920x1080.webp` |
| `PH-G-rubber` | projects/rubber.html gallery | Gallery for RUBBER | 16:9, 1920x1080, webp <350 KB; rig viewport capture at 100% zoom | `assets/img/projects/rubber-gallery-01..NN.webp` |
| `PH-P-rally-project` | projects/rally-project.html hero + work.html card | Frame time / render target instrumentation | 16:9, 1920x1080, PNG (no recompression on graph text) <400 KB | `assets/img/projects/rally-project-hero-1920x1080.webp` |
| `PH-G-rally-project` | projects/rally-project.html gallery | Gallery for Rally Project | 16:9, 1920x1080, PNG (no recompression on graph text) <400 KB | `assets/img/projects/rally-project-gallery-01..NN.webp` |
| `PH-P-lastmeal` | projects/lastmeal.html hero + work.html card | On-hardware capture | 4:3, 640x480 native (upscale to 1280x960 for the web), webp <250 KB | `assets/img/projects/lastmeal-hero-1920x1080.webp` |
| `PH-G-lastmeal` | projects/lastmeal.html gallery | Gallery for LASTMEAL | 4:3, 640x480 native (upscale to 1280x960 for the web), webp <250 KB | `assets/img/projects/lastmeal-gallery-01..NN.webp` |
| `PH-P-movies-cgi` | projects/movies-cgi.html hero + work.html card | Cinematic stills / shot breakdown | 16:9, 1920x1080 to 2560x1440, webp <400 KB; a 10-20 s mp4 excerpt is stronger | `assets/img/projects/movies-cgi-hero-1920x1080.webp` |
| `PH-G-movies-cgi` | projects/movies-cgi.html gallery | Gallery for Real-Time Cinematics | 16:9, 1920x1080 to 2560x1440, webp <400 KB; a 10-20 s mp4 excerpt is stronger | `assets/img/projects/movies-cgi-gallery-01..NN.webp` |
| `PH-P-environment-art` | projects/environment-art.html hero + work.html card | World Machine node graph -> final environment | 16:9, 1920x1080, PNG for the graph (text legibility), webp for renders <350 KB | `assets/img/projects/environment-art-hero-1920x1080.webp` |
| `PH-G-environment-art` | projects/environment-art.html gallery | Gallery for Environment Art & Procedural Terrain | 16:9, 1920x1080, PNG for the graph (text legibility), webp for renders <350 KB | `assets/img/projects/environment-art-gallery-01..NN.webp` |
| `PH-P-dietemna` | projects/dietemna.html hero + work.html card | Three-room set, one per intention | 16:9, 1920x1080, webp <350 KB; keep the three rooms to the same exposure | `assets/img/projects/dietemna-hero-1920x1080.webp` |
| `PH-G-dietemna` | projects/dietemna.html gallery | Gallery for Dietemna | 16:9, 1920x1080, webp <350 KB; keep the three rooms to the same exposure | `assets/img/projects/dietemna-gallery-01..NN.webp` |
| `PH-P-architectural-visualisation` | projects/architectural-visualisation.html hero + work.html card | Final stills (check the redaction note first) | 16:9, 1920x1080, webp <300 KB | `assets/img/projects/architectural-visualisation-hero-1920x1080.webp` |
| `PH-G-architectural-visualisation` | projects/architectural-visualisation.html gallery | Gallery for Architectural Visualisation | 16:9, 1920x1080, webp <300 KB | `assets/img/projects/architectural-visualisation-gallery-01..NN.webp` |
| `PH-P-game-jams` | projects/game-jams.html hero + work.html card | Jam captures + covers | 16:9, 1920x1080, webp <250 KB; 2-4 s mp4 loops work well for a jam grid | `assets/img/projects/game-jams-hero-1920x1080.webp` |
| `PH-G-game-jams` | projects/game-jams.html gallery | Gallery for Game Jams & Prototypes | 16:9, 1920x1080, webp <250 KB; 2-4 s mp4 loops work well for a jam grid | `assets/img/projects/game-jams-gallery-01..NN.webp` |
| `PH-RD-01` | breakdown.html | Multi-view instrumentation with Scene Capture 2D — proof visual | 16:9, 1920x1080, PNG <=400 KB (keep graph text lossless) | `assets/img/breakdown/scene-capture-frame-time-1920x1080.png` |
| `PH-RD-02` | breakdown.html | Deterministic material regeneration — proof visual | 16:9, 2560x1440, PNG <=600 KB, node labels must be legible | `assets/img/breakdown/material-regeneration-node-graph-2560x1440.png` |
| `PH-RD-03` | breakdown.html | Headless Blender automation as an artist tool — proof visual | 16:9, 1920x1080, PNG or webp <=300 KB | `assets/img/breakdown/headless-blender-pipeline-1920x1080.png` |
| `PH-RD-04` | breakdown.html | Animation validation tool for animators — proof visual | 16:9, 1920x1080, PNG <=300 KB | `assets/img/breakdown/unity-animation-validation-tool-1920x1080.png` |
| `PH-RD-05` | breakdown.html | Six-wheel vehicle dynamics on Chaos Vehicle — proof visual | 16:9, 1920x1080, webp <=350 KB; viewport captures at 100% zoom | `assets/img/breakdown/chaos-vehicle-six-wheel-rig-1920x1080.webp` |
| `PH-RD-06` | breakdown.html | Modular destruction without physics debris — proof visual | 16:9, 1920x1080, webp <=350 KB; a 3-6 s mp4 loop is the strongest form | `assets/img/breakdown/morpher-destruction-1920x1080.webp` |
| `PH-RD-07` | breakdown.html | Procedural terrain: World Machine into engine — proof visual | 16:9, 1920x1080, PNG for the node graph (text legibility), webp for renders | `assets/img/breakdown/world-machine-node-graph-1920x1080.png` |
| `PH-RD-08` | breakdown.html | Draw call reduction across six console targets — proof visual | 16:9, 1920x1080, PNG for profiler captures <=400 KB | `assets/img/breakdown/draw-call-profiler-1920x1080.png` |
| `PH-RD-09` | breakdown.html | Designing to 2 MB of RAM and 1 MB of VRAM — proof visual | 4:3, 640x480 native upscaled to 1280x960, webp <=250 KB | `assets/img/breakdown/ps1-vram-budget-1280x960.webp` |
| `PH-RD-10` | breakdown.html | Runtime gaze decoupled from baked animation — proof visual | 16:9, 1920x1080, webp <=300 KB, tight crop on the face | `assets/img/breakdown/runtime-gaze-system-1920x1080.webp` |
| `PH-RD-11` | breakdown.html | Large-scale world streaming on a proprietary engine — proof visual | 16:9, 2560x1440, webp <=400 KB | `assets/img/breakdown/world-streaming-sectors-2560x1440.webp` |
| `PH-RD-12` | breakdown.html | Making unusable CAD deliverable — proof visual | 16:9, 1920x1080, webp <=300 KB | `assets/img/breakdown/cad-repair-before-after-1920x1080.webp` |
| `PH-RD-13` | breakdown.html | (Optional slot) Houdini / procedural tooling — proof visual | 16:9, 2560x1440, PNG <=600 KB | `assets/img/breakdown/houdini-network-2560x1440.png` |
| `PH-LEVELS` | skills.html | Self-rated proficiency levels | Set each level honestly: 5 = lead-level, 4 = production-strong, 3 = working, 2 = basic. Nothing was invented here on purpose. | `LEVELS_TO_SET` |
| `PH-11` | about.html | The true console-target list | Your site claims '6 console targets' but names five (PS4, PS5, Switch, Switch 2, Xbox Series X|S). Name the sixth or change the number everywhere - a console panel will count. | `CONSOLE_LIST_TO_CONFIRM` |

---

## 7. Before you add any asset: rights and NDA rules

This rebuild copies **nothing** from the source folder. When you supply assets, apply these rules —
they are the reason the previous build had a problem, and they are not optional for client work:

1. **Your own captures only, or work you are contractually cleared to show.** If a screenshot came
   from a publisher's press kit, a retailer's product page, or a stock library, do not use it.
   Four specific exclusions in the source folder: a retail product boxshot whose filename pairs a
   publisher with a year-edition bundle (find it with the `Get-ChildItem … -match 'thq|nordic|bundle'`
   command in `AUDIT.md`, defect B2); a named artist's WARNO cover art; four Unsplash photographs;
   and vendor logos used as skill icons.
2. **No unannounced content.** Not a filename, not a placeholder string, not alt text, not a URL slug.
   If an edition, character or feature is unreleased, it does not go on the site.
3. **Client work gets an anonymised description and a placeholder**, not the client's art — unless the
   contract says otherwise in writing. Ask. Studios say yes far more often than people assume, and when
   they say no it is much cheaper to have asked first.
4. **No personal data you would not put on a business card.** No phone number, no home address, no
   personal email unless you have decided to publish that address. The CV PDF is the usual leak:
   check it, it often carries a phone number in the footer.
5. **These two files are documentation, not the site.** `README.md` and `AUDIT.md` discuss your
   situation and the defects found. Delete them before a public push if your host serves every file.

---

## 8. Drop-in snippets for the common cases

### 8.1 The showreel (PH-REEL + PH-REEL-POSTER)

Put `showreel.mp4` (1920×1080, 45–90 s, <25 MB) in `assets/media/` and the poster frame in
`assets/img/reel/`, then replace the placeholder box in `index.html`:

```html
<!-- delete the <div class="ph ph--21x9">…</div> block and put this in its place -->
<div class="reel reveal" data-reel>
  <video controls preload="none" playsinline hidden
         poster="assets/img/reel/showreel-poster-1920x1080.jpg"
         width="1920" height="1080">
    <source src="assets/media/showreel.mp4" type="video/mp4">
    Your browser cannot play this video.
    <a href="assets/media/showreel.mp4">Download the showreel instead.</a>
  </video>
  <button class="reel__poster" type="button" data-reel-play aria-label="Play the showreel">
    <img src="assets/img/reel/showreel-poster-1920x1080.jpg" alt="" aria-hidden="true"
         width="1920" height="1080" loading="lazy" decoding="async">
    <span class="reel__play"><span aria-hidden="true">&#9654;</span> Play showreel</span>
  </button>
  <span class="reel__badge">Real-time &middot; Unreal Engine 5 &middot; Unity</span>
</div>
```

The `.reel` styles and the player in `assets/js/site.js` are already in place — nothing else to wire.
Also update the section heading, which currently says "not supplied yet".

### 8.2 The CV (PH-08)

Drop the PDF at exactly `assets/files/cv-francisco-de-carvalho-pereira.pdf`, then turn the markers
into links:

```html
<!-- header / hero -->
<a class="btn btn--primary" href="assets/files/cv-francisco-de-carvalho-pereira.pdf" download>Download CV</a>

<!-- footer, in place of the "PH-08 CV" <li> -->
<li><a href="assets/files/cv-francisco-de-carvalho-pereira.pdf" download>CV (PDF)</a></li>
```

On project pages the path is `../assets/files/…`. Keep the PDF under 800 KB and make sure its text
layer is intact — recruiters' systems parse it.

### 8.3 Contact and social (PH-02 … PH-06)

In `contact.html`, replace each `<div class="channel">` with an anchor, and in the footer replace each
`<li>`:

```html
<a class="channel" href="mailto:you@example.com">
  <span><span class="channel__k">Email</span>
  <span class="channel__v">you@example.com</span>
  <span class="channel__note">Best for roles and freelance</span></span>
  <span class="arw" aria-hidden="true">&nearr;</span>
</a>

<li><a href="https://www.linkedin.com/in/your-profile/" rel="me noopener" target="_blank">LinkedIn</a></li>
```

Pick **one** LinkedIn URL — your existing site lists two. Once the real URLs exist, add them back to
the JSON-LD `sameAs` array in the page `<head>` (it was deliberately left empty while they were
placeholders).

### 8.4 Any project visual (PH-P-* and PH-G-*)

```html
<img src="assets/img/projects/rally-project-hero-1920x1080.webp"
     alt="Frame-time readout with all four camera views live, landing at 13 ms inside a 16.6 ms budget"
     width="1920" height="1080" loading="lazy" decoding="async">
```

Alt text is content, not decoration: for a breakdown, say what the image proves. Use
`alt=""` only for genuinely decorative images. Consider `srcset` if you export a 720 px card variant.

### 8.5 Skill levels (PH-LEVELS)

Each skill row in `skills.html` looks like this — set the level by adding `data-level` and removing
the `meter--unrated` class:

```html
<div class="meter" data-level="4" role="img" aria-label="Proficiency: advanced">
  <i></i><i></i><i></i><i></i><i></i>
</div>
<div class="meter__legend">Advanced &mdash; shipped in production</div>
```

Scale: `5` lead-level · `4` production-strong · `3` working · `2` basic. Update the `aria-label` too.

### 8.6 Availability (PH-07)

One factual line in two places: the callout under the hero on `index.html`, and the callout at the
bottom of `contact.html`. Replace `AVAILABILITY_TO_CONFIRM` with something like:

> Open to relocation to Japan or China; would require visa sponsorship. Available remote from France.

Studios in Tokyo and Shanghai look for this early. Leaving it blank does not read as neutral.

---

## 9. What was verified, and what was not

**Verified on the built output** (a build gate re-runs these; last run: *PROBLEMS: none*):

- 19 pages parse with balanced tags; no duplicate `id` attributes; one `<h1>` each.
- **Zero** broken internal links or missing asset targets, across every `href`, `src` and `poster`.
- **Zero** external resource references; CSS contains no `@import`, no `url()` and no `@font-face`.
- Unique `<title>` and unique meta description on all 19 pages; canonical, `og:*` and `twitter:*` present.
- Every visible placeholder carries a preceding `PLACEHOLDER` comment and all four self-documenting parts.
- **58 visible placeholder boxes** across the 19 pages, covering **40 distinct** placeholder ids from the
  **52** in the registry (per-project visuals appear twice: once on the work index card and once on the
  case study). Every registered id appears somewhere on the site; none is orphaned in the docs.
- No leaked private data: no email address, no phone number, no address, and none of the source's
  client/publisher strings — checked folder-wide, including this README and `AUDIT.md`.

**Not verified — you should do this:**

- **No browser accessibility or performance run.** This environment cannot render the site, so there is
  no axe or Lighthouse result, no real-device screenshot and no measured paint timing. Run Lighthouse
  on the deployed URL before you send it to anyone.
- **Page count and contents of the previous CV PDF** could not be extracted (the byte read failed at the
  shell layer). Check it yourself for a phone number or home address before reusing it — that is a real
  privacy leak when it happens, and it usually hides in the PDF footer.
- **The font licence question** in the source remains open. It no longer affects this build (no font is
  shipped), but if you ever restore `madefor.woff2`, confirm its licence first.
