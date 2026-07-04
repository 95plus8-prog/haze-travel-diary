# HAZE — Illustrated Travel Diary

A quiet, editorial, museum-grade site for a personal illustrated travel
diary — real trips, redrawn in comic/anime style. Plain HTML/CSS/JS — no
build step, no framework, no dependencies to install.

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

Source photos live in `漫画作品/` (untouched, original filenames, full-res
PNG). The copies actually used by the site are in `assets/covers/<slug>.jpg`
— resized to a 1600px-max edge and re-compressed with `sips` (built into
macOS) so pages load quickly; originals average ~2.8MB each, the site
copies average ~600KB.

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

Then open `http://localhost:4173/index.html`. Root-relative paths
(`/css/style.css`, `/assets/...`) mean it must be served over HTTP — opening
`index.html` directly via `file://` will not resolve those correctly.

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
assets/covers/<slug>.png         The real photo/illustration for each entry
assets/journal/<slug>.svg        Decorative header art for journal posts
                                  (abstract, generated — see generate_art.py)
assets/hero.svg, portrait.svg    Abstract decorative art (home hero, About)
漫画作品/                          Original source photos, untouched
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

1. Drop the photo/illustration into `assets/covers/<new-slug>.png` (or
   `.jpg`/`.webp` — just update the extension in the places below to match).
2. Add an entry to `TRIPS` in `scripts/generate_detail_pages.py` (title,
   volume number, date, place, one-line deck, 1–2 short observational notes).
3. Run `python3 scripts/generate_detail_pages.py` — regenerates all 8+
   pages with correct prev/next links.
4. Add a card for it to `work.html` (and optionally `index.html`) by copying
   an existing `<figure class="gallery-item ...">` block — check the PNG's
   actual pixel dimensions (`width`/`height` attributes) to avoid layout
   shift, and use the `ratio-wide` class on `.work-card-frame` for landscape
   photos.
5. Add the new URL to `sitemap.xml`.
6. Optionally add a line to the About page timeline.

## Known gaps vs. the original brief

- No Sanity/Contentful/Notion integration — flat files only.
- No automated Lighthouse/CI run in this environment; the CSS/JS was
  written with performance in mind (no layout thrashing, IntersectionObserver
  instead of scroll-jacking, `prefers-reduced-motion` respected, lazy-loaded
  below-the-fold images) but hasn't been benchmarked here. The real photos
  are several MB each (uncompressed PNG) — worth running through an image
  compressor/converting to WebP before a real deploy.
- Smooth scroll is native (`scroll-behavior: smooth` for in-page anchors)
  rather than a hand-rolled Lenis-style virtual scroll — a deliberate choice
  favoring accessibility and robustness over a heavier scroll-jacking effect.
