# AUDIT — `PortfolioEnhancedAndremastered`

**Audited:** `C:\Users\Fran6\Desktop\PortfolioEnhancedAndremastered` (read-only; nothing in it was modified, renamed, moved or deleted)
**Date:** 2026-09-23
**Reviewer stance:** senior Technical Artist / Technical Director doing a hiring review, then a senior front-end reviewer doing a code review.
**Rebuilt output:** `C:\Users\Fran6\Desktop\NewPortfolioV00`

> **Post-audit change (same day).** After this audit, the art direction of the rebuilt site was
> replaced at the owner's request, using the DA on the page at `C:\Users\Fran6\Desktop\exemple.txt`.
> That changed the visual system only — palette, type, geometry, texture, plus one new component
> (the pipeline flow diagram, used on the Blender pipeline case study). **§1–§7 below still describe
> the source folder and are unchanged**; §8's account of the rebuild remains accurate on structure,
> accessibility, metadata, the placeholder system and the defect fixes, but the *visual* descriptions
> of the rebuilt site (cool near-black palette, system-UI type) are superseded. The current system is
> documented in `README.md` §4 and lives in the token block of `assets/css/site.css`. Contrast was
> re-measured on the new palette and still passes AA on every pair actually used (worst pair 5.12:1).

---

## 0. What this audited, and how the numbers were obtained

**A correction to the brief first.** The brief describes `PortfolioEnhancedAndremastered` as the source. It is not a Wix export — it is *itself already a rebuild*, produced from an earlier export by a Python builder (`_tools/build_site.py`, driven by `_data/content.py`). Its own `README.md` (in French) documents a previous pass that already killed the worst Wix artefacts. So this is an audit of **pass 2**, not pass 1. That matters, because most of the easy wins are already spent, and the remaining defects are the structural ones.

**Method.** Everything below was measured on this machine, not inferred:

- File inventory, byte sizes, directory totals: `Get-ChildItem` / `Measure-Object`.
- Duplicate detection: `Get-FileHash -Algorithm SHA256` over all 581 files in `assets/img`.
- Link and asset resolution: every `href` / `src` / `srcset` / `poster` in all 18 HTML files resolved against the filesystem.
- External dependency scan: regex over all HTML + CSS + JS for `http(s)://`, `//`, `@import`, `url(http…)`.
- Colour contrast: WCAG 2.x relative-luminance computation in PowerShell (formula below), not eyeballed.
- `<img>` hygiene: parsed from raw HTML, counted by attribute.

**Honesty note on limits.** I could not render the site in a browser, so there is **no Lighthouse/axe run, no real-device screenshot, and no measured paint timing** in this report. Contrast, byte sizes, link graph, tag hygiene and inventory are hard measurements. Anything I could not measure is labelled **UNAVAILABLE** rather than guessed.

**Totals measured.** 18 HTML pages. 681 files. `assets/img` = 581 files / 10.5 MB (580 `.webp` + `favicon.svg`). `assets/media` = 3 `.mp4` / 19.3 MB. CSS 35,045 B (1,101 lines). JS 7,111 B (171 lines). Font 40,188 B. CV PDF 40,240 B.

---

## 1. Verdict in one paragraph

**This is a strong portfolio carrying a broken delivery layer.** The writing is the best I have seen in a technical-art portfolio: twelve case studies that each state a problem, a contribution and a *number*, with the occasional admission of what went wrong and what would be done differently (`projects/rally-project.html` gives its own frame budget and then says where it would still break). The accessibility and markup hygiene are better than most shipped studio sites: 115 `<img>` tags, all 115 with `alt`, `loading` and `width`/`height`; skip links, landmarks, live regions, `prefers-reduced-motion`, and a working keyboard-closable menu. **But as delivered it is invisible and unshareable** — every canonical URL, every Open Graph tag, the entire sitemap and `robots.txt` point at unresolved placeholders, so search engines and social previews get nothing. Two of the twelve case studies have no imagery at all, the hero promises a showreel that does not exist, and a published product boxshot naming a client and an unannounced edition is shipped in the open. Fix the delivery layer and the ethics/asset problem and this is a portfolio that gets interviews; leave them and the best content on the site never reaches a reader.

