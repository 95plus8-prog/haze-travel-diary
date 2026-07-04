# HAZE — Illustrated Travel Diary

**Live:** https://95plus8-prog.github.io/haze-travel-diary/

A quiet, editorial, museum-grade site for a personal illustrated travel
diary — real trips, redrawn in comic/anime style. Plain HTML/CSS/JS — no
build step, no framework, no dependencies to install. Site copy is in
Simplified Chinese (`lang="zh-CN"`); this README stays in English since
it's for whoever maintains the code, not site visitors.

## Content model

Every entry is a **real photo**, illustrated afterward — not invented
fiction. Captions describe what's actually visible in frame (a menu, a
finish line, a tram going past) rather than made-up backstory. The eight
current volumes:

| Slug | Title | What it is |
|---|---|---|
| `paris` | Paris | Street corner near the Eiffel Tower |
| `canada-cup` | Canada Cup | Matchday selfie outside a Starbucks |
| `old-town` | Old Town | An old quarter alley, paper umbrellas |
| `match-day` | Match Day | Kicking a ball on a grass field |
| `run-van-marathon` | Run Van Marathon | Group finish-line photo |
| `alaska` | Alaska | Cruise dock, gulls, mountains |
| `yixin-chicken` | Yixin Chicken | A restaurant window table |
| `amsterdam` | Amsterdam | Café window seat, tram passing |

Source photos live in `漫画作品/` locally (untouched, original filenames,
full-res PNG) but are **git-ignored** — not pushed to GitHub, since they're
un-optimized, several MB each, and show recognizable faces with no reason
to be public. The copies actually used by the site are in
`assets/covers/<slug>.jpg` — resized to a 1600px-max edge and re-compressed
with `sips` (built into macOS) so pages load quickly; originals average
~2.8MB each, the site copies average ~600KB.

## Why static HTML, not Next.js

The original brief called for Next.js/React/TypeScript/Framer Motion. This
machine has no Node.js installed (confirmed — not in PATH, not in any common
install location, even in a login shell), so that toolchain can't be
installed, built, or run here. This was built as a dependency-free static
site instead: same design system, same motion language — just vanilla CSS
and JS. It runs anywhere, needs no `npm install`, and can be ported into
Next.js later if you want React back (component boundaries map cleanly:
Nav, Footer, WorkCard, Hero, RevealSection, etc.).

## Running it locally

Any static file server works. From this folder:

```
python3 -m http.server 4173
```

Then open `http://localhost:4173/index.html`. All internal links/assets use
document-relative paths (`css/style.css`, `../css/style.css` from a page one
level deep) rather than root-absolute ones — this is what lets the same
files work both locally and at a sub-path like
`https://95plus8-prog.github.io/haze-travel-diary/`. It should still be
served over HTTP rather than opened via `file://`, since some browsers
restrict `fetch`/relative-path resolution for local files.

## Structure

```
index.html            Home
work.html              Gallery (all 8 diary entries)
work/<slug>.html       One page per entry — detail page
about.html             Why the diary exists, the 8 volumes, how entries get made
journal.html           Journal index
journal/<slug>.html    Journal entries
journal/rss.xml        RSS feed for the journal
contact.html           Contact links
css/style.css          Full design system (tokens, type, layout, motion)
js/main.js             Loader, nav glass, scroll reveal, custom cursor,
                        magnetic buttons, scroll progress — no dependencies
assets/covers/<slug>.jpg         The real photo/illustration for each entry
assets/journal/<slug>.svg        Decorative header art for journal posts
                                  (abstract, generated — see generate_art.py)
assets/hero.svg, portrait.svg    Abstract decorative art (home hero, About)
漫画作品/                          Original source photos, untouched, git-ignored
scripts/generate_art.py          Regenerates the *abstract decorative* SVGs
                                  only (journal headers, hero, portrait) —
                                  does not touch the real photos in covers/
scripts/generate_detail_pages.py Regenerates the 8 work/<slug>.html pages
                                  from the TRIPS data dict in that file
sitemap.xml, robots.txt, site.webmanifest, journal/rss.xml   SEO/PWA
```

## Adding a new entry

There's no CMS wired up — content lives directly in HTML plus one Python
data dict, which is the simplest thing that can still be edited without
touching markup by hand:

1. Resize/compress the photo (e.g. `sips -Z 1600 -s format jpeg -s
   formatOptions 78 in.png --out assets/covers/<new-slug>.jpg`) — keep it
   under ~800KB.
2. Add an entry to `TRIPS` in `scripts/generate_detail_pages.py` (title,
   volume number, date, place, one-line deck, 1–2 short observational notes)
   — the template already emits the correct `../` relative paths.
3. Run `python3 scripts/generate_detail_pages.py` — regenerates all 8+
   pages with correct prev/next links.
4. Add a card for it to `work.html` (and optionally `index.html`) by copying
   an existing `<figure class="gallery-item ...">` block. Check the actual
   pixel dimensions (`sips -g pixelWidth -g pixelHeight file.jpg`) and set
   the `width`/`height` attributes to match — the CSS shows images at their
   natural aspect ratio (no forced crop), so accurate dimensions just avoid
   layout shift while loading, portrait or landscape both work as-is.
5. Add the new URL to `sitemap.xml` (use the full
   `https://95plus8-prog.github.io/haze-travel-diary/...` URL).
6. Optionally add a line to the About page timeline.
7. Commit and push to `main` — GitHub Pages redeploys automatically.

## Known gaps vs. the original brief

- No Sanity/Contentful/Notion integration — flat files only.
- No automated Lighthouse/CI run in this environment; the CSS/JS was
  written with performance in mind (no layout thrashing, IntersectionObserver
  instead of scroll-jacking, `prefers-reduced-motion` respected, lazy-loaded
  below-the-fold images). Photos are already compressed JPEGs (~600KB avg);
  converting to WebP would shave more off but wasn't done here.
- Smooth scroll is native (`scroll-behavior: smooth` for in-page anchors)
  rather than a hand-rolled Lenis-style virtual scroll — a deliberate choice
  favoring accessibility and robustness over a heavier scroll-jacking effect.
