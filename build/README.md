# `build/` — the one-time asset pipeline

**The site does not need any of this to run or deploy.** The HTML is the source
of truth and is hand-edited and committed. These scripts are the tooling that
turned the original Wix export into the current pages, kept so the imagery can be
re-cut or extended later.

Run the whole thing:

```powershell
.\build\build.ps1
```

It resets the site to the last commit, regenerates every image, rewrites the
markup, applies the stylesheet patches, and finishes by running `verify.py` —
the gate that reports **problems: 0** across all 19 pages.

## Source imagery

The scripts read from an image library kept **outside** the repository, because
it is large and is not needed to serve the site:

```
C:\Users\Fran6\Documents\GitHub\_wix_source_backup\assets\img
C:\Users\Fran6\Documents\GitHub\_wix_source_backup\assets\media
C:\Users\Fran6\Documents\GitHub\_wix_source_backup\assets\files
```

That folder is the original Wix export of the old site — the full-resolution
originals the 782 hashed filenames refer to. If it is deleted the site still
works; you just cannot re-cut the images.

## Order matters

Each step assumes the previous one ran, and each one is idempotent.

| Step | What it does |
|---|---|
| `01-assets.py` | Picks the source image per project, converts to WebP at page-appropriate size, writes to `assets/img/projects/`. Emits `_assets.json` (alt text + dimensions) that step 04 reads. |
| `02-media.py` | Re-encodes the environment clip, pulls its poster frame, composes the 1200×630 Open Graph card, installs the CV. |
| `03-breakdown-shots.py` | Cuts the R&D evidence stills from the same library. |
| `04-rewrite.py` | The big one: swaps every `YOUR_SITE_URL` token, replaces every placeholder box with real `<img>` / gallery markup, wires the contact channels, the footer links, the CV and the availability line. |
| `05-reel-cv-bio.py` | The showreel player, the CV buttons and the long-form bio. |
| `06-no-still-panels.py` | The three case studies that have no publishable capture get a designed "no still" panel instead of a broken image box. |
| `07-seo-sitemap.py` | `robots.txt`, `sitemap.xml` with `lastmod`, and drops `decoding="async"` from every image. |
| `08-consoles-skills-bio.py` | The six-target console list, and the 27 skill ratings. |
| `09-css.py` | The stylesheet patches — the gallery, portrait, "no still" and R&D shot components, plus three fixes to pre-existing rules (see below). |
| `verify.py` | The gate. Run it any time. |

## The three CSS fixes

`09-css.py` also repairs three rules that were wrong in the previous build:

1. `.step__t` / `.step__d` were inline `<span>`s, so every `PROBLEM` /
   `CONTRIBUTION` / `RESULT` label ran straight into the body text.
2. `.reel__poster > *` stretched the Play button across the whole poster frame,
   hiding the poster image behind a solid accent block.
3. `.nav > a` set `color: var(--accent)` at specificity (0,1,1) and beat
   `.btn--primary` at (0,1,0), so the header's "Get in touch" button rendered
   yellow-on-yellow with no visible label.

## Screenshots

```powershell
.\build\shot.ps1 -Pages @("index.html", "work.html")
```

Writes PNGs to `%LOCALAPPDATA%\Temp\opencode\shots`. Note that headless Chrome
clamps the window to roughly 485 px wide, so `--window-size` below that is
clipped in the output rather than actually emulating a narrower viewport.