---

## 2. The 60-second read (hiring TD, first impression)

**What a TD gets in 60 seconds.** A near-black, precise, restrained page. The `h1` is the name, and immediately below it sits the single most useful line on the site:

> "Technical Artist / Technical Director — Real-time 3D, pipeline automation and performance across six console targets." (`index.html:8`, `index.html:70`)

Below that, a four-cell proof band with real numbers: *6 console targets · 300+ assets / month · ~2 days saved / week · Screened theatrically* (`index.html:75-79`). That is exactly what a technical hiring manager wants in the first screen: role, specialism, evidence.

**Where it loses the reader.** The hero's primary call to action is **"Watch the showreel"** (`index.html:74`), and there is no showreel. `README.md:93-96` admits the "showreel" is `6e8aee0e-file.mp4`, a 14 MB background loop that used to autoplay on 15 pages, promoted to a featured reel because it was the only video available. A TD clicks that button first, every time. Clicking it delivers a repurposed background loop, not a curated reel.

**Second loss.** The hero backdrop is `assets/img/77f61acdf31c460e.webp`, declared as `1440×486` (`index.html:54`) — an aspect ratio of **2.96:1**, a letterboxed card crop, not a cinematic frame. It is the same file used as the poster, the card image and the `og:image` on all 18 pages.

**Verdict on the 60 seconds:** the words earn a second look; the media stack does not. Positioning 8/10, proof 9/10, first-click experience 4/10.

---

## 3. Scorecard

| Category | /10 |
|---|---|
| First impression & one-line positioning | 7.5 |
| Storytelling & project narrative | 9.0 |
| TechArt credibility | 8.5 |
| UX / navigation / information architecture | 7.0 |
| Visual design & consistency | 8.5 |
| Responsiveness & mobile | 7.0 |
| Accessibility | 8.5 |
| Performance | 8.0 |
| SEO / metadata / social sharing | 5.0 |
| Content completeness | 6.5 |
| **Weighted overall** | **7.6** |

Each score with the evidence behind it:

