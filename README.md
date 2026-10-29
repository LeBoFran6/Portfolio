# Francisco De Carvalho Pereira — Technical Artist — Tools & Pipeline

Static portfolio. Hand-built HTML, one stylesheet, one 8 KB script, real project
imagery. **No framework, no CDN, no build step, no trackers, no webfont.** It works
from `file://` and on GitHub Pages with no configuration.

- **Live:** <https://lebofran6.github.io/Portfolio/>
- 19 pages, ~12.4 MB total, of which 7.1 MB is one click-to-play video that is
  never fetched unless a visitor presses play.
- English only, `lang="en"`.

---

## Running it

Nothing to install.

```powershell
# open directly
start .\index.html

# or serve it, which matches production
python -m http.server 8080
```

## Deploying

Push to `main` with **Settings → Pages → Source: `main` / `/ (root)`**. There is
no build and no configuration. `sitemap.xml` lists all 19 pages with `.html`
URLs and a `lastmod`, and `robots.txt` points at it.

---

## Layout

```
index.html            home — positioning, proof band, clip, six selected projects
work.html             all twelve case studies, with discipline filters
breakdown.html        thirteen R&D cards: problem / method / result / next
about.html            bio, long-form bio, facts
skills.html           27 skills, each rated from the work that proves it
contact.html          live channels + a mailto form
404.html
projects/*.html       twelve case studies
assets/css/site.css   the whole design system, tokens at the top
assets/js/site.js     filters, reel player, form, reveal — all optional
assets/img/           project stills, R&D shots, OG card, portrait
assets/media/         the environment clip
assets/files/         CV (PDF)
build/                one-time tooling — not needed to run or deploy
```

## Design system

One token block at the top of `assets/css/site.css` drives everything: a warm
anthracite ladder (`#1A1A1A` → `#333231`), a single accent (`#FFDE34`), Impact /
Arial Black display type over Courier New, zero corner radius, 2px structural
borders and hard offset shadows.

Contrast is measured, not eyeballed: `--text` 16.58:1, `--muted` 10.40:1,
`--dim` 6.97:1, `--accent` 13.05:1 on `--bg`; the worst pair actually used is
5.12:1. All pass WCAG AA. The original graphite `#4F4F4F` measures 2.12:1 and is
therefore used for shadows and borders only, never as text.

## Accessibility

One `<h1>` per page; `main` / `nav` / `footer` landmarks and a skip link on all
19; mobile navigation is a native `<details>` element so it works with JavaScript
disabled (JS only adds Escape-to-close and focus return); every `<img>` has an
`alt` that says what the image *proves*, plus `width`/`height` to prevent layout
shift; `prefers-reduced-motion` disables all motion; the video is
`preload="none"` and click-to-play.

## Performance

No external requests of any kind. Images are WebP, sized when they were cut and
carried only on pages that use them. Above-the-fold images deliberately carry no
`decoding="async"`, because on this site the imagery is the argument and it should
be in the first paint. Below-the-fold images are `loading="lazy"`.

## Verifying

```powershell
python .\build\verify.py
```

The gate checks all 19 pages and currently reports **problems: 0**: no broken
internal link, no missing asset, no dead anchor, no duplicate `id`, one `<h1>`
each, a unique title per page, `alt` and dimensions on every image, and no
external resource references.

## Content still to supply

Three case studies have no publishable capture and say so honestly in a designed
"no still" panel rather than showing a broken image box:

| Page | Why | What would fix it |
|---|---|---|
| `projects/rally-project.html` | captures still in progress | a frame-time readout with all four camera views live |
| `projects/lastmeal.html` | visuals withheld | an on-hardware capture of the PS1 target |
| `projects/movies-cgi.html` | screened theatrically | one cleared still |

Two smaller gaps: the portrait is a 450×338 original, so export a 1200×1500 one
if you have a better camera shot; and the R&D cards for PS1 VRAM budgeting and
the (deliberately optional) Houdini slot are marked rather than filled.

## Rights

Every image on this site is Francisco's own work: in-engine captures, renders,
DCC screenshots and viewport captures from his own machines. No third-party
editorial, stock photography, vendor logo or publisher press asset is used, and
no unannounced content is named. Client and studio names appear as credit only.

## Before you send this to anyone

Run Lighthouse or axe against the deployed URL — this was built and checked
without a browser automation pass.