- **First impression & one-line positioning — 7.5.** Positioning line is excellent and appears in the `title`, the `og:description` and the visible `lede`, consistently. Loses 2.5 for: the showreel CTA leading nowhere real; a 2.96:1 letterbox as the hero backdrop; the same single image used as hero, poster, card and `og:image` on all 18 pages.
- **Storytelling & project narrative — 9.0.** The strongest thing here. Every case study follows problem → contribution → measured result, and several add a "what I owned" and a "what I would change" section (`automated-blender-render-pipeline.html`, `rally-project.html`). Real numbers throughout: "½ day → <60 s", "~2 days saved / week", "~13 ms frame time inside a 16.6 ms budget, 12 ms of it render thread". The two strongest cases are the ones *without* imagery, which is the core tension of this site.
- **TechArt credibility — 8.5.** Headless Blender + `bpy` automation, a Unity C# animation-validation tool, Scene Capture 2D instrumentation written to render targets, a custom 6-wheel Chaos Vehicle rig, Morpher-driven destruction, World Machine terrain, LOD/batching across six console configs, and PS1 budgeting at 2 MB RAM / 1 MB VRAM. Deductions: no node graph, no shader code, no profiler capture, no before/after, no dedicated R&D surface. Everything is *claimed in prose* and nothing is *shown*.
- **UX / navigation / information architecture — 7.0.** Clean five-item nav, a twelve-card index with working filters, prev/next case-study navigation, an `aria-current` active state. Deductions: `href="#top"` is on **all 18 pages but `id="top"` exists only on `index.html`** (measured: 18 occurrences, 1 definition) so the footer's back-to-top is a dead control on 17 pages; project pages mark **"Work"** as `aria-current="page"` while being detail pages, not the index; filters do not survive a reload or a share (no URL state); no R&D section.
- **Visual design & consistency — 8.5.** Genuinely coherent "precision instrument" system, documented as numbered token sections in `assets/css/site.css`, a single accent (`#FFDE34`) used only for CTA/active/metrics, hairline borders, tabular numerals in metrics. Deductions: the `--dim` contrast failure below, and placeholder boxes that do not share the visual language of the real cards.
- **Responsiveness & mobile — 7.0.** Fluid `clamp()` type scale, four breakpoints (1560 / 1024 / 860 / 620 px), mobile panel with Escape-to-close and focus return. Deductions: **desktop-first** — every breakpoint is `max-width`, there is not a single `min-width` query; `body { overflow-x: hidden }` (`site.css:114`) *hides* overflow instead of diagnosing it; the mobile menu is JS-only (see Accessibility).
- **Accessibility — 8.5.** Measured: 115/115 `<img>` with `alt` (17 deliberately empty for decoration), 115/115 with `loading`, 115/115 with `width`+`height`, one `<h1>` per page, skip link on all 18, `main`/`nav`/`footer` landmarks, 34 `aria-current` attributes, `aria-pressed` on filters, an `aria-live` status region for filter results, `prefers-reduced-motion` honoured at `site.css:1093` and `site.css:1103`, and a `:focus-visible` rule at `site.css:126`. Deductions below — chiefly a real AA contrast failure and a mobile menu that needs JavaScript.
- **Performance — 8.0.** CSS 35 KB, JS 7 KB, no framework, no CDN, no external font request beyond one self-hosted `.woff2`, the 14 MB video demoted to `preload="none"` + click-to-play, `loading="lazy"` below the fold, `width`/`height` on every image. The referenced image payload is only **107 files / 1.87 MB** total. Deductions: **475 files / ~14.4 MB shipped and never referenced** (473 `.webp` / 8.58 MB + 2 `.mp4` / 5.83 MB) — dead weight in the repository; **236 byte-identical duplicate files, 3.31 MB redundant** (each `.card.webp` is byte-for-byte the same as its full-size sibling when the source was ≤720 px wide, so the "downscale" was a no-op); no `srcset` and no `<picture>` anywhere, so the card-variant choice is made by hand at author time.
- **SEO / metadata / social sharing — 5.0.** The *structure* is right and complete: unique `<title>` and unique meta description on all 18 pages (verified — no duplicates), canonical, `og:type/site_name/title/description/url/image`, `twitter:card`, JSON-LD `Person`, `sitemap.xml`, `robots.txt`, `theme-color`, `lang="en"`. The *values* make it worthless: canonical and `og:url` are `PLACEHOLDER_URL_DU_SITE/...` on all 18 pages; all 17 `<loc>` entries in `sitemap.xml` are the same placeholder; `robots.txt:6` advertises `https://example.com/sitemap.xml` — a *different* wrong host. `og:image` is a **relative** path (Open Graph requires absolute), it is the same 2.96:1 image on every page (wrong aspect for `summary_large_image`, which wants 1.91:1), and there is no per-project image, no `CreativeWork`/`BreadcrumbList` structured data for the twelve case studies, and no `robots` directives. As shipped, the site cannot be found, and any link pasted into Slack, LinkedIn or X renders without a working preview.
- **Content completeness — 6.5.** No lorem ipsum, no Wix leftovers, no dead internal links (verified: zero), no duplicate ids. But: 7 open placeholders (`PLACEHOLDER_URL_DU_SITE`, 2 × `IMAGE_ICI`, `PORTRAIT_A_REMPLACER`, `BIO_A_REMPLACER`, `NIVEAUX_A_REMPLACER`, `EMAIL_CONFIRM`), two case studies with **no imagery at all**, an empty skills-proficiency column, a placeholder bio, and no R&D/breakdown surface to hold the technical proof. `README.md:113` is candid that the skill levels are "volontairement vide" — deliberately blank, because inventing them would be the fastest way to lose a technical reader's trust. That judgement is correct; it just means the job is unfinished.

---

## 4. Defect register

Severity: **blocker** = stops the site doing its job or creates legal/reputational risk; **major** = a reader notices and it costs you; **minor** = polish.

### Blockers

**B1 — The site is unindexable and unshareable.**
*Where:* `index.html:11`, `:17` and the equivalent lines on 17 further pages; `sitemap.xml:3-19`; `robots.txt:6`.
*Evidence:* canonical and `og:url` are `PLACEHOLDER_URL_DU_SITE/...`; all 17 `<loc>` values are the placeholder; `robots.txt` names a third host (`example.com`).
*Fix:* set one real base URL in `_data/content.py` (`SITE["base_url"]`), regenerate, and correct `robots.txt`. One value, one rebuild.

**B2 — A published product boxshot naming a client and an unannounced edition is served in public.**
*Where:* one image in `assets/img`, used at `index.html` (card), `work.html` (card) and `projects/automated-blender-render-pipeline.html`. Its filename has a `.webp.webp` double extension.
*Evidence:* the filename itself pairs a publisher's name with a year-edition product bundle, and the file is retail product art rather than a render. **The filename is deliberately not printed in this report** — it is itself the leak. To locate it:

```powershell
Get-ChildItem "C:\Users\Fran6\Desktop\PortfolioEnhancedAndremastered\assets\img" |
  Where-Object Name -match 'thq|nordic|bundle'
```

*Fix:* delete the image and every reference. Replace with a marked placeholder. Naming a shipped title you worked on is a credit; shipping a publisher's unannounced product art is a liability. See §5.

**B3 — The primary call to action promises an asset that does not exist.**
*Where:* `index.html:74` ("Watch the showreel"), `index.html:98-112` (the reel block).
*Evidence:* `README.md:93-96` states the reel is the repurposed 14 MB background loop `6e8aee0e-file.mp4`.
*Fix:* either cut the CTA, or cut a real 45–90 s reel. A TD opens the reel first; this is the highest-leverage single asset on the site.

**B4 — Two of the twelve case studies have no image at all, and they are the strongest two.**
*Where:* `projects/rally-project.html:153` and `projects/lastmeal.html:142` render `IMAGE_ICI` placeholder blocks; `work.html:123`, `:151` likewise.
*Evidence:* `Rally Project` carries the best technical number on the site (13 ms inside a 16.6 ms budget); `LASTMEAL` carries the most interesting constraint (2 MB RAM, real 1994 hardware). Both are image-free.
*Fix:* supply a frame-time readout and an on-hardware capture. These two projects are the entire "this person does real technical work" argument and they are currently invisible.

**B5 — Mobile navigation does not work without JavaScript, and the JS file claims it does.**
*Where:* the mobile panel relies on the `hidden` attribute flipped by JS (`assets/js/site.js:20-24`); the burger is `display:none` until JS runs.
*Evidence:* `assets/js/site.js:2-4` asserts "The site is fully usable with JavaScript disabled: navigation, links, images and text are plain HTML." False for the mobile menu below 861 px.
*Fix:* a `<details>`-based panel (no JS required), with JS only adding Escape-to-close. *(The rebuild does this.)*

### Majors

**M1 — Text contrast fails WCAG AA.**
*Where:* `--dim: #6E7681` (`site.css:46`), used for the 10–11 px monospace micro-labels at `site.css:562-568`, `975-1004`, `1018-1026`, `1055-1063`, `1172-1179`.
*Evidence (computed):* `#6E7681` on `--bg #0A0B0D` = **4.29:1**; on `--panel #14171C` = **3.91:1**. AA for normal text requires 4.5:1. For the other tokens, measured: `--text #F2F4F7` 17.87 / 16.30, `--muted #9BA3AE` 7.73 / 7.05, `--accent #FFDE34` 14.77 / 13.47 — all pass.
*Fix:* raise `--dim` to `#8B93A0` (6.36 / 5.80 on the same surfaces). *(The rebuild does this.)*

**M2 — Font licence is unresolvable from the repository.**
*Where:* `assets/fonts/madefor.woff2` (40,188 B), declared at `site.css:2-8` with `font-display: swap`.
*Evidence:* a repository-wide search for a licence document or attribution returns nothing; the file's internal name tables could not be read. "Wix Madefor" is SIL OFL; "MadeFor" (Meta/WeTransfer) is proprietary. No licence text exists in the tree either way.
*Fix:* confirm provenance; if it is not OFL, either licence it or drop it for a system stack. A redistributed webfont with no licence file is a real risk for a commercial portfolio. *(The rebuild ships a system stack instead, at zero cost and no legal exposure.)*

**M3 — Third-party creative work is embedded with no rights trail and no attribution.**
*Where (examples, all measured in `assets/img`):* `marius-andrei-marius-andrei-warno-cover_.jpg` (a named artist's WARNO cover art), `hasan-almasi-…-unsplash.jpg`, `matt-artz-…-unsplash_copy.jpg`, `noah-boyer-…-unsplash.jpg`, `sumner-mahaffey-…-unsplash.jpg` (four Unsplash photographs), `71hg2w3omyl__sl1500_-1702253257.jpg` (retail product-image naming pattern), plus vendor logos used as skill icons (`250px-unreal-engine-logo.png`, `blender_logo_no_text_svg.png`, `substance-painter.png`, `autodesk_3ds_max-logo…png`, `visual_studio_icon_2019_svg.png`).
*Fix:* keep only assets you hold the rights to; replace the rest with marked placeholders. Note that only 93 of 581 images are human-named — 488 are MD5-prefixed, which partially hides *which* is which. That is not a safeguard, it is an inconsistency.

**M4 — Dead back-to-top control on 17 of 18 pages.**
*Where:* `href="#top"` appears on all 18 pages; `id="top"` exists once, at `index.html:52`.
*Fix:* add the anchor to a shared element, or link to the page top properly.

**M5 — `#top`-class navigation semantics: the active state lies on 12 pages.**
*Where:* every `projects/*.html` marks the **Work** nav item `aria-current="page"` (e.g. `projects/warno.html:40`). The current page is a case study, not the work index.
*Fix:* mark `aria-current="true"` (or a parent-trail style) for section membership rather than page identity, or omit it on detail pages.

**M6 — The console-target count does not match the console list, and the list is never the same twice.**
*Where:* `README.md:51` and the homepage proof band claim **"6 console targets"**, but the list beside it names **five** (PS4, PS5, Switch, Switch 2, Xbox Series X|S). The `index.html:8` meta description names a *different* four (PS4, PS5, Xbox Series X|S, Nintendo Switch), and `projects/lets-sing-voxler.html` names five again in a third order.
*Evidence:* three places, three different enumerations, none matching the stated count.
*Fix:* decide the true number and the true list, then use one string everywhere. A console-focused panel counts, and an unresolved count on the positioning line costs more than the number itself. *(This is inherited from the source content and is carried into the rebuild as an explicit confirm-item, `PH-11` — the rebuild does not repeat a wrong enumeration in its own metadata.)*

### Minors

- **m1** — Four files carry a `.webp.webp` double extension. Cosmetic, but it is the kind of detail a reviewer notices.
- **m2** — Build tooling is machine-bound: `_tools/build_site.py:17` hard-codes `ROOT = Path(r"C:\Users\Fran6\Desktop\PortfolioEnhancedAndremastered")` and reads `_tools/audit/*.json` produced by earlier runs. The build only works on this machine, with those artefacts present.
- **m3** — Dangling provenance in CSS: `site.css:1` credits `_tools/setup_font.py` and `site.css:1171` credits `_tools/patch_css.py`; neither script exists in `_tools/`.
- **m4** — `README.md:8-9` encourages hand-editing the generated HTML *and* regenerating with the builder. Those two instructions will silently diverge. The twelve case studies are generated from `_data/content.py`; editing the HTML means the next build destroys the edit.
- **m5** — `body { overflow-x: hidden }` (`site.css:114`) hides horizontal overflow rather than fixing its cause.
- **m6** — No `srcset`/`<picture>` (0 occurrences across 18 pages) despite two variants existing per image.
- **m7** — `robots.txt` and `sitemap.xml` carry no dates; `sitemap.xml` has no `lastmod`.
- **m8** — `404.html` carries `aria-current` on no nav item (defensible — it is a `NAV` non-member — but inconsistent with the other 17).
- **m9** — No `:focus-visible` treatment beyond the single global rule at `site.css:126`; interactive cards and the reel button rely on the default ring only.
- **m10** — `README.md` is in French while the site it describes is English, and the deliverable brief requires English documentation. The site itself contains **no French content**, so there is nothing French worth toggling to (see §5.4).
- **m11** — Not a git repository: no history, no blame, no way to diff a hand-edit against a generated page.
- **m12** — `.nojekyll` is present (good for GitHub Pages) but zero bytes are reported by a plain read; worth confirming it is the intended empty file rather than a truncated one.
- **m13** — The CV PDF is 40,240 B and could not be inspected in this environment (the byte read failed at the shell layer). **UNAVAILABLE:** page count, and whether it contains a phone number or home address. Given the brief's privacy rule, verify this by hand before publishing.

---

## 5. Cross-cutting findings

### 5.1 NDA and client-asset exposure

The site names its employers and clients in copy — Voxler (18 files), Eugen Systems (6), FittingBox (5), THQ Nordic (4), TECHREFT (3), Ubisoft / Isard Film Production (2 each). **Naming shipped titles you worked on is legitimate credit and should stay.** The problem is not the names; it is the *artwork*:

- **The THQ Nordic / "Let's Sing 2027" retail boxshot** (B2) is the clear liability — a publisher's marketing image, on a public page, naming a future edition.
- **Third-party artist and stock work** (M3) has no rights trail.
- **Vendor logos** used as skill icons are third-party trademarks; they are all currently unreferenced, so deleting them is free.

Everything client-facing should either be your own capture of work you are cleared to show, or a marked placeholder. Nothing on this site should be a publisher's press asset.

### 5.2 Privacy

A real personal email address (a Gmail account — **not printed here on purpose**, see the `mailto:` links in `_data/content.py`) is published in the JSON-LD `Person` block and in `mailto:` links on all 18 pages, and the CV PDF is offered for download. The brief forbids inventing personal data and requires placeholders for private data. **Recommendation:** keep the address as a placeholder token everywhere, and treat the published address as an explicit decision rather than a default. No phone number or home address appears in the HTML. The CV PDF is unverified (§4, m13).

### 5.3 The French-content question

The brief allows a lightweight FR toggle "if the source has French content worth keeping". **It does not.** The site is entirely English; the only French is in `README.md` and the internal `_tools/` audit dumps. Adding a toggle would mean translating 12 case studies, which would weaken text that is already written as excellent technical English. **Decision: EN only.** (Documented in `NewPortfolioV00/README.md`.)

### 5.4 Dead weight

475 of 580 images and 2 of 3 videos — ~14.4 MB — are never referenced by any page. Plus 236 byte-identical duplicate pairs (3.31 MB). The shipped site references only 107 images totalling 1.87 MB. The build pipeline optimised well and then never pruned; the repository carries roughly seven times the payload the site actually serves.

---

## 6. Placeholders and missing assets in the source

| Marker | File | What is missing |
|---|---|---|
| `PLACEHOLDER_URL_DU_SITE` | `_data/content.py:31` → all 18 pages, `sitemap.xml`, `robots.txt` | The public URL. Powers canonical, `og:url`, JSON-LD, sitemap. |
| `IMAGE_ICI` | `projects/rally-project.html`, `projects/lastmeal.html` | Any visual for the two strongest technical projects. |
| `PORTRAIT_A_REMPLACER` | `about.html:68` | A current headshot. |
| `BIO_A_REMPLACER` | `about.html:125` | The long-form biography. |
| `NIVEAUX_A_REMPLACER` | `skills.html` | Skill proficiency levels — deliberately blank, correctly. |
| `EMAIL_CONFIRM` | `contact.html` | Confirmation of the public address, and **one** LinkedIn URL (two are listed). |
| `PLACEHOLDER_SHOWREEL` | `index.html` | A real showreel. |
| Poster frame | `index.html` | A genuine still from the reel. |

Measured placeholder count across the tree: **40 occurrences**.

---

## 7. Prioritised action plan

### P0 — do before anyone sees this (all are blockers)

1. **Set one real base URL** and regenerate: fixes canonical, `og:url`, JSON-LD and the sitemap; then correct the host in `robots.txt:6`. *(≈15 min, one value.)*
2. **Delete the THQ Nordic / "Let's Sing 2027" boxshot** and every reference to it. Replace with a marked placeholder. *(≈10 min.)*
3. **Produce the showreel**, or remove the CTA that promises it. 45–90 s, 1080p. *(the largest single asset task — and the highest-return one.)*
4. **Give `Rally Project` and `LASTMEAL` one image each.** A frame-time readout, an on-hardware capture. *(2 assets, disproportionate return.)*
5. **Replace the `og:image`** with a real absolute-URL 1200×630 card; add per-project images for the share that matters most.
6. **Decide the private-email question** and confirm the CV PDF contains no phone number or home address.

### P1 — quality, done next

7. **Fix `--dim` contrast** to `#8B93A0` (4.29:1 → 6.36:1 at zero visual cost).
8. **Resolve the font licence.** Keep it with a licence file, or move to a system stack.
9. **Make mobile navigation work without JS** (`<details>`/`<summary>`).
10. **Purge the 475 unreferenced files and the 236 duplicates** — removes ~14.4 MB and ~3.3 MB respectively.
11. **Fix `href="#top"`** and the incorrect `aria-current` on project pages.
12. **Replace or credit the third-party artwork** (Unsplash, artist covers, vendor logos).
13. **Add an R&D / breakdown surface** so shaders, tooling, node graphs and profiling have a home; every case study currently *claims* technique and *shows* none.
14. **Add `srcset`/`<picture>`**, since both variants already exist.

### P2 — polish and maintenance

15. Strip the `.webp.webp` double extensions.
16. Make the build portable (remove the hard-coded `ROOT`, drop the dependency on stale `_tools/audit/*.json`), or delete the toolchain and treat the HTML as the source of truth — but not both, which is the current contradiction.
17. Remove the dangling `setup_font.py` / `patch_css.py` references from the CSS comments.
18. Add `lastmod` to the sitemap; add `CreativeWork` + `BreadcrumbList` JSON-LD for the 12 case studies.
19. Remove `body { overflow-x: hidden }` once the underlying overflow is fixed.
20. Simplify the case-study nav semantics, then re-run an axe/Lighthouse pass in a real browser — the one class of check this audit could not perform.

---

## 8. What the rebuild does about it

Every P0 and P1 item is addressed in `C:\Users\Fran6\Desktop\NewPortfolioV00`, except those that require the owner's own assets, which are represented by a documented placeholder system instead:

- **P0-1, P0-5** → a single `YOUR_SITE_URL` token, plus a one-line documented replace; absolute `og:image` at 1200×630; unique per-page titles and descriptions; `sitemap.xml` and `robots.txt` regenerated from the same token.
- **P0-2, P0-4** → no client or third-party artwork is copied at all. Every visual is a self-documenting placeholder carrying what it is, its ideal resolution and format, and its recommended filename.
- **P0-3** → the showreel slot is present and honest (`PH-REEL`), with the exact drop-in `<video>` markup in `README.md`. The player JS is already wired.
- **P0-6** → no email, phone or address is published: contact details are placeholder tokens, and the `Person` JSON-LD carries no address or email.
- **P1-7** → `--dim` is `#8B93A0` (6.36:1 on background, 5.80:1 on panels), asserted numerically in the build's gate.
- **P1-8** → system font stack only; **zero** `@font-face`, zero external requests.
- **P1-9** → `<details>`-based mobile navigation that works with JavaScript disabled.
- **P1-10** → nothing inherited, so nothing to purge: the entire built site is 348.6 KB across 24 files.
- **P1-11** → one `<h1>` per page, no dead anchors (verified), `aria-current` only on the genuinely current page.
- **P1-13** → a new `breakdown.html`: 13 R&D cards covering Scene Capture instrumentation, deterministic material regeneration, headless Blender, animation validation, Chaos Vehicle, Morpher destruction, World Machine, draw calls, PS1 budgeting, gaze, world streaming and CAD repair — each with problem / method / result / next, and a proof placeholder. The Houdini card is present but explicitly marked *optional*, because no Houdini work appears anywhere in the source and inventing one would be a fabrication.
- **P2-17** → no dangling build-script references.

**Limits of the rebuild, stated plainly.** All ~40 placeholders are still placeholders; the site has **zero real imagery** until assets are supplied. Skills proficiency is left deliberately `UNRATED` with the one-line edit documented, because inventing self-scores is exactly the failure the source README warned about. Availability/relocation (`PH-07`) is left as a placeholder because it is a fact only the owner holds. No browser-based accessibility or performance run was possible in this environment